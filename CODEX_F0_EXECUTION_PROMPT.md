# CODEX F0 EXECUTION PROMPT — Engineering Contract

> Repository: `whzy3185/iclr`
> Authority: **this file is the Codex launcher for F0 execution**
> Scientific authority: `CODEX_F0_MASTER.md`
> Status: **AUTHORIZED**
> Scientific proposal generation: **FORBIDDEN**
> Expected branch: `codex/f0-source-feasibility`

## 0. Mission

Execute a source-only feasibility audit for the current ICLR experiment.

You are not testing the scientific hypothesis. You are determining whether the real ICLR 2025/2026 literature can support enough temporally auditable, multi-route, relevance-matched, pairwise-matched evidence blocks to justify a later controlled LLM experiment.

The sole final scientific-engineering question for this task is:

> **Can the source universe support a broad enough bank of valid `seed × route-pair` blocks with `k=6/8/12` pairwise matched A/B evidence slots, without using any research-proposal outcomes?**

Do not generate research ideas/proposals in F0.

---

# 1. Branch and synchronization contract

Start from the latest remote `main`. Do **not** continue the stale branch `codex/p0-task0-task1`.

Required startup commands, adapting only transport details if necessary:

```bash
git fetch origin main codex/p0-task0-task1
git switch --detach origin/main
git switch -c codex/f0-source-feasibility
```

Record immediately in:

```text
experiments/idea_collapse/feasibility_1/STATUS.md
```

- `origin/main` SHA;
- new branch SHA;
- old Codex branch SHA;
- Python version;
- OS/platform;
- available CPU/GPU/MPS;
- network availability;
- dependency manager.

## Never merge the old Codex branch wholesale

The old branch implemented an obsolete top-k/MMR/540-idea study. It is not scientifically authoritative.

### Old-branch migration allowlist

You MAY reuse/reimplement from `origin/codex/p0-task0-task1` only after inspecting the code:

```text
experiments/idea_collapse/generation/provenance.py
experiments/idea_collapse/corpus/index_proceedings.py
experiments/idea_collapse/tests/test_index.py
```

You MAY additionally reuse small pure utility functions for:

- canonical JSON serialization;
- SHA256 hashing;
- exclusive/immutable writes;
- Git-state recording;
- strict JSON parsing;

only if they contain no old scientific assumptions.

### Explicitly forbidden to migrate as authoritative scientific logic

Do not migrate or reuse without a complete rewrite/review:

```text
old pilot configs
old top-k/MMR condition logic
old 3-domain hard-coded corpus schema
old 540-generation design
old diversity metrics as primary F0 logic
old scientific generation runner/provider configuration
old PILOT_LOCK/PILOT_RESULT logic
```

Create:

```text
experiments/idea_collapse/feasibility_1/MIGRATION_LOG.md
```

For every reused old-branch file/function record:

```text
source branch/path
source blob SHA
new path
kept functions
removed/rewritten assumptions
reason for reuse
new tests covering it
```

No unlogged old-branch migration is allowed.

---

# 2. Read order and authority

Read in this order before implementation:

1. `README.md`
2. `CODEX_F0_EXECUTION_PROMPT.md`
3. `CODEX_F0_MASTER.md`
4. `research/iclr_fit_validation/round27_route_equipoise_and_admissibility_audit.md`
5. `research/iclr_fit_validation/round30_seed_validity_method_masking_and_accessibility.md`
6. `research/iclr_fit_validation/round33_staged_execution_and_hard_gates.md`
7. `research/iclr_fit_validation/round44_pairwise_matched_evidence_slot_design.md`
8. `research/iclr_fit_validation/round45_balanced_packet_randomization_design.md`
9. `research/iclr_fit_validation/round46_source_route_purity_and_mixed_contribution_handling.md`
10. `research/iclr_fit_validation/round50_codex_branch_pi_audit.md`

If a referenced historical research filename is absent or renamed, record the mismatch in `STATUS.md` and use the latest source-of-truth concept in `README.md`, `CODEX_F0_MASTER.md`, and this execution prompt. Do not invent missing scientific requirements.

Priority for F0 conflicts:

```text
CODEX_F0_EXECUTION_PROMPT.md
> CODEX_F0_MASTER.md
> latest round files
> historical amendments/tasks
```

---

# 3. Hard scientific safety rails

During F0, absolutely do NOT:

- ask any LLM to propose a research idea, hypothesis, experiment, method, or paper;
- run no-context scientific proposal generation;
- run evidence-conditioned scientific proposal generation;
- estimate baseline route propensity from proposal generations;
- estimate treatment effects;
- tune routes, matching, seeds, thresholds, or retrieval using imagined future effects;
- rank/select seeds because they look likely to create a strong paper;
- write an abstract/results section that implies a phenomenon was observed;
- silently drop failed seeds, route pairs, papers, or matched slots;
- use LLM novelty/quality judgments as F0 ground truth.

Allowed LLM use is limited to **source-document transformation/classification**, such as:

- provisional route classification of a paper abstract;
- provisional Artifact/Knowledge family classification;
- source-grounded method masking of a focal abstract/problem statement;

and only if:

1. the input source text is preserved;
2. prompt/model/version is recorded;
3. raw classifier output is preserved;
4. the result is marked `PROVISIONAL`;
5. a human-audit packet is emitted;
6. the LLM is never asked what research direction should be pursued.

---

# 4. Engineering layout

All new F0 code goes under:

```text
experiments/idea_collapse/f0/
```

Target layout:

```text
experiments/idea_collapse/f0/
├── __init__.py
├── schemas.py
├── provenance.py
├── acquire_proceedings.py
├── acquire_abstracts.py
├── resolve_public_dates.py
├── build_seed_candidates.py
├── route_annotation.py
├── retrieval.py
├── matching.py
├── packet_simulation.py
├── reporting.py
└── config/
    └── f0.json

experiments/idea_collapse/tests/f0/
├── test_provenance.py
├── test_proceedings.py
├── test_temporal.py
├── test_seed_schema.py
├── test_route_schema.py
├── test_retrieval.py
├── test_matching.py
├── test_packet_simulation.py
└── test_reporting.py
```

All generated source-only F0 artifacts go under:

```text
experiments/idea_collapse/feasibility_1/
```

Do not place generated scientific outcomes anywhere because there must be none.

---

# 5. Phase E0 — migrate only reusable engineering assets

Goal: reuse old engineering work without importing obsolete scientific design.

Tasks:

1. inspect the migration allowlist files from `origin/codex/p0-task0-task1`;
2. copy/reimplement only useful pure utilities;
3. move provenance utilities into `f0/provenance.py` rather than treating `generation/` as authoritative;
4. port the official proceedings parser into `f0/acquire_proceedings.py`;
5. port/update the parser tests;
6. write `MIGRATION_LOG.md`.

Acceptance criteria:

```text
- no old pilot condition names in active F0 code
- no old fixed domains hard-coded in active F0 code
- no scientific generation import in F0 modules
- all migrated functionality covered by tests
```

Commit checkpoint:

```text
f0: migrate audited provenance and proceedings ingestion
```

If this phase cannot be completed cleanly, stop and record `BLOCKED_MIGRATION`.

---

# 6. Phase E1 — official proceedings + abstracts

## Evidence universe

ICLR 2025 accepted papers from official ICLR proceedings/OpenReview-linked metadata.

## Seed universe

ICLR 2026 accepted papers from official ICLR proceedings/OpenReview-linked metadata.

Acquire at minimum:

```text
paper_id
iclr_year
title
abstract
proceedings_abstract_url
paper_pdf_url if available
openreview_url if available
authors if available
keywords/area if available
```

### Acquisition rules

- official proceedings is the canonical acceptance universe;
- third-party lists may only be used as a cross-check, never silent replacement;
- every raw downloaded page/file gets SHA256;
- every normalized table gets SHA256;
- parse failures remain in a failure ledger;
- do not infer an abstract from title alone.

Required outputs:

```text
feasibility_1/raw_sources_manifest.jsonl
feasibility_1/iclr2025_papers.jsonl
feasibility_1/iclr2026_papers.jsonl
feasibility_1/acquisition_failures.jsonl
feasibility_1/corpus_hash.txt
```

Acceptance criteria:

```text
ICLR 2025:
  title+abstract coverage >= 95% of official proceedings entries

ICLR 2026:
  title+abstract coverage >= 95% of official proceedings entries

otherwise:
  mark ACQUISITION_INCOMPLETE and continue only if missingness is characterized;
  do not silently reduce the denominator.
```

Commit checkpoint:

```text
f0: acquire official ICLR 2025-2026 source corpus
```

---

# 7. Phase E2 — temporal cleanliness

Primary clean evidence rule:

```text
first_public_date > 2024-08-31
```

For each ICLR 2025 evidence paper resolve the earliest confidently discovered public date.

Priority sources:

1. arXiv first-submission date if confidently matched;
2. OpenReview original public submission date;
3. other official/public preprint metadata;
4. otherwise `UNKNOWN`.

Store:

```text
first_public_date
first_public_source
earliest_candidate_dates[]
earlier_public_version_found
earlier_version_search_status
temporal_status
```

Allowed temporal statuses:

```text
CLEAN
FAIL_PRE_CUTOFF
UNKNOWN
AMBIGUOUS_MATCH
```

Never call a paper CLEAN merely because the ICLR proceedings date is after the cutoff.

### arXiv matching rule

A discovered arXiv record is considered a confident match only if title normalization is near-exact and available author metadata is compatible. Record match score/method. Ambiguous matches remain `AMBIGUOUS_MATCH`.

Required output:

```text
feasibility_1/temporal_cleanliness.jsonl
feasibility_1/temporal_cleanliness_report.md
```

Report exact counts/percentages for all statuses.

Commit checkpoint:

```text
f0: resolve temporal-clean evidence subset
```

---

# 8. Phase E3 — candidate seed construction

Construct candidate seeds from ICLR 2026 papers.

Each seed is a **method-masked research problem/question**, not the focal paper's method and not a generated new research direction.

Required schema:

```text
seed_id
focal_paper_id
subfield
raw_problem_context
method_masked_question
removed_solution_tokens_entities[]
focal_first_public_date
problem_clarity
background_sufficiency
method_neutrality
multi_route_openness
technical_substance
iclr_relevance
focal_method_leak
solution_prescribed
distinctive_phrase_leak
too_broad
too_narrow
post_cutoff_concept_needs_definition
seed_to_title_similarity
seed_to_abstract_similarity
distinctive_ngram_overlap[]
status
```

Use statuses rather than deletion:

```text
CANDIDATE
LEAKAGE_RISK
SOLUTION_PRESCRIBED
TOO_BROAD
TOO_NARROW
INSUFFICIENT_CONTEXT
PENDING_HUMAN_AUDIT
```

### Method masking rule

The masked seed must remove:

- proposed method name;
- focal paper title wording that identifies the method;
- author names;
- solution-specific acronym/entity introduced by the paper;
- sentences that directly disclose the focal solution.

It must preserve:

- problem object;
- known limitation/problem;
- evaluation goal or scientific uncertainty;
- enough technical context for multiple plausible routes.

If machine-assisted masking is used, preserve input/prompt/output and mark provisional.

Required outputs:

```text
feasibility_1/seed_candidates.jsonl
feasibility_1/seed_validity_audit_packet.csv
```

Do not solve the seeds.

Commit checkpoint:

```text
f0: build method-masked ICLR 2026 seed candidates
```

---

# 9. Phase E4 — retrieval candidate pools

## Dense retriever

Preferred default:

```text
BAAI/bge-base-en-v1.5
```

## Independent reranker

Preferred default:

```text
BAAI/bge-reranker-base
```

Pin exact resolved model/revision/commit in `retrieval_config.json`.

If these exact models are unavailable, use a documented open substitute and mark:

```text
retrieval_stack_status = DEGRADED
```

Do not silently substitute.

For every seed:

1. query with the frozen method-masked seed text only;
2. retrieve a generous pool from temporal-clean ICLR 2025 evidence;
3. save dense score/rank for all retained candidates;
4. rerank the retained pool if reranker available;
5. do not modify the query using route labels.

Default candidate-pool target:

```text
top 200 dense candidates per seed
```

If the clean corpus has fewer, use the full clean corpus.

Required output:

```text
feasibility_1/retrieval_candidates.parquet OR .jsonl
feasibility_1/retrieval_config.json
```

Commit checkpoint:

```text
f0: build frozen source-only retrieval candidate pools
```

---

# 10. Phase E5 — provisional source-route annotation

Annotate only papers that appear in the union of retained retrieval candidate pools unless a full-corpus annotation is operationally cheaper.

Fine primary route enum:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
VERIFY_FALSIFY_REPLICATE
MIXED_UNCLEAR
```

Required annotation fields:

```text
primary_route
secondary_routes[]
route_purity 0..1
opposite_route_contamination
fine_route_confidence
coarse_contribution_family
coarse_confidence
rationale_source_span
annotation_backend
annotation_version
status
```

Coarse family:

```text
ARTIFACT
KNOWLEDGE
BOTH
UNCLEAR
```

### Route-clear core filter

For primary matched-slot feasibility counts, use route-clear source papers:

```text
primary_route != MIXED_UNCLEAR
route_purity >= 0.70
fine_route_confidence >= 0.70
```

Also report sensitivity at purity thresholds:

```text
0.60 / 0.70 / 0.80
```

These are source-only sensitivity checks, not treatment tuning.

### Required lexical shortcut audit

Fit/report a deliberately simple lexical baseline predicting fine routes from abstracts. This is a diagnostic, not a route classifier used as ground truth.

Required outputs:

```text
feasibility_1/source_route_annotations.jsonl
feasibility_1/route_label_summary.json
feasibility_1/route_annotation_audit_packet.csv
feasibility_1/lexical_route_baseline.json
```

Commit checkpoint:

```text
f0: annotate source contribution routes with audit trail
```

---

# 11. Phase E6 — predeclared route-pair coverage

Audit these route contrasts exactly:

```text
R1 BUILD_IMPROVE        vs DIAGNOSE_STRESS_TEST
R2 BUILD_IMPROVE        vs MEASURE_EVALUATE
R3 BUILD_IMPROVE        vs EXPLAIN_MECHANISM_THEORY
R4 DIAGNOSE_STRESS_TEST vs EXPLAIN_MECHANISM_THEORY
```

Do not replace R1-R4 because another pair has better coverage.

For every `seed × R1..R4`, report source counts above the frozen candidate/relevance floor.

Also report:

```text
n_supported_routes
eligible_3plus_routes_provisional
best_triplet_if_any
triplet_min_evidence_count
```

Do not prioritize 3-route seeds in the core recommendation.

Required outputs:

```text
feasibility_1/route_pair_coverage.csv
feasibility_1/multi_route_coverage.csv
```

---

# 12. Phase E7 — pairwise matched evidence slots

This is the primary F0 engineering object.

For every promising `seed × route pair`, form slots:

```text
slot_j = (A_paper_j, B_paper_j)
```

A and B differ in scientific route but are similar on source-only covariates.

## Matching covariates

Required:

```text
dense relevance percentile within seed pool
reranker relevance percentile if available
log abstract token length
first-public date
topic embedding
```

## Matching algorithm

Preferred:

```text
minimum-cost bipartite matching without replacement
```

with deterministic tie-breaking.

Matching cost uses equal-weight standardized differences for scalar covariates plus topic embedding distance. Save the exact formula in config.

## Predeclared caliper tiers

Evaluate all three source-only tiers; do not select a tier based on future scientific outcomes.

### STRICT

```text
dense relevance percentile difference <= 0.05
reranker percentile difference <= 0.05 if available
token-length ratio <= 1.25
absolute public-date difference <= 180 days
topic cosine distance <= 0.10
```

### BASE — primary F0 recommendation tier

```text
dense relevance percentile difference <= 0.10
reranker percentile difference <= 0.10 if available
token-length ratio <= 1.50
absolute public-date difference <= 365 days
topic cosine distance <= 0.20
```

### RELAXED — sensitivity only

```text
dense relevance percentile difference <= 0.20
reranker percentile difference <= 0.20 if available
token-length ratio <= 2.00
absolute public-date difference <= 540 days
topic cosine distance <= 0.30
```

If reranker is unavailable, report all matched-slot counts as `NO_RERANKER` and do not hide the limitation.

For each block/tier report:

```text
n_A_candidates
n_B_candidates
max_matched_slots
median_match_cost
p90_match_cost
max_match_cost
relevance_diff_summary
reranker_diff_summary
length_diff_summary
date_diff_summary
topic_diff_summary
unmatched_A_count
unmatched_B_count
```

Required output:

```text
feasibility_1/matched_evidence_slots.csv
feasibility_1/matching_diagnostics/*.json
```

---

# 13. Phase E8 — scientific equipoise audit packets

Codex does not invent human ratings.

For every BASE-tier block supporting at least `k=6`, prepare a human audit row with:

```text
seed_id
route_pair_id
neutral_route_A_description
neutral_route_B_description
representative_A_paper_ids
representative_B_paper_ids
A_relevance_summary
B_relevance_summary
max_BASE_matched_slots
```

and blank columns:

```text
A_RELEVANCE_TO_SEED 1-5
B_RELEVANCE_TO_SEED 1-5
A_SCIENTIFIC_PLAUSIBILITY 1-5
B_SCIENTIFIC_PLAUSIBILITY 1-5
DISTINGUISHABILITY 1-5
EQUIPOISE 1-5
NON_SUBSUMPTION 1-5
ANNOTATABILITY 1-5
COMPOSABILITY 1-5
ROUTE_DOMINANCE
HUMAN_NOTES
```

Also emit provisional source-only pair type:

```text
TYPE_I_COMPETING_STRATEGIC
TYPE_II_COMPETING_EPISTEMIC
TYPE_III_COMPLEMENTARY_HIGH_COMPOSABILITY
TYPE_IV_HIERARCHICAL_OR_SUBSUMED
UNCLEAR
```

Required output:

```text
feasibility_1/route_equipoise_audit_packet.csv
```

---

# 14. Phase E9 — paper-ID-only packet balance simulation

For every BASE-tier block with at least `k=8` matched slots, simulate paper-ID-only packet assignments using the same matched-slot bank at:

```text
alpha = 0,.25,.5,.75,1
```

For `k=8`, use counts:

```text
0/8, 2/6, 4/4, 6/2, 8/0
```

Use deterministic balanced/complementary slot assignments. Generate multiple packet realizations if the slot bank permits, but no scientific model calls.

Report across alpha:

```text
total tokens
mean/median dense relevance
mean/median reranker relevance
public-date distribution
topic-coverage summary
route-purity summary
slot-identity balance
```

Required output:

```text
feasibility_1/packet_balance_simulation.csv
```

---

# 15. Phase E10 — attrition + final F0 report

Produce the full denominator-preserving waterfall:

```text
ICLR 2026 official focal papers
→ source-parsed focal papers
→ method-maskable seeds
→ seed-validity candidates
→ multi-route-open candidates
→ >=2 source-supported routes
→ R1-R4 candidate blocks
→ BASE relevance-matchable blocks
→ >=6 matched slots
→ >=8 matched slots
→ >=12 matched slots
→ source-feasible blocks pending human equipoise
```

Required output:

```text
feasibility_1/attrition_waterfall.csv
feasibility_1/FEASIBILITY_RESULT.md
```

## Predeclared F0 recommendation thresholds

These thresholds concern **source constructibility only** and are fixed before seeing F0 results.

### SOURCE_FEASIBLE_BROAD

All must hold at BASE calipers:

```text
>= 30 unique seeds with at least one route pair supporting >= 8 matched slots
>= 3 distinct subfields represented among those seeds
>= 2 of R1-R4 represented by >= 8 unique seeds each
route-clear filtering does not remove > 70% of otherwise matchable blocks
at least 20 unique seeds can support >= 2 balanced packet realizations at k=8
no single subfield contributes > 60% of k=8 seeds
```

### SOURCE_FEASIBLE_NARROW

Any of:

```text
15-29 unique seeds with >=8 BASE matched slots
OR >=30 such seeds but concentrated in <3 subfields
OR only one route pair dominates strongly
```

provided there are still >=20 unique seeds with >=6 BASE matched slots.

### MARGINAL

```text
8-14 unique seeds with >=8 BASE matched slots
OR 12-19 unique seeds with >=6 BASE matched slots
```

or broad counts exist only under RELAXED calipers/purity threshold 0.60.

### NOT_FEASIBLE

```text
<8 unique seeds with >=8 BASE matched slots
AND <12 unique seeds with >=6 BASE matched slots
```

or temporal/purity/relevance failures make the paired causal design scientifically indefensible.

Do not alter these thresholds after seeing counts.

## FEASIBILITY_RESULT.md required sections

```text
1. Executive recommendation
2. Exact branch/commit and source hashes
3. Acquisition coverage
4. Temporal-clean evidence coverage
5. Seed construction/validity counts
6. Fine/coarse route annotation counts and ambiguity
7. Route-pair coverage R1-R4
8. Matched-slot counts under STRICT/BASE/RELAXED
9. k=6/k=8/k=12 unique-seed counts
10. Subfield distribution
11. 3-route coverage
12. Route-purity sensitivity
13. Packet-balance simulation summary
14. Attrition waterfall
15. Dominant blockers
16. Human audit files requiring PI review
17. Migration/reuse log
18. Tests executed
19. Deviations
20. Hard-stop statement: no scientific proposal generation performed
```

---

# 16. Required tests

At minimum implement and pass tests for:

```text
proceedings parser schema
abstract parser schema
canonical hashing reproducibility
exclusive/immutable writes
temporal cutoff boundary at 2024-08-31
temporal UNKNOWN/AMBIGUOUS states
seed schema validation
focal-paper exclusion from evidence pool
route enum/schema validation
route purity threshold behavior
retrieval deterministic ranking/ties
matching deterministic output
matching without replacement
STRICT/BASE/RELAXED calipers
k=6/8/12 slot counts
balanced alpha assignment
packet identity complementarity
no duplicate paper within a packet
attrition denominator preservation
report threshold classification
scientific-generation import/call guard
```

Run at each checkpoint:

```bash
python -m unittest discover -s experiments/idea_collapse/tests -v
# or pytest if the branch explicitly standardizes on pytest

git diff --check
```

Do not switch test framework mid-task without recording why.

---

# 17. Commit discipline

Use small commits by phase. Recommended commit messages:

```text
f0: migrate audited provenance and proceedings ingestion
f0: acquire official ICLR 2025-2026 source corpus
f0: resolve temporal-clean evidence subset
f0: build method-masked ICLR 2026 seed candidates
f0: build frozen source-only retrieval candidate pools
f0: annotate source contribution routes with audit trail
f0: implement pairwise matched-slot feasibility
f0: emit equipoise and packet-balance audit artifacts
f0: publish source-only feasibility result
```

Update `feasibility_1/STATUS.md` at each checkpoint with:

```text
phase
commit
commands
counts
artifacts
tests
blockers
deviations
next phase
```

Do not squash away failed attempts or exclusions that matter for provenance.

---

# 18. Stop-on-failure behavior

If a transient download/model-download error occurs, retry once with a bounded alternative mirror/source and record it.

Do not repeatedly retry unchanged failures.

Stop early and write an explicit partial `FEASIBILITY_RESULT.md` if any of these occurs:

```text
official ICLR source acquisition is fundamentally inaccessible
abstract coverage cannot reach 80%
temporal-date resolution is too incomplete to define a clean subset
route annotation cannot produce auditable labels even provisionally
retrieval/matching implementation cannot be made deterministic
```

Use recommendation `NOT_FEASIBLE` or `MARGINAL` only according to the fixed criteria, and distinguish engineering blockage from scientific source sparsity.

---

# 19. Push/handoff contract

When F0 is complete:

1. ensure working tree is clean;
2. run all tests;
3. record final commit SHA in `FEASIBILITY_RESULT.md` and `STATUS.md`;
4. push:

```bash
git push -u origin codex/f0-source-feasibility
```

If push fails, do not modify `main`. Record transport failure and preserve the complete local commit history/bundle if useful.

Final Codex response must contain exactly these factual fields:

```text
BRANCH:
FINAL_COMMIT:
F0_RECOMMENDATION:
ICLR2025_TOTAL:
ICLR2025_ABSTRACT_COVERAGE:
TEMPORAL_CLEAN_EVIDENCE_COUNT:
ICLR2026_TOTAL:
METHOD_MASKABLE_SEEDS:
MULTI_ROUTE_SEEDS:
K6_BASE_UNIQUE_SEEDS:
K8_BASE_UNIQUE_SEEDS:
K12_BASE_UNIQUE_SEEDS:
THREE_ROUTE_SEEDS:
SUBFIELDS_WITH_K8_BLOCKS:
DOMINANT_BLOCKER:
HUMAN_REVIEW_FILES:
TEST_RESULT:
SCIENTIFIC_GENERATIONS_PERFORMED: 0
```

Then STOP.

Do not start P0 baseline generation, treatment generation, analysis, or paper writing. The research lead will review the pushed branch and issue a new task only if justified.
