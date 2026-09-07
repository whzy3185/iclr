# Research Round 48 — Proposal Quality Guardrail and Non-Inferiority Logic

## 1. Trigger

A treatment may produce a large A/B route shift for the wrong reason:

```text
one evidence condition confuses the model
→ output becomes vague/off-topic
→ annotators force the remaining valid proposals toward the other route
```

or a route-enriched context may yield scientifically weaker proposals because the route is poorly supported for that seed.

Therefore route movement must be separated from proposal validity/quality.

The paper does **not** need to show one route is better, but it must rule out obvious quality collapse as the explanation for the causal effect.

## 2. Quality is a guardrail, not the primary objective

Primary outcome remains:

```text
blinded scientific route score
```

Quality is measured independently and must not be combined into a single route-quality metric.

Do not redefine the main effect as a quality leaderboard.

## 3. Minimum quality dimensions

On a blinded human/expert subset, rate separately:

```text
RELEVANCE_TO_SEED
SCIENTIFIC_COHERENCE
TECHNICAL_SUBSTANCE
TESTABILITY
COARSE_FEASIBILITY
```

Suggested simple ordinal scale:

```text
1 = clearly poor
2 = weak
3 = acceptable
4 = strong
5 = very strong
```

Exact rubric/anchors are frozen in F1/P0.

## 4. Invalid output is separate

Before quality scoring label:

```text
VALID_PROPOSAL
OFF_TOPIC
INCOHERENT
NON_RESEARCH_RESPONSE
FORMAT_FAILURE
REFUSAL
```

Invalid categories are reported by condition/model.

Do not silently exclude invalid responses from the unconditional route effect.

## 5. Two route-effect analyses

Report:

### Unconditional

All generations with invalid/neither represented explicitly.

This reflects actual system behavior.

### Valid-proposal conditional

Route effect among proposals passing a frozen validity rule.

If the treatment effect exists only after large condition-specific exclusions, interpretation is weak.

## 6. Quality-balance question

For each alpha/model compare quality distributions.

The desired scientific statement is modest:

> Evidence composition changes research direction **without a large systematic collapse in proposal validity or scientific quality**.

We do not require exact equality or quality improvement.

## 7. Non-inferiority planning logic

A formal quality non-inferiority margin can be useful, but should not be chosen before human score variability is known.

After F1/P0 and before P1:

1. inspect quality-rubric reliability/dispersion;
2. define a smallest meaningful quality degradation;
3. freeze a non-inferiority margin or a descriptive guardrail CI criterion.

Illustrative only:

```text
if mean quality is on 1–5 scale,
a drop of 0.1 may be trivial,
a drop of 0.5 may be clearly meaningful.
```

Do not freeze these example numbers as the actual margin.

## 8. Route-specific quality is not a confound by definition

Different scientific strategies can legitimately differ in perceived feasibility or ambition.

Source-level equipoise is intended to prevent gross asymmetry, not guarantee identical downstream quality.

Interpretation rule:

- small route-specific quality differences: report and continue;
- large systematic degradation tied to evidence direction: investigate/possibly fail validity gate;
- quality difference fully explains route annotations: kill causal scientific-choice story.

## 9. Human expertise requirement

High-level A/B route classification may be possible for trained ML annotators, but feasibility/technical-substance scoring benefits more from domain expertise.

Recommended hierarchy:

### Route outcome

- broad technically knowledgeable ML annotators, after rubric calibration;
- expert adjudication on difficult blocks.

### Quality guardrail

- smaller stratified subset rated by researchers/graduate-level domain experts where feasible.

Do not attempt to scale broad quality scoring purely with an LLM judge; recent ideation studies show meaningful judge–expert disagreement.

## 10. Treatment blindness

Quality annotators see:

- seed;
- proposal;

Optionally route definitions only if needed for relevance interpretation, but **not evidence packet, alpha, or model identity**.

Prefer not to show route definitions for generic quality ratings so judges do not treat one route as intended.

## 11. Pairwise expert comparison optional

For a smaller subset, pair proposals generated under opposing evidence conditions but normalize presentation order and hide condition.

Ask:

```text
Which proposal is more scientifically compelling overall?
```

This is exploratory/guardrail only.

A consistent preference for one condition could reveal route-quality asymmetry that the source equipoise audit missed.

Do not make this another leaderboard.

## 12. Treatment may affect ambition

Evidence routes may shift not only scientific direction but project scope/ambition.

Track on an exploratory subset:

```text
project_scope
engineering_cost
empirical_breadth
```

If Route A is systematically a large systems build and Route B a small diagnostic study, differences in feasibility may be structurally expected.

This is another reason to report pair type/composability rather than pool blindly.

## 13. Strong result pattern

```text
route score changes strongly with alpha
valid rate stable
quality dimensions approximately stable
```

This supports genuine scientific-choice redistribution.

## 14. Acceptable but nuanced pattern

```text
route shift exists
one route has modest feasibility cost
other quality dimensions stable
```

Report the trade-off rather than hiding it.

## 15. Weak/kill-relevant pattern

```text
route shift driven by:
- invalid responses,
- off-topic proposals,
- major feasibility collapse,
- severe relevance loss,
- one evidence route producing generic/low-substance output.
```

Then the manipulation does not demonstrate meaningful high-level scientific choice.

## 16. Natural-RAG quality check

Held-out natural RAG should use the same validity/quality guardrails.

If controlled packets produce high-quality proposals but natural packets yield qualitatively different validity behavior, this may explain prediction failure and should be analyzed.

## 17. Decision

**QUALITY = REQUIRED GUARDRAIL, NOT PRIMARY ENDPOINT.**

A scientifically interesting evidence-response law must survive basic validity and avoid major condition-specific proposal-quality collapse.