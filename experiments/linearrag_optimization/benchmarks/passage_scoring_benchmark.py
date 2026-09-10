#!/usr/bin/env python3
"""Conservative microbenchmark for vectorizing passage/entity bonus scoring."""
from __future__ import annotations

import argparse
import json
import time

import numpy as np
from scipy import sparse


def build_case(seed: int, n_passages: int, n_entities: int, entities_per_passage: int, active_entities: int):
    rng = np.random.default_rng(seed)
    rows = np.repeat(np.arange(n_passages), entities_per_passage)
    cols = np.concatenate([
        rng.choice(n_entities, size=entities_per_passage, replace=False)
        for _ in range(n_passages)
    ])
    data = np.ones(rows.size, dtype=np.float64)
    contain = sparse.csr_matrix((data, (rows, cols)), shape=(n_passages, n_entities))
    active_idx = rng.choice(n_entities, size=active_entities, replace=False)
    active_score = rng.uniform(0.1, 1.0, size=active_entities)
    return contain, active_idx, active_score


def python_nested(contain: sparse.csr_matrix, active_idx: np.ndarray, active_score: np.ndarray):
    row_sets = [set(contain.indices[contain.indptr[i]:contain.indptr[i + 1]]) for i in range(contain.shape[0])]
    out = np.zeros(contain.shape[0], dtype=np.float64)
    for i, ents in enumerate(row_sets):
        total = 0.0
        for e, score in zip(active_idx, active_score):
            if int(e) in ents:
                total += float(score)
        out[i] = total
    return out


def sparse_matvec(contain: sparse.csr_matrix, active_idx: np.ndarray, active_score: np.ndarray):
    vec = np.zeros(contain.shape[1], dtype=np.float64)
    vec[active_idx] = active_score
    return np.asarray(contain @ vec).ravel()


def timed(fn, *args, repeats=3):
    values = []
    result = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = fn(*args)
        values.append(time.perf_counter() - t0)
    return result, min(values)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passages", type=int, default=20000)
    ap.add_argument("--entities", type=int, default=10000)
    ap.add_argument("--entities-per-passage", type=int, default=6)
    ap.add_argument("--active-entities", type=int, default=64)
    args = ap.parse_args()

    contain, active_idx, active_score = build_case(
        0, args.passages, args.entities, args.entities_per_passage, args.active_entities
    )
    nested_result, nested_time = timed(python_nested, contain, active_idx, active_score)
    sparse_result, sparse_time = timed(sparse_matvec, contain, active_idx, active_score)
    max_abs_diff = float(np.max(np.abs(nested_result - sparse_result)))

    print(json.dumps({
        "n_passages": args.passages,
        "n_entities": args.entities,
        "entities_per_passage": args.entities_per_passage,
        "active_entities": args.active_entities,
        "python_nested_s": nested_time,
        "sparse_matvec_s": sparse_time,
        "speedup": nested_time / sparse_time,
        "max_abs_diff": max_abs_diff,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
