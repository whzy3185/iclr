# Research Round 28 — Estimands, Hierarchy, and Inference Plan

## 1. Trigger

The design now allows multiple route pairs for the same seed question. Therefore `seed × route-pair` blocks are useful experimental objects but are **not fully independent scientific replications** when they share the same seed.

This round freezes a simpler and more defensible inference hierarchy to avoid pseudoreplication and significance inflation.

## 2. Data hierarchy

Observed generations are nested:

```text
seed
  └─ route pair / block
       └─ model family/checkpoint
            └─ alpha evidence level
                 └─ packet realization
                      └─ stochastic generation
```

Important distinction:

- generation = Monte Carlo draw from one model/context condition;
- packet = evidence-instance replicate;
- route block = one scientific A/B contrast;
- seed = underlying scientific question and main cluster for generalization;
- model = crossed/repeated factor, not a new scientific question.

## 3. Generalization unit

If each seed contributes only one route pair, block-level and seed-level inference coincide.

If a seed contributes multiple route pairs, primary uncertainty must account for shared seed context.

Recommended primary bootstrap:

```text
cluster bootstrap by seed
```

resampling all route pairs/models/conditions belonging to a seed together.

A block-level bootstrap can be reported only as a sensitivity analysis and should be labeled less conservative when multiple blocks share seeds.

## 4. Primary outcome

Human-anchored ordinal route score:

```text
S ∈ {-2,-1,0,+1,+2}
```

with invalid/neither handled separately.

For seed `s`, route pair `r`, model `m`, alpha `a`:

```text
mu_srm(a) = E[S | s,r,m,a]
```

estimated from packet/generation replicates.

## 5. Primary estimand 1 — extreme evidence effect

For every eligible `s,r,m`:

```text
Delta_srm
 = mu_srm(alpha=1) - mu_srm(alpha=0)
```

This is easy to explain and minimally model-dependent.

Population target within model `m`:

```text
ATE_m = mean over eligible seed-route population of Delta_srm
```

with seed-clustered uncertainty.

The pooled cross-model average is secondary; always report within-model ATE first.

## 6. Primary estimand 2 — ordered dose-response

Use all five alpha levels to test whether evidence composition produces an ordered directional response.

Simple block-level summary options:

```text
linear trend slope of mu(alpha)
Spearman correlation between alpha and mu(alpha)
monotone contrast / endpoint-consistent trend
```

Do not require strict linearity.

Predeclare one primary trend statistic before treatment outcomes.

Recommended simple primary:

```text
weighted linear slope across alpha = 0,.25,.5,.75,1
```

with nonlinear plots and spline/ordinal models as descriptive sensitivity.

## 7. Baseline route propensity

From no-context generations estimate, for each `s,r,m`:

```text
b_srm = E[S | no retrieval]
```

or sign/log-odds equivalent.

Baseline is measured after treatment routes are frozen.

Primary interaction question:

> Does evidence response depend systematically on the model's no-context route tendency?

Simple block-level model:

```text
Delta_srm
 = gamma_0
 + gamma_1 * b_srm
 + model / route-pair terms
 + error
```

A negative `gamma_1` under a consistent coding can indicate resistance to movement against a strong baseline, but exact sign interpretation must be frozen with A/B orientation convention.

## 8. A/B orientation convention

To prevent post-hoc sign flipping, route orientation must be frozen before baseline outcomes.

Recommended convention:

- A/B orientation inherited from global route-pair roster, not from which route model prefers;
- e.g. `BUILD` may always be A in `BUILD vs DIAGNOSE`;
- all signs remain in this orientation throughout analysis.

Only in descriptive figures may curves be re-expressed as `toward baseline-favored` vs `away from baseline-favored`, with transformation code frozen and disclosed.

## 9. Primary inferential strategy

Prefer transparent block/seed summaries over a complicated model as the only evidence.

### Main report

For each model:

- seed-clustered mean extreme effect;
- seed-clustered 95% CI;
- distribution of block effects;
- ordered dose-response figure;
- eligibility and invalid-output rates.

### Secondary hierarchical model

A mixed/ordinal model may use generation-level data:

```text
route_score
 ~ alpha
 + baseline_propensity
 + alpha × baseline_propensity
 + model
 + route-pair type
 + (1 + alpha | seed)
 + (1 | seed:route_pair)
```

Exact implementation depends on convergence and software; do not let one fragile GLMM determine the conclusion.

## 10. Packet realization effects

If multiple packet realizations exist per alpha, model/estimate packet variance separately.

A route effect that depends on one specific paper set is weak evidence.

Useful variance decomposition:

```text
between seed
between route pair within seed
between packet within route/alpha
within packet generation randomness
```

The design goal is that composition effect exceeds packet identity noise and prompt/order noise.

## 11. Randomization/permutation robustness

Because packet composition is experimentally assigned within block, use a randomization-style robustness test where feasible:

- shuffle alpha labels within block/packet structure under the sharp null;
- recompute block/seed aggregated trend statistic;
- compare observed statistic to permutation distribution.

This is not required as the sole primary test, but it provides a model-light causal check.

## 12. Multiple hypotheses

Freeze a small hierarchy.

### Confirmatory H1

Matched evidence composition changes blinded high-level route score.

### Confirmatory H2

Evidence response depends on independently measured baseline route propensity.

### Confirmatory/strong-validation H3

Controlled response improves held-out natural-RAG prediction over baseline-only model.

### Secondary

- abstraction hierarchy;
- component knockout;
- post-training/base-vs-instruct;
- route-pair heterogeneity;
- external taxonomy axes.

Do not use secondary significance to rescue failure of H1/H3.

## 13. Effect-size interpretation

Avoid defining success solely as `p < 0.05`.

Before full run, choose a scientifically meaningful minimum effect based on pilot variability and human annotation scale.

Example logic, not a frozen threshold:

```text
mean shift of 0.05 on [-2,2] = likely trivial
mean shift of 0.3–0.5 = readily interpretable
```

The actual smallest effect of interest should be frozen after an engineering/annotation pilot but before full confirmatory outcomes.

## 14. Precision-based scaling

Pilot purpose:

- estimate packet variance;
- estimate annotation reliability;
- estimate invalid-output rate;
- estimate block heterogeneity.

Then freeze either:

```text
fixed N seeds/blocks
```

or

```text
confidence interval width target + maximum budget
```

before full confirmatory generation.

Never repeatedly peek and stop when H1 becomes significant.

## 15. Correction to earlier language

Earlier rounds sometimes called `seed × route block` the scientific replication unit. More precisely:

> the block is the causal contrast object, but **seed is the primary clustering/generalization unit whenever multiple route pairs share a seed**.

This correction is made before scientific outcomes and should be preserved in provenance.

## 16. Decision

**FREEZE THIS HIERARCHY BEFORE GENERATION.**

The paper should rely on transparent seed-clustered effect sizes and held-out prediction, with hierarchical models used to sharpen—not manufacture—the conclusion.