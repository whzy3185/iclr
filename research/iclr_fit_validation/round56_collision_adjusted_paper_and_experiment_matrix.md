# Research Round 56 — Collision-Adjusted Paper Architecture and Experiment Matrix

Date: 2026-09-08

## 1. Decision

KEEP the project, but narrow the main paper identity further.

The core paper is **not** about generic steerability, generic source effects, generic scientific ideation quality, or generic baseline-vs-context conflict. Recent/adjacent work already covers those broad objects.

The main scientific object is:

> For a human-certified open scientific question with at least two valid research routes, does randomized composition of source-anonymous, relevance-matched scientific evidence causally change the LLM's high-level research-route distribution?

Everything else is secondary structure.

## 2. Collision-adjusted novelty boundary

Do not claim:

- first shared-literature-context ideation benchmark (Ideation Arena already uses shared contexts);
- first falsifiable literature-to-proposal benchmark (Lit2Test already does this);
- first generic in-context steerability study (Spectrum Tuning);
- first relationship between model preference and steerability (CLASH reports preference-steerability correlation in value dilemmas);
- first finding that source/citation metadata changes LLM behavior (source-preference and search-augmented evaluation work already establishes source effects broadly);
- first use of external stimuli to alter scientific/algorithmic ideation (MetaMuse).

Candidate novelty claim:

> a controlled, source-anonymous scientific-evidence composition intervention over high-level research-route choices, with treatment routes certified independently of model outcomes and evaluated as a distribution rather than a quality score.

## 3. Minimum viable paper

A minimum viable main paper needs all of:

1. human-certified method-masked seeds;
2. two scientifically plausible, distinguishable, non-subsumed routes per block;
3. source-anonymous matched evidence slots;
4. randomized evidence composition with multiple packet realizations;
5. at least two auditable model families;
6. blind human route annotation;
7. seed-clustered uncertainty;
8. quality/invalid/copy guardrails;
9. effect survives at least one cue-reduced or identity-control condition.

If these hold, the paper can stand as a controlled-context behavior study even if natural-RAG prediction fails.

## 4. Strong paper upgrades

A strong paper requires the minimum viable core plus at least one replicated second-order regularity:

- controlled response predicts held-out natural-RAG route distributions;
- cross-route replacements have substantially larger directional effects than within-route replacements;
- cue-reduced evidence retains a meaningful fraction of the route effect;
- baseline information improves held-out prediction beyond a fixed nonlinear response model;
- a stable model-family/post-training regularity appears on held-out seeds.

Do not require all upgrades.

## 5. F0/F1 prerequisite

Do not launch scientific model generation until the source bank passes semantic and human validation.

F0 completion must add:

- semantic dense relevance;
- independent reranker or documented degraded status;
- earliest-public-date audit;
- explicit source-anonymization transform;
- matching frontier under observed covariates;
- seed/route audit packets.

F1 must certify:

- seed comprehensibility;
- method neutrality;
- multi-route openness;
- A relevance/plausibility;
- B relevance/plausibility;
- distinguishability;
- non-subsumption;
- equipoise;
- annotatability.

Rubric calibration occurs on a development sample, then freezes before certification of confirmatory candidates.

## 6. Seed-level partition

Before scientific generation, partition unique seeds into:

- D: development / engineering / annotation calibration;
- C: controlled confirmatory study;
- N: untouched natural-RAG validation.

All route pairs from one seed remain in the same partition.

No P0 effect magnitude may be used to move a seed from D to C.

## 7. Core treatment design

For each certified block `(seed, route A, route B)` create matched slots:

`slot_j = (A_j, B_j)`.

Match/control nuisance variables using source-only information:

- semantic relevance to seed;
- reranker relevance;
- length/token budget;
- first-public time;
- problem/topic compatibility.

Do not overmatch away the scientific-route content itself.

Core evidence presentation removes:

- title;
- author;
- venue label;
- URL;
- citation count;
- retrieval scores/ranks;
- source prestige markers.

Retain the actual abstract/scientific content in the ecological core condition.

For final `k` supporting quarters (prefer 4/8/12 if construct validity and source coverage permit), randomize composition:

`alpha in {0, .25, .50, .75, 1}`.

Use multiple balanced packet realizations from the same matched slot bank.

## 8. Generator output contract

One proposal per call.

Route-neutral output fields:

1. Scientific objective
2. Core research question or claim
3. Study design / technical approach
4. Key experiment or analysis
5. Evaluation and decision criteria
6. Expected scientific contribution

Do not request "a novel method", "a benchmark", or "a falsification study" in the main prompt.

## 9. Primary outcome

Blind human categorical annotation:

- A_LEANING
- B_LEANING
- MIXED
- NEITHER
- INVALID

Keep annotation failure / cannot-judge separate from INVALID where operationally possible.

Primary directional summary:

`D(alpha) = P(A_LEANING|alpha) - P(B_LEANING|alpha)`.

Primary causal contrast:

`Delta_route = D(1) - D(0)`.

Always report the full outcome distribution alongside `D`:

`[P(A), P(B), P(MIXED), P(NEITHER), P(INVALID)]`.

Also report route engagement:

`P(A or B)`.

Do not condition the primary analysis on post-treatment copy/quality variables.

## 10. Primary statistical unit and model

Scientific replication unit: unique seed.

Hierarchy:

`seed -> route block -> packet bank -> alpha -> generation`.

Primary uncertainty:

- seed-cluster bootstrap; or
- hierarchical multinomial/ordinal model with seed-level random effects.

Generations estimate conditional distributions; they are not independent scientific replications.

## 11. P0 development pilot

Use D only.

Compact design:

- two model families;
- alpha = 0, .5, 1;
- multiple packet realizations;
- modest generations per cell.

P0 estimates:

- invalid rate;
- annotation agreement;
- generation variance;
- packet-bank variance;
- prompt/order nuisance;
- copy rate;
- rough variance required for precision planning.

P0 must not select high-effect seeds, routes or models for C.

## 12. Confirmatory P1

Before P1 freeze:

- C seed IDs and route pairs;
- model checkpoints;
- final k;
- five alpha levels;
- packet banks/realization algorithm;
- prompt hashes;
- generation settings;
- annotation protocol;
- primary outcome/contrast;
- fixed-N or valid sequential design;
- SESOI/ROPE if used;
- N holdout hash.

Run the full five-level composition design once on C.

## 13. Baseline propensity — secondary response modeling only

Measure no-context baseline only after treatment construction is frozen.

Estimate baseline on independent batches.

Do not interpret probability-scale attenuation as special resistance.

Compare on held-out seeds:

- M0: seed baseline/intercept + common nonlinear evidence response;
- M1: M0 + baseline-by-evidence interaction or predeclared richer response term.

Only claim an additional baseline-dependent regularity if M1 improves held-out predictive fit/calibration beyond M0.

## 14. Core anti-triviality set

Keep this small and predeclared.

### R1. Cue-reduced evidence

Human-audited content representation removing explicit method identity/prescriptive wording while retaining problem/finding/scope information.

Question: is explicit method wording necessary for the high-level route effect?

### R2. Within-route vs cross-route replacement

Replace one matched document with:

- another document from the same route;
- its matched opposite-route document.

Question: does route-changing replacement move route choice more than paper identity changes?

### R3. Copy/quality guardrails

Measure direct-copy, invalidity and proposal-quality outcomes on the full randomized sample.

Do not delete copied outputs and recompute the primary causal effect as though treatment assignment were preserved.

## 15. Natural-RAG validation

Use N only after controlled model is frozen.

Run ordinary retrieval on each seed. Annotate natural packet route composition under the frozen route system.

Compare held-out predictors:

- global/null;
- baseline only;
- evidence composition only;
- baseline + evidence;
- baseline + evidence + interaction.

Primary validation metrics:

- held-out log loss;
- Brier score;
- calibration.

Natural-RAG failure narrows the claim; it does not invalidate a clean controlled causal effect.

## 16. Paper structure

### 1. Introduction

Problem: literature-grounded scientific assistants are increasingly used for open-ended research ideation, but it is unclear whether changing which relevant scientific evidence is presented changes the model's high-level research choice rather than merely its wording/source references.

Contributions: certified scientific-choice object; randomized matched literature intervention; distributional response measurement; robustness/prediction if supported.

### 2. Related Work

- scientific ideation and human evaluation;
- RAG/search-grounded scientific systems;
- in-context steerability/context-vs-prior;
- source/metadata preference effects;
- contribution/route taxonomies.

### 3. Experimental Object

- source universe;
- method-masked seeds;
- route certification;
- matched evidence slots;
- source anonymization;
- randomization.

### 4. Main Controlled Experiment

- models;
- prompt;
- five alpha conditions;
- blind human route outcomes;
- hierarchical inference.

### 5. What Explains the Response?

- baseline nonlinear null vs richer response;
- cue-reduced evidence;
- within-vs-cross replacement;
- copy/quality guardrails.

### 6. Does the Controlled Law Predict Natural RAG?

Held-out N only.

### 7. Limitations

- target population is human-certified multi-route ICLR-style problems;
- evidence route is bundled scientific content, not an isolated semantic primitive;
- LLM behavior does not establish human-science monoculture;
- source/corpus temporal cleanliness is model-dependent.

## 17. Main figures

Figure 1: matched-slot randomized intervention schematic.

Figure 2: stacked A/B/Mixed/Neither/Invalid distribution across alpha plus D(alpha).

Figure 3: seed-level treatment effects and model heterogeneity; nonlinear baseline model comparison if supported.

Figure 4: cue-reduced + within/cross replacement + copy/quality guardrails.

Figure 5: controlled-to-natural held-out prediction if successful.

## 18. Result branches

### Strong positive

Multiple models/seeds show coherent dose-response, full distribution remains valid, and at least one anti-triviality control survives.

Claim: scientific evidence composition causally shifts LLM research-route choice in the certified target population.

### Heterogeneous

Average modest, but predeclared model/route/seed structure replicates on held-out seeds.

Claim must emphasize heterogeneity rather than a universal effect.

### Cue/identity dominated

RAW effect large, cue-reduced/cross-vs-within evidence fails.

Downgrade: literature context affects outputs mainly through explicit method/document cues; do not call this high-level scientific redirection.

### Precise null

Adequately powered/precise C shows effects inside the predeclared practically trivial region while outcome measurement is reliable.

This can support a limits-of-literature-conditioning paper only if the null is genuinely precise and contrasts with clear lower-level evidence uptake.

### Construct failure

F1 cannot certify enough seeds/routes or annotation reliability remains poor.

KILL or redesign before model scaling.

## 19. Current operational priority

Do not add more high-upside extensions yet.

Priority order:

1. complete F0 semantic/date/source-anonymization pipeline;
2. execute F1 calibration and human certification;
3. freeze D/C/N split and D0 treatment bank;
4. authorize only then the small D pilot;
5. use P0 for variance/engineering, not effect-based selection.

## 20. Current assessment

F0 lexical recovery makes source sparsity less likely to be the existential bottleneck. The current existential risks are construct validity and semantic treatment validity.

Paper viability is therefore now conditional on whether the large provisional candidate space survives human/semantic certification at a useful scale.
