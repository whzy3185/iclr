# Codex Task — Complete ICLR 2024–2026 Abstract Corpus

Status: AUTHORIZED DATA-ONLY TASK
Scientific proposal generation: FORBIDDEN
Target: all accepted ICLR Conference papers for 2024, 2025, 2026

## Objective

Produce one complete, auditable, normalized abstract corpus for ICLR 2024–2026.

Official denominators currently known:
- ICLR 2024: 2260
- ICLR 2025: 3703
- ICLR 2026: 5351

Reuse existing recovery assets/caches. Do not redownload verified pages unless needed for integrity repair.

## Branch / existing work

Start from or continue the existing recovery work containing the cached 2025/2026 pages:
`codex/f0-recovery-20260908`

Before editing, fetch latest `main` and read this task file. Preserve all existing recovery artifacts and provenance.

## Task chain

### T1 — Inventory

Create `experiments/idea_collapse/corpus/iclr_2024_2026/STATUS.md` and record, per year:
- official denominator
- cached pages
- parsed abstracts
- missing IDs
- parse failures
- duplicate IDs
- source hashes

Do not infer missing abstracts from titles.

### T2 — Complete acquisition

Complete all missing official Conference abstract pages for 2024–2026.

Source priority:
1. official `proceedings.iclr.cc` abstract page
2. linked OpenReview metadata only when official abstract retrieval remains unavailable
3. no generated/synthesized abstract under any condition

Use bounded retries and preserve every failure/retry reason.

Do not overwrite already verified cache entries unless hash/integrity checks fail.

### T3 — Normalize

Produce one row per official paper with schema:

```text
paper_id
year
title
abstract
authors
proceedings_abstract_url
openreview_url
pdf_url
source_type
source_retrieved_at
source_sha256
abstract_sha256
parse_status
```

Required outputs:

```text
experiments/idea_collapse/corpus/iclr_2024_2026/
  iclr2024_abstracts.jsonl
  iclr2025_abstracts.jsonl
  iclr2026_abstracts.jsonl
  iclr2024_missing.jsonl
  iclr2025_missing.jsonl
  iclr2026_missing.jsonl
  corpus_2024_2026.jsonl
  corpus_manifest.json
  corpus_sha256.txt
  acquisition_failures.jsonl
  STATUS.md
```

### T4 — Validate completeness

For each year verify:

```text
unique normalized rows == official denominator
non-empty abstract count == official denominator
paper IDs unique
all rows map to official Conference index
no title-only surrogate abstracts
no silently dropped IDs
```

If any abstract is still unavailable, keep the official paper row with `abstract=null`, explicit failure status, and report exact missing IDs. Never claim 100% completeness unless these checks pass.

### T5 — Reproducibility tests

Add tests for:
- official index denominator reconciliation
- duplicate rejection
- empty/HTML-error abstract rejection
- deterministic normalization
- hash stability
- resume without redownloading verified cache

Run full corpus pipeline twice and confirm normalized outputs are byte-identical.

### T6 — Final report and STOP

Create:

`experiments/idea_collapse/corpus/iclr_2024_2026/CORPUS_COMPLETION_REPORT.md`

Report exactly:

```text
ICLR2024_OFFICIAL=
ICLR2024_ABSTRACTS=
ICLR2024_MISSING=
ICLR2025_OFFICIAL=
ICLR2025_ABSTRACTS=
ICLR2025_MISSING=
ICLR2026_OFFICIAL=
ICLR2026_ABSTRACTS=
ICLR2026_MISSING=
TOTAL_OFFICIAL=
TOTAL_ABSTRACTS=
TOTAL_MISSING=
CORPUS_SHA256=
TESTS=
```

Push the branch and return commit SHA plus the fields above.

STOP after corpus completion.

## Hard prohibitions

Do not run:
- route-effect experiments
- research proposal generation
- ARS/model pilot
- baseline propensity estimation
- treatment generation
- paper-result writing

This task only completes and verifies the ICLR 2024–2026 abstract dataset.
