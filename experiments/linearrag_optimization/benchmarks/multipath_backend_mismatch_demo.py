#!/usr/bin/env python3
"""Show a semantic mismatch between per-path last-write state and summed matrix state."""
from __future__ import annotations

import json


def main():
    source_scores = [0.90, 0.80]
    sentence_similarity = 0.70
    path_scores = [x * sentence_similarity for x in source_scores]
    bfs_entity_weight = sum(path_scores)
    bfs_activated_state_forward_order = path_scores[-1]
    bfs_activated_state_reverse_order = path_scores[0]
    vectorized_activated_state = sum(source_scores) * sentence_similarity
    print(json.dumps({
        "path_scores": path_scores,
        "bfs_entity_weight_accumulator": bfs_entity_weight,
        "bfs_activated_state_forward_order": bfs_activated_state_forward_order,
        "bfs_activated_state_reverse_order": bfs_activated_state_reverse_order,
        "vectorized_activated_state": vectorized_activated_state,
        "vectorized_over_forward_bfs_state": vectorized_activated_state / bfs_activated_state_forward_order,
        "order_dependence": bfs_activated_state_forward_order != bfs_activated_state_reverse_order,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
