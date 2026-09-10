from pathlib import Path
import sys

import numpy as np
from scipy import sparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from linearrag_opt import BridgeConfig, contextual_seed_candidates, semantic_bridge


def test_gold_chain_propagates_three_hops():
    mention = sparse.csr_matrix([
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
    ], dtype=float)
    sigma = np.array([0.9, 0.8, 0.7])
    result = semantic_bridge(
        mention,
        sigma,
        {0: 1.0},
        BridgeConfig(max_hops=3, threshold=0.1, normalization="entity_degree"),
    )
    assert np.all(result.scores > 0)
    assert result.first_hop[0] == 0
    assert result.first_hop[3] == 3


def test_contextual_seed_can_correct_surface_only_error():
    surface = np.array([0.96, 0.92])
    context = np.array([0.18, 0.91])
    selected, _ = contextual_seed_candidates(surface, context, alpha=0.55, ambiguity_margin=0.08)
    assert selected.tolist() == [1]
