# Research Round 31 — Three-Route Simplex Extension

## 1. Trigger

A binary A/B design is experimentally clean but may invite a reviewer objection:

> The apparent response could be specific to one hand-constructed contrast rather than evidence composition acting on a broader scientific-choice distribution.

For seeds with unusually rich contemporaneous literature, a three-route experiment can test whether the phenomenon generalizes beyond binary choice.

This is a **stretch extension**, not a prerequisite for the core pilot.

## 2. Eligibility is intentionally strict

A seed enters the three-route study only if three routes `(A,B,C)` independently pass:

- seed relevance;
- scientific plausibility;
- pairwise distinguishability;
- source evidence count;
- relevance/covariate matching;
- no obvious dominance;
- annotation reliability.

Do not manufacture a third route to increase complexity.

## 3. Example route triplets

Illustrative only; actual triplets are source-selected before outcomes.

```text
BUILD / IMPROVE
DIAGNOSE / STRESS-TEST
MEASURE / EVALUATE
```

or

```text
BUILD / IMPROVE
MEASURE / EVALUATE
EXPLAIN / MECHANISM
```

Triplets should represent genuinely different scientific objectives for the same seed.

## 4. Evidence simplex

For fixed packet size `k`, evidence composition lies on:

```text
alpha_A + alpha_B + alpha_C = 1
```

For `k=9`, use a compact predeclared design such as:

### Vertices

```text
(1,0,0)
(0,1,0)
(0,0,1)
```

### Center

```text
(1/3,1/3,1/3)
```

### Edge mixtures

```text
(2/3,1/3,0)
(1/3,2/3,0)
(2/3,0,1/3)
(1/3,0,2/3)
(0,2/3,1/3)
(0,1/3,2/3)
```

This yields a modest 10-condition simplex design.

Do not tune compositions based on outcome curvature.

## 5. Measurement

Blinded annotators see neutral definitions of A/B/C and label proposal:

```text
PRIMARY_A
PRIMARY_B
PRIMARY_C
MIXED_AB
MIXED_AC
MIXED_BC
MIXED_ABC
OTHER
INVALID
```

For scalable modeling, derive soft route allocation if annotation supports it, but categorical human judgments remain the anchor.

## 6. Main question

Does increasing evidence mass for route `j` increase the probability that output primarily follows route `j`, after controlling for baseline model × seed route propensity?

A simple multinomial model:

```text
P(Y=j)
 = softmax(
     intercept_j
     + beta_E * alpha_j
     + beta_B * baseline_j
     + beta_EB * alpha_j * baseline_j
   )
```

The exact model is secondary; simplex plots are primary descriptive evidence.

## 7. Strong result

The most compelling pattern would be:

```text
evidence vertices → output distributions move toward corresponding route
center → more balanced/mixed output
edge mixtures → intermediate route allocation
```

with model-specific distortion explained by no-context baseline propensity.

This would show that scientific evidence composition acts on a multi-way choice distribution rather than producing a binary priming artifact.

## 8. Prior-bound / anisotropic result

Another interesting pattern:

```text
A evidence easily shifts model toward A
B evidence shifts moderately
C evidence barely moves output
```

and these anisotropies correlate with baseline route probabilities.

This produces an intuitive geometric interpretation:

> The model's scientific search space is not equally steerable in all directions.

Possible paper language only if robust:

```text
anisotropic scientific evidence response
```

Do not invent a new term unless the effect is strong and reproducible.

## 9. Visualization

Use a ternary/simplex figure.

For each evidence composition point:

- position = evidence A/B/C fractions;
- color/marker or vector = observed output route distribution;
- arrows = displacement from no-context baseline.

A particularly clean figure could compare two model families on the same simplex.

## 10. Natural-RAG extension

For three-route held-out seeds, project natural retrieval packet into the same simplex:

```text
(E_A, E_B, E_C)
```

Use the controlled response model to predict natural output distribution.

This would be a stronger external-validity test than pairwise prediction, but only if sufficient triplets exist.

## 11. Cost/complexity warning

The simplex design multiplies conditions and human annotation burden.

Do not run unless:

- pairwise core effect is robust;
- source-only feasibility finds enough 3-route seeds;
- annotation can distinguish routes reliably;
- the expected contribution is worth the additional cost.

## 12. Why this matters for ICLR positioning

Spectrum-style distributional work studies movement among known target distributions. Our setting remains distinct because scientific evidence implicitly suggests several legitimate research strategies without instructing the model to follow a target route.

A successful three-route result would make that distinction visually and statistically stronger.

## 13. Decision

**STRETCH / HIGH UPSIDE.**

Do not block the binary core study. If source feasibility reveals many `ELIGIBLE_3PLUS_MODES` seeds, reserve a subset before outcomes so the extension does not become post-hoc.