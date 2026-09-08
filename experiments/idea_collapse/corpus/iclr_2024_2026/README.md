# ICLR 2024-2026 Accepted Conference Abstract Corpus

This directory contains actual source abstracts, not generated summaries.
Read `CORPUS_COMPLETION_REPORT.md`, `corpus_manifest.json` and `VERIFICATION.json`.

## Data

- `corpus_2024_2026.jsonl`: all 11314 official paper IDs, ordered by year and ID.
- `iclr2024_abstracts.jsonl`, `iclr2025_abstracts.jsonl`, `iclr2026_abstracts.jsonl`:
  per-year tables, with 2260, 3703 and 5351 verified nonempty abstracts.
- `iclr*_missing.jsonl`: retained missing-ID tables, currently empty.
- `acquisition_failures.jsonl`: 136 retained unsuccessful attempts, subsequently
  resolved within the bounded retry policy; these are not 136 missing papers.
- `raw_sources_manifest.jsonl`: source hash and local relative cache mapping.
- `inventory/`, `pass1/`, `pass2/`: preserved inventory and both complete passes.
- `indexes/`: frozen official Conference indexes and membership evidence.

Every source is official proceedings. Linked OpenReview fallback is implemented
and tested but was not needed. The 7440 verified legacy pages were never
redownloaded. Acquisition involved only the 3874 initially missing paper IDs.

Legacy caches do not record reliable historical retrieval times. Their
`source_retrieved_at` is null. New acquisition times are retained from immutable
request records, not regenerated while normalizing or replaying. Raw HTML remains
in the original cache or this directory's ignored `_cache/`; source URLs and
hashes remain published. Public accessibility is not a new license grant; retain
the original authors/source attribution and respect original source terms.

## Reproduce

Python 3.12 standard library only. All commands below run from the repository
root. Supply the original F0 source root as `LEGACY_ROOT`; its cache is read-only.
For an external clone without those raw caches, missing pages will be acquired
from the saved official indexes. A fresh network acquisition can change raw page
bytes and retrieval timestamps; the published SHA identifies this frozen snapshot.

```sh
python3.12 -m unittest discover -s experiments/idea_collapse/corpus/iclr_2024_2026/tests -v
python3.12 experiments/idea_collapse/corpus/iclr_2024_2026/scripts/complete_corpus.py --legacy-root "$LEGACY_ROOT" --verified-manifest experiments/idea_collapse/feasibility_1/runs/R0_20260908/raw_sources_manifest.jsonl.gz --workers 6 --output rerun1
python3.12 experiments/idea_collapse/corpus/iclr_2024_2026/scripts/complete_corpus.py --legacy-root "$LEGACY_ROOT" --verified-manifest experiments/idea_collapse/feasibility_1/runs/R0_20260908/raw_sources_manifest.jsonl.gz --workers 6 --output rerun2
```

An optional `--proxy` selects the host's configured proxy; no credentials are
hard-coded. Use new output-directory names: prior results are not overwritten.
The actual completed executions used `--output pass1` and `--output pass2`.
The finalizer reparsed each included abstract from source bytes, verified source
and abstract SHA256, reconciled all denominators and compared both normalized
passes. Different per-pass request counts live only in execution manifests.

No ARS, model, baseline/treatment or research-proposal experiment was executed.
