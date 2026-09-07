# Research Round 33 — Staged Execution and Hard Gates

## 1. Purpose

The project now has enough possible extensions to create scope creep. This round defines a strict staged execution plan so that expensive generation is authorized only after upstream construct validity passes.

The ordering is scientific, not deadline-driven.

## 2. Stage F0 — Source-Only Feasibility

No scientific model generation.

Required outputs:

- temporally clean ICLR evidence corpus;
- seed manifest;
- source route annotations;
- route-pair inventory;
- relevance/matching diagnostics;
- equipoise/admissibility audit plan;
- `FEASIBILITY_RESULT.md`.

### Green signal

A broad enough set of unique seeds across multiple ICLR subfields supports at least two high-relevance, scientifically plausible, matchable routes.

Illustrative planning target (not yet a frozen threshold):

```text
>= 24 unique seeds
>= 3 subfields
multiple route-pair types
```

with additional 3-route seeds a bonus.

### Yellow signal

Enough blocks exist for a meaningful pilot but coverage is narrow, e.g. one/two route contrasts dominate or only 12–23 unique seeds survive.

Decision: run a narrow proof-of-design but do not assume full ICLR generality.

### Red signal

Too few unique seeds, severe relevance imbalance, or routes require hand-picking weak/off-topic papers.

Decision: **KILL before generation.**

Do not lower validity gates to manufacture sample size.

## 3. Stage F1 — Construct / Annotation Audit

Still no confirmatory treatment generation.

Tasks:

- freeze neutral route descriptions;
- seed validity audit;
- route equipoise audit;
- annotation rubric dry-run;
- blinded ordinal route score reliability;
- source taxonomy reliability;
- evidence-card extraction dry-run for later mechanism analysis.

### Pass condition

Humans can reliably distinguish A vs B route direction on representative proposal examples without treatment information.

### Fail condition

If route direction is inherently ambiguous, merge/redesign contrasts now or drop them.

Never let an LLM classifier rescue a failed human construct.

## 4. Stage P0 — Engineering / Variance Pilot

This is the first scientific generation stage, but it is not a confirmatory paper result.

### Block selection

Random/stratified sample from all pre-treatment eligible blocks.

Do not select blocks because they look likely to produce an effect.

### Compact conditions

Use:

```text
alpha = 0, .5, 1
```

rather than all five levels initially.

Two core model families.

Multiple packet realizations where possible.

### Pilot goals

Estimate:

- invalid-output rate;
- route annotation reliability on actual model outputs;
- packet variance;
- generation stochasticity;
- rough effect-size variance;
- prompt/order nuisance;
- whether RAW abstract effect is obviously just direct copying.

### Pilot prohibition

Do not:

- drop weak-effect blocks;
- choose the final route roster based on effect size;
- tune evidence matching to enlarge treatment effects;
- promote an exploratory p-value to the final claim.

The pilot may inform sample-size/precision design, not hypothesis selection.

## 5. Gate G0 — Is Full Confirmatory Study Justified?

Continue only if:

1. source/equipoise validity remains strong;
2. actual generated proposals can be reliably route-annotated;
3. treatment context does not cause major quality/invalid collapse;
4. packet identity noise is not overwhelming;
5. at least some route movement is plausible enough that the full study can estimate a meaningful effect with reasonable precision.

A near-zero pilot does not automatically kill if uncertainty is wide, but a precise trivial effect plus no deeper phenomenon should stop expansion.

## 6. Stage P1 — Confirmatory Matched-Mixture Study

Freeze before launch:

- all seeds and route pairs;
- core models/checkpoints;
- five alpha levels;
- packet-construction algorithm;
- packet realizations;
- prompt/version;
- human annotation plan;
- primary effect statistic;
- baseline interaction statistic;
- full-N or precision stopping rule;
- natural-RAG holdout split.

Conditions:

```text
alpha = 0, .25, .5, .75, 1
```

Primary output:

```text
seed-clustered evidence-response effect
+ dose-response curve
```

## 7. Gate G1 — Is There a Nontrivial Scientific Phenomenon?

### Continue path A

Robust high-level route response across models/blocks.

Proceed to mechanism + natural validation.

### Continue path B

Weak average response but clear, replicated baseline-dependent/asymmetric response.

Proceed if interaction is pre-specified and robust.

### Continue path C

Strong low-level uptake with systematic high-level attenuation.

Proceed only if abstraction hierarchy is reliable and not merely annotation artifacts.

### Kill

- effect only lexical/copying;
- one model / one hand-picked block;
- route outcome unreliable;
- relevance/equipoise confounded;
- effect scientifically tiny with precise CI.

## 8. Stage P2 — Mechanism Robustness

Only after G1.

Prioritized order:

1. content component knockout (`PF`, `PFM`, `PFL`);
2. within-route vs cross-route single-document replacement;
3. direct-copy exclusion;
4. prompt/order robustness;
5. abstraction-level uptake profile.

Do not start all at once. Each experiment must answer a specific Reviewer #2 objection.

## 9. Gate G2 — Is It More Than Priming?

Strong pass if at least one holds robustly:

- PF/PFL context retains substantial high-level effect without explicit method cues;
- cross-route replacement effect exceeds within-route document identity effect;
- route response persists after direct method-copy exclusions;
- baseline propensity systematically predicts response magnitude/direction;
- high-level response shows a reproducible nontrivial pattern across abstraction levels.

If none hold, downgrade/kill.

## 10. Stage P3 — Held-Out Natural RAG

Response model is frozen before held-out natural outcomes.

Compare:

```text
global/null
baseline only
evidence only
baseline + evidence
baseline + evidence + interaction
```

Primary question:

> Does evidence composition materially improve out-of-sample prediction beyond baseline route propensity?

## 11. Gate G3 — Paper-Level External Validity

### Strong pass

Controlled response law improves held-out natural-RAG prediction with reasonable calibration.

### Partial pass

Controlled effect is robust but natural prediction weak. Paper scope must remain controlled-context behavior unless another strong mechanism result compensates.

### Fail

Natural behavior is baseline-only and controlled effects have no explanatory bridge. Likely too artificial for the intended main claim.

## 12. Stage P4 — High-Upside Extensions

Only after the paper core is already viable:

- base vs instruction-tuned pairs;
- three-route simplex;
- frontier API external validity;
- established context-attribution bridge;
- generative-root / MUSES extension.

These improve breadth but cannot repair a broken core.

## 13. Paper freeze rule

A full paper draft should begin only after G1 has a clear scientific branch and preferably after G2.

Introduction/related work scaffolding is fine earlier, but do not write observed-result claims before data.

## 14. Codex authorization rule

Codex may execute only the currently authorized stage.

At every gate, the research lead reviews artifacts and writes an explicit next-stage authorization.

A previous broad workflow prompt never authorizes later scientific stages automatically.

## 15. Current status

As of this round:

```text
Stage = F0 source-only feasibility
Scientific generation = NOT AUTHORIZED
```

The experimental design is ready enough that source feasibility—not more brainstormed metrics—is the next empirical bottleneck.

## 16. Decision

**FREEZE STAGED GATES.**

Future research may refine details, but expensive execution should follow F0 → F1 → P0 → G0 → P1 → G1 → P2 → G2 → P3 → G3 in order.