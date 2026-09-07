# Research Round 49 — Baseline Route Propensity Reliability and Measurement Error

## 1. Trigger

H2 asks whether evidence response depends on the model × seed's no-context baseline route tendency.

But baseline route propensity is not directly observed. It is estimated from a finite number of stochastic generations:

```text
b_hat ≈ E[S | no retrieval]
```

Using a noisy `b_hat` as an ordinary regression covariate can attenuate or destabilize the evidence × baseline interaction.

Therefore baseline measurement needs its own reliability design.

## 2. Baseline is block/model-specific

Formal object:

```text
b_srm = E[S | seed=s, route pair=r, model=m, no retrieval]
```

Do not call this an immutable model-wide prior.

It legitimately depends on:

- seed wording/problem;
- route definitions;
- model/checkpoint;
- generator prompt;
- decoding distribution.

## 3. Baseline is measured after treatment freeze

Critical ordering remains:

```text
seed/route/evidence treatment selection
→ freeze treatment manifest
→ only then generate no-context baseline
```

Baseline can never be used to select which A/B routes enter the experiment.

## 4. Baseline reliability split

For every confirmatory block/model, generate baseline draws in at least two independently identified batches:

```text
B1
B2
```

They can be collected in the same broader run window but use distinct generation IDs/randomness.

Purpose:

- estimate test/retest Monte Carlo reliability;
- detect unstable route distributions;
- quantify measurement error.

Because treatment selection is independent, B1/B2 are not needed for anti-selection cross-fitting; they are needed for **measurement reliability**.

## 5. Baseline summaries

For each batch report:

```text
mean ordinal route score
P(A-leaning)
P(B-leaning)
P(mixed)
invalid rate
uncertainty interval
```

Combined primary baseline estimate may use B1+B2 after reliability is assessed.

## 6. Reliability metrics

Across blocks/models evaluate:

### Sign stability

```text
sign(b_B1) == sign(b_B2)
```

for baselines sufficiently far from zero.

### Continuous agreement

- correlation between `b_B1` and `b_B2`;
- mean absolute difference;
- reliability/ICC-type estimate where meaningful.

### Distributional stability

Compare full A/B/MIXED distribution using e.g. Jensen–Shannon distance.

## 7. Baseline near zero is not a failure

A block may have:

```text
b ≈ 0
```

This means the model has little baseline preference between the two source-selected routes.

It remains informative for H1 and for estimating evidence slope.

Do not exclude near-zero blocks solely because they weaken the dramatic `override` story.

## 8. Unstable baseline is different

If B1 strongly favors A and B2 strongly favors B, the baseline estimate is unreliable at the chosen sample size.

Options before P1 freeze:

- increase baseline generations uniformly under a predeclared precision rule;
- treat baseline-interaction analysis as lower-confidence;
- use a joint measurement model.

Do not drop unstable blocks while retaining only stable/extreme ones to strengthen H2.

## 9. Baseline sample-size precision rule

After P0 estimate per-generation route-score variance.

Before P1 choose either:

### Fixed baseline N

For example planning range:

```text
40–60 generations per block/model
```

### Precision rule

Choose N so the expected CI/SE for `b` is below a predeclared tolerance, capped at a maximum budget.

Freeze rule before P1 baselines.

Do not continue sampling a block until the baseline becomes statistically nonzero.

## 10. Errors-in-variables problem

Naive model:

```text
Delta ~ b_hat
```

with noisy `b_hat` biases the slope toward zero under classical measurement error.

Therefore H2 should use at least one uncertainty-aware strategy.

## 11. Preferred transparent strategy — bootstrap both baseline and treatment

Cluster/bootstrap at seed level while resampling:

- baseline generations within block/model;
- treatment packet/generation observations;

For every bootstrap draw recompute:

```text
b_hat
Delta_hat
interaction coefficient
```

This propagates much of finite-sample baseline uncertainty into the H2 interval.

It does not fully solve all measurement-error bias, but is transparent and model-light.

## 12. Secondary joint hierarchical measurement model

If data support it, model latent baseline and treatment behavior jointly.

Conceptual structure:

```text
latent b_srm
  ↓
no-context route observations

latent b_srm + evidence exposure
  ↓
treatment route observations
```

This can avoid treating `b_hat` as error-free.

Use as secondary/confirmatory support, not the sole result if model assumptions are complex.

## 13. Split-baseline sensitivity

A very simple robustness test:

Fit H2 separately using:

```text
b_B1
b_B2
```

A real baseline-dependent regularity should not exist only for one random baseline half.

Also use one half for H2 fit and the other as an independent replication of the baseline covariate ranking if useful.

## 14. Baseline strength vs direction

Predeclare distinction:

```text
signed baseline b
absolute baseline strength |b|
```

Questions differ:

### Signed interaction

Does evidence toward A/B interact with which route is favored?

### Strength interaction

Are strong route tendencies generally harder to reverse regardless of direction?

Do not choose whichever transformation yields significance after outcomes.

Preferred core H2 should be expressed using the fixed A/B orientation and signed `b`, with `|b|` as a pre-specified secondary analysis if needed.

## 15. Baseline vs prompt nuisance

Prompt paraphrase robustness can reveal whether baseline is a stable model × problem behavior or an artifact of exact wording.

For a subset:

```text
baseline under prompt P1
baseline under neutral paraphrase P2
```

If baseline rankings collapse under harmless wording changes, H2's interpretation must be narrow.

## 16. Cross-model matched blocks

A particularly clean H2 visualization uses the same block/evidence packets across model families:

```text
Model 1: b = +0.8
Model 2: b = -0.1
same evidence mixture
→ compare route response
```

This avoids conflating baseline with different scientific problems.

## 17. Natural-RAG prediction uses uncertainty too

When `b` feeds held-out natural-RAG predictor M1/M3/M4, use the frozen combined baseline estimate and include baseline uncertainty in predictive evaluation/bootstrap where feasible.

Do not use natural-RAG outcomes to refine baseline.

## 18. H2 failure does not kill H1

Possible result:

```text
H1 robust evidence response
H2 baseline interaction weak/unreliable
H3 evidence improves natural prediction
```

This is still a viable evidence-composition paper.

Do not force an interaction story if baseline measurement or true effect does not support it.

## 19. Decision

**BASELINE MUST HAVE INDEPENDENT RELIABILITY AUDIT AND UNCERTAINTY PROPAGATION.**

H2 is high-value but secondary to H1. The design should prevent noisy baseline estimates from creating either false confidence or false null conclusions.