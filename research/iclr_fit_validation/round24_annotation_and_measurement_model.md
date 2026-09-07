# Research Round 24 — Annotation and Measurement Model

## 1. Trigger

The primary scientific object is now a seed-local A/B research-choice response. This reduces dependence on a global taxonomy, but only if the A/B outcome itself can be measured reliably.

Recent scientific-ideation evaluation work gives a strong warning: automated LLM judges can diverge materially from expert judgments of novelty and research quality. Therefore the paper should not make an LLM judge the primary scientific ground truth for high-level route choice.

## 2. Primary outcome becomes an ordinal route score

Replace a purely nominal label with an ordinal blinded judgment while retaining categorical labels for interpretability.

For each generated proposal, annotators see:

- the method-masked seed question;
- neutral definitions of Route A and Route B for that seed/block;
- the generated proposal;
- **no treatment condition, no evidence packet, no model identity**.

They assign:

```text
+2  STRONGLY_A
+1  LEANS_A
 0  MIXED / EQUALLY A-B
-1  LEANS_B
-2  STRONGLY_B
NA  NEITHER / INVALID / UNINTERPRETABLE
```

This yields a signed route score `S ∈ {-2,-1,0,1,2}`.

Categorical outputs remain derivable:

```text
A_LEANING = S > 0
B_LEANING = S < 0
MIXED     = S = 0
```

`NEITHER/INVALID` remain separate missing/quality categories, not silently mapped to zero.

## 3. Why ordinal scoring is preferable

A/B classification alone discards information when a proposal clearly combines both routes but has a dominant direction.

Ordinal scoring allows:

- block-level mean response curves;
- ordinal mixed-effects models;
- easy human interpretation;
- robust binary sensitivity analysis;
- less reliance on arbitrary probability extraction from an LLM judge.

Primary confirmatory endpoint can be either:

```text
E[S | alpha]
```

or the pre-registered probability contrast:

```text
P(S>0) - P(S<0)
```

Both should be reported; one must be declared primary before treatment outcomes.

## 4. Route definitions must be frozen and neutral

For every block, Route A/B descriptions are created from source-only evidence before model generation.

Requirements:

- 1–3 sentences per route;
- equal approximate length;
- no value-laden terms (`better`, `more rigorous`, `novel`);
- no paper titles/authors;
- no exact proposed-method names unless route identity cannot otherwise be expressed;
- route definitions describe scientific objective/framing, not an implementation recipe;
- A/B order randomized for annotators.

Example:

```text
Route A: Develop or modify a model/training/inference method to directly improve long-context task performance or efficiency.

Route B: Diagnose or characterize failure modes and boundary conditions that explain when long-context systems fail.
```

## 5. Human annotation protocol

### Development phase

Before treatment results:

1. construct 30–50 pilot items from source-paper or synthetic non-treatment proposals;
2. use at least two knowledgeable annotators;
3. discuss disagreements to refine the rubric;
4. freeze annotation guide and examples.

### Confirmatory treatment phase

For the main blinded audit:

- at least 2 independent annotators per item;
- 3 annotators on a stratified adjudication/reliability subset;
- condition/model/evidence hidden;
- random item order;
- block A/B presentation orientation randomized.

Do not show annotators which result direction is hypothesized.

## 6. Reliability metrics

Report at least:

- exact/adjacent agreement;
- weighted Cohen's kappa for two-rater subsets or equivalent ordinal agreement;
- Krippendorff alpha (ordinal) where suitable;
- disagreement rate for `A vs B` sign;
- reliability stratified by route pair and abstraction difficulty.

Important gate:

> If annotators cannot reliably determine whether a proposal leans A or B, that block/contrast is not a valid primary scientific measurement object.

Do not rescue low-reliability blocks using an LLM classifier.

## 7. Scalable classifier after human freeze

If generation scale exceeds feasible full human labeling, an automated parser/classifier may be trained/prompted only **after** the human rubric is frozen.

Allowed procedure:

1. collect human-labeled calibration set;
2. freeze train/dev/test split by block;
3. fit/prompt classifier without treatment labels;
4. measure human agreement on held-out blocks;
5. use classifier for scale only if pre-specified performance gate is met;
6. main paper still reports human-only confirmatory estimates on a stratified subset.

### Suggested performance gate

Do not freeze an exact threshold until annotation dry-run, but the automated sign (`A vs B`) should have high enough held-out human agreement that classifier error is materially smaller than the expected treatment effect.

If not, use human labels only.

## 8. Avoid evaluator leakage

The classifier/judge prompt must not include:

- alpha;
- evidence packet;
- source-paper route counts;
- model baseline propensity;
- expected direction.

Its task is only:

> Given seed question + Route A/B definitions + proposal, classify proposal direction.

## 9. Quality guardrail is separate from route direction

Route movement can be meaningless if one condition produces incoherent ideas.

Separately label on a subset:

```text
RELEVANT_TO_SEED
SCIENTIFICALLY_COHERENT
TESTABLE
COARSELY_FEASIBLE
```

Do not combine quality into the route score.

Primary route effect should be reported:

- unconditional;
- conditional on valid/relevant outputs;
- with invalid-rate differences by treatment.

A route effect caused by one route yielding nonsense is not scientific steering.

## 10. Secondary external taxonomy axis

Retain the coarse external contribution axis inspired by existing literature:

```text
ARTIFACT / KNOWLEDGE / BOTH / UNCLEAR
```

This serves as a robustness analysis only.

The paper's primary inference should survive without the six-way global scientific-move taxonomy.

## 11. Measurement model

At generation `g` inside block `b`, model `m`, evidence level `alpha`:

```text
S_gbma ∈ {-2,-1,0,1,2}
```

Primary block-level descriptive quantity:

```text
mu_bm(alpha) = E[S | block=b, model=m, alpha]
```

Primary extreme contrast:

```text
Delta_bm = mu_bm(1) - mu_bm(0)
```

Population analysis should aggregate across independent blocks, not treat generations as independent scientific replications.

Possible confirmatory hierarchical model:

```text
S ~ alpha
  + baseline_route_propensity
  + alpha × baseline_route_propensity
  + model effects
  + route-pair effects
  + block random effects
```

Use an ordinal model if stable; block-level nonparametric/continuous summaries remain an important robustness analysis.

## 12. A useful measurement falsification test

Before scientific interpretation, check whether a blinded annotator can identify the treatment condition itself from the proposal with accuracy far above what is explained by route direction.

If treatment-condition identification is driven by copied paper-specific entities, the effect may be source imitation rather than abstract scientific-choice movement.

Therefore retain direct-copy/entity-transfer diagnostics separately.

## 13. Decision

**KEEP / HUMAN-ANCHORED MEASUREMENT REQUIRED.**

The primary result should be anchored in blinded human route judgments. Automated judges may scale annotation but cannot define the scientific effect by themselves.