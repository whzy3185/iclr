# F0 Recovery Inventory

Date: 2026-09-08. This is source recovery, not research-proposal evidence.

- Baseline main: `b9cbbfdf0bafcf30adc7b8e261fdad6f08eb0ff8`.
- Preserved implementation parent: `049a313ed2900f1acd9c2d6673abd2124280b85f`.
- Earlier reported snapshot: `e3eb75948dcd6745eb77f1def0ad0898cb1c839b`.
- Original branch: `codex/f0-source-only-snapshot`, clean, no running F0 process.
- Integration branch: `codex/f0-recovery-20260908`, separate worktree from current
  main. The original checkout and source cache were not modified.
- Actual recovered implementation: `legacy/f0_source_only_audit.py` (1012 lines).
  This is an archived legacy entry point, not the corrected runner; do not run
  its main function, which contains historical acquisition/overwrite behavior.
- Actual recovery entry point so far: `scripts/preserve_snapshot.py`.

## Verified R0 Data

| Universe | Official index | Cached pages | Parsed title and abstract |
| --- | ---: | ---: | ---: |
| ICLR 2025 evidence | 3703 | 3703 | 3703 |
| ICLR 2026 focal | 5351 | 3737 | 3737 |

All 9054 official IDs have a source-manifest row. Missing focal pages remain
visible. Recovery made zero acquisition requests and never inferred abstracts
from titles. The 1614 missing focal pages have not been downloaded in R0.

The frozen inventory is `runs/R0_20260908/R0_MANIFEST.json`, with source URLs,
raw-byte hashes, local relative cache keys, parse/missing status, normalized
corpus hashes and hashes of the four current specification documents.

## First Failure Must Remain Visible

`runs/R0_20260908/first_failed_run.zip` preserves the original output bytes,
including previous misleading report wording. The wrapper manifest supersedes
its scientific interpretation: **INCOMPLETE_GATE_SHORT_CIRCUIT**.

The old seed table contains 5351 `REVIEW_OR_FAIL` rows. Matching files contain
only empty tables. Matching cardinality is **null / NOT_RUN**, not measured 0.
The committed legacy source includes a subsequent seed-gate correction, so its
exact relationship to the earlier output-producing working tree is UNKNOWN.
Do not claim these earlier outputs were replayed from that corrected code.

Initial identified defects: warning/review states conflated with structural
failure; TF-IDF named dense relevance; greedy cardinality labeled maximum;
proceedings dates stored as first-public dates; uncalibrated keyword confidence;
zero/default values for computations not performed. These are engineering
diagnoses, not proof for or against the research hypothesis.

## Audit Selection and Publication Boundary

The first ten official IDs in each year form the R0 excerpt. Selection occurred
before corrected matching and does not depend on source-match success.
No legacy test suite was found. Recovery tests are not yet claimed at R0.
Large raw HTML caches remain at the preserved source checkout; official URLs,
content hashes and relative keys permit independent retrieval/verification.
The author-provided archive checksums remain in the original source archives.
Public abstract text is retained with attribution/URLs; no paper PDFs, credentials
or private keys are included. Public accessibility is not a new license grant.

The latest user request permits later ARS preparation/pilot only after F0 and its
decision table are complete. This does not change the source-only boundary
during recovery. No pilot, new route, MUSES or base-vs-instruct extension ran.
