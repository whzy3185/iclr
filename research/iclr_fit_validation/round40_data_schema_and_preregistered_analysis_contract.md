# Research Round 40 — Data Schema and Preregistered Analysis Contract

## 1. Trigger

The research design now spans source audits, route definitions, matched packets, stochastic generations, human annotations, baseline behavior, robustness conditions, and natural-RAG prediction.

Without a stable relational/data contract, implementation can silently blur pre-treatment variables with outcomes or make later reproducibility difficult.

This round freezes the conceptual schema. Exact serialization formats may change during engineering, but scientific field meanings and provenance rules should remain stable.

## 2. Core entity graph

```text
Paper
  ↓
EvidenceCandidate ← Seed
  ↓                  ↓
RouteDefinition → SeedRouteBlock
                     ↓
                EvidencePacket
                     ↓
                  Generation
                     ↓
                  Annotation

SeedRouteBlock
  ↓
NoContextGeneration
  ↓
BaselineSummary

HeldOutSeedRouteBlock
  ↓
NaturalRetrievalPacket
  ↓
NaturalGeneration
  ↓
NaturalAnnotation
```

Every downstream object carries immutable parent IDs/hashes.

## 3. Paper table

One row per source paper.

Required fields:

```text
paper_id
iclr_year
title
abstract
proceedings_url
openreview_id/openreview_url
first_public_date
first_public_source
earliest_version_url
temporal_status
subfield_source_tags
abstract_sha256
metadata_sha256
```

Pre-treatment source annotation fields:

```text
fine_route_label_provisional/frozen
coarse_contribution_family
route_annotation_version
route_annotation_confidence
```

Do not overwrite a provisional label after freeze. New labels require a new version field.

## 4. Seed table

One row per candidate method-masked problem.

```text
seed_id
focal_paper_id
subfield
raw_problem_context
masked_seed_text
seed_text_sha256
masking_version
removed_entities
removed_method_tokens
focal_first_public_date
```

Validity fields:

```text
problem_clarity
background_sufficiency
method_neutrality
multi_route_openness
technical_substance
iclr_relevance
leakage_flags
accessibility_status
seed_status
```

All candidate seeds remain in the table, including failures.

## 5. Route definition table

Global route categories:

```text
route_category_id
route_category_name
category_definition
category_version
```

Seed-local route definitions:

```text
seed_route_id
seed_id
route_category_id
neutral_route_description
route_description_sha256
source_derivation_notes
```

A/B orientation is stored explicitly and frozen before baseline outcomes.

## 6. Seed-route block table

One row per candidate/eligible A/B contrast.

```text
block_id
seed_id
route_A_id
route_B_id
pair_roster_id
pair_type
composability_rating
equipoise_status
admissibility_status
source_matchability_status
final_pre_treatment_status
```

Human/source-only audit fields link to a separate audit table rather than being overwritten.

A block must have one of transparent statuses:

```text
CANDIDATE
SEED_INVALID
INSUFFICIENT_ROUTE_SUPPORT
RELEVANCE_MATCH_FAIL
EQUIPOISE_FAIL
ANNOTATABILITY_FAIL
SOURCE_ELIGIBLE
CONFIRMATORY_ELIGIBLE
```

`CONFIRMATORY_ELIGIBLE` cannot be assigned until all required pre-treatment gates are passed.

## 7. Evidence candidate table

One row per `seed × paper` candidate.

```text
seed_id
paper_id
retriever_version
retrieval_query_sha256
dense_relevance
reranker_relevance
rank_dense
rank_reranker
token_length
topic_cluster
route_label_at_freeze
candidate_status
```

Optional source-quality/popularity covariates are frozen with timestamps if used.

No treatment outcomes may appear in this table.

## 8. Evidence packet table

One row per packet realization.

```text
packet_id
block_id
alpha_target
alpha_realized
k
representation_type  # RAW / PF / PFM / PFL / etc.
packet_realization_index
ordered_paper_ids
paper_order_seed
packet_text_sha256
packet_definition_sha256
matching_config_sha256
```

Also store pre-treatment diagnostics:

```text
mean_relevance
relevance_distribution_summary
token_budget
date_distribution
route_counts
route_weighted_exposure
```

For the confirmatory study, packet definitions/hashes exist before generation.

## 9. Generation table

One row per stochastic model generation.

```text
generation_id
run_batch_id
block_id
packet_id | null
condition_type  # TREATMENT / NO_CONTEXT / NATURAL_RAG / CONTROL
alpha | null
model_family
checkpoint_id
checkpoint_revision
model_type  # base/instruct
prompt_template_version
prompt_sha256
decoding_config_sha256
random_seed_if_supported
timestamp
raw_response
raw_response_sha256
parse_status
```

Derived output fields should live in a separate parsed-output table/version rather than mutate raw generations.

## 10. Parsed proposal table

```text
generation_id
parser_version
proposal_text
research_question_field
method_field
experiment_field
parse_valid
```

Optional structural extractions:

```text
problem_object
failure_or_limitation
mechanism
intervention_family
evaluation_target
```

LLM parser outputs are not ground truth and always carry parser version/provenance.

## 11. Human annotation table

One row per `generation × annotator`.

```text
annotation_id
generation_id
annotation_protocol_version
annotator_pseudonymous_id
route_A_B_orientation_shown
route_score  # -2..2 or null
neither_flag
invalid_flag
relevant_to_seed
scientifically_coherent
testable
coarse_feasible
annotation_timestamp
```

Do not store treatment information in the annotation interface export.

Adjudication is a new annotation row/status, not destructive replacement of disagreements.

## 12. Automated annotation table

Separate from human labels:

```text
generation_id
classifier_id
classifier_version
classifier_prompt_sha256
predicted_route_score
predicted_probabilities
calibration_split_id
```

Never merge automated predictions into the human table.

## 13. Baseline summary table

Computed only after route treatments are frozen.

```text
block_id
model_checkpoint_id
no_context_batch_ids
n_valid
mean_route_score_b
P_A
P_B
P_mixed
invalid_rate
baseline_ci
baseline_definition_version
```

This table must never feed back into treatment selection.

## 14. Main block/model outcome table

Derived reproducibly from raw annotations:

```text
block_id
model_checkpoint_id
alpha
n_packets
n_generations
n_human_labels
mean_route_score
P_A
P_B
P_mixed
P_invalid
packet_variance
```

Primary endpoint summaries:

```text
Delta_extreme
ordered_slope
reinforcement_displacement
override_displacement
alpha_zero_if_identifiable
```

Every derived field carries `analysis_version`.

## 15. Natural-RAG tables

Natural retrieval packet:

```text
natural_packet_id
heldout_block_id
retriever_version
ordered_paper_ids
route_A_weight
route_B_weight
other_weight
E_nat
coverage
purity
entropy
packet_sha256
```

Prediction:

```text
heldout_block_id
model_checkpoint_id
predictor_version
predictor_type  # M0..M4
predicted_route_distribution
```

Observed natural outcomes are stored separately and never used to refit the frozen predictor.

## 16. Analysis configuration file concept

Before P1, produce immutable:

```text
preregistered_analysis.json
```

with at least:

```json
{
  "primary_outcome": "human_ordinal_route_score",
  "primary_effect": "alpha1_minus_alpha0",
  "primary_cluster_unit": "seed_id",
  "dose_levels": [0, 0.25, 0.5, 0.75, 1],
  "route_orientation_rule": "global_roster",
  "invalid_handling": "report_unconditional_and_valid_conditional",
  "primary_models": [],
  "primary_blocks_hash": "...",
  "packet_manifest_hash": "...",
  "annotation_protocol_hash": "...",
  "baseline_interaction_spec": "...",
  "natural_holdout_hash": "...",
  "stopping_rule": "..."
}
```

Do not create/freeze the final values until F0/F1/P0 give the allowed pre-confirmatory design information.

## 17. Data freeze levels

Use explicit freeze milestones.

### Freeze S — source universe

```text
corpus hash
seed candidate hash
retrieval config
```

### Freeze T — treatments

```text
route roster
route definitions
equipoise-approved blocks
packet manifests
```

Occurs before no-context baseline.

### Freeze A — analysis

```text
primary block list
models
alpha levels
sample sizes
primary estimands
annotation protocol
natural holdout split
```

Occurs before confirmatory P1 outcomes.

## 18. Provenance rule

Never overwrite a scientific input after a freeze.

If a correction is required:

```text
old artifact remains
new artifact gets new version/hash
reason recorded in deviation log
whether any outcomes had been observed is stated explicitly
```

## 19. Missingness and failures are data

Retain:

- source temporal ambiguity;
- failed matching;
- failed equipoise;
- invalid model output;
- parse failure;
- human disagreement;
- API/inference failure.

Never delete them from the manifest and recompute denominators on the surviving "good" cases without transparent status rules.

## 20. Figure/table reproducibility

Every main figure/table should be reproducible from:

```text
raw immutable artifacts
+ one analysis config/hash
+ one git commit
```

Generated figure data should be saved as machine-readable tables before plotting.

## 21. Decision

**SCHEMA CONCEPT FROZEN; FINAL SERIALIZATION PENDING ENGINEERING.**

Codex may later implement these entities once the authorized stage requires them, but scientific generations remain forbidden until the explicit gate is passed.