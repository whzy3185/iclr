# Research Round 38 — Effect Size, Precision, and Full-Run Planning

## 1. Trigger

The project needs a pre-data answer to a practical scientific question:

> How large must the evidence-conditioned route shift be to matter, and how many independent scientific questions are needed to estimate it precisely enough for an ICLR claim?

This round uses **synthetic planning assumptions only**. No project outcomes exist. The numbers below are not target results and must not be optimized toward.

## 2. Outcome scale

Primary human route score:

```text
-2  STRONGLY_B
-1  LEANS_B
 0  MIXED
+1  LEANS_A
+2  STRONGLY_A
```

Primary endpoint contrast per `seed × route × model`:

```text
Delta = E[S | alpha=1] - E[S | alpha=0]
```

The full outcome range is 4 points.

## 3. Scientific rather than statistical significance

A tiny but precisely estimated shift should not sustain the paper.

Pre-pilot interpretation bands for discussion only:

```text
|Delta| < 0.15     likely scientifically small / possibly trivial
0.15–0.30          modest; needs strong mechanism/external-validity support
0.30–0.50          clearly interpretable directional movement
> 0.50             large evidence-conditioned route shift
```

These are **planning bands**, not frozen smallest-effect thresholds.

The final smallest effect of interest (SESOI) must be frozen after F1/P0 reveals:

- human annotation reliability;
- empirical route-score dispersion;
- invalid rate;
- packet identity variance;

and before P1 confirmatory outcomes.

## 4. Intuition for `Delta ≈ 0.3`

On a `[-2,2]` score, a 0.3 mean movement is not enormous, but it generally requires a visible redistribution in route choices.

For example, holding other categories roughly fixed, moving ~15% of outputs from `MIXED`/weak-B toward `LEANS_A`, or a smaller fraction by two ordinal levels, can generate a shift of this order.

Therefore `0.3` is a useful planning-scale effect: large enough to be human-visible, not so large that the experiment assumes near-deterministic steering.

Do not convert this intuition into a success criterion until the annotation pilot is complete.

## 5. Synthetic precision simulation

For planning only, assume approximately:

```text
per-generation route-score SD        = 1.0
additional packet-level endpoint SD  = 0.12 per condition
between-block true-effect SD         = 0.35
```

These values are deliberately generic; P0 will replace them with empirical variance estimates.

Under these assumptions, using only the extreme `alpha=0` and `alpha=1` endpoint contrast gives approximately:

| independent blocks | generations / endpoint | approximate 95% CI half-width on mean Delta | approximate power for Delta=0.3 |
|---:|---:|---:|---:|
| 24 | 30 | 0.19 | 0.88 |
| 30 | 30 | 0.17 | 0.94 |
| 36 | 30 | 0.15 | 0.97 |
| 48 | 30 | 0.13 | 0.99 |
| 24 | 45 | 0.18 | 0.91 |
| 30 | 45 | 0.16 | 0.96 |
| 36 | 45 | 0.15 | 0.98 |

These values are **not formal power guarantees**. They show the qualitative lesson:

> Adding independent seeds/blocks improves population precision more than repeatedly sampling the same block after Monte Carlo noise is already moderate.

## 6. Breadth-first sampling principle

Prefer:

```text
more independent seeds / valid route blocks
```

over:

```text
hundreds of generations from a few convenient seeds
```

Once each condition has enough draws to estimate its route distribution, the main uncertainty becomes variation across scientific questions/route contrasts.

This is especially important because seed is the clustering/generalization unit when multiple route pairs share a seed.

## 7. Recommended P0 engineering/variance pilot

P0 remains intentionally smaller and uses three alpha conditions:

```text
alpha = 0, .5, 1
```

Illustrative target if F0 supports it:

```text
12 unique seeds
~1 primary route pair per seed initially
2 model families
3 alpha levels
3 packet realizations / alpha
10 generations / packet
```

Treatment generations:

```text
12 × 2 × 3 × 3 × 10 = 2,160
```

Plus no-context generations, e.g. 30–60 per `seed × model × route-pair` depending baseline precision needs.

P0 is not powered for final claims. It estimates variance and validates the measurement chain.

## 8. Candidate full confirmatory structure

If F0/F1/P0 pass and source coverage permits, a strong P1 design would target roughly:

```text
30–40 unique seeds
2 core model families / confirmatory checkpoints
5 alpha levels
3–5 packet realizations / alpha
10–15 stochastic generations / packet
```

Example mid-grid:

```text
36 seeds
× 2 models
× 5 alpha
× 4 packets
× 10 generations
= 14,400 treatment generations
```

No-context baseline, prompt/order controls, and human labeling are additional.

This is a planning example, not an authorized run.

## 9. Baseline route propensity precision

The evidence-response interaction requires a reasonably precise no-context baseline for each block/model.

Do not over-spend baseline sampling uniformly.

After P0, estimate how many no-context generations are required so uncertainty in `b_srm` is small relative to cross-block variation.

Possible strategy before P1:

```text
fixed 40–60 no-context generations per block/model
```

or a predeclared precision rule.

Do not adapt baseline sample count based on whether the estimated baseline is narratively interesting.

## 10. Packet allocation

Multiple packet realizations are scientifically important.

Prefer:

```text
4 packets × 10 generations
```

over:

```text
1 packet × 40 generations
```

when cost is comparable, because the first design estimates document-identity variance and better represents the route evidence pool.

The exact packet/generation tradeoff should be chosen from P0 variance decomposition before P1 freeze.

## 11. Human annotation budget strategy

Human annotation should anchor the science but need not label every generation if scale is large.

Preferred structure:

### Full human labels

- all P0 outputs or a large enough subset to develop/reliability-test the rubric;
- all outputs for a confirmatory stratified block/model subset;
- all key anti-priming/component experiments on the main subset.

### Calibrated scale classifier

Only after human freeze, apply an automated classifier to remaining outputs if held-out block-level agreement is sufficiently high.

Main paper should show human-only effect estimates alongside scaled estimates.

## 12. Precision-based confirmatory gate

Before P1, freeze one of two strategies.

### Option A — fixed design

```text
N unique seeds/blocks
R packet realizations
G generations/packet
```

Simple and easy to audit.

### Option B — precision target

For example, after P0 variance estimates:

> choose the smallest fixed N (subject to an upper cap) predicted to yield a 95% CI half-width no larger than a predeclared tolerance for the mean extreme effect.

Then freeze N **before P1 data collection**.

Do not sequentially stop based on statistical significance.

## 13. Suggested precision target concept

A planning goal of roughly:

```text
95% CI half-width <= 0.15–0.20 route-score units
```

would often distinguish a practically meaningful ~0.3 shift from near-zero behavior.

The final tolerance must depend on P0 reliability and SESOI and is not frozen by this round.

## 14. Heterogeneity is not a nuisance to average away

Even if the mean effect is clear, report:

- distribution of seed/block effects;
- model-specific effects;
- route-pair type heterogeneity;
- subfield heterogeneity;
- fraction of blocks with effect in the expected evidence direction.

A paper with `mean Delta=0.3` but wildly inconsistent signs may imply the low-dimensional route explanation is incomplete.

## 15. Stronger success criterion than power

A high-quality paper should satisfy simultaneously:

```text
mean effect is nontrivial
CI is reasonably narrow
most/meaningful fraction of blocks respond directionally
result replicates across model families
anti-priming controls retain effect
natural-RAG prediction improves
```

Statistical power on one pooled coefficient is not enough.

## 16. Decision

**BREADTH-FIRST FULL-RUN PLANNING.**

Current design intuition favors roughly 30–40 independent seeds for a strong confirmatory study if source feasibility supports them. Exact N and SESOI remain deliberately unfrozen until source/annotation/variance pilots provide the information needed to choose them without outcome-driven tuning.