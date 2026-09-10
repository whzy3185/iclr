"""Passage scoring and PPR prototypes for relation-free Tri-Graph retrieval."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy import sparse


@dataclass(frozen=True)
class PPRConfig:
    damping: float = 0.85
    max_iter: int = 100
    tol: float = 1e-10
    passage_similarity_weight: float = 0.05
    hub_correction: bool = False


def entity_idf(contain: sparse.csr_matrix) -> np.ndarray:
    contain = contain.tocsr()
    n_passages = contain.shape[0]
    document_frequency = np.asarray((contain > 0).sum(axis=0)).ravel()
    return np.log((n_passages + 1.0) / (document_frequency + 1.0)) + 1.0


def passage_reset_scores(
    contain: sparse.csr_matrix,
    activated_entity_scores: np.ndarray,
    passage_similarity: np.ndarray,
    first_hop: Optional[np.ndarray] = None,
    similarity_weight: float = 0.05,
    hub_correction: bool = False,
) -> np.ndarray:
    """Construct a passage prior close in spirit to the paper's Eq. (7).

    The implementation keeps the components easy to inspect. Entity evidence
    is log-compressed; optional IDF reduces generic entity hubs. ``first_hop``
    uses 1-based levels in the denominator: seed=1, first bridge=2, etc.
    """
    contain = contain.tocsr().astype(np.float64)
    a = np.asarray(activated_entity_scores, dtype=np.float64)
    sim = np.asarray(passage_similarity, dtype=np.float64)
    if contain.shape[1] != a.shape[0]:
        raise ValueError("entity score length mismatch")
    if contain.shape[0] != sim.shape[0]:
        raise ValueError("passage similarity length mismatch")

    if first_hop is None:
        level_weight = np.ones_like(a)
    else:
        first_hop = np.asarray(first_hop)
        # -1 means never activated. seed hop 0 -> level 1.
        level_weight = np.zeros_like(a)
        active = first_hop >= 0
        level_weight[active] = 1.0 / (first_hop[active] + 1.0)

    entity_weight = a * level_weight
    if hub_correction:
        entity_weight = entity_weight * entity_idf(contain)

    # Binary contain matrices are enough for the synthetic tests. Log1p makes
    # the prior robust if counts are supplied in a future real-data adapter.
    entity_mass = np.asarray(contain @ entity_weight).ravel()
    return similarity_weight * sim + np.log1p(np.maximum(entity_mass, 0.0))


def personalized_pagerank_bipartite(
    contain: sparse.csr_matrix,
    entity_reset: np.ndarray,
    passage_reset: np.ndarray,
    config: PPRConfig,
) -> tuple[np.ndarray, np.ndarray]:
    """Run PPR on a passage/entity bipartite graph."""
    contain = contain.tocsr().astype(np.float64)
    p, e = contain.shape
    zero_pp = sparse.csr_matrix((p, p), dtype=np.float64)
    zero_ee = sparse.csr_matrix((e, e), dtype=np.float64)
    adjacency = sparse.bmat([[zero_pp, contain], [contain.T, zero_ee]], format="csr")

    degrees = np.asarray(adjacency.sum(axis=1)).ravel()
    inv_degree = np.zeros_like(degrees)
    mask = degrees > 0
    inv_degree[mask] = 1.0 / degrees[mask]
    transition = sparse.diags(inv_degree) @ adjacency

    reset = np.concatenate([
        np.maximum(np.asarray(passage_reset, dtype=np.float64), 0.0),
        np.maximum(np.asarray(entity_reset, dtype=np.float64), 0.0),
    ])
    total = reset.sum()
    if total <= 0:
        reset[:] = 1.0 / reset.size
    else:
        reset /= total

    rank = reset.copy()
    for _ in range(config.max_iter):
        next_rank = (1.0 - config.damping) * reset + config.damping * (transition.T @ rank)
        if np.abs(next_rank - rank).sum() <= config.tol:
            rank = next_rank
            break
        rank = next_rank

    return rank[:p], rank[p:]


def rank_passages(
    contain: sparse.csr_matrix,
    activated_entity_scores: np.ndarray,
    passage_similarity: np.ndarray,
    first_hop: np.ndarray,
    config: PPRConfig,
) -> np.ndarray:
    reset_passage = passage_reset_scores(
        contain,
        activated_entity_scores,
        passage_similarity,
        first_hop=first_hop,
        similarity_weight=config.passage_similarity_weight,
        hub_correction=config.hub_correction,
    )
    passage_rank, _ = personalized_pagerank_bipartite(
        contain,
        entity_reset=activated_entity_scores,
        passage_reset=reset_passage,
        config=config,
    )
    return np.argsort(passage_rank)[::-1]
