# Research Round 39 — Response-Curve Geometry and Override Thresholds

## 1. Trigger

A mean endpoint effect answers whether evidence matters, but not **how** evidence competes with the model × seed baseline research choice.

ICLR context-steerability work suggests that response can be nonlinear, asymmetric, or resistant to prior-opposing context. Our scientific setting may exhibit analogous structure, but the terminology and estimands should remain specific to open-ended research choice.

This round defines interpretable response-curve summaries without turning them into a new benchmark/metric contribution.

## 2. Core curve

For block `s,r,m`, define:

```text
mu(alpha) = E[S | evidence A fraction = alpha]
```

where:

```text
alpha ∈ {0,.25,.5,.75,1}
S ∈ [-2,2]
```

and A/B orientation is frozen before no-context outcomes.

No-context baseline:

```text
b = E[S | no retrieval]
```

## 3. Curve summaries

### 3.1 Extreme evidence effect

Already primary:

```text
Delta = mu(1) - mu(0)
```

### 3.2 Local/ordered slope

Fit a simple predeclared monotone/linear summary:

```text
slope = d mu / d alpha
```

Use a flexible curve only for visualization/sensitivity; do not choose functional form after observing whichever looks most interesting.

### 3.3 Endpoint displacement from baseline

```text
E_A = mu(1) - b
E_B = b - mu(0)
```

Under fixed route orientation:

- `E_A` measures how much all-A evidence moves the choice toward A relative to no context;
- `E_B` measures how much all-B evidence moves toward B.

Both can be negative in pathological cases.

## 4. Baseline-congruent reinforcement vs baseline-opposing override

After baseline is measured, classify the baseline-favored route descriptively.

If `b > 0` (A favored):

```text
reinforcement = mu(1) - b
override      = b - mu(0)
```

If `b < 0` (B favored):

```text
reinforcement = b - mu(0)
override      = mu(1) - b
```

This transformation is derived only after treatment orientation is already fixed and is for secondary interpretation.

Key question:

> Is evidence more effective at reinforcing an existing route tendency than at overriding it?

No direction is assumed.

## 5. Neutralization / flip threshold

If the fitted response curve crosses zero, define:

```text
alpha_zero = evidence A fraction at which predicted mean route score = 0
```

Interpretation:

> the mixture at which the model is predicted to be neutral between A/B routes.

For a model with A-favored baseline (`b>0`), a small `alpha_zero` means relatively strong B evidence is needed to neutralize A preference; the exact interpretation depends on curve orientation.

Do not report `alpha_zero` when:

- the curve never crosses zero in [0,1];
- uncertainty is too wide;
- monotonicity is badly violated;
- the fitted threshold is driven by extrapolation.

## 6. Evidence needed to reverse baseline sign

For blocks with a stable nonzero baseline, define a more intuitive descriptive quantity:

```text
override_margin
```

as the minimum observed/fitted movement in evidence composition from the neutral mixture (`alpha=.5`) required to produce a mean route score with sign opposite the no-context baseline.

This should remain a descriptive curve property, not a new headline metric.

## 7. Saturation and thresholds

Possible curve patterns:

### Linear-ish

```text
mu(alpha) changes smoothly across the full range
```

Interpretation: approximately graded evidence response.

### Thresholded

```text
little movement until evidence becomes strongly dominated by one route
```

Interpretation: high-level research choice requires a critical mass of supporting context.

### Saturating

```text
large early movement, little additional change at extremes
```

Interpretation: a small amount of route evidence is sufficient and more papers add little.

### Non-monotone

Could indicate:

- mixed evidence produces synthesis rather than interpolation;
- packet identity noise;
- route composability;
- measurement instability.

Do not force a monotone story if data are non-monotone.

## 8. Mixed proposals are informative

A balanced packet may increase `MIXED` proposals rather than simply interpolate between A/B probabilities.

Therefore analyze:

```text
P(MIXED | alpha)
```

separately.

Interesting possibility:

```text
P(MIXED) peaks near alpha=.5
```

This would suggest the model can integrate competing scientific routes rather than merely choose one.

However, high `MIXED` rate can also reflect route composability or annotation ambiguity, so interpret alongside Round 27 composability ratings.

## 9. Response geometry × route composability

Secondary pre-result hypothesis:

High-composability route pairs may show:

- more MIXED outputs;
- flatter signed route curves;
- less interpretable flip thresholds.

Low/moderate-composability competing routes may show clearer directional response.

This is useful for understanding heterogeneity but should not become a post-hoc exclusion rule.

## 10. Response geometry × baseline strength

Instead of only regressing `Delta` on baseline, examine whether baseline strength predicts:

- override displacement;
- reinforcement displacement;
- zero-crossing threshold;
- saturation/threshold shape.

The simplest strong regularity would be:

> blocks with stronger baseline route tendency require more opposing evidence to reverse high-level research choice.

This is a pre-result hypothesis motivated by context-prior literature, not an assumed finding.

## 11. Model-family comparison

For identical frozen blocks/evidence packets, compare curve geometry across model families.

Potential strong result:

```text
same evidence axis
+ different baseline b
→ response curves differ predictably in offset/override threshold
```

Stronger still:

```text
a shared evidence-response slope
+ model-specific baseline offset
```

predicts much of cross-model behavior.

Alternatively, family-specific slopes would imply different evidence sensitivity.

## 12. Connection to natural RAG

Natural packets typically occupy only a subset of the controlled evidence-composition range.

Plot natural `E_nat` values on top of the controlled response curve.

This can reveal why ordinary RAG may appear weak even when the controlled system is steerable:

```text
natural retrieval may cluster near one narrow exposure region
```

or why baseline dominates:

```text
natural packets rarely provide enough opposing evidence to cross the override threshold
```

This is a particularly interpretable bridge if supported by held-out prediction.

## 13. Figure concept

For one anonymized illustrative block:

```text
route score
 +2 |                         ●
    |                   ●
  0 |-----------●-------------  no-choice boundary
    |     ●
 -2 | ●
    +-------------------------
      0 .25 .50 .75 1.0
      evidence A fraction
```

Add:

- horizontal no-context baseline `b`;
- natural-RAG packet location;
- uncertainty bands;
- optionally zero-crossing threshold.

Then aggregate curve parameters across seeds/models rather than choosing a single dramatic example as evidence.

## 14. No new-metric overclaim

Do not market `alpha_zero`, override margin, or reinforcement/override displacement as a new benchmark metric.

They are interpretable descriptive estimands for the scientific behavior under study.

The paper contribution remains the empirical/model-behavior finding, not naming quantities.

## 15. Decision

**ADD RESPONSE-GEOMETRY ANALYSIS AFTER H1 IS ESTABLISHED.**

The endpoint contrast remains the simplest primary effect. Curve geometry is the main path for converting a binary context-sensitivity result into a more informative regularity about how scientific evidence competes with baseline research choices.