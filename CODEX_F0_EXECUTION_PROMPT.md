# CODEX F0 EXECUTION PROMPT — Engineering Contract v2

> Repository: `whzy3185/iclr`
> Authority: **this file is the Codex launcher for F0 execution**
> Scientific authority: `CODEX_F0_MASTER.md` + `research/iclr_fit_validation/round51_hard_gate_and_workflow_audit.md`
> Status: **AUTHORIZED**
> Scientific proposal generation: **FORBIDDEN**
> Expected branch: `codex/f0-source-feasibility`

## 0. Mission

Execute a source-only feasibility audit for the current ICLR experiment.

You are not testing the scientific hypothesis and you are not deciding whether the paper should continue.

Your job is to produce a complete, reproducible map of whether the real ICLR 2025/2026 literature can support multi-route, relevance-matched, pairwise-matched evidence blocks under several predeclared source-only design regimes.

The research lead will make the scientific decision after reviewing your artifacts.

Final F0 output state is only one of:

```text
F0_COMPLETE
F0_INCOMPLETE
F0_BLOCKED
```

Do **not** output `SOURCE_FEASIBLE_BROAD/NARROW/MARGINAL/NOT_FEASIBLE` as an automatic decision in v2.

---

# 1. Branch and synchronization contract

Start from latest remote main.

Do not continue `codex/p0-task0-task1`.

Required startup sequence, adapting transport details only when necessary:

```bash
git fetch origin main codex/p0-task0-task1
git switch --detach origin/main
git switch -c codex/f0-source-feasibility
```

Immediately create/update:

```text
experiments/idea_collapse/feasibility_1/STATUS.md
```

Record:

```text
origin_main_sha
branch_start_sha
old_codex_branch_sha
python_version
platform
cpu_gpu_mps
network_status
dependency_manager
```

---

# 2. Authority and read order

Read before implementation:

1. `README.md`
2. `CODEX_F0_EXECUTION_PROMPT.md`
3. `CODEX_F0_MASTER.md`
4. `research/iclr_fit_validation/round51_hard_gate_and_workflow_audit.md`
5. `research/iclr_fit_validation/round27_route_equipoise_and_admissibility_audit.md`
6. `research/iclr_fit_validation/round30_seed_validity_method_masking_and_accessibility.md`
7. `research/iclr_fit_validation/round33_staged_execution_and_hard_gates.md`
8. `research/iclr_fit_validation/round40_data_schema_and_preregistered_analysis_contract.md`
9. `research/iclr_fit_validation/round44_pairwise_matched_evidence_slot_design.md`
10. `research/iclr_fit_validation/round45_balanced_packet_randomization_design.md`
11. `research/iclr_fit_validation/round46_source_route_purity_and_multilabel_exposure.md`
12. `research/iclr_fit_validation/round50_codex_branch_pi_audit.md`

Priority for F0 conflicts:

```text
this file
> round51 hard-gate audit
> CODEX_F0_MASTER.md
> latest round files
> historical tasks/amendments
```

If a referenced file is absent/renamed, record the mismatch. Do not invent a replacement requirement.

---

# 3. Non-negotiable hard gates

These are true hard gates and must not be relaxed.

## H1 — no scientific outcomes in F0

Forbidden:

- research proposal generation;
- no-context scientific idea generation;
- evidence-conditioned scientific idea generation;
- baseline route-propensity estimation;
- treatment-effect estimation;
- scientific outcome annotation;
- paper-result writing.

## H2 — no outcome-dependent source construction

Do not use any model proposal outcome to alter:

- seed masking;
- route definitions;
- retrieval;
- route filters;
- matching;
- packet size;
- packet composition;
- calipers;
- temporal tier.

## H3 — denominator preservation

No paper/seed/route pair/matching failure may disappear silently.

Every exclusion requires a machine-readable reason.

## H4 — no off-topic evidence to manufacture a contrast

Do not lower topical relevance simply to create route diversity.

## H5 — no invented human labels

Human-audit columns remain blank until actual human review.

## H6 — no automatic scientific continue/kill decision

Codex reports source facts and engineering status only.

The research lead decides F1/P0 authorization.

---

# 4. Old-branch migration policy

Never merge `codex/p0-task0-task1` wholesale.

Allowed migration candidates after inspection:

```text
experiments/idea_collapse/generation/provenance.py
experiments/idea_collapse/corpus/index_proceedings.py
experiments/idea_collapse/tests/test_index.py
```

Additional pure utilities may be reimplemented only for:

- canonical JSON;
- SHA256;
- immutable/exclusive writes;
- Git-state capture;
- strict JSON parsing.

Forbidden as authoritative logic:

- old top-k/MMR study arms;
- old fixed 3-domain schema;
- old 540-generation design;
- old pilot configs;
- old diversity metrics as F0 criteria;
- old generation/provider configs;
- old pilot lock/result decision logic.

Create:

```text
feasibility_1/MIGRATION_LOG.md
```

For every reused function/file record:

```text
source_path
source_blob_sha
new_path
kept_logic
removed_old_assumptions
reason_for_reuse
tests_added
```

---

# 5. Engineering layout

Active F0 code:

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
```

Tests:

```text
experiments/idea_collapse/tests/f0/
```

Generated source-only artifacts:

```text
experiments/idea_collapse/feasibility_1/
```

---

# 6. Phase F0A-1 — audited utility migration

Implement only pure reusable engineering assets.

Acceptance checks:

```text
no old pilot condition names in active F0 code
no old fixed domains in active F0 code
no scientific-generation imports in F0 modules
all migrated functionality covered by tests
```

Checkpoint commit:

```text
f0: migrate audited provenance and proceedings utilities
```

If clean migration is impossible, set:

```text
F0_DATA_STATUS = F0_BLOCKED
BLOCKER = BLOCKED_MIGRATION
```

and stop.

---

# 7. Phase F0A-2 — official ICLR source acquisition

Canonical acceptance universes:

```text
ICLR 2025 accepted papers = evidence universe
ICLR 2026 accepted papers = focal/seed universe
```

Acquire at minimum:

```text
paper_id
year
title
abstract
proceedings_abstract_url
paper_pdf_url_if_available
openreview_url_if_available
authors_if_available
keywords_area_if_available
```

Rules:

- official proceedings defines denominator;
- third-party sources are cross-checks only;
- hash every raw source;
- hash every normalized table;
- preserve parse/download failures;
- never infer missing abstracts from titles.

Required outputs:

```text
raw_sources_manifest.jsonl
iclr2025_papers.jsonl
iclr2026_papers.jsonl
acquisition_failures.jsonl
corpus_hash.txt
```

Engineering completeness target:

```text
title+abstract coverage >=95%
```

This is a target, not an automatic scientific kill threshold.

If coverage <95%:

1. quantify missingness;
2. report missingness by subfield/metadata availability if possible;
3. set `ACQUISITION_WARNING=true`;
4. continue only if denominator and missingness remain auditable.

If the official denominator itself cannot be established or missingness cannot be characterized, set `F0_BLOCKED`.

Checkpoint:

```text
f0: acquire and hash official ICLR source universe
```

---

# 8. Phase F0A-3 — temporal map, not a single automatic cutoff gate

For every ICLR 2025 paper resolve earliest confidently discovered public date.

Priority:

1. arXiv first submission;
2. OpenReview original public submission;
3. other official/public preprint metadata;
4. otherwise UNKNOWN.

Statuses:

```text
CLEAN
FAIL_PRE_CUTOFF
UNKNOWN
AMBIGUOUS_MATCH
```

Never call a paper clean only because proceedings publication is recent.

Report coverage under three temporal tiers:

```text
T0_COMMON_STRICT:
  first_public_date > 2024-08-31

T1_LLAMA_CLEANER:
  first_public_date > 2023-12-31

T2_ALL_ACCEPTED:
  all accepted ICLR 2025 papers, contamination-uncertain
```

Do not choose the final scientific temporal tier.

Required:

```text
temporal_cleanliness.jsonl
temporal_cleanliness_report.md
```

Report counts, percentages, subfield attrition, UNKNOWN/AMBIGUOUS rates for all tiers.

Checkpoint:

```text
f0: map temporal-clean evidence tiers
```

---

# 9. Phase F0B-1 — method-masked seed candidates

From ICLR 2026 focal papers construct source-grounded, method-masked research questions.

Do not solve them.

Required fields:

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

Preserve all candidates using statuses such as:

```text
CANDIDATE
LEAKAGE_RISK
SOLUTION_PRESCRIBED
TOO_BROAD
TOO_NARROW
INSUFFICIENT_CONTEXT
PENDING_HUMAN_AUDIT
```

If machine-assisted masking is used:

- preserve input;
- preserve prompt;
- preserve model/version;
- preserve raw output;
- mark provisional.

Required:

```text
seed_candidates.jsonl
seed_validity_audit_packet.csv
```

Checkpoint:

```text
f0: build auditable method-masked seed candidates
```

---

# 10. Phase F0B-2 — retrieval candidate pools

Preferred dense encoder:

```text
BAAI/bge-base-en-v1.5
```

Preferred independent reranker:

```text
BAAI/bge-reranker-base
```

Pin exact resolved revision.

If unavailable, use a documented open substitute and mark `DEGRADED`; never silently substitute.

For every seed and each temporal tier needed for reporting:

1. query only with frozen method-masked seed text;
2. retrieve a generous candidate pool;
3. store dense scores/ranks;
4. rerank if available;
5. do not alter query using route labels.

Default pool:

```text
top 200 dense candidates or full available corpus if smaller
```

Required:

```text
retrieval_candidates.parquet OR retrieval_candidates.jsonl
retrieval_config.json
```

Checkpoint:

```text
f0: build frozen source-only retrieval pools
```

---

# 11. Phase F0B-3 — provisional source-route map

Fine route enum:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
VERIFY_FALSIFY_REPLICATE
MIXED_UNCLEAR
```

Coarse external robustness family:

```text
ARTIFACT
KNOWLEDGE
BOTH
UNCLEAR
```

Required fields:

```text
primary_route
secondary_routes[]
route_purity
opposite_route_contamination
fine_route_confidence
coarse_family
coarse_confidence
rationale_source_span
annotation_backend
annotation_version
status
```

Important:

`route_purity` and classifier confidence are provisional source descriptors, not calibrated scientific truth.

Report all source-feasibility results at route-purity sensitivity thresholds:

```text
0.60
0.70
0.80
```

Do not automatically choose one threshold as the scientific filter.

Also run a simple lexical baseline to quantify how easily route labels can be predicted from wording.

Required:

```text
source_route_annotations.jsonl
route_label_summary.json
route_annotation_audit_packet.csv
lexical_route_baseline.json
```

Checkpoint:

```text
f0: build provisional source-route map and sensitivity audit
```

---

# 12. Phase F0B-4 — predeclared route contrasts

Always audit:

```text
R1 BUILD_IMPROVE        vs DIAGNOSE_STRESS_TEST
R2 BUILD_IMPROVE        vs MEASURE_EVALUATE
R3 BUILD_IMPROVE        vs EXPLAIN_MECHANISM_THEORY
R4 DIAGNOSE_STRESS_TEST vs EXPLAIN_MECHANISM_THEORY
```

Do not replace R1-R4 because another pair has better coverage.

For every seed × route pair × temporal tier × purity sensitivity:

report source counts and candidate relevance distributions.

Also report:

```text
n_supported_routes
eligible_3plus_routes_provisional
best_triplet_if_any
triplet_min_evidence_count
```

Required:

```text
route_pair_coverage.csv
multi_route_coverage.csv
```

---

# 13. Phase F0B-5 — pairwise matched evidence slots

Primary engineering object:

```text
slot_j = (A_paper_j, B_paper_j)
```

Required matching covariates:

```text
dense relevance percentile within seed pool
reranker percentile if available
log abstract token length
first-public date
topic embedding distance
```

Preferred algorithm:

```text
minimum-cost bipartite matching without replacement
```

with deterministic tie-breaking.

Predeclared diagnostic caliper tiers:

### STRICT

```text
dense percentile diff <= .05
reranker percentile diff <= .05 if available
token ratio <= 1.25
date diff <= 180 days
topic cosine distance <= .10
```

### BASE

```text
dense percentile diff <= .10
reranker percentile diff <= .10 if available
token ratio <= 1.50
date diff <= 365 days
topic cosine distance <= .20
```

### RELAXED

```text
dense percentile diff <= .20
reranker percentile diff <= .20 if available
token ratio <= 2.00
date diff <= 540 days
topic cosine distance <= .30
```

Critical v2 rule:

> These are sensitivity tiers, not automatic scientific feasibility gates.

For every block/tier report:

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

Required:

```text
matched_evidence_slots.csv
matching_diagnostics/*.json
```

---

# 14. Packet-size coverage grid

Report matched-slot coverage at:

```text
k = 4 / 6 / 8 / 12
```

Do not choose final scientific k.

Notes:

- k=4/8/12 can support exact quarter mixtures;
- k=6 is an intermediate source-coverage diagnostic;
- final k is chosen by research lead after F0/F1 and before scientific outcomes.

For each k report:

```text
unique_seed_count
route_pair_count
subfield_count
multiple_packet_realization_count
```

across:

```text
T0/T1/T2 temporal tiers
STRICT/BASE/RELAXED matching tiers
0.60/0.70/0.80 purity thresholds
```

Every grid cell must be preserved. Do not highlight only the best cell.

---

# 15. Phase F0B-6 — equipoise packet preparation

For every reasonably source-supported block, prepare a human-review row.

Codex does not fill human ratings.

Required metadata:

```text
seed_id
route_pair_id
neutral_route_A_description
neutral_route_B_description
representative_A_paper_ids
representative_B_paper_ids
relevance_summaries
matched_slot_counts_by_tier
```

Blank human fields:

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

Also include provisional source-only pair type:

```text
TYPE_I_COMPETING_STRATEGIC
TYPE_II_COMPETING_EPISTEMIC
TYPE_III_COMPLEMENTARY_HIGH_COMPOSABILITY
TYPE_IV_HIERARCHICAL_OR_SUBSUMED
UNCLEAR
```

Required:

```text
route_equipoise_audit_packet.csv
```

---

# 16. Phase F0B-7 — paper-ID-only packet simulation

For k values supporting exact quarter mixtures (`4/8/12`), simulate:

```text
alpha = 0/.25/.5/.75/1
```

using the same matched-slot bank with deterministic balanced/complementary assignments.

No scientific model calls.

Report:

```text
total_tokens
mean_median_dense_relevance
mean_median_reranker_relevance
public_date_distribution
topic_coverage
route_purity
slot_identity_balance
```

Required:

```text
packet_balance_simulation.csv
```

---

# 17. F0 final report — descriptive, not scientific adjudication

Required:

```text
attrition_waterfall.csv
coverage_balance_frontier.csv
FEASIBILITY_RESULT.md
```

`coverage_balance_frontier.csv` must cross-tabulate at minimum:

```text
temporal_tier
purity_threshold
matching_tier
k
unique_seeds
route_pairs
subfields
seeds_with_multiple_packet_realizations
median_relevance_diff
p90_relevance_diff
median_topic_distance
p90_topic_distance
```

`FEASIBILITY_RESULT.md` must contain:

```text
1. F0_DATA_STATUS: F0_COMPLETE/F0_INCOMPLETE/F0_BLOCKED
2. branch/commit/source hashes
3. official acquisition coverage and missingness
4. temporal-tier coverage
5. seed masking/leakage summary
6. provisional route-map ambiguity/purity summary
7. R1-R4 source coverage
8. complete k=4/6/8/12 coverage grid
9. complete STRICT/BASE/RELAXED balance frontier
10. T0/T1/T2 sensitivity
11. 0.60/0.70/0.80 purity sensitivity
12. subfield/route-pair concentration
13. matched-slot attrition
14. packet-realization capacity
15. dominant engineering/source blockers
16. files requiring human F1 review
17. explicit statement: SCIENTIFIC_DECISION = RESEARCH_LEAD_REQUIRED
18. explicit statement: SCIENTIFIC_GENERATIONS_PERFORMED = 0
```

Codex must not call the project scientifically feasible/infeasible.

---

# 18. Engineering hard-stop conditions

Set `F0_BLOCKED` and stop only if one of these prevents an auditable source map:

- cannot establish official ICLR denominator;
- acquisition missingness cannot be characterized;
- source provenance/hashing is unreliable;
- retrieval/matching implementation cannot be made deterministic/reproducible;
- required artifacts cannot be produced without violating F0 scientific prohibitions.

Do not block merely because source counts are low. Low counts are a scientific design fact for research-lead review.

---

# 19. Tests

At minimum test:

```text
canonical serialization/hash stability
exclusive-write behavior
proceedings parser correctness
duplicate paper IDs
temporal cutoff boundary logic
ambiguous-date status handling
seed schema validation
focal-paper exclusion
route enum/schema validation
retrieval deterministic ties
matching without replacement
caliper enforcement
unmatched-paper retention
packet alpha composition
balanced/complementary assignment determinism
coverage-frontier denominator preservation
reporting completeness
hard prohibition: F0 modules import no scientific generation runner
```

Run full tests before each major checkpoint and at final handoff.

---

# 20. Checkpoint policy

Commit after major phases using descriptive commits, e.g.:

```text
f0: migrate audited provenance utilities
f0: acquire official ICLR source universe
f0: map temporal source tiers
f0: build method-masked seed candidates
f0: build frozen retrieval pools
f0: build provisional route map
f0: compute matching coverage frontier
f0: prepare human audit and packet-balance artifacts
f0: publish complete source-feasibility report
```

Do not squash away intermediate failed/partial evidence before research-lead review.

---

# 21. Final response contract

After pushing the branch, report exactly:

```text
BRANCH:
FINAL_COMMIT:
F0_DATA_STATUS:
ICLR2025_OFFICIAL_COUNT:
ICLR2025_ABSTRACT_COVERAGE:
ICLR2026_OFFICIAL_COUNT:
ICLR2026_ABSTRACT_COVERAGE:
T0_COMMON_STRICT_COUNT:
T1_LLAMA_CLEANER_COUNT:
METHOD_MASKABLE_SEEDS:
MULTI_ROUTE_SEEDS_PROVISIONAL:
K4_COVERAGE_SUMMARY:
K6_COVERAGE_SUMMARY:
K8_COVERAGE_SUMMARY:
K12_COVERAGE_SUMMARY:
DOMINANT_SOURCE_BLOCKER:
HUMAN_REVIEW_FILES:
TEST_RESULT:
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
SCIENTIFIC_GENERATIONS_PERFORMED: 0
```

Then stop.

Do not start F1 or P0.
