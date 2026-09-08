# Codex Task — F0 Semantic + Temporal + Source-Anonymization Gate

Base commit: `c5e4391f3af6f7ff67291352c632731d58350293`

## Scope

This is a **source-side engineering / feasibility task only**. Do not run any research-proposal generation, ARS, baseline measurement, treatment outcome experiment, or LLM scientific-choice experiment.

The 2024–2026 accepted ICLR abstract corpus is now frozen and complete:

- ICLR 2024: 2260 / 2260
- ICLR 2025: 3703 / 3703
- ICLR 2026: 5351 / 5351
- corpus SHA256: `0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807`

Primary causal-core roles remain frozen for this round:

- **Seeds:** ICLR 2026 accepted Conference papers, converted to the existing method-masked scientific-question representation.
- **Evidence pool:** ICLR 2025 accepted Conference papers.
- **ICLR 2024:** retain as a complete auxiliary corpus for engineering checks / future robustness, but do **not** silently mix it into the confirmatory evidence pool in this round.

The goal is to replace the current `LEXICAL_PROVISIONAL` matching status with a measured semantic/temporal/source-anonymous candidate bank suitable for later F1 human construct certification.

---

## Hard scientific constraints

1. No scientific outcomes may be generated or inspected.
2. Do not choose seeds, route pairs, thresholds, models, or packet size based on any proposal-generation outcome.
3. Preserve every denominator, null, failure, and attrition reason.
4. Do not manufacture contrast with off-topic evidence.
5. Matching objective must be **maximize cardinality first, then minimize declared nuisance-matching cost**.
6. Do not overmatch away route content itself. Route-changing method/finding content is the intended treatment difference.
7. Source anonymity removes metadata cues, not scientific content. Do not rewrite abstracts into summaries in the ecological core.
8. Human construct validity remains unresolved after this task. Do not label candidate blocks as scientifically valid merely because semantic scores are high.

---

# T0 — Reconcile frozen inputs

Verify the complete corpus against the base commit and existing F0 recovery artifacts.

Must confirm:

- 11314 unique official IDs total
- 2024 = 2260
- 2025 = 3703
- 2026 = 5351
- 0 missing abstracts
- frozen corpus SHA matches the value above
- previous route definitions / method-masked seed artifacts are loaded without changing their scientific definitions

Write `T0_INPUT_RECONCILIATION.json`.

If the corpus SHA differs, STOP and report the mismatch.

---

# T1 — Earliest-public-date map

Construct a provenance-preserving earliest-public-date map for the papers actually relevant to the causal core: all candidate ICLR 2025 evidence papers and all candidate ICLR 2026 seeds.

For each paper, attempt to recover verifiable public dates from available public sources, preferring evidence that reflects actual public availability. Candidate sources include:

- arXiv v1 submission date
- OpenReview public forum / public posting date
- official proceedings publication date when earlier-public evidence is unavailable

Define:

`earliest_public_date = min(verifiable public dates)`

Never infer a date from local file mtimes, cache times, acceptance year, or filename. Unknown stays null.

For every non-null date retain:

- paper_id
- date
- date_source_type
- source URL / stable identifier
- source field used
- source retrieval timestamp if newly fetched
- source hash / provenance record when feasible

Output:

- `temporal/earliest_public_dates.jsonl`
- `temporal/temporal_failures.jsonl`
- `temporal/temporal_summary.json`

Report coverage separately for 2025 evidence and 2026 seeds.

Also compute the actual distribution of evidence-date minus seed-date feasibility for the existing candidate relationships. Do not assume all 2025 evidence is temporally clean merely from conference year.

---

# T2 — Frozen semantic retrieval backend

Implement a reproducible semantic retrieval backend over the real abstracts.

Requirements:

- one frozen open dense retriever
- one **independent** frozen reranker / semantic relevance model
- exact model IDs, revisions, library versions, tokenizer versions, device, dtype, and normalization recorded
- deterministic preprocessing and deterministic candidate ordering
- cache all embeddings and reranker scores
- no silent fallback to lexical similarity if model acquisition/inference fails

Recommended default configuration if technically available:

- dense retriever: `BAAI/bge-base-en-v1.5`
- reranker: `BAAI/bge-reranker-base`

If a different model is necessary, document the reason before running and keep the backend frozen thereafter. Do not compare many models and select the one that yields the largest candidate bank.

Use the existing method-masked seed representation as the query object. Retrieve from ICLR 2025 evidence only.

For each seed retain at least top-200 dense candidates before route filtering where capacity allows.

Output:

- `semantic/model_manifest.json`
- `semantic/seed_embeddings_manifest.jsonl`
- `semantic/evidence_embeddings_manifest.jsonl`
- `semantic/dense_candidates.jsonl`
- `semantic/reranked_candidates.jsonl`

---

# T3 — Semantic relevance diagnostics

For every candidate source relationship, retain source-side relevance signals including:

- dense similarity
- independent reranker score
- lexical score from the prior F0 backend where available, for diagnostic comparison only
- seed/evidence token length
- title-free abstract text hash
- earliest-public dates and date gap where known

Produce diagnostics, not outcome-driven thresholds.

Report:

- score distributions
- lexical-vs-dense overlap at top-k
- dense-vs-reranker rank agreement
- examples of high lexical / low semantic candidates
- examples of low lexical / high semantic candidates
- missing temporal coverage

Create a small **development-only relevance audit sheet** containing a stratified sample of candidate seed–paper pairs for later human inspection. Do not assign human labels yourself.

---

# T4 — Source-anonymous evidence transform

Create the exact representation that could later be shown to a generator.

For the core RAW evidence representation:

REMOVE metadata cues including:

- paper title
- authors
- venue label
- conference year
- URL
- paper ID
- citation count
- retrieval score / rank
- source database label

RETAIN:

- the real scientific abstract content, with only deterministic whitespace / Unicode normalization

Do **not** remove method names, findings, limitations, or technical vocabulary from the abstract in this core transform. Cue-reduced evidence is a later robustness experiment, not part of F0.

Each anonymous evidence object must have an internal non-presented key so it can be traced back to its source without exposing source identity to the generator.

Output:

- `anonymization/anonymous_evidence.jsonl`
- `anonymization/anonymization_manifest.json`
- `anonymization/leak_audit.json`

Leak audit must programmatically test that rendered evidence packets do not expose title/authors/venue/year/URL/paper ID/retrieval score/rank via metadata fields or templates. Do not alter abstract semantics just to pass the leak audit.

---

# T5 — Rebuild pairwise matched slots with semantic nuisance matching

Use the existing source-side route taxonomy and route-pair definitions as **provisional engineering labels**. Do not call them human-certified.

For each seed × route-pair block, construct A/B source slots from semantically relevant evidence.

The matching objective is lexicographic:

1. maximize number of valid A/B matched slots;
2. among maximum-cardinality matchings, minimize declared nuisance mismatch cost.

Nuisance variables may include:

- seed relevance from dense retrieval
- seed relevance from independent reranker
- token length
- earliest-public date / date gap when available
- topic/problem compatibility signals

Do not include a cost that forces A/B abstracts to be globally semantically identical in a way that removes the route-level method/finding distinction itself.

Retain exact edge eligibility reasons, unmatched reasons, and final matching cost components.

Re-run deterministic max-cardinality counterexample tests from Round 52.

Output:

- `matching/eligible_edges.jsonl`
- `matching/matched_slots.jsonl`
- `matching/unmatched_rows.jsonl`
- `matching/matching_manifest.json`

---

# T6 — Coverage frontier

Measure unique-seed coverage after semantic/temporal/source-side filtering for packet-size targets:

- k = 4
- k = 6
- k = 8
- k = 12

Report by route pair:

- BUILD vs DIAGNOSE
- BUILD vs MEASURE
- BUILD vs EXPLAIN
- DIAGNOSE vs EXPLAIN

Do not define an automatic scientific PASS/FAIL threshold based on these counts.

Produce an attrition waterfall from:

`all 2026 seeds -> method-masked candidates -> route-pair candidates -> semantic candidates -> temporal-known/clean subset -> matched-slot capacity -> k coverage`

Every subtraction must have an explicit reason code.

---

# T7 — Prepare F1 candidate audit package

Do not perform F1 labels. Prepare the material for human construct certification.

Create a stratified candidate package that includes enough blocks to calibrate and then certify approximately 30–50 final independent seeds if the construct survives.

Stratify across:

- route pair
- semantic relevance strength
- matching difficulty
- topic area
- lexical-vs-semantic disagreement

For each candidate block prepare a human-readable record containing:

- method-masked seed
- neutral route A description
- neutral route B description
- representative source-anonymous A evidence abstracts
- representative source-anonymous B evidence abstracts
- hidden provenance reference in a separate machine-readable mapping

Do not expose generator outcomes because none should exist.

Output:

- `f1_package/F1_CALIBRATION_CANDIDATES.jsonl`
- `f1_package/F1_CERTIFICATION_CANDIDATES.jsonl`
- `f1_package/F1_HIDDEN_PROVENANCE.jsonl`
- `f1_package/F1_PACKAGE_MANIFEST.json`

---

# T8 — Final source-only checkpoint

Write `F0_SEMANTIC_TEMPORAL_RESULT.md` with exact measured values and statuses:

```text
CORPUS_SHA256=
DENSE_BACKEND=
RERANKER_BACKEND=
TEMPORAL_2025_COVERAGE=
TEMPORAL_2026_COVERAGE=
SEMANTIC_SEEDS_PROCESSED=
K4_UNIQUE_SEEDS=
K6_UNIQUE_SEEDS=
K8_UNIQUE_SEEDS=
K12_UNIQUE_SEEDS=
ROUTE_PAIR_K8_COUNTS=
ANONYMIZATION_LEAK_TESTS=
MATCHING_TESTS=
F1_CALIBRATION_BLOCKS=
F1_CERTIFICATION_BLOCKS=
SCIENTIFIC_PROPOSAL_GENERATIONS=0
SCIENTIFIC_HYPOTHESIS_STATUS=UNTESTED
NEXT_GATE=F1_HUMAN_CONSTRUCT_CERTIFICATION
```

Also write:

- `attrition_waterfall.csv`
- `semantic_temporal_decision_table.md`
- `FINAL_CHECKPOINT.md`

The scientific conclusion must distinguish:

- MEASURED
- NOT_RUN
- BLOCKED
- PENDING_HUMAN_REVIEW

Do not claim that a block is scientifically valid because it passed semantic or matching filters.

---

## Reproducibility

- cache all remote artifacts and model revisions
- preserve raw failed attempts
- no overwrite-in-place of prior F0 recovery artifacts
- deterministic normalized output ordering
- run source-side pipeline replay twice where practical and compare normalized artifacts
- record hardware/device differences if exact floating-point byte identity is not feasible for embedding computation; require deterministic IDs/ranks/scores within declared tolerance and document tolerance before comparison

---

## STOP condition

After publishing the source-side checkpoint and F1 package:

**STOP.**

Do not run F1 labels automatically.
Do not run GPT/LLM research-proposal generation.
Do not measure baseline propensity.
Do not construct outcome-dependent treatments.
Do not run P0/P1.

Push the branch and return the commit SHA plus the exact T8 summary block.