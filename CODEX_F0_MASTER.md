# CODEX F0 MASTER — Source-Only Feasibility Audit

> Status: **AUTHORIZED NOW**
> Scope: **F0 SOURCE-ONLY FEASIBILITY**
> Scientific proposal generation: **FORBIDDEN**
> Repository: `whzy3185/iclr`

This file is the single operational handoff for Codex F0. It consolidates `CODEX_FEASIBILITY_TASK_1.md` and Amendments A/B/C. Historical files remain for provenance, but when wording conflicts for F0 execution, this file wins.

## 0. Objective

Determine whether the proposed ICLR causal experiment is constructible from real, temporally auditable ICLR literature **before any scientific model outcomes are generated**.

The later experiment asks whether matched scientific evidence composition changes an LLM's high-level research choice and whether that response depends on the model's independently measured baseline route propensity. F0 does **not** test that scientific hypothesis.

F0 answers only:

> Can we build enough valid, multi-route, relevance-matched, pairwise matched ICLR evidence blocks to justify running the experiment?

## 1. Read order

Read before implementation:

1. `README.md`
2. `CODEX_F0_MASTER.md`
3. `research/iclr_fit_validation/round27_route_equipoise_and_admissibility_audit.md`
4. `research/iclr_fit_validation/round30_seed_validity_method_masking_and_accessibility.md`
5. `research/iclr_fit_validation/round33_staged_execution_and_hard_gates.md`
6. `research/iclr_fit_validation/round40_data_schema_reproducibility_and_analysis_freeze.md`
7. `research/iclr_fit_validation/round44_pairwise_matched_evidence_slot_design.md`
8. `research/iclr_fit_validation/round46_source_route_purity_and_mixed_contribution_handling.md`
9. `research/iclr_fit_validation/round47_lit2test_collision_and_prompt_neutrality_update.md`
10. historical `CODEX_FEASIBILITY_TASK_1.md` + Amendments A/B/C only as provenance/details if needed.

## 2. Hard prohibition

During F0 you MUST NOT:

- generate research proposals/ideas with any LLM;
- run no-context scientific proposal generation;
- estimate baseline route propensity from model generations;
- run evidence-conditioned scientific generation;
- inspect or estimate treatment effects;
- optimize route definitions, matching thresholds, or seed selection using imagined/model outcomes;
- write paper results or an abstract as though a phenomenon has been observed;
- use an LLM novelty/quality score as ground truth.

Allowed:

- metadata/data ingestion;
- deterministic preprocessing;
- embeddings/rerankers for source relevance;
- source-paper classification/annotation tooling;
- LLM-assisted source annotation only as provisional labels with preserved raw text and human-audit packets;
- paper-ID-only packet simulations.

## 3. Source universe

### Evidence

Primary universe: ICLR 2025 accepted papers.

For the temporal-clean shared subset, prefer evidence first public after `2024-08-31`, recording earlier versions explicitly.

Minimum fields:

```text
paper_id
title
abstract
iclr_year
proceedings_url/openreview_url
first_public_date
earlier_public_version_found
temporal_status
token_length
fine_route_label_provisional
route_purity
secondary_routes
coarse_contribution_family_provisional
annotation_confidence
```

Temporal status must allow `UNKNOWN`; never fabricate dates.

### Seeds

Candidate seeds: ICLR 2026 accepted papers.

Produce method-masked research questions/problem statements without solving them.

For each seed record:

```text
seed_id
focal_paper_id
subfield
raw_problem_context
method_masked_question
removed_solution_tokens/entities
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
```

Leakage diagnostics:

- seed-to-focal-title lexical similarity;
- seed-to-focal-abstract similarity;
- distinctive n-gram/acronym overlap;
- removed method/entity strings.

Do not use the focal paper's method as a gold answer.

## 4. Route system

Audit the predeclared fine route contrasts first:

```text
R1 BUILD_IMPROVE        vs DIAGNOSE_STRESS_TEST
R2 BUILD_IMPROVE        vs MEASURE_EVALUATE
R3 BUILD_IMPROVE        vs EXPLAIN_MECHANISM_THEORY
R4 DIAGNOSE_STRESS_TEST vs EXPLAIN_MECHANISM_THEORY
```

Do not drop an R1–R4 pair because coverage is poor. Poor coverage is an F0 result.

For each source paper record:

- primary fine route;
- optional secondary routes;
- route purity/mixedness;
- opposite-route contamination where relevant;
- confidence.

Also record the external coarse contribution-family robustness axis:

```text
ARTIFACT
KNOWLEDGE
BOTH
UNCLEAR
```

Do not claim this coarse taxonomy as ours.

## 5. Retrieval and relevance

For every seed:

1. retrieve a generous source-only candidate pool from the frozen evidence corpus;
2. compute frozen dense relevance;
3. add an independent reranker score if practical;
4. preserve all candidates and scores;
5. attach provisional source-route labels;
6. never alter the seed query based on route labels or model outcomes.

Freeze retrieval/reranker versions/configs and hashes.

## 6. Seed-route equipoise / admissibility

For each promising `seed × route pair`, prepare a human audit row with neutral, source-derived route descriptions and representative evidence.

Blank human fields must include:

```text
A_RELEVANCE_TO_SEED 1–5
B_RELEVANCE_TO_SEED 1–5
A_SCIENTIFIC_PLAUSIBILITY 1–5
B_SCIENTIFIC_PLAUSIBILITY 1–5
DISTINGUISHABILITY 1–5
EQUIPOISE 1–5
NON_SUBSUMPTION 1–5
ANNOTATABILITY 1–5
COMPOSABILITY 1–5
ROUTE_DOMINANCE
```

Codex prepares the packet but does not invent human ratings.

Also record provisional pair type:

```text
TYPE_I_COMPETING_STRATEGIC
TYPE_II_COMPETING_EPISTEMIC
TYPE_III_COMPLEMENTARY_HIGH_COMPOSABILITY
TYPE_IV_HIERARCHICAL_OR_SUBSUMED
UNCLEAR
```

Do not silently remove hierarchical/high-composability cases; report them.

## 7. Pairwise matched evidence slots — primary F0 object

For every promising block, attempt to create:

```text
slot_j = (A_paper_j, B_paper_j)
```

A/B must differ in scientific route while being matched on frozen source-only covariates.

Required matching variables:

```text
dense relevance
reranker relevance if available
abstract token length
first-public date / time distance
topic embedding/cluster distance
```

Use a deterministic source-only algorithm such as minimum-cost bipartite matching, optimal matching, or deterministic nearest-neighbor without replacement.

Record:

- matching cost definition;
- hard calipers;
- deterministic tie breaks;
- unmatched papers/reasons;
- code/config/hash.

Never tune matching weights against future treatment outcomes.

For every `seed × route pair` report:

```text
n_A_above_floor
n_B_above_floor
max_matched_slots_under_calipers
median_match_cost
p90_match_cost
max_match_cost
matched_relevance_difference
matched_length_difference
matched_date_difference
matched_topic_distance
```

Audit support at:

```text
k = 6
k = 8
k = 12
```

Do not force one k; report coverage at all three.

## 8. Packet feasibility simulation

Paper-ID-only packet simulations are allowed.

Using the same matched-slot bank, simulate source-only assignments at:

```text
alpha = 0, .25, .5, .75, 1
```

Prefer balanced/complementary assignments so middle alpha conditions do not systematically privilege particular slot identities.

Check balance across alpha on:

- relevance;
- total tokens;
- public dates;
- topic distance/coverage;
- route purity.

No scientific generation may be called.

## 9. Multi-route coverage

For every seed report:

```text
n_supported_routes
eligible_3plus_routes_provisional
best_triplet_if_any
triplet_min_evidence_count
triplet_matchability_status
```

This evaluates whether a future three-route simplex extension is even possible. Do not prioritize three-route seeds over valid two-route seeds in the core F0 decision.

## 10. Required lexical/purity diagnostics

For source-route annotation:

- test a simple lexical/keyword classifier for both coarse and fine labels;
- report route-label ambiguity;
- report route-purity distribution;
- report how much coverage is lost when restricting to route-clear papers.

High lexical predictability is not automatically fatal, but it must be flagged as future priming risk.

## 11. Required outputs

Create/update under:

```text
experiments/idea_collapse/feasibility_1/
```

At minimum:

```text
README.md
STATUS.md
corpus_manifest.jsonl
corpus_hash.txt
seed_candidates.jsonl
retrieval_config.json
route_label_summary.json
route_pair_coverage.csv
route_pair_matchability.csv
matched_evidence_slots.csv
packet_balance_simulation.csv
multi_route_coverage.csv
attrition_waterfall.csv
seed_validity_audit_packet.csv
route_equipoise_audit_packet.csv
route_annotation_audit_packet.csv
matching_diagnostics/
temporal_cleanliness_report.md
FEASIBILITY_RESULT.md
```

## 12. Attrition waterfall

`FEASIBILITY_RESULT.md` must explicitly show:

```text
ICLR 2026 focal candidates
→ extractable method-masked seeds
→ seed validity/leakage pass candidates
→ multi-route-open candidates
→ >=2 source-supported routes
→ relevance-matchable route pairs
→ >=6 / >=8 / >=12 pairwise matched-slot banks
→ source-feasible blocks awaiting human equipoise
→ potential final experimental blocks
```

No candidate may disappear silently.

## 13. FEASIBILITY_RESULT questions

Answer, without scientific outcomes:

1. How many candidate seeds were audited?
2. How many unique seeds have >=2 supported routes?
3. How many have >=3 supported routes?
4. How many unique seeds have at least one route pair with >=6, >=8, >=12 matched slots?
5. Coverage by R1–R4 and by subfield?
6. Does pairwise slot matching materially reduce coverage vs loose packet-level matching?
7. Are route-clear papers sufficient after purity filtering?
8. Are A/B evidence relevance/matching distributions comparable enough for a paired causal design?
9. Is the coarse Artifact/Knowledge distinction easier to audit than the fine route taxonomy?
10. What is the dominant failure mode: seed leakage, route sparsity, relevance mismatch, temporal uncertainty, mixed-route contamination, equipoise/composability, or matching calipers?
11. Does the universe support multiple packet realizations per block?
12. Recommendation: one of:

```text
SOURCE_FEASIBLE_BROAD
SOURCE_FEASIBLE_NARROW
MARGINAL
NOT_FEASIBLE
```

This recommendation is about constructibility only.

## 14. Stop condition

After `FEASIBILITY_RESULT.md` and the source-only artifacts are complete, STOP.

Do not run:

- P0 baseline generations;
- scientific proposal generations;
- evidence-conditioned generations;
- treatment-outcome annotations;
- paper-result writing.

The research lead will review F0 and decide whether P0 scientific generation is authorized.
