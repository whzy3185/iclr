from pathlib import Path
import sys

import numpy as np
from scipy import sparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from linearrag_opt.retrieval import entity_idf, personalized_pagerank_bipartite, PPRConfig


def test_idf_downweights_common_entity():
    contain = sparse.csr_matrix([
        [1, 1],
        [1, 0],
        [1, 0],
    ], dtype=float)
    weights = entity_idf(contain)
    assert weights[1] > weights[0]


def test_ppr_returns_normalized_mass():
    contain = sparse.csr_matrix([[1, 0], [0, 1]], dtype=float)
    p, e = personalized_pagerank_bipartite(
        contain,
        entity_reset=np.array([1.0, 0.0]),
        passage_reset=np.array([0.5, 0.0]),
        config=PPRConfig(),
    )
    assert np.isclose(p.sum() + e.sum(), 1.0, atol=1e-8)
    assert p[0] > p[1]
