# Source-side Semantic, Temporal and Anonymization Gate

Authority: `CODEX_F0_SEMANTIC_TEMPORAL_ANONYMIZATION_TASK.md`, from research
branch commit `b57e83a6c85ce14d6d64b3e041709a2d14906a80`.
Input base: `c5e4391f3af6f7ff67291352c632731d58350293`.

This is not ARS, P0/P1, a baseline-propensity measurement, or a proposal experiment.
Only frozen source text, embedding/cross-encoder scores, candidate matching, and
unlabelled human-review materials are processed. ICLR 2024 is not evidence here.

## Run Order

1. `scripts/prepare_sources.py`: corpus reconciliation, unchanged legacy seed
   transform, discovered-date sources, metadata-only anonymity. Raw corpus
   caches are reused, not redownloaded.
2. `scripts/semantic_compute.py encode`: all 5351 seed queries, 3703 evidence
   abstracts, top-200 before route filtering. Exact model revisions are in config.
3. `scripts/semantic_compute.py rerank`: every top-200 pair for each existing
   source-gate-allowed seed. Blocked seed records remain present with null scores.
4. `scripts/build_bank.py`: relevance diagnostics, exact matching, attrition and
   fixed-stratum F1 candidates. Run twice to compare immutable outputs.
5. `scripts/final_checkpoint.py`: source/cache/packet verification and exact T8 report.

Example commands from repository root, using a prepared Python environment and
local safetensors snapshots downloaded at the exact configured revisions:

```sh
python -m unittest discover -s experiments/idea_collapse/f0_semantic_temporal/tests -v
python experiments/idea_collapse/f0_semantic_temporal/scripts/prepare_sources.py --legacy-root "$LEGACY_F0_SOURCE_ROOT"
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTORCH_ENABLE_MPS_FALLBACK=0 python experiments/idea_collapse/f0_semantic_temporal/scripts/semantic_compute.py encode --dense-path "$DENSE_MODEL_PATH" --reranker-path "$RERANKER_MODEL_PATH"
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTORCH_ENABLE_MPS_FALLBACK=0 python experiments/idea_collapse/f0_semantic_temporal/scripts/semantic_compute.py rerank --dense-path "$DENSE_MODEL_PATH" --reranker-path "$RERANKER_MODEL_PATH"
HF_HUB_OFFLINE=1 python experiments/idea_collapse/f0_semantic_temporal/scripts/build_bank.py --reranker-path "$RERANKER_MODEL_PATH"
HF_HUB_OFFLINE=1 python experiments/idea_collapse/f0_semantic_temporal/scripts/build_bank.py --reranker-path "$RERANKER_MODEL_PATH"
python experiments/idea_collapse/f0_semantic_temporal/scripts/final_checkpoint.py
```

Library/file versions, tokenizer hashes, dtype, device and preprocessing are in
`semantic/model_manifest.json`. Model weights stay outside Git; IDs/revisions
and file SHA256 permit retrieval of the same public snapshots. No remote code
is trusted and no generative model class is loaded. Numerical tolerances were
fixed before source inference. Exact-cache replay is distinct from independent
recomputation; repeated inference is checked on a declared engineering subset.

`semantic/inference_provenance.json` records code snapshots and the fact that
initial execution began before the implementation commit was created. This
timing is not relabeled. The later cache-replay repair changes no source scores.

## Artifact Schemas

Dense/reranked JSONL records use parallel arrays, one row per seed. The array
position is the dense rank; the independent reranker order/ranks are retained
in the relevance diagnostics. Query/evidence hashes and tokenizer lengths are
in embedding manifests. Larger diagnostic arrays are gzip JSONL, not filtered.

`matching/eligible_edges.jsonl` provides A/B paper-ID arrays and numeric edge
tuples with an explicit field list. Rejected edge reasons live in
`matching/rejected_edges.jsonl.gz`, keyed by the same seed/pair and A/B array
indices. Source exclusions are in `matching/source_exclusions.jsonl.gz`.
`matching/unmatched_rows.jsonl` uses side/index/reason-code tuples with a legend.
These encodings avoid repeating source IDs/reasons millions of times; no
inadmissible edge or failed row is silently dropped.

## Important Boundaries

Discovered public dates are not a certificate of actual earliest history.
OpenReview challenge-required access was not bypassed. Proceedings fallback
dates must be carried into human/source-history review; do not rename the bank
historically temporal-clean merely because discovered-date inequalities pass.

The anonymous renderer emits only normalized real abstracts. Intrinsic method
names, years, URLs or self-identifying prose remain. This is metadata anonymity,
not a guarantee that sources cannot be recognized. Distribute only the visible
F1 candidate files to annotators, not hidden provenance or score tables.

F1 selection is disjoint by unique seed, fixed before generator outcomes, and
stratified over source-side descriptors. No human label is filled automatically.
All scientific hypotheses remain UNTESTED. STOP at the human certification gate.
