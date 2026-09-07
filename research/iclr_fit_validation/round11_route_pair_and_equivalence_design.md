# Round 11 — Predeclared Scientific-Route Contrasts and Equivalence Design

> Status: **RESEARCH DESIGN — CODEX HOLD**  
> Goal: remove another selection-bias channel and make the core context-steerability experiment reviewer-defensible without relying on a fragile global taxonomy.

---

## 0. Main conclusion

Do **not** choose one A/B contrast per seed because it looks especially interesting or because the model has a strong prior on it.

A cleaner high-resource design is:

> **Predeclare a small roster of scientifically distinct route contrasts. For every seed, include every contrast that passes source-only evidence availability and matching gates.**

This avoids:

- choosing the most dramatic pair;
- selecting treatments based on model prior;
- silently discarding weak-response route pairs;
- making the global taxonomy itself the scientific contribution.

The full experiment can be larger; interpretability is more important than minimizing calls.

---

## 1. Why a route-pair roster is preferable

Accepted ICLR work provides a useful design analogy.

**BiasBusters (ICLR 2026)** creates functionally equivalent tool alternatives and studies which features shift model choices under controlled conditions.

https://proceedings.iclr.cc/paper_files/paper/2026/hash/a79875cc0d046ce7ce65f03f3affaa9e-Abstract-Conference.html

For scientific ideation, exact functional equivalence is impossible because research directions are open ended. The appropriate analogue is:

```text
same seed scientific problem
+ both routes scientifically plausible
+ both supported by real, comparably relevant literature
+ neither route asserted to be objectively optimal
+ evidence amount held fixed
```

The causal question is not which route is better. It is how the model redistributes search probability when evidence support changes.

---

## 2. Proposed predeclared contrast roster

Start with contrasts likely to be meaningful across multiple ICLR areas.

### Contrast R1 — BUILD vs DIAGNOSE

```text
BUILD_IMPROVE
vs
DIAGNOSE_STRESS_TEST
```

Interpretation:

- route A asks how to construct/improve a system;
- route B asks where/why the current paradigm fails or under what boundary conditions it breaks.

This is likely the highest-coverage contrast.

### Contrast R2 — BUILD vs MEASURE

```text
BUILD_IMPROVE
vs
MEASURE_EVALUATE
```

Interpretation:

- route A changes the model/system;
- route B changes or interrogates how behavior is measured.

Useful because modern ICLR contains many evaluation-reframe papers alongside algorithm papers.

### Contrast R3 — BUILD vs EXPLAIN

```text
BUILD_IMPROVE
vs
EXPLAIN_MECHANISM_THEORY
```

Interpretation:

- route A targets capability/performance;
- route B targets explanation/mechanism/theory.

This contrast directly tests whether model research advice defaults toward intervention rather than understanding.

### Contrast R4 — DIAGNOSE vs EXPLAIN

```text
DIAGNOSE_STRESS_TEST
vs
EXPLAIN_MECHANISM_THEORY
```

Interpretation:

- identify where a phenomenon fails;
- explain why it occurs.

This is subtler than R1–R3 and should only be included where human annotation can distinguish it reliably.

### Secondary/exploratory contrasts

`OPTIMIZE_EFFICIENCY` and `VERIFY_FALSIFY_REPLICATE` remain measurable but should not initially define primary route pairs unless source coverage is demonstrated.

`VERIFY/FALSIFY` may be particularly scientifically interesting if sparse, but sparsity must not be turned into a hand-picked treatment.

---

## 3. Seed inclusion rule

For every candidate seed `s` and every predeclared route contrast `r=(A,B)`:

1. create a large source-only candidate pool from temporally eligible ICLR literature;
2. apply a frozen relevance floor;
3. independently annotate source papers for scientific route;
4. require minimum evidence count for both A and B;
5. attempt relevance/covariate matching;
6. include the `seed × route-pair` block if and only if the match passes the frozen balance gate.

Record all failure reasons:

```text
PASS
INSUFFICIENT_A
INSUFFICIENT_B
RELEVANCE_FLOOR_FAIL
MATCHING_FAIL
ANNOTATION_AMBIGUOUS
TEMPORAL_FAIL
SEED_TOO_NARROW
```

No model generation is involved in inclusion.

---

## 4. Scientific equivalence is not "same relevance score"

A dense embedding score alone is not enough to claim A and B packets are equally scientifically plausible.

Use a layered gate.

### Layer E1 — topic relevance

Automated retrieval/reranking:

- dense similarity;
- cross-encoder/reranker score if available;
- same candidate universe.

### Layer E2 — scientific usefulness to seed

Pre-treatment blinded annotation on candidate evidence:

> Does this paper contain findings/methods/failures/analysis that could reasonably inform a serious research proposal addressing the seed question?

Ordinal rating, e.g. 1–5.

This rating concerns usefulness/relevance only, not whether the annotator prefers the route.

### Layer E3 — route validity

Annotator judges whether the paper genuinely exemplifies route A/B rather than merely containing a keyword.

### Layer E4 — packet balance

Before generation, compare A/B packets on:

- automated relevance;
- human scientific-usefulness rating on audited subset;
- token length;
- public date/year;
- topic cluster;
- venue fixed to ICLR for core corpus;
- optional popularity only if measured consistently.

Do not claim true causal isolation if relevance distributions remain materially separated.

---

## 5. Primary outcome should be local and blinded

For a generated proposal from seed `s` under route pair `(A,B)`, primary human outcome is:

```text
A-LEANING
B-LEANING
MIXED/BOTH
NEITHER/OTHER
INVALID/NOT-RESPONSIVE
```

Annotators see:

- seed research question;
- operational descriptions of A and B;
- generated proposal.

They do **not** see:

- evidence condition;
- evidence mixture fraction;
- model identity if removable;
- no-context prior;
- study hypothesis.

This outcome is easier to defend than asking humans to map every proposal into a six-way universal ontology.

### Agreement target

Before confirmatory treatment outcomes, perform a pre-treatment annotation pilot on source papers and unrelated/no-context proposal examples.

If A/B distinction cannot achieve acceptable agreement, that route contrast is removed globally before treatment data are inspected.

Do not delete individual seed outcomes because they are inconvenient.

---

## 6. Mixture intervention

For each passing `seed × pair` block and fixed `k`:

```text
alpha(A) = 0.00, 0.25, 0.50, 0.75, 1.00
```

Each mixture must sample from matched route-specific evidence pools.

Primary response curve:

```text
P(A-LEANING | alpha(A))
```

Secondary:

```text
P(B-LEANING)
P(MIXED)
P(OTHER)
```

This preserves open-ended generation while giving a clear causal target.

---

## 7. Prior becomes a moderator

Only after route-pair/treatment construction is frozen, run no-context generations.

For each `model × seed × route pair`, estimate:

```text
p0_A
p0_B
```

from independently annotated no-context outputs.

Then test:

### Main evidence effect

Does increasing A evidence increase A-leaning output?

### Prior effect

Does the model favor A/B without literature context?

### Interaction

Does equal evidence have less leverage when it pushes against a stronger prior?

A particularly strong result is cross-model:

```text
same seed
same frozen evidence packets
model 1: strong A prior
model 2: weak/reversed A prior
↓
different response curves predicted by prior strength
```

This is much harder to explain as simple source imitation.

---

## 8. Distinguish four levels of evidence response

Do not collapse all context following into one variable.

For a blinded subset measure:

1. **SOURCE/ENTITY UPTAKE** — uses source-specific names/entities;
2. **CONCEPT/FINDING UPTAKE** — uses supplied scientific finding/limitation;
3. **METHOD-FAMILY UPTAKE** — changes concrete methodological family;
4. **ROUTE UPTAKE** — switches the high-level scientific objective A↔B;
5. **CENTRAL-FRAMING UPTAKE** — changes the central scientific question/failure/mechanism.

The scientifically interesting phenomenon may be a dissociation rather than monotone hierarchy.

Avoid constructing a score that assumes `1 > 2 > 3 > 4 > 5` before data.

---

## 9. Why this remains distinct from nearest work

### Carlon et al. 2026

https://arxiv.org/abs/2606.26130

Shows LLM-generated methodologies are much narrower than paper-derived inventories and that this concentration is shared across models.

Our study should treat this as evidence that a default scientific-method prior exists, not claim it as new. We ask whether real literature can causally override/differentially interact with that prior.

### Spectrum Tuning, ICLR 2026

Studies distributional steerability where context defines a target distribution.

Our evidence does not tell the model which route to choose; it provides ecologically realistic scientific literature whose composition serves as an implicit signal.

### Scientific hypothesis diversity/search work

Already proposes methods to increase portfolio diversity.

We are not optimizing diversity. We are measuring causal response and prior resistance in open-ended scientific search.

---

## 10. New kill criteria

Kill or fundamentally pivot if any of the following occurs:

1. route A/B human distinction is not reproducible before treatment;
2. matching cannot make A/B evidence comparably relevant/useful;
3. dose response is explained almost entirely by explicit route words or exact method copying;
4. within-route packet swaps produce effects as large as cross-route composition changes;
5. model prior does not add explanatory/predictive value beyond evidence text alone;
6. controlled response fails to improve held-out natural-RAG prediction;
7. the effect only exists for one hand-picked route pair/domain/model.

---

## 11. Codex status

**Still HOLD.**

The remaining research task is to validate that the predeclared route roster has adequate ICLR source coverage and can be operationalized without ambiguous annotations.

Codex becomes useful once the following are frozen:

- route roster;
- seed eligibility rules;
- source relevance/usefulness gate;
- exact temporal ICLR corpus policy;
- annotation protocol;
- packet matching tolerances.

At that point corpus construction and matching become engineering/data work and should be handed to Codex.