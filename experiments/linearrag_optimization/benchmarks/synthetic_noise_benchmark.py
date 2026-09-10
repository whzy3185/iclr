#!/usr/bin/env python3
"""Mechanism benchmark for noisy relation-free entity propagation."""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from linearrag_opt import BridgeConfig, PPRConfig, make_hub_noise_case, rank_passages, semantic_bridge


VARIANTS = {
    "paper_like_raw": (BridgeConfig(normalization="none", threshold=0.15, max_hops=3), PPRConfig(hub_correction=False)),
    "degree_normalized": (BridgeConfig(normalization="entity_degree", threshold=0.15, max_hops=3), PPRConfig(hub_correction=False)),
    "degree_norm_budget": (BridgeConfig(normalization="entity_degree", threshold=0.15, max_hops=3, frontier_budget=32), PPRConfig(hub_correction=False)),
    "degree_norm_budget_idf": (BridgeConfig(normalization="entity_degree", threshold=0.15, max_hops=3, frontier_budget=32), PPRConfig(hub_correction=True)),
}


def evaluate_one(case, bridge_cfg, ppr_cfg, top_k=5):
    t0 = time.perf_counter()
    bridge = semantic_bridge(case.mention, case.sentence_similarity, case.seed_scores, bridge_cfg)
    ranking = rank_passages(case.contain, bridge.scores, case.passage_similarity, bridge.first_hop, ppr_cfg)
    elapsed = time.perf_counter() - t0

    top = ranking[:top_k]
    gold = set(case.gold_passages.tolist())
    recall = len(gold.intersection(top.tolist())) / len(gold)
    precision = len(gold.intersection(top.tolist())) / top_k
    gold_entity_recall = np.mean(bridge.scores[case.gold_entities] > 0)
    hub_score = float(bridge.scores[case.hub_entity])
    active = int(np.count_nonzero(bridge.scores))
    return {
        "passage_recall_at_k": recall,
        "passage_precision_at_k": precision,
        "gold_entity_recall": float(gold_entity_recall),
        "hub_score": hub_score,
        "active_entities": active,
        "runtime_ms": elapsed * 1000.0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    all_rows = []
    for trial in range(args.trials):
        case = make_hub_noise_case(seed=trial)
        for name, (bridge_cfg, ppr_cfg) in VARIANTS.items():
            metrics = evaluate_one(case, bridge_cfg, ppr_cfg, top_k=args.top_k)
            all_rows.append({"trial": trial, "variant": name, **metrics})

    summary = {}
    for name in VARIANTS:
        rows = [r for r in all_rows if r["variant"] == name]
        summary[name] = {
            key: {
                "mean": float(np.mean([r[key] for r in rows])),
                "std": float(np.std([r[key] for r in rows], ddof=1)),
            }
            for key in [
                "passage_recall_at_k",
                "passage_precision_at_k",
                "gold_entity_recall",
                "hub_score",
                "active_entities",
                "runtime_ms",
            ]
        }

    payload = {
        "trials": args.trials,
        "top_k": args.top_k,
        "variants": {
            name: {"bridge": asdict(b), "ppr": asdict(p)}
            for name, (b, p) in VARIANTS.items()
        },
        "summary": summary,
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
