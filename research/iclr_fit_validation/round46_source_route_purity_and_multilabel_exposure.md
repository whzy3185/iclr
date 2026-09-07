# Research Round 46 — Source Route Purity and Multi-Label Exposure

## 1. Trigger

Real ICLR papers frequently make multiple contributions.

Example structure:

```text
diagnose failure
→ explain mechanism
→ propose mitigation
→ evaluate benchmark
```

Labeling such a paper as only `DIAGNOSE` or only `BUILD` can create measurement error in the evidence treatment.

The core experiment therefore needs to distinguish:

```text
primary scientific route
secondary scientific content
route purity / ambiguity
```

before model outcomes.

## 2. Source-paper route annotation becomes multi-label

For every evidence paper, source-only annotation should include:

```json
{
  "primary_route": "DIAGNOSE_STRESS_TEST",
  "secondary_routes": ["BUILD_IMPROVE"],
  "primary_route_strength": 4,
  "opposite_route_contamination": 1,
  "confidence": 0.85
}
```

`primary_route_strength` planning scale:

```text
5 = paper is overwhelmingly organized around this scientific objective
4 = clearly primary, with minor secondary contributions
3 = mixed/multiple central objectives
2 = weak primary distinction
1 = cannot meaningfully assign a primary route
```

Exact rubric is frozen in F1.

## 3. Core matched-slot eligibility prefers route-clear papers

For confirmatory A/B matched slots, prefer evidence papers with:

```text
primary_route_strength >= predeclared threshold
```

and without a strong secondary label equal to the opposite route.

Example:

For `BUILD vs DIAGNOSE`:

- a paper that discovers a failure and then adds a small repair can still be DIAGNOSE;
- a paper whose main contribution is a new method plus a long failure analysis may be too mixed for a clean slot.

Do not set the purity threshold after seeing model responses.

## 4. Source feasibility must report purity attrition

F0 should distinguish:

```text
raw route count
route-clear count
matched route-clear slots
```

If the route-clear filter destroys coverage, that is a real design limitation.

Do not silently relax purity to increase k.

## 5. Treatment purity is not binary reality

Even a route-clear paper contains facts/methods that may support other directions.

Therefore the paper should say:

> evidence packets are **enriched for** Route A vs Route B scientific objectives

rather than claiming every word belongs to one route.

This wording is more scientifically accurate.

## 6. Hard route label for primary causal design

Use the frozen primary route label to construct the matched-slot experiment because it keeps the intervention transparent:

```text
A paper vs matched B paper
```

Primary alpha is based on primary-route membership.

Do not replace this with an opaque LLM-derived continuous route score as the main treatment variable.

## 7. Soft/multi-label exposure as robustness

Secondary analysis can calculate a source-only soft route exposure using audited multi-label annotations.

For paper i in A/B block, define illustrative source weights:

```text
q_i(A), q_i(B)
```

from human/source annotation, with:

```text
q_i(A) + q_i(B) <= 1
```

remaining mass represents other/mixed objectives.

Packet soft exposure:

```text
E_soft(C)
 = sum_i [q_i(A) - q_i(B)] / k
```

Use only as robustness/predictive feature if annotation reliability supports it.

## 8. Opposite-route contamination diagnostic

For each matched slot:

```text
A_i ↔ B_i
```

record whether:

- A paper contains substantial B-route content;
- B paper contains substantial A-route content.

High contamination slots can be:

- excluded by a pre-treatment purity rule;
- retained in a broad sensitivity sample;
- analyzed separately.

Never drop them based on treatment response.

## 9. Mixed papers may be useful negative controls

A high-composability/multi-route paper could be used later as a secondary context condition:

```text
route-pure A
route-pure B
mixed A+B paper
```

Question:

> Does mixed evidence increase MIXED proposals or reduce directional response?

This is optional; do not add to core unless motivated by main data.

## 10. Primary vs secondary contribution extraction

Annotation question for source paper:

> If the authors could preserve only one contribution/result as the main reason this paper matters, what scientific objective would it be?

Then record secondary central objectives separately.

This is preferable to keyword counting or section-length heuristics.

## 11. Abstract-only limitation

The primary evidence context is abstract text. Route annotation should therefore ideally be based on the same abstract for treatment purity, with full paper consulted only to resolve ambiguity.

Otherwise a paper may be labeled from full text based on a contribution that is barely represented in the abstract the model actually sees.

Store:

```text
route_label_from_abstract
fulltext_resolution_used
```

## 12. Lexical separability does not define purity

A route-pure paper may still use generic wording, and a mixed paper may contain obvious route keywords.

Purity is a scientific contribution judgment, not classifier confidence.

Use lexical classifier only as a priming diagnostic.

## 13. Human reliability gate

On a pre-treatment sample report agreement for:

- primary route;
- whether an opposite route is a major secondary contribution;
- primary-route strength bin (e.g. high/medium/low).

If fine-grained strength has low reliability, use a simpler frozen binary:

```text
ROUTE_CLEAR
MIXED_OR_AMBIGUOUS
```

Core design should prefer a reliable coarse purity criterion over noisy numeric pseudo-precision.

## 14. Natural-RAG implication

Natural top-k packets will contain many mixed/other papers.

For controlled experiments:

```text
hard route-enriched packets
```

For natural prediction:

use:

- hard primary-route composition as simple predictor;
- soft/multi-label route content as robustness if validated;
- explicit `OTHER/MIXED` coverage.

If natural prediction improves only with rich soft labels, report that low-dimensional hard composition is insufficient.

## 15. Revised causal wording

Strong but precise:

> Replacing matched literature whose **primary scientific objective** supports Route B with literature whose primary objective supports Route A shifts the distribution of generated research strategies.

Avoid:

> We manipulate the exact scientific information content while changing only route.

That stronger statement would be impossible with real papers.

## 16. Decision

**ADD PRE-TREATMENT ROUTE-PURITY GATE AND MULTI-LABEL ROBUSTNESS.**

The core experiment remains hard-label/matched-slot for interpretability, but source ambiguity must be measured rather than hidden.