#!/usr/bin/env python3
"""Demonstrate the impact of an off-by-one entity level in passage priors."""
from __future__ import annotations

import json
import math


def bonus(score: float, occurrence: int, tier: int) -> float:
    return score * math.log1p(occurrence) / max(tier, 1)


def main():
    bridge_score = 0.70
    target_score = 0.80
    dense_weight = 0.20
    distractor_dense = 0.10
    gold_dense = 0.80
    old_distractor = dense_weight * distractor_dense + bonus(bridge_score, 1, tier=1)
    fixed_distractor = dense_weight * distractor_dense + bonus(bridge_score, 1, tier=2)
    gold = dense_weight * gold_dense + bonus(target_score, 1, tier=3)
    payload = {
        "old_first_hop_tier": 1,
        "correct_first_hop_tier": 2,
        "old_distractor_score": old_distractor,
        "fixed_distractor_score": fixed_distractor,
        "gold_score": gold,
        "old_ranking": "distractor>gold" if old_distractor > gold else "gold>=distractor",
        "fixed_ranking": "distractor>gold" if fixed_distractor > gold else "gold>=distractor",
        "first_hop_bonus_inflation": bonus(bridge_score, 1, 1) / bonus(bridge_score, 1, 2),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
