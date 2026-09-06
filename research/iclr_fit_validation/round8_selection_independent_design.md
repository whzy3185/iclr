# Round 8 — Selection-Independent Context Treatments

> Date: 2026-09-06  
> Goal: remove the remaining winner's-curse / cherry-picking channel from the causal experiment.  
> Status: research design refinement before outcomes.

---

## 0. Key improvement

Earlier designs used a no-context discovery batch to identify a model's favored mode and then chose a counter-prior evidence mode.

Even with cross-fitting, a skeptical reviewer can object:

> “You searched for a strong model prior and then chose the treatment contrast most likely to move it.”

A cleaner design is:

> **Choose all context treatment modes using only the source literature and seed question, before observing any model generations. Estimate the model prior independently afterward.**

Then `prior-congruent` and `counter-prior` become **descriptive analysis labels**, not treatment-selection criteria.

This makes treatment assignment independent of the model outcome distribution.

---

## 1. Revised causal ordering

```text
ICLR source corpus
   ↓
source-paper taxonomy (frozen)
   ↓
seed-specific relevance pools
   ↓
select eligible scientific-move treatments
WITHOUT model outputs
   ↓
freeze evidence packets / matching rules
   ↓
independently estimate no-context model prior
   ↓
run context treatments
   ↓
measure output distribution
   ↓
relate treatment response to independently measured prior strength
```

This ordering is preferable to:

```text
estimate prior → choose counter-prior → test effect
```

because the intervention exists independently of the model's observed prior.

---

## 2. Global treatment-mode candidates

Use the frozen Layer-A taxonomy from `taxonomy_design_draft.md` after pre-treatment audit.

The most likely high-coverage modes are:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
```

`VERIFY_FALSIFY_REPLICATE` may be too sparse to serve as a primary treatment but should remain measurable as an output mode if annotation reliability permits.

---

## 3. Seed eligibility must be model-independent

For each seed question:

1. retrieve a large candidate pool from the temporally clean ICLR evidence corpus;
2. annotate source-paper research modes;
3. apply a fixed relevance floor;
4. check which research modes contain enough high-relevance evidence;
5. run matching diagnostics across those modes.

A seed is treatment-eligible if at least two scientific modes have enough evidence to create matched packets.

### Record every seed

Possible statuses:

```text
ELIGIBLE_2_MODES
ELIGIBLE_3PLUS_MODES
INSUFFICIENT_MODE_COVERAGE
RELEVANCE_MATCH_FAILURE
TEMPORAL_CLEANLINESS_FAILURE
TAXONOMY_AMBIGUITY
```

These statuses are determined before model treatment output.

---

## 4. Treatment pair/triplet selection algorithm

Do not hand-pick a mode pair per seed based on what seems narratively interesting.

Two acceptable options:

### Option A — Global fixed pair

Use one pair across all eligible seeds, e.g.:

```text
BUILD_IMPROVE
vs
DIAGNOSE_STRESS_TEST
```

Advantages:

- maximally simple interpretation;
- identical causal contrast across subfields.

Disadvantages:

- may discard many seeds;
- may not probe the model's strongest prior for every seed/model.

### Option B — Predeclared deterministic pair selection — recommended initially

For every seed:

1. compute evidence availability after relevance floor for every mode;
2. identify all pairs satisfying the matching gate;
3. select a pair using a deterministic rule independent of model outputs, e.g.:
   - maximize the minimum available matched evidence count;
   - ties broken by a globally frozen priority order.

Freeze the selected pair in `seed_manifest.json` before no-context model generation.

Advantages:

- better seed coverage;
- treatment remains outcome-independent.

Disadvantage:

- pair semantics vary across seeds, so pooled analysis must use abstract mode identities and hierarchical modeling.

### Option C — Multi-mode treatment

For high-resource full experiments, treat all eligible modes rather than choosing one pair.

This is statistically clean but much more expensive and analytically complex.

---

## 5. No-context prior becomes a modifier, not a selector

After treatment modes are frozen, estimate:

```text
P0_model,seed(mode)
```

with independent repeated generations.

For each treatment mode `m`, define pre-treatment covariates such as:

```text
prior_probability = P0(m)
prior_rank = rank of m under P0
prior_log_odds = log(P0(m)+eps) - log(P0(reference)+eps)
```

Then ask:

> Is evidence response systematically weaker for modes that had lower no-context prior probability?

This yields a clean **prior-strength × evidence** interaction without choosing treatment based on the prior.

---

## 6. Main confirmatory model under selection-independent treatments

For output mode `j`:

```text
logit P(Y=j)
 = intercept
 + evidence_support_j
 + prior_probability_j
 + evidence_support_j × prior_probability_j
 + model/seed/subfield effects
```

Interpretation:

### Evidence coefficient

Does supplying more evidence of type `j` increase probability of output mode `j`?

### Prior coefficient

Does the model default toward `j` without context?

### Interaction

Does prior strength modulate how effectively evidence can steer the model?

A negative interaction in the appropriate parameterization may indicate stronger priors are harder to override; exact sign depends on coding and should be pre-specified.

---

## 7. Clean asymmetry test

Instead of defining “counter-prior treatment” by construction, derive asymmetry after prior estimation.

For each treatment contrast:

- identify which mode is higher-prior under P0;
- measure evidence-induced movement toward each mode;
- compare movement as a function of prior difference.

Strong prior-bound evidence would be:

```text
equal matched evidence shifts outputs more easily toward high-prior modes
than toward low-prior modes
```

with the treatment modes having been chosen before P0 was measured.

This is much harder to dismiss as cherry-picking.

---

## 8. Mixture design

For each pre-frozen mode pair A/B, keep:

```text
alpha(A) = 0 / .25 / .50 / .75 / 1
```

Packets are matched on relevance and covariates.

### Symmetry advantage

Because A/B are not chosen based on model prior, the same evidence curve can be evaluated for different models with different priors.

A particularly interesting observation would be:

> the same literature mixture produces different response curves across model families because each model enters with a different scientific prior.

That directly demonstrates context × model-prior interaction.

---

## 9. Strong natural experiment inside the design

If two model families have different no-context priors for the same seed and receive **identical frozen evidence packets**, compare their output response.

This creates a powerful matched-context contrast:

```text
same x
same C
model 1 prior != model 2 prior
↓
different response?
```

If response differences are predicted by P0 prior differences, the prior-competition interpretation gains credibility.

---

## 10. Relationship to general in-context steerability

Spectrum Tuning studies contexts that specify a desired novel data-generating distribution.

Our evidence packets do not explicitly command:

> “Generate mode A.”

They expose the model to scientifically relevant literature with a controlled framing distribution.

Therefore the experiment asks a different and harder ecological question:

> How much implicit distributional control does scientific evidence exert without an explicit steering instruction?

This distinction should be explicit in the paper.

---

## 11. Relationship to ProjectionBench

ProjectionBench progressively reveals more information from a focal experiment and asks models to project the paper's outcomes.

Our design differs on three key axes:

1. **information amount is held fixed** while evidence composition changes;
2. there is no single ground-truth scientific answer/method;
3. the target is distributional steering among multiple plausible scientific moves, not convergence toward the focal paper's known result.

ProjectionBench is therefore a close conceptual neighbor for scientific context disclosure, but not a direct collision.

---

## 12. Updated treatment freeze artifact

Before any no-context generation, Codex should eventually produce:

```text
TREATMENT_MODE_SELECTION.md
```

containing:

- eligible seed list;
- mode availability counts by seed;
- relevance-floor rule;
- deterministic pair/triplet selection algorithm;
- selected mode pair(s) for every seed;
- evidence matching diagnostics or pointers;
- hash of the selection table.

This file must exist before P0 model prior outcomes if we adopt the strictest selection-independent design.

---

## 13. Recommendation

Adopt the **selection-independent treatment design** for the confirmatory paper.

P0-DISCOVERY can still exist as an engineering/taxonomy exploration artifact, but it should not determine treatment modes.

The cleanest causal claim then becomes:

> **For treatment framings selected independently of model behavior, the effect of matched scientific evidence on hypothesis choice depends systematically on the model's independently measured no-context prior.**

This is stronger than simply showing a literature packet can prime an output.
