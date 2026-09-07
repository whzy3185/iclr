# PRE-RUN AMENDMENT E — Selection-Independent Scientific Context Treatments

> Date: 2026-09-07  
> Status: **PRE-SCIENTIFIC-RUN AMENDMENT**  
> Trigger: Round 8 + independent Round 9 validation identified a cleaner causal design than the prior-driven treatment selection in Amendments C/D.  
> Provenance: README, PREREGISTRATION_V1, and Amendments A–D remain unchanged.  
> Repository check before this amendment: the experiment directory contains preregistration/amendment files but no `STATUS.md`, generated scientific outcomes, or `PILOT_RESULT.md` in the directory listing inspected before this write.

---

## 0. Why Amendment E is necessary

Amendments C/D strengthened the project by introducing scientific priors, temporal cleanliness, matching, and anti-priming controls. However, their treatment logic still allowed the workflow:

```text
observe model no-context prior
   ↓
choose a low-prior / counter-prior scientific mode
   ↓
build evidence to push toward that mode
   ↓
measure displacement
```

Even with cross-fitting, a skeptical reviewer can argue that we searched the model output space for a direction likely to yield an interesting treatment contrast.

The stronger confirmatory design is:

```text
ICLR corpus + seed question only
   ↓
freeze valid scientific-mode treatments
   ↓
freeze evidence packets and matching
   ↓
ONLY THEN measure model no-context prior
   ↓
run the already-frozen treatments
   ↓
test prior × evidence interaction
```

The model prior becomes an **effect modifier**, not a treatment-selection variable.

This amendment supersedes the prior-driven treatment-selection portions of C/D for the confirmatory experiment.

---

# 1. Current confirmatory research question

> **When scientifically valid evidence treatments are selected independently of model behavior, does the effect of matched scientific literature on high-level hypothesis choice depend systematically on the model's independently measured no-context prior?**

Secondary question:

> Does context influence attenuate from source/content grounding toward method, research-mode, and problem-framing choices?

The empirical object is:

```text
P_M(H | x, C)
```

where `M` is frozen, `x` is a scientific problem, `C` is a pre-frozen real-literature packet, and `H` is a structured scientific choice.

---

# 2. Treatment modes must be selected without model outputs

Use the pre-treatment Layer-A taxonomy after reliability audit.

Candidate modes:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
VERIFY_FALSIFY_REPLICATE
```

For each seed, use only the frozen ICLR evidence corpus to determine which modes have enough scientifically relevant evidence.

Forbidden inputs during treatment selection:

- no-context generations;
- model prior probabilities;
- treatment generations;
- downstream diversity/steerability metrics;
- hand-selected model examples that suggest a desired story.

---

# 3. Seed eligibility is model-independent

For every candidate seed:

1. retrieve a large candidate evidence pool;
2. apply the frozen relevance floor;
3. annotate source-paper research mode;
4. verify temporal cleanliness;
5. determine evidence availability by mode;
6. run packet-matching diagnostics for candidate mode pairs;
7. assign a status before any model outcome is viewed.

Required statuses include:

```text
ELIGIBLE_2_MODES
ELIGIBLE_3PLUS_MODES
INSUFFICIENT_MODE_COVERAGE
RELEVANCE_MATCH_FAILURE
TEMPORAL_CLEANLINESS_FAILURE
TAXONOMY_AMBIGUITY
```

Preserve all failed seeds and the reason for failure.

---

# 4. Deterministic treatment-pair selection

For the first confirmatory design, choose between two predeclared options **before outcomes**.

## Option A — global pair

Use one high-coverage pair across all eligible seeds, e.g.:

```text
BUILD_IMPROVE
vs
DIAGNOSE_STRESS_TEST
```

Use this only if the pre-treatment corpus audit shows enough matched evidence across a sufficiently broad seed set.

## Option B — deterministic seed-specific pair — default if global coverage is weak

For each seed:

1. enumerate all mode pairs satisfying evidence-count and matching gates;
2. score each pair only using pre-treatment quantities such as minimum matched evidence count / overlap quality;
3. choose the pair maximizing the predeclared coverage criterion;
4. resolve ties using a globally frozen mode-priority order;
5. record the selected pair in the frozen seed manifest.

No model output may break a tie.

---

# 5. Treatment packet freeze occurs before prior estimation

For every eligible seed and selected pair A/B:

- freeze `k`;
- freeze packet-construction algorithm;
- freeze relevance/matching thresholds;
- freeze mixture levels;
- build/hash candidate packet assignments or deterministic packet-generation seeds;
- produce balance diagnostics.

Primary mixture remains:

```text
alpha(A) = 0.00 / 0.25 / 0.50 / 0.75 / 1.00
```

For `k=12`:

```text
0/12, 3/9, 6/6, 9/3, 12/0
```

A/B semantics may vary by seed under Option B, but the abstract treatment variable is frozen scientific-mode composition.

---

# 6. Mandatory treatment-freeze artifact

Before any confirmatory no-context prior generation, create:

```text
TREATMENT_MODE_SELECTION.md
```

and a machine-readable manifest containing at minimum:

```text
seed_id
seed_source
seed_first_public_date
eligible_status
candidate_modes
candidate_pair_balance
selected_mode_A
selected_mode_B
pair_selection_rule_version
relevance_floor_version
matching_config_hash
evidence_pool_hash
packet_assignment_hash_or_seed
```

The artifact must be committed before confirmatory P0 generations.

---

# 7. No-context prior is measured after treatment freeze

After the treatment design is immutable, estimate:

```text
P0_model,seed(mode)
```

using repeated no-context generation.

Primary prior covariates:

```text
prior_probability(mode)
prior_log_odds(A vs B)
prior_entropy
prior_rank(A)
prior_rank(B)
```

Do **not** exclude a seed merely because the measured model prior is weak or surprising after treatment freeze, except for predeclared output-validity failures.

The fact that different model families may have different priors for the same frozen packet is scientifically useful rather than a nuisance.

---

# 8. Strong matched-context cross-model test

Apply the same frozen evidence packets to at least two model families.

For the same seed and packet:

```text
x same
C same
model 1 prior != model 2 prior
```

Then test whether treatment response differs in a way predicted by the independently measured prior difference.

This is a high-value design because context is held fixed while prior varies naturally across models.

---

# 9. Primary confirmatory endpoint

Primary endpoint remains **Layer A / L3 scientific move**.

For a treated mode `j`, model:

```text
P(output primary move = j)
```

as a function of:

```text
evidence_fraction_j
prior_probability_j
evidence_fraction_j × prior_probability_j
```

with seed/model structure and predeclared nuisance variables.

A suitable schematic model is:

```text
logit P(Y=j)
  = beta0
  + beta_evidence * evidence_fraction_j
  + beta_prior * prior_probability_j
  + beta_interaction * evidence_fraction_j * prior_probability_j
  + seed/model effects
```

Exact coding/sign conventions must be frozen before treatment outcomes.

---

# 10. Predeclared asymmetry analysis

After priors are measured, label the two already-selected treatment modes descriptively as:

```text
higher-prior mode
lower-prior mode
```

Then compare matched evidence leverage:

> Does the same magnitude of evidence shift the model more easily toward its higher-prior scientific move than toward its lower-prior move?

Crucially, the treatments were not chosen because of this prior.

A strong result is therefore not constructed by selecting a convenient counter-prior direction.

---

# 11. Hierarchical grounding-vs-steering analysis remains secondary/core-supporting

Retain the predeclared uptake layers:

```text
L0 source attribution
L1 content/concept uptake
L2 method-family uptake
L3 scientific-move uptake  <- primary scientific choice endpoint
L4 central problem framing <- secondary/exploratory unless reliability is strong
```

Possible Branch B phenomenon:

```text
L0/L1 strong
L3/L4 weak or prior-asymmetric
```

Possible Branch A phenomenon:

```text
L3 tracks evidence mixture smoothly and predictably
```

Do not force a monotone hierarchy in scoring or plotting.

---

# 12. Temporal-clean causal core remains mandatory

For causal-core models, retain documented-cutoff discipline.

Current candidate families:

- Llama 3.1 — official pretraining cutoff December 2023;
- Gemma 3 — official training-data knowledge cutoff August 2024.

Primary evidence corpus should use individually verified papers after the latest relevant cutoff, preferably ICLR-only for the core.

Conference year alone does not establish temporal cleanliness. Record first-public dates and earlier versions.

Frontier APIs with uncertain training data may be used only as external-validity extensions.

---

# 13. Evidence matching and anti-priming controls remain mandatory

Amendment D controls are retained:

- relevance matching;
- token-length/year/topic balance;
- mode-preserving packet swaps;
- order randomization;
- prompt-paraphrase noise floor;
- exact-method copying diagnostic;
- lexical treatment-predictability audit;
- content-normalized robustness subset;
- valid-scientific-output guardrail.

A result that is adequately explained by category-word copying is insufficient for the main paper.

---

# 14. Controlled-to-natural RAG prediction remains a required full-paper validation

If the controlled causal core works:

1. fit response coefficients using controlled mixtures;
2. freeze analysis;
3. run held-out natural top-k retrieval;
4. annotate natural packet composition;
5. predict output-mode allocation from prior + evidence composition;
6. compare against observed natural-RAG behavior.

Required baseline:

```text
prior-only
vs
prior + evidence composition
```

A material held-out improvement is one of the strongest arguments that the controlled experiment reveals a real mechanism rather than artificial priming.

---

# 15. Updated proof-of-design gate

Before confirmatory treatment generation, the following artifacts must exist:

```text
TAXONOMY.md
annotation_audit_pre_treatment.md
corpus_manifest.json
model_cutoff_manifest.json
seed_manifest.json
TREATMENT_MODE_SELECTION.md
evidence_matching_report.md
packet_manifest.json
prior_generation_spec.json
preregistered_analysis.json
```

`P0_DISCOVERY` from Amendment D is no longer required to choose treatment modes. If an engineering/discovery batch exists, it must not affect confirmatory treatment selection.

---

# 16. Updated success conditions

A strong ICLR-relevant result requires at least one deeper regularity beyond trivial context copying:

- evidence × independently measured prior interaction;
- higher-prior vs lower-prior response asymmetry under pre-frozen treatments;
- abstraction-level grounding/steering dissociation;
- nonlinear/threshold dose response;
- consistent model-family difference predicted by prior;
- controlled model predicts held-out natural-RAG behavior;
- structural scientific-choice effect hidden by coarse duplicate metrics.

The cleanest possible claim is:

> **For scientific evidence treatments selected independently of model behavior, matched literature composition causally shifts open-ended scientific choices, and the leverage of that context is systematically modulated by the model's pre-existing scientific prior.**

or, if high-level resistance dominates:

> **LLMs can be strongly grounded in retrieved scientific evidence while remaining prior-bound in high-level research choice, revealing a hierarchy between evidence use and scientific steerability.**

---

# 17. Kill conditions

Kill/downgrade the main paper if:

- Layer-A labels are not reliable under independent audit;
- too few seeds permit relevance-matched alternative scientific modes;
- effect is mostly lexical/source copying;
- effect does not exceed prompt/order/document-identity noise;
- context response has no reproducible relation to evidence composition or prior;
- result exists only in a single narrow model/domain without a mechanistic explanation;
- natural-RAG validation fails and no stronger controlled mechanism appears;
- a direct concurrent paper establishes an equivalent selection-independent matched-literature prior×context experiment.

Do not add new post-hoc primary metrics to rescue a weak result.
