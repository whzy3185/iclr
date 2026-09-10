#!/usr/bin/env python3
"""Tiny demonstration of full-query context in ambiguous seed selection."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from linearrag_opt import contextual_seed_candidates


def main():
    surface = np.array([0.96, 0.92])
    context = np.array([0.18, 0.91])
    baseline = int(np.argmax(surface))
    selected, scores = contextual_seed_candidates(surface, context, alpha=0.55, top_m=2, ambiguity_margin=0.08)
    print(json.dumps({
        "surface_only_choice": baseline,
        "contextual_choices": selected.tolist(),
        "contextual_scores": scores.tolist(),
        "expected_right_sense": 1,
    }, indent=2))


if __name__ == "__main__":
    main()
