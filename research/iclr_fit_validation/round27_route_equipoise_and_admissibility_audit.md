# Research Round 27 — Route Equipoise and Admissibility Audit

## 1. Trigger

Even perfect relevance matching is not enough. For a given seed question, Route A and Route B may differ in scientific plausibility, specificity, maturity, or whether one route simply dominates/subsumes the other.

If a model resists B because B is scientifically weak, that is not evidence of a model baseline resisting context. Conversely, if A is an obvious direct solution and B is a peripheral analysis, an A-heavy output is not a meaningful prior.

Therefore each seed-route block requires a **pre-treatment scientific equipoise audit**.

## 2. Definition of an admissible route pair

For seed question `x`, routes `(A,B)` are admissible only if both satisfy:

1. **Relevance** — directly addresses the seed's scientific problem.
2. **Plausibility** — a competent ICLR researcher could reasonably pursue the route.
3. **Distinctness** — A and B represent meaningfully different research objectives/strategies.
4. **Non-subsumption** — one route is not merely a necessary substep of the other.
5. **Evidence support** — the ICLR evidence corpus contains enough high-relevance papers for both.
6. **No obvious dominance** — based on source-only information, neither route is clearly the unique rational choice.
7. **Annotatability** — a generated proposal can, in principle, be judged as leaning A, B, mixed, or neither.

## 3. Pre-treatment human/source-only audit

Before any model baseline or treatment generation, present auditors with:

- method-masked seed question;
- neutral Route A description;
- neutral Route B description;
- representative source-paper evidence summaries for both routes if needed;
- no model outputs.

For each route separately rate 1–5:

```text
RELEVANCE_TO_SEED
SCIENTIFIC_PLAUSIBILITY
EVIDENCE_SUPPORT
```

For the pair rate 1–5:

```text
DISTINGUISHABILITY
EQUIPOISE
NON_SUBSUMPTION
ANNOTATABILITY
```

## 4. Suggested eligibility rule

Exact thresholds should be frozen after a small pre-treatment audit, but a candidate primary block should require approximately:

```text
A relevance >= 4/5
B relevance >= 4/5
A plausibility >= 4/5
B plausibility >= 4/5
pair distinguishability >= 4/5
pair annotatability >= 4/5
```

and no severe dominance/non-subsumption failure.

Do not weaken thresholds to increase block count after treatment outcomes.

## 5. Route pair types

Not every pair should be treated identically.

### Type I — Competing strategic emphasis

Example:

```text
BUILD / IMPROVE
vs
DIAGNOSE / STRESS-TEST
```

Both can answer the seed, but they prioritize different scientific moves.

Best suited to route-choice analysis.

### Type II — Competing epistemic objective

Example:

```text
MEASURE / EVALUATE
vs
EXPLAIN / MECHANISM
```

One route asks how to measure the phenomenon; the other asks why it occurs.

Potentially strong because neither is simply a different algorithm.

### Type III — Complementary / easily combinable

Example:

```text
DIAGNOSE
vs
EXPLAIN
```

Many good papers naturally do both.

These blocks may yield many `MIXED` proposals. They can still be informative but should be labeled as high-composability pairs and not pooled blindly with Type I/II.

### Type IV — Hierarchical/subsumed

Example:

```text
BUILD method
vs
OPTIMIZE efficiency of that same method
```

Often one can be nested inside the other. Avoid as primary A/B treatment unless audit shows genuine distinct strategic choices.

## 6. Add composability score

For every route pair, pre-treatment auditors assign:

```text
COMPOSABILITY 1–5
```

Question:

> How naturally could a single coherent ICLR project pursue both routes as co-primary aims?

High composability predicts more `MIXED` outputs and weaker forced directional separation.

This is not a nuisance to hide; it is a scientifically meaningful moderator.

Possible analysis:

```text
route_response ~ evidence_exposure × composability
```

But treat this as secondary unless block count is large enough.

## 7. Dominance / quality confounding

Add a blinded source-only question:

> If you had to advise a researcher today, with no access to model outputs or treatment condition, which route is more scientifically promising for this seed?

Allowed labels:

```text
A clearly stronger
A somewhat stronger
roughly equal
B somewhat stronger
B clearly stronger
cannot judge
```

Primary blocks should favor `roughly equal` or only mild asymmetry.

If one route is systematically stronger, include this score as a pre-treatment covariate and report sensitivity; do not reinterpret model preference as a baseline bias.

## 8. Evidence packet matching gains another dimension

For each A/B evidence pool, match not only:

- relevance;
- date;
- length;
- topic cluster;

but also monitor route-level source quality proxies available without outcome peeking.

Because the primary universe is accepted ICLR papers, venue is fixed, which helps. Still inspect:

- oral/spotlight/status if used at all;
- citation/popularity only at a frozen date, if included;
- empirical/theoretical evidence specificity;
- whether one route pool consists mostly benchmark papers and the other mostly full algorithm papers.

Do not overengineer a scalar "paper quality" score. Human equipoise is the primary guardrail.

## 9. Block-level causal interpretation

The clean causal statement is conditional:

> Among seed-route blocks where two research strategies are independently judged relevant, plausible, distinguishable, and approximately in equipoise, changing matched evidence composition changes the model's research-choice distribution.

This is narrower than a universal statement about science but much more defensible.

## 10. Generalization reporting

Report:

```text
candidate seeds
→ seeds with >=2 evidence-supported routes
→ route pairs passing relevance matching
→ route pairs passing equipoise/admissibility
→ final experimental blocks
```

This attrition diagram should appear in the paper or appendix.

If only a tiny fraction of seeds survive equipoise, the target population is narrow and the paper must say so.

## 11. Kill condition added

KILL or substantially narrow the project if:

- most source-supported route pairs fail scientific equipoise;
- B routes require weaker or less relevant evidence to construct;
- annotators consistently judge one route as obviously superior;
- route pairs are too composable to support interpretable directional outcomes;
- enough primary blocks cannot be formed without hand-picking unusual questions.

## 12. Decision

**REQUIRED PRE-TREATMENT GATE.**

Relevance matching answers whether the documents are comparable. Scientific equipoise answers whether the *research choices* are comparable. Both are needed for causal interpretation.