# PRE-RUN AMENDMENT C — Scientific-Prior Steerability

> Date: 2026-09-06  
> Status: **PRE-SCIENTIFIC-RUN AMENDMENT**  
> Trigger: ICLR-specific collision research identified a stronger and more defensible primary question.  
> Historical provenance: README + Amendments A/B remain unchanged.  
> Repository check immediately before this amendment found **no `STATUS.md`, scientific generations, `PILOT_RESULT.md`, or other outcome files** in this directory.

---

## 0. Primary research question

The experiment no longer treats “research monoculture” or “retrieval diversity” as the main scientific endpoint.

Primary question:

> **Can retrieved scientific literature override an LLM's default scientific-method / research-mode prior, and does evidence uptake weaken at higher abstraction levels?**

Candidate phenomenon:

> **Grounding without steering** — a model may cite/use retrieved concepts while remaining anchored to its no-retrieval prior in high-level methodology or problem framing.

This phenomenon is a hypothesis, not an assumed result.

---

## 1. Why this supersedes the earlier main hypothesis

Three prior findings change the design:

1. Si et al. (ICLR 2025) report a near-null effect of RAG paper count (`k=0/5/10/20`) on their near-duplicate idea metric while model backbones differ strongly.
2. Carlon et al. (2026) find strong shared concentration in LLM-recommended scientific methods under research-question-only prompting.
3. Spectrum Tuning (ICLR 2026) defines in-context steerability as using context to override a prior and move toward a novel output distribution.

Therefore our central intervention should measure **prior-vs-context competition**, not generic source overlap.

---

## 2. Primary variables

For model `M`, research seed `x`, evidence packet `C`, and generated hypothesis `H`:

```text
H ~ P_M(H | x, C)
```

### No-context prior

Estimate:

```text
P0_M(H | x) = P_M(H | x, C=∅)
```

using repeated generations before assigning context treatments.

### Context treatment

Evidence packets differ in their **scientific framing composition** while being matched on topical relevance and other observable properties.

---

## 3. Primary research-mode taxonomy

Freeze the following cross-ICLR categories before treatment outcomes are generated:

```text
1 BUILD_IMPROVE
2 DIAGNOSE_STRESS_TEST
3 MEASURE_EVALUATE
4 EXPLAIN_MECHANISM_THEORY
5 OPTIMIZE_EFFICIENCY
6 REPLICATE_FALSIFY_NULL
```

Every generated idea receives:

- one primary research mode;
- optional secondary mode;
- structured tuple:
  `(problem_object, failure_or_assumption, mechanism, intervention_method, evaluation_target)`.

### Reliability gate

Before full scientific runs:

- create annotation instructions with positive/negative examples;
- independently annotate a blinded sample;
- measure agreement;
- if a category is unreliable, merge/redefine **before treatment-effect inspection**;
- save taxonomy version and SHA256.

---

## 4. Pilot Stage P0 — estimate model priors

Use a fixed set of seed research questions with no retrieval.

Minimum useful pilot:

```text
24 seed questions
× 2 model families
× 20 generations
= 960 no-context generations
```

Prefer 3 ICLR subfields with 8 seeds each for the first stage.

Required outputs per `model × seed`:

- mode-frequency distribution;
- entropy/effective number of modes;
- method-family distribution;
- structured tuple inventory.

### Prior eligibility criterion

A seed is eligible for counter-prior treatment only if:

- the no-context prior shows a reproducible preference for at least one mode; AND
- the source corpus contains scientifically plausible, highly relevant evidence representing at least one underrepresented alternative mode.

Do not manufacture counter-prior packets for seeds where the alternative direction is scientifically artificial.

---

## 5. Pilot Stage P1 — matched framing-mixture intervention

### Default endpoints

For each eligible seed, select two evidence framings:

```text
A = prior-congruent / relatively favored mode
B = counter-prior / relatively underrepresented but plausible mode
```

The labels A/B must be based on P0 and corpus annotations, not treatment outcomes.

### Mixture levels

For fixed `k=12`:

```text
α(A) ∈ {0.00, 0.25, 0.50, 0.75, 1.00}
```

Packet examples:

```text
α=0.00:  0 A + 12 B
α=0.25:  3 A +  9 B
α=0.50:  6 A +  6 B
α=0.75:  9 A +  3 B
α=1.00: 12 A +  0 B
```

Do not tune these levels after outcomes.

---

## 6. Evidence matching requirements

A/B papers must be selected from the same seed-specific candidate pool and matched/stratified before generation.

Record for every paper:

- topical relevance score;
- optional cross-encoder relevance score;
- year;
- venue;
- abstract/context token length;
- citation/popularity metadata if used;
- research-mode annotation;
- source paper ID/URL.

### Required balance diagnostics

Before generation, report by condition:

- relevance mean/median/distribution;
- token length;
- year;
- venue distribution;
- any quality/popularity covariates used.

If a major imbalance is discovered, fix packet construction **before outcome generation**.

### Forbidden construction

Do not create counter-prior evidence by:

- sampling random off-topic papers;
- lowering relevance thresholds;
- hand-picking obviously weak work;
- including explicit instructions such as “use method B.”

The intervention must be literature composition, not task instruction.

---

## 7. Primary treatment outcome

For mode A:

```text
response(α) = P(output primary mode = A | α)
```

Estimate dose-response separately within each model and seed/subfield.

### Key contrasts

- `α=1.0` vs `α=0.0`;
- counter-prior evidence vs no-context prior;
- prior-congruent reinforcement vs counter-prior override;
- slope/nonlinearity across α.

### Possible patterns

```text
A. Steerable:
response rises strongly with α.

B. Prior-bound:
response remains near P0 despite evidence mixture.

C. Asymmetric:
prior-congruent evidence reinforces strongly,
counter-prior evidence overrides weakly.

D. Thresholded:
response changes only past a high evidence fraction.
```

All are interpretable; do not privilege one when coding analysis.

---

## 8. Hierarchical context-uptake endpoints

For every generation compute/audit:

### L0_SOURCE

- cites or explicitly draws from supplied source;
- source-specific entity/term uptake.

### L1_CONCEPT

- adopts supplied mechanism/phenomenon/assumption.

### L2_METHOD

- adopts method/model/dataset/experimental family emphasized in evidence.

### L3_RESEARCH_MODE

- shifts among the frozen universal research modes.

### L4_PROBLEM_FRAMING

- central problem/failure/causal target follows the evidence framing.

### Main hierarchical hypothesis

Potential, not guaranteed:

```text
uptake(L0) > uptake(L1) > uptake(L2) > uptake(L3/L4)
```

Do not construct an aggregate score that forces this ordering.

---

## 9. Required control conditions

### C0 — no retrieval

Estimates model prior.

### C1 — natural top-k retrieval

Locates ordinary RAG behavior relative to controlled mixture curve.

### C2 — matched A/B mixture

Primary causal intervention.

### C3 — prompt/order nuisance

For a subset:

- semantic prompt paraphrases;
- evidence-order permutations;
- formatting variants.

Estimate nuisance variance. Treatment effects must exceed this noise floor.

### C4 — sampling diversity

At least standard and high temperature. Optional established diversity method if implementation is clean.

Purpose:

```text
sampling breadth != context search direction
```

---

## 10. E0 compatibility with Si et al.

Retain Amendment B's RAG-quantity baseline:

```text
k = 0 / 5 / 10 / 20
```

and a Si-compatible near-duplicate metric.

This is a secondary compatibility analysis.

A near-null duplicate result does **not** kill this hypothesis.

The important comparison is whether structural / hierarchical context response exists despite the duplicate metric being flat.

---

## 11. Primary statistical model

Pre-specify a hierarchical multinomial/logistic analysis.

Illustrative binary A-vs-not-A form:

```text
logit P(Y=A)
 = β0
 + β1 * α
 + β2 * prior_strength
 + β3 * α × prior_strength
 + model effects
 + subfield effects
 + seed random effects
```

Where useful, distinguish whether A is prior-congruent or counter-prior.

### Primary reporting

- dose-response plots by model;
- marginal effect of evidence mixture;
- prior-congruence asymmetry;
- bootstrap/hierarchical uncertainty over seed questions;
- held-out prediction.

### No pseudo-replication

Do not report pairwise text-similarity p-values as if O(N²) pairs are independent.

---

## 12. Predictive mechanism gate

For a strong `structured context prior` claim, test whether evidence composition predicts held-out output behavior.

Split by seed question:

```text
train seeds / validation seeds / held-out test seeds
```

Compare:

```text
Model A: no-context prior only
Model B: prior + evidence composition
```

If Model B does not improve held-out prediction meaningfully, mechanism language must be weakened.

---

## 13. Human / independent audit

LLM extraction is permitted for scale, but not as unquestioned ground truth.

Required:

- frozen annotation guide;
- blinded stratified human/independent audit;
- report agreement/error by abstraction level;
- save raw labels and disagreements;
- no same-generator-model self-evaluation as the only evaluator.

Do not use a generic LLM novelty score as a primary endpoint.

---

## 14. Scientific run scale

### Engineering smoke test

Small runs only to validate:

- packet construction;
- parser/schema;
- API caching;
- annotation pipeline.

No research decision.

### Minimum scientific pilot after reliability passes

Suggested:

```text
24 seeds
× 2 model families
× 5 mixture levels
× 10 generations
= 2,400 treatment generations
```

plus no-context prior runs and control subsets.

If prior estimation requires more repetitions, increase P0 independently.

Do not expand to tens of thousands of runs until treatment construction and annotation are validated.

---

## 15. Pre-specified success / failure branches

### CONTINUE-A: high steerability

Requirements:

- significant/substantive within-model dose response in >=2 families;
- effect across >=3 subfields;
- effect exceeds prompt/order noise;
- high-level L3/L4 shift confirmed by audit;
- held-out evidence model improves prediction.

Paper frame:

> evidence composition systematically steers scientific-search distributions.

### CONTINUE-B: grounded but prior-bound

Requirements:

- verified strong L0/L1 context uptake;
- weak L3/L4 counter-prior override across >=2 models/subfields;
- asymmetry or hierarchy robust to prompt/order/sampling controls;
- natural top-k also sits near the prior-bound regime or another interpretable point.

Paper frame:

> retrieval grounding does not imply high-level scientific steerability.

### KILL-C: obvious copying

Kill if:

- context trivially changes outputs only because packets contain explicit method names and the effect disappears with abstraction/paraphrase controls;
- no nontrivial prior interaction/hierarchy appears;
- the main result is merely “model talks about what it reads.”

### KILL-D: noisy/unreliable taxonomy

Kill/pivot if high-level output categories cannot be annotated reproducibly.

### KILL-E: confounded evidence packets

Kill/pivot if A/B relevance or scientific validity cannot be matched sufficiently.

---

## 16. Prohibited post-hoc moves

After treatment outcomes exist, do NOT:

- change research-mode categories to maximize an effect;
- change which mode counts as “counter-prior”;
- drop seeds because their dose-response is inconvenient;
- choose a relevance metric because it improves the result;
- tune packet composition using generated outcomes;
- switch the primary endpoint to an embedding metric because structural results are null;
- call a natural model-family difference a retrieval effect.

All exploratory analyses must be clearly labeled exploratory.

---

## 17. Files Codex must produce before scientific generation

```text
experiments/idea_collapse/
├── TAXONOMY.md
├── taxonomy_version.json
├── corpus_manifest.json
├── seed_manifest.json
├── evidence_matching_report.md
├── preregistered_analysis.json
└── STATUS.md
```

`evidence_matching_report.md` must be reviewed before the treatment generation command is run.

---

## 18. Updated scientific target

The core paper claim, if supported, is no longer:

> Shared retrieval causes research monoculture.

It is one of two evidence-dependent claims:

### Steerability branch

> **Retrieved evidence composition causally and predictably steers the high-level scientific hypothesis distribution of LLMs, an effect not captured by standard duplicate-diversity metrics.**

### Prior-bound branch

> **LLMs can be strongly grounded in retrieved literature while remaining resistant to that literature at the level of scientific methods and problem framing, revealing hierarchical context reliance in scientific ideation.**

The experiment must determine which, if either, is true.
