"""Relation-free entity activation prototypes inspired by LinearRAG.

This module intentionally does not depend on the upstream implementation. It
implements small, auditable variants of the sentence/entity propagation rule so
that mechanism-level hypotheses can be tested on synthetic graphs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Optional

import numpy as np
from scipy import sparse


@dataclass(frozen=True)
class BridgeConfig:
    max_hops: int = 3
    threshold: float = 0.20
    normalization: Literal["none", "entity_degree", "symmetric"] = "none"
    frontier_budget: Optional[int] = None
    keep_seed_scores: bool = True


@dataclass
class BridgeResult:
    scores: np.ndarray
    first_hop: np.ndarray
    active_counts: list[int]


def _safe_inv(x: np.ndarray, power: float = 1.0) -> np.ndarray:
    out = np.zeros_like(x, dtype=np.float64)
    mask = x > 0
    out[mask] = np.power(x[mask], -power)
    return out


def _normalize_incidence(
    mention: sparse.csr_matrix,
    mode: Literal["none", "entity_degree", "symmetric"],
) -> sparse.csr_matrix:
    """Return the propagation incidence matrix used for one hop.

    ``mention`` has shape [num_sentences, num_entities]. The paper uses a
    binary matrix. The variants here keep the graph relation-free and only
    change query-time propagation normalization.
    """
    mention = mention.astype(np.float64).tocsr()
    if mode == "none":
        return mention

    sentence_degree = np.asarray(mention.sum(axis=1)).ravel()
    entity_degree = np.asarray(mention.sum(axis=0)).ravel()

    if mode == "entity_degree":
        # Down-weight destinations that are generic hubs. This leaves sentence
        # aggregation unchanged and applies D_e^-1 on the outward projection.
        d_e_inv = sparse.diags(_safe_inv(entity_degree))
        return mention @ d_e_inv

    if mode == "symmetric":
        # A symmetric bipartite normalization, analogous to normalized message
        # passing, but still with no extracted relations.
        d_s_inv_sqrt = sparse.diags(_safe_inv(sentence_degree, 0.5))
        d_e_inv_sqrt = sparse.diags(_safe_inv(entity_degree, 0.5))
        return d_s_inv_sqrt @ mention @ d_e_inv_sqrt

    raise ValueError(f"Unknown normalization: {mode}")


def _prune_frontier(scores: np.ndarray, threshold: float, budget: Optional[int]) -> np.ndarray:
    frontier = np.where(scores >= threshold)[0]
    if budget is None or frontier.size <= budget:
        return frontier
    top_local = np.argpartition(scores[frontier], -budget)[-budget:]
    return frontier[top_local]


def semantic_bridge(
    mention: sparse.csr_matrix,
    sentence_similarity: np.ndarray,
    seed_scores: Dict[int, float],
    config: BridgeConfig,
) -> BridgeResult:
    """Activate entities using a LinearRAG-style sentence bridge.

    The update follows the spirit of Eq. (5): entity evidence is projected to
    sentences, modulated by query/sentence similarity, then projected back to
    entities. ``max`` persistence is used across hops. The optional frontier
    budget only activates when the fixed threshold admits too many entities;
    it is therefore not the distance-decaying threshold rejected in the paper.
    """
    mention = mention.tocsr().astype(np.float64)
    sigma = np.asarray(sentence_similarity, dtype=np.float64)
    if mention.shape[0] != sigma.shape[0]:
        raise ValueError("sentence_similarity length must equal number of sentences")

    n_entities = mention.shape[1]
    current = np.zeros(n_entities, dtype=np.float64)
    first_hop = np.full(n_entities, -1, dtype=np.int64)
    for idx, score in seed_scores.items():
        current[idx] = max(current[idx], float(score))
        first_hop[idx] = 0

    best = current.copy()
    active_counts = [int(np.count_nonzero(current))]

    normalized = _normalize_incidence(mention, config.normalization)
    # Use the original incidence for gathering evidence into sentences. Only
    # the outward projection is normalized for entity-degree mode.
    inward = mention
    outward = normalized.T.tocsr()

    for hop in range(1, config.max_hops + 1):
        frontier_idx = _prune_frontier(current, config.threshold, config.frontier_budget)
        if frontier_idx.size == 0:
            break

        frontier = np.zeros_like(current)
        frontier[frontier_idx] = current[frontier_idx]

        sentence_activation = inward @ frontier
        weighted_sentence = sigma * sentence_activation
        proposed = np.asarray(outward @ weighted_sentence).ravel()

        proposed[proposed < config.threshold] = 0.0
        new_mask = (proposed > 0) & (first_hop < 0)
        first_hop[new_mask] = hop

        if config.keep_seed_scores:
            best = np.maximum(best, proposed)
        else:
            best = proposed.copy()

        # Avoid repeatedly re-propagating old maxima; this approximates a
        # frontier expansion rather than a full diffusion at each step.
        current = proposed
        active_counts.append(int(np.count_nonzero(current)))

    return BridgeResult(scores=best, first_hop=first_hop, active_counts=active_counts)


def contextual_seed_candidates(
    surface_similarity: np.ndarray,
    context_similarity: np.ndarray,
    alpha: float = 0.55,
    top_m: int = 2,
    ambiguity_margin: float = 0.08,
) -> tuple[np.ndarray, np.ndarray]:
    """Context-conditioned seed selection for ambiguous entity mentions.

    A candidate receives a convex combination of mention-level similarity and
    full-query-to-candidate-context similarity. If the best candidate is well
    separated, only it is kept; otherwise multiple candidates are retained so
    that subsequent sentence bridging can disambiguate them.
    """
    surface_similarity = np.asarray(surface_similarity, dtype=np.float64)
    context_similarity = np.asarray(context_similarity, dtype=np.float64)
    if surface_similarity.shape != context_similarity.shape:
        raise ValueError("surface_similarity and context_similarity must have the same shape")
    if surface_similarity.ndim != 1:
        raise ValueError("candidate similarities must be one-dimensional")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be in [0, 1]")

    scores = alpha * surface_similarity + (1.0 - alpha) * context_similarity
    order = np.argsort(scores)[::-1]
    if order.size <= 1:
        return order, scores[order]

    margin = scores[order[0]] - scores[order[1]]
    keep = 1 if margin >= ambiguity_margin else min(top_m, order.size)
    selected = order[:keep]
    return selected, scores[selected]
