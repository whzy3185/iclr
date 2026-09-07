# Research Round 14 — Post-Collision Paper Shape and Success Gate

## 1. Trigger

Rounds 12–13 materially narrowed the novelty boundary:

- familiar/default solution bias already appears in MetaMuse (ICLR 2026);
- external stimuli steering already appears in MetaMuse;
- general context-vs-prior steerability is established by Spectrum Tuning and related ICLR work;
- evidence neglect in AI scientists has direct 2026 evidence;
- scientific hypothesis priors/updating and future-research forecasting are now active neighboring areas.

Therefore, before any scientific outcomes exist, define exactly what a successful ICLR paper would need to show.

## 2. Current paper question

Preferred neutral pre-result question:

> **Can real scientific literature redirect an LLM's high-level research choices, and how does that leverage interact with the model's default research prior?**

More formal:

For model `M`, seed problem `x`, frozen scientific route pair `(A,B)`, evidence packet `C_alpha`, and open-ended proposal `Y`:

```text
Y ~ P_M(Y | x, C_alpha)
```

where `C_alpha` changes only the matched composition of evidence supporting route A vs route B.

The primary object is the response surface:

```text
P(route=A | evidence_fraction_A, no_context_prior_A, model, seed)
```

not generic idea diversity.

## 3. Minimum ICLR paper shape

A viable paper must have four linked pieces.

### Piece 1 — Controlled causal response

At fixed:

- seed question;
- model/version;
- prompt;
- context size;
- topical relevance distribution;
- evidence quality/time strata;

changing route composition in real scientific evidence must cause a reproducible change in high-level proposal direction.

A result that exists only in embeddings/lexical metrics is insufficient.

### Piece 2 — Non-trivial regularity beyond priming

At least one deeper regularity must hold:

- evidence × prior interaction;
- prior-congruence asymmetry;
- nonlinear/threshold dose response;
- abstraction-dependent uptake hierarchy;
- model/post-training-specific resistance pattern;
- treatment effect remains after content normalization / lexical controls.

Without one of these, the result is too close to “models mention what they read.”

### Piece 3 — Cross-setting replication

The primary regularity must reproduce across:

- multiple model families;
- multiple ICLR subfields/seeds;
- more than one predeclared route contrast where feasible.

One dramatic route pair or one model is not sufficient.

### Piece 4 — Controlled-to-natural prediction

Fit the response relation using controlled matched evidence only.

Then freeze it and test held-out natural top-k RAG seeds.

Compare:

```text
prior-only predictor
vs
prior + observed natural evidence composition
```

A strong paper should show that the controlled mechanism improves prediction of the model's natural-RAG route choices.

This is a mechanism-validation test, not forecasting what the scientific community will publish.

## 4. Pre-result Figure 1 specification

Figure 1 should make the entire paper understandable without requiring the taxonomy appendix.

### Panel A — controlled intervention

```text
same seed question
same model
same relevance
same context budget

Evidence packet A-heavy  ---> proposal leans route A
Evidence packet B-heavy  ---> proposal leans route B
```

### Panel B — dose response

```text
x-axis: fraction of evidence supporting route A
0 / .25 / .50 / .75 / 1

y-axis: blinded probability proposal is A-leaning
```

Include the no-context prior as a reference line.

### Panel C — prior interaction

Show two model/seed strata with different independently measured no-context preferences receiving identical treatment mixtures.

The ideal interpretable pattern is:

```text
same evidence
+
different priors
-> different response curves
```

## 5. Figure 2 — grounding versus high-level steering

Measure context uptake at increasing abstraction:

```text
source/entity uptake
concept/finding uptake
method-family uptake
local A/B research-route choice
coarse Artifact/Knowledge contribution family
central problem framing
```

Do not force monotonicity.

A publishable `prior-bound` branch requires evidence to be clearly used at lower levels while high-level route/problem response is disproportionately weaker or asymmetric.

## 6. Figure 3 — anti-triviality controls

At least three of the following should appear in the main paper or strong appendix:

- within-route paper swap;
- evidence order permutation;
- prompt paraphrase noise floor;
- matched relevance diagnostics;
- lexical treatment classifier;
- content-normalized evidence subset;
- exact-method copying diagnostic;
- temperature/sampling breadth control.

A convincing result should separate:

```text
source identity
lexical priming
generic sampling diversity
from
scientific route composition
```

## 7. Figure 4 — natural RAG prediction

For held-out seeds:

1. retrieve natural top-k literature;
2. annotate its route composition without seeing model outputs;
3. estimate no-context prior independently;
4. predict route allocation using the controlled response model;
5. run the generator;
6. compare predicted vs observed choices.

Report:

```text
prior-only
vs
prior + evidence composition
```

using seed-level uncertainty.

## 8. Outcome-conditioned paper branch A — strong steerability

Possible title:

**Same Relevance, Different Science: Scientific Evidence Steers LLM Research Search**

Required empirical pattern:

- matched evidence composition produces strong route-level dose response;
- effect survives anti-priming controls;
- prior explains systematic heterogeneity;
- controlled model predicts natural RAG.

Defensible claim:

> Real scientific literature acts as an implicit, quantitatively predictable control signal over open-ended research choices, and its leverage depends on the model's default scientific prior.

Do not claim first discovery of steering, context sensitivity, or idea diversity.

## 9. Outcome-conditioned paper branch B — grounded but prior-bound

Possible title:

**Grounded but Prior-Bound: Limits of Literature Steering in LLM Scientific Search**

Required empirical pattern:

- source/concept grounding is demonstrably high;
- high-level route steering is substantially weaker, asymmetric, thresholded, or prior-dependent;
- high prior strength predicts resistance to counter-route evidence;
- result survives relevance and lexical controls;
- natural RAG lies in the same predicted regime.

Defensible claim:

> Literature grounding and high-level scientific steerability are distinct capabilities: models can incorporate evidence while remaining systematically constrained by their default research-policy distribution.

Use “research-policy distribution” only as descriptive language unless formally defined; do not claim a general belief-action gap.

## 10. Outcome branch C — significant but still KILL

Kill or substantially pivot even if p-values are small when any of the following describes the result:

### C1 lexical priming only

A few obvious category words explain the treatment and generated route.

### C2 relevance mismatch

A/B route packets differ materially in relevance/quality and the effect disappears after matching.

### C3 source identity only

Within-route paper swaps move outputs about as much as cross-route composition changes.

### C4 taxonomy dependence

The result is strong under one custom classifier but weak under local A/B human judgments or the external coarse contribution family.

### C5 no cross-model replication

Only one model family responds.

### C6 one-pair story

Only one hand-favorable route contrast works while the predeclared roster mostly fails.

### C7 no external validity

Controlled priming works but does not help predict behavior under held-out natural retrieval.

### C8 trivial full-context compliance

Outputs simply reproduce explicit source methods without meaningful recombination or higher-level route change.

## 11. Novelty statement after latest collision scan

The strongest pre-result novelty statement remains:

> **Unlike prior work on factual context conflicts, known target distributions, arbitrary creative stimuli, or scientific-idea quality/diversity, we study how equally relevant real scientific literature implicitly redistributes open-ended research choices and whether that causal leverage is modulated by an independently measured model prior.**

This novelty lives in the combined causal design, not in any one term.

## 12. Decision

**CONTINUE, source-only feasibility first.**

Do not authorize scientific generation until Codex Feasibility Task 1 passes review.

## 13. Next action

Parallel tracks:

1. Codex: source-only feasibility audit under the frozen task contract.
2. Research lead: continue direct-collision monitoring and refine human annotation / matching gates.
3. After feasibility output: review coverage and matching before deciding whether to freeze the authoritative preregistration for generation.
