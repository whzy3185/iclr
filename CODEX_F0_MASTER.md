# CODEX F0 MASTER — Source-Only Feasibility Audit v2

> Repository: `whzy3185/iclr`
> Stage: F0 SOURCE-ONLY FEASIBILITY
> Scientific proposal generation: FORBIDDEN
> Engineering launcher: `CODEX_F0_EXECUTION_PROMPT.md`
> Gate-policy authority: `research/iclr_fit_validation/round51_hard_gate_and_workflow_audit.md`

## 0. Scientific purpose

F0 does not test the paper hypothesis and does not decide whether the project should continue.

F0 maps whether real ICLR 2025/2026 literature can support auditable multi-route matched-evidence blocks before any scientific model outputs exist.

The later scientific question is about evidence-conditioned research-choice response and its interaction with independently measured baseline route propensity. None of that is estimated in F0.

## 1. Hard invariants

The following are non-negotiable:

1. no research-proposal generation in F0;
2. no baseline-propensity estimation;
3. no treatment-effect estimation;
4. no outcome-dependent seed/route/retrieval/matching decisions;
5. no off-topic evidence to manufacture route contrast;
6. preserve every denominator, exclusion, ambiguity, and matching failure;
7. no invented human ratings;
8. treatment construction must eventually be frozen before baseline scientific generations;
9. LLM-assisted source labels remain provisional until human audit;
10. Codex cannot authorize F1/P0.

## 2. Source universe

Primary source universes:

```text
Evidence: ICLR 2025 accepted papers
Seeds/focal problems: ICLR 2026 accepted papers
```

Official proceedings defines denominators.

Every normalized paper record should retain source URLs, hashes, title, abstract, metadata, and acquisition failures.

## 3. Temporal map

Do not reduce F0 to one automatic cutoff pass/fail.

Report at least:

```text
T0_COMMON_STRICT: first public > 2024-08-31
T1_LLAMA_CLEANER: first public > 2023-12-31
T2_ALL_ACCEPTED: all ICLR 2025, contamination-uncertain
```

Statuses must include UNKNOWN/AMBIGUOUS; never fabricate dates.

Final scientific temporal tier is chosen by research lead before model outcomes.

## 4. Seed construction

Create source-grounded method-masked ICLR 2026 research questions.

Remove focal solution/method identifiers while preserving the scientific problem and enough context for multiple plausible routes.

Preserve all candidate seeds with leakage/clarity/status metadata and emit a human-audit packet.

Do not solve the seeds.

## 5. Route system

Always audit:

```text
R1 BUILD_IMPROVE        vs DIAGNOSE_STRESS_TEST
R2 BUILD_IMPROVE        vs MEASURE_EVALUATE
R3 BUILD_IMPROVE        vs EXPLAIN_MECHANISM_THEORY
R4 DIAGNOSE_STRESS_TEST vs EXPLAIN_MECHANISM_THEORY
```

Source papers may have primary + secondary routes and mixedness.

Fine labels are provisional source descriptors.

Also report the external coarse contribution axis:

```text
ARTIFACT
KNOWLEDGE
BOTH
UNCLEAR
```

## 6. Route-purity sensitivity

Do not treat a model/parser confidence value as calibrated scientific truth.

Report source-feasibility sensitivity at:

```text
route_purity >= .60 / .70 / .80
```

Human F1 review determines which contrasts/papers are actually route-clear.

## 7. Retrieval

Use a frozen open dense retriever and, when practical, an independent reranker.

Preserve exact model revisions/configuration and all candidate scores.

Seed query text must not be altered using route labels.

## 8. Pairwise matched evidence slots

Primary F0 object:

```text
slot_j = (A_paper_j, B_paper_j)
```

A/B differ in scientific route while being similar on source-only covariates such as relevance, reranker score, length, public date, and topic.

Use deterministic matching without replacement.

Report full matching failures and match-cost distributions.

## 9. Matching sensitivity, not automatic pass/fail

Evaluate predeclared diagnostic matching tiers:

```text
STRICT
BASE
RELAXED
```

Exact numeric calipers are defined in `CODEX_F0_EXECUTION_PROMPT.md`.

These tiers map the coverage–balance frontier. They do not by themselves decide scientific feasibility.

## 10. Packet-size sensitivity

Report matched-slot coverage at:

```text
k = 4 / 6 / 8 / 12
```

Final scientific k is chosen after F0/F1 and before scientific outcomes.

k=4/8/12 permit exact quarter mixtures; k=6 is an intermediate source-coverage diagnostic.

## 11. Equipoise preparation

For source-supported seed × route-pair blocks, create human-review packets covering:

- relevance to seed;
- scientific plausibility;
- distinguishability;
- equipoise;
- non-subsumption;
- annotatability;
- composability;
- route dominance.

Codex leaves human ratings blank.

## 12. Required F0 scorecard

F0 must produce a multidimensional source map rather than a single automatic scientific verdict.

### Coverage

- unique seeds with >=2 routes;
- >=3 route coverage;
- k=4/6/8/12 matched-slot counts;
- route-pair distribution;
- subfield distribution;
- packet-realization capacity.

### Balance

- relevance differences;
- reranker differences;
- token-length differences;
- date differences;
- topic-distance distributions;
- matching cost.

### Construct risk

- seed leakage;
- route ambiguity;
- route purity;
- lexical shortcut strength;
- hierarchical/subsumed route pairs;
- composability.

### Temporal risk

- T0/T1/T2 coverage;
- UNKNOWN/AMBIGUOUS rates;
- subfield attrition.

### Concentration

- subfield concentration;
- route-pair concentration;
- attrition waterfall.

## 13. Required artifacts

Under:

```text
experiments/idea_collapse/feasibility_1/
```

create at minimum:

```text
README.md
STATUS.md
MIGRATION_LOG.md
raw_sources_manifest.jsonl
iclr2025_papers.jsonl
iclr2026_papers.jsonl
acquisition_failures.jsonl
corpus_hash.txt
temporal_cleanliness.jsonl
temporal_cleanliness_report.md
seed_candidates.jsonl
seed_validity_audit_packet.csv
retrieval_config.json
retrieval_candidates.parquet or .jsonl
source_route_annotations.jsonl
route_label_summary.json
route_annotation_audit_packet.csv
lexical_route_baseline.json
route_pair_coverage.csv
multi_route_coverage.csv
matched_evidence_slots.csv
matching_diagnostics/
route_equipoise_audit_packet.csv
packet_balance_simulation.csv
attrition_waterfall.csv
coverage_balance_frontier.csv
FEASIBILITY_RESULT.md
```

## 14. F0 final status

Codex reports only one engineering state:

```text
F0_COMPLETE
F0_INCOMPLETE
F0_BLOCKED
```

`FEASIBILITY_RESULT.md` must explicitly state:

```text
SCIENTIFIC_DECISION = RESEARCH_LEAD_REQUIRED
SCIENTIFIC_GENERATIONS_PERFORMED = 0
```

Do not output an automatic BROAD/NARROW/MARGINAL/NOT_FEASIBLE scientific classification.

## 15. Engineering hard-stop conditions

F0 may stop as BLOCKED only if an auditable source map cannot be produced, e.g.:

- official denominator cannot be established;
- acquisition missingness cannot be characterized;
- provenance/hashing is unreliable;
- deterministic retrieval/matching cannot be implemented;
- required artifacts would require violating F0 prohibitions.

Low source counts are not an engineering blocker. They are a result for research-lead review.

## 16. Stop condition

After complete source-only artifacts and `FEASIBILITY_RESULT.md`, STOP.

Do not start:

- F1 human adjudication beyond packet preparation;
- P0 baseline generation;
- scientific proposal generation;
- treatment generation;
- scientific outcome annotation;
- paper-result writing.

The research lead reviews F0 and writes the next-stage authorization.
