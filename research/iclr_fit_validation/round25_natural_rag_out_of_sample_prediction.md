# Research Round 25 — Natural-RAG Out-of-Sample Prediction

## 1. Trigger

The controlled A/B mixture experiment can establish a causal response under artificial packet construction. A strong ICLR paper still needs to show that this response law explains behavior under ordinary retrieval, otherwise Reviewer #2 can dismiss the study as an engineered priming environment.

Natural top-k RAG should therefore be a **held-out prediction target**, not another descriptive baseline.

## 2. Core validation question

> Can a response model learned only from controlled matched evidence mixtures predict the research-choice distribution produced by ordinary top-k retrieval on new scientific questions?

The target is the LLM's own behavior under natural RAG, not the future behavior of human science.

## 3. Data split must be by seed/block

Before treatment outcomes:

```text
TRAIN / CONTROLLED-FIT BLOCKS
HELD-OUT NATURAL-RAG BLOCKS
```

Preferred approach:

- fit response parameters on a predeclared subset of eligible seed-route blocks;
- reserve distinct seed questions for natural-RAG validation;
- no generation from held-out natural-RAG blocks may be used to choose route definitions, tune response functional form, or tune retrieval-composition features.

If sample size is too small for one fixed split, use block-level cross-fitting, but every prediction for a block must come from a model that did not use that block's natural-RAG outcomes.

## 4. Controlled exposure variable

For controlled A/B packets, define a signed exposure score.

Simplest fixed-count version:

```text
E(C) = 2 * alpha - 1
```

where:

```text
alpha = fraction of A-route evidence among A/B papers
E = -1 means all B
E =  0 means balanced
E = +1 means all A
```

Also retain a relevance-weighted version as robustness:

```text
E_w(C)
 = (sum_i w_i * s_i) / (sum_i w_i * |s_i|)
```

where:

```text
s_i = +1 for route A evidence
      -1 for route B evidence
       0 for off-route/other evidence
w_i = frozen retrieval/relevance weight
```

Primary weighting rule must be frozen before natural-RAG outcomes.

## 5. Natural packet representation

For a held-out seed-route block, run the ordinary frozen retriever exactly as a realistic research agent would.

For every retrieved paper assign, using the frozen source taxonomy:

```text
A_ROUTE
B_ROUTE
OTHER / UNCLEAR
```

Compute:

```text
E_nat       signed A-vs-B exposure
coverage    fraction/weight of packet classified A or B
purity      degree to which one eligible route dominates
entropy     route-composition entropy
```

The prediction target is only valid when enough natural packet mass maps to the predeclared A/B route contrast.

Predeclare a coverage floor before outcomes. Low-coverage blocks remain reported but may be excluded from the primary natural-RAG prediction estimand for a principled reason.

## 6. Baseline propensity

For each held-out block/model, estimate no-retrieval route propensity independently:

```text
b = signed no-context A-vs-B tendency
```

This uses no natural-RAG outcomes.

## 7. Prediction models

Compare at minimum:

### M0 — Global/null predictor

Uses only global/model average route frequencies.

### M1 — Baseline-only

```text
P(route | no-context baseline propensity)
```

### M2 — Evidence-only

```text
P(route | natural evidence composition)
```

### M3 — Baseline + Evidence

```text
P(route | baseline propensity, natural evidence composition)
```

### M4 — Baseline + Evidence + Interaction

```text
P(route | b, E_nat, b × E_nat)
```

M4 is the strongest mechanistic prediction but should not be favored unless controlled data support the interaction.

## 8. Controlled-fit response law

An illustrative model learned on controlled packets:

```text
logit P(A_LEANING)
 = beta_0
 + beta_E * E(C)
 + beta_B * b
 + beta_EB * E(C) * b
 + route-pair/model terms
```

or ordinal equivalent for score `S`.

Crucial rule:

> Coefficients used for natural-RAG prediction are learned from controlled intervention data, not refit to natural-RAG outcomes.

Natural-RAG data only evaluate prediction.

## 9. Primary evaluation metrics

At block/model level report:

- held-out log loss;
- Brier score for A-vs-B directional probabilities;
- calibration error / calibration plot where sample permits;
- correlation between predicted and observed block-level signed route score;
- likelihood/deviance improvement of `M3/M4` over `M1`;
- prediction intervals / block bootstrap uncertainty.

Do not use plain classification accuracy as the only metric because route distributions can be imbalanced.

## 10. Strong result patterns

### Pattern A — Controlled law predicts natural RAG

```text
M3/M4 materially better than M1
```

Interpretation:

Evidence composition is not merely an artificial treatment variable; it explains realistic retrieval-conditioned scientific-choice behavior beyond the model's no-context baseline.

This is a major paper-strengthening result.

### Pattern B — Controlled response exists but does not predict natural RAG

Interpretation possibilities:

- natural packets contain many off-route documents;
- controlled treatments are too artificial;
- route composition is insufficient without document identity / richer semantic features;
- ordinary retrieval sits in a narrow exposure range.

Paper must downgrade from a general RAG mechanism claim to a controlled steerability study.

### Pattern C — Natural RAG predicted by baseline only

If `M1 ≈ M3/M4`, ordinary retrieval adds little explanatory value after baseline route propensity.

This could still be interesting only if there is a robust controlled evidence effect and a principled reason natural retrieval fails to reach effective exposure levels. Otherwise likely KILL.

### Pattern D — Evidence-only beats baseline and interaction is weak

Interpretation:

Scientific-choice behavior is strongly context-driven rather than baseline-resistant.

This supports the strong-steerability branch.

## 11. Natural retrieval is not tuned for A/B contrast

Do not modify the natural retriever to increase route coverage after seeing results.

The natural condition should use an ordinary pre-frozen retrieval stack/query process.

If route coverage is low, that is an empirical property of natural retrieval and should be reported.

A separate exploratory reranker can be studied later, but not retroactively redefine the primary natural-RAG validation.

## 12. Packet identity versus composition

To test whether composition alone is enough, compare:

```text
composition model
vs
composition + document-identity/features model
```

The paper's strong general mechanism claim prefers substantial predictive power from low-dimensional route composition.

If prediction requires memorizing individual paper identities, the result is less general.

## 13. Cross-model transfer stretch test

After within-model validation, test whether response coefficients learned from model family 1 partially predict model family 2 when combined with family-2 baseline propensity.

Possible interpretation:

```text
shared evidence-response structure
+ model-specific baseline
```

would be especially compelling.

This is exploratory unless sample size supports a predeclared test.

## 14. Figure design

### Figure: Controlled → Natural

Left:

```text
controlled alpha / exposure
→ observed route response curve
```

Right:

```text
held-out natural packets
predicted route propensity vs observed route propensity
```

Overlay baseline-only and baseline+evidence models.

A visible improvement in held-out calibration/prediction would make the mechanistic story immediately understandable.

## 15. Decision

**REQUIRED FOR STRONG PAPER CLAIM.**

The controlled experiment can establish causality. Natural-RAG out-of-sample prediction determines whether the learned response law is explanatory beyond the artificial intervention environment.