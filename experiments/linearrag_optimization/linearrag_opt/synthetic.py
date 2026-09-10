"""Synthetic relation-free graphs with controllable hub noise."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse


@dataclass
class SyntheticCase:
    mention: sparse.csr_matrix
    contain: sparse.csr_matrix
    sentence_similarity: np.ndarray
    passage_similarity: np.ndarray
    seed_scores: dict[int, float]
    gold_entities: np.ndarray
    gold_passages: np.ndarray
    hub_entity: int


def make_hub_noise_case(
    seed: int,
    n_entities: int = 500,
    n_passages: int = 300,
    n_background_sentences: int = 700,
    hub_sentence_count: int = 120,
    seed_hub_sentence_count: int = 18,
) -> SyntheticCase:
    """Create a 3-hop gold chain plus a high-degree distractor hub."""
    rng = np.random.default_rng(seed)
    gold_entities = np.array([0, 1, 2, 3], dtype=np.int64)
    hub = 4

    rows: list[int] = []
    cols: list[int] = []
    sigma: list[float] = []

    def add_sentence(entities, relevance):
        r = len(sigma)
        sigma.append(float(relevance))
        for ent in entities:
            rows.append(r)
            cols.append(int(ent))

    for i, rel in enumerate((0.97, 0.92, 0.87)):
        add_sentence([gold_entities[i], gold_entities[i + 1]], rel)

    for _ in range(seed_hub_sentence_count):
        add_sentence([0, hub], rng.uniform(0.68, 0.82))

    noise_entities = np.arange(5, n_entities)
    for _ in range(hub_sentence_count):
        other = int(rng.choice(noise_entities))
        add_sentence([hub, other], rng.uniform(0.45, 0.73))

    for _ in range(n_background_sentences):
        e1, e2 = rng.choice(noise_entities, size=2, replace=False)
        add_sentence([int(e1), int(e2)], rng.uniform(0.05, 0.50))

    mention = sparse.coo_matrix(
        (np.ones(len(rows), dtype=np.float64), (rows, cols)),
        shape=(len(sigma), n_entities),
    ).tocsr()

    p_rows: list[int] = []
    p_cols: list[int] = []

    def add_passage(p, entities):
        for ent in entities:
            p_rows.append(int(p))
            p_cols.append(int(ent))

    gold_passages = np.array([0, 1, 2], dtype=np.int64)
    add_passage(0, [0, 1])
    add_passage(1, [1, 2])
    add_passage(2, [2, 3])

    for p in range(3, min(90, n_passages)):
        add_passage(p, [hub, int(rng.choice(noise_entities))])

    for p in range(90, n_passages):
        ents = rng.choice(noise_entities, size=int(rng.integers(2, 5)), replace=False)
        add_passage(p, ents)

    contain = sparse.coo_matrix(
        (np.ones(len(p_rows), dtype=np.float64), (p_rows, p_cols)),
        shape=(n_passages, n_entities),
    ).tocsr()

    passage_similarity = rng.uniform(0.05, 0.48, size=n_passages)
    passage_similarity[gold_passages] = np.array([0.78, 0.68, 0.60])
    hard = rng.choice(np.arange(3, n_passages), size=12, replace=False)
    passage_similarity[hard] = rng.uniform(0.60, 0.76, size=hard.size)

    return SyntheticCase(
        mention=mention,
        contain=contain,
        sentence_similarity=np.asarray(sigma, dtype=np.float64),
        passage_similarity=passage_similarity,
        seed_scores={0: 1.0},
        gold_entities=gold_entities,
        gold_passages=gold_passages,
        hub_entity=hub,
    )
