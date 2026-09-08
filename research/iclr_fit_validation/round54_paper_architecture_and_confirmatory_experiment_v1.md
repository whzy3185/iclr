# Research Round 54 — Paper Architecture and Confirmatory Experiment V1

Date: 2026-09-08
Status: PRE-OUTCOME DESIGN RESEARCH. No scientific proposal-generation result exists.

## 1. Executive decision

KEEP the project, but narrow the paper identity further.

The paper should not be sold as generic RAG steerability, generic source effects, generic prior-vs-context behavior, or generic scientific-ideation quality. Recent work already occupies each of those neighborhoods.

The safest paper-level object is:

> **For open-ended scientific problems with multiple human-certified valid research routes, how does randomized composition of source-anonymized, relevance-matched literature change the distribution of an LLM's high-level research choices?**

A second question is allowed only if it survives a strong null:

> Does independently measured no-context route propensity explain additional heterogeneity in evidence response beyond ordinary nonlinear response geometry?

A third, high-upside question is:

> Does a response law estimated under controlled packets improve prediction of the same model's choices under held-out natural retrieval?

F0 remains source-feasibility evidence only. It is not a paper result about LLM behavior.

---

## 2. Why the paper identity must be this narrow

### 2.1 Generic shared-context scientific ideation is occupied

Ideation Arena (arXiv 2608.29696) gives models and research agents a shared literature context and evaluates proposals with >6,000 double-blind comparisons from 105 active CS researchers. Therefore we cannot claim that using a common literature starting point for scientific ideation is new.

### 2.2 Literature-to-proposal/falsifiability benchmarking is occupied

Lit2Test / *What Proves You Wrong* (arXiv 2608.22948) builds 200 real-paper neighborhoods and evaluates falsifiable proposal contracts. Therefore falsifiability fields, literature neighborhoods, or proposal-stage evaluation are not our novelty.

### 2.3 External stimuli steering ideation is occupied

MetaMuse (ICLR 2026) shows that external stimuli can help algorithm ideation escape familiar designs. Therefore "external evidence can redirect ideation" is too generic.

### 2.4 Generic in-context steerability is occupied

Spectrum Tuning (ICLR 2026) explicitly studies in-context steerability as overriding an existing output distribution with context. Therefore do not present steerability itself as a new construct.

### 2.5 Baseline preference × steerability is not generically new

CLASH (ICLR 2026) reports that steerability toward a value is significantly correlated with models' value preferences. Therefore a baseline-dependent response pattern in our study would be a scientific-domain regularity, not the first demonstration that baseline preference relates to steerability.

### 2.6 Source identity itself is a known steering nuisance

*In Agents We Trust, but Who Do Agents Trust?* (ICLR 2026 / arXiv 2602.15456) finds systematic latent source preferences across news, research-paper selection, and product choice, with source framing sometimes outweighing content. This creates a direct nuisance for our experiment.

**Design consequence:** the causal core must remove source-identifying metadata shown to the generator:

- no title;
- no authors;
- no venue label;
- no citation count/popularity;
- no source URL;
- no explicit ranking score.

All core evidence is from the same conference year (ICLR 2025), further reducing venue/year prestige confounding. Exact scientific method names inside abstracts are content and remain in the ecological RAW condition; explicit method-cue reduction is a later robustness condition.

---

## 3. Working title and one-sentence thesis

### Safest pre-result title

**Same Question, Different Literature: Controlled Evidence Interventions for LLM Research-Route Choice**

Alternative:

**Scientific Evidence Composition and LLM Research Choices**

Do not use "steering", "prior-bound", "monoculture", or "source preference" in the title unless actual outcomes justify them.

### Thesis if the main effect is robust

> Holding the scientific question, evidence budget, venue/year, and source relevance approximately fixed, randomized changes in which scientifically valid literature routes are represented cause systematic changes in LLM research-choice distributions.

This is the minimum main-paper finding. Everything else must add explanatory value rather than replace it.

---

## 4. Contribution hierarchy

The paper should have at most four contributions.

### C1 — A human-certified scientific choice object

Construct ICLR seed-route blocks where:

- one masked scientific problem admits at least two source-supported routes;
- both routes are independently judged relevant and scientifically plausible;
- routes are distinguishable and not obviously hierarchical/subsumed;
- focal solution information is removed;
- all candidate/excluded blocks and attrition are preserved.

This is not claimed as a universal ontology of science. It defines the study's target population: **multi-route-support ICLR-style scientific problems**.

### C2 — A controlled literature-composition intervention

Within each certified block, form matched evidence slots:

`slot_j = (A_j, B_j)`

and randomize which member of each slot is shown while keeping packet size and the matching scaffold fixed.

The main treatment is scientific evidence composition, not source identity, document count, venue, or prompt wording.

### C3 — A distributional response characterization

Estimate how the full research-choice distribution changes with literature composition and test whether any apparent baseline dependence exceeds a fixed-response nonlinear null.

Do not claim a special prior-resistance mechanism merely from probability saturation or a zero-crossing threshold.

### C4 — Held-out natural-retrieval prediction, if it works

Fit the controlled response model without natural-RAG outcomes, freeze it, and ask whether natural packet composition improves prediction of route choices on a seed-level holdout.

If this fails, narrow the paper to controlled-context behavior rather than treating the entire controlled result as invalid.

---

## 5. Paper architecture for a 9-page ICLR main paper

### 1. Introduction (~1 page)

Motivation:

- scientific agents increasingly retrieve literature before proposing research;
- existing evaluations typically compare systems under a fixed/shared context or score proposal quality;
- that does not reveal whether the *composition of equally relevant scientific evidence* changes which scientific route a model chooses.

State the question, the randomized intervention, and the target population.

Contributions: C1–C4 above.

### 2. Related Work (~0.75 page)

Four compact clusters:

1. scientific ideation and research agents: Si et al., Ideation Arena, Lit2Test, MetaMuse;
2. context/steerability: Spectrum Tuning, Context-Parametric Inversion, Controllable Context Sensitivity;
3. evidence/source effects: latent source preferences, Expert Heads, RAG evidence reasoning;
4. scientific contribution/route taxonomies and evaluation reliability.

Do not turn related work into a survey.

### 3. Constructing Multi-Route Scientific Choice Blocks (~1.5 pages)

Include:

- ICLR 2025 evidence / ICLR 2026 seeds;
- temporal audit;
- method masking;
- seed-local routes;
- human relevance/plausibility/equipoise audit;
- matched evidence slots;
- source anonymity;
- attrition and target population.

This section is essential because Reviewer #2's strongest attack will be "your routes are arbitrary / one route is weaker".

### 4. Controlled Evidence-Composition Experiment (~1.25 pages)

Define:

- packet bank;
- randomization;
- alpha conditions;
- model families;
- neutral generator prompt;
- blinded human output labels;
- primary estimand;
- seed-level inference.

### 5. Main Results: Evidence-Conditioned Research Choice (~1.25 pages)

Lead with the full categorical route distribution, not only one scalar.

Then show:

- extreme-condition primary contrast;
- dose-response;
- model/route-pair heterogeneity;
- route engagement and invalid/quality guardrails.

### 6. What Explains the Response? (~1.25 pages)

Only include analyses justified by data:

- fixed-response nonlinear null vs baseline-dependent model;
- method-cue-reduced context;
- within-route vs cross-route replacement;
- direct-copy rate as a separate outcome.

Do not claim mechanistic interpretability without internal-model evidence.

### 7. Held-Out Natural Retrieval (~0.75 page)

Compare predictive models on untouched seeds:

- global/null;
- no-context baseline;
- evidence composition;
- baseline + evidence;
- baseline + evidence interaction if pre-specified.

### 8. Limitations / Discussion (~0.5 page)

Explicitly bound:

- ICLR-style multi-route support population;
- no claim about human scientists;
- route abstractions are study instruments;
- matched packets do not make scientific contents identical;
- temporal cleanliness is audited, not perfect proof of non-contamination.

---

## 6. Experimental population and data split

After F0 semantic matching and F1 human certification, freeze a **unique-seed-level** split before any scientific proposal generation.

Recommended structure, with exact proportions chosen after the certified-bank size is known:

### D — development / engineering set

Use only for:

- generator formatting;
- route-label rubric calibration;
- parser/error handling;
- P0 variance estimates;
- prompt/order nuisance estimates.

Once model outcomes are observed here, these seeds cannot become confirmatory seeds.

### C — controlled confirmatory set

Used for the primary randomized literature-composition experiment.

### N — natural-retrieval validation set

Never used to tune the controlled response law. Used only after that law is frozen.

All route pairs belonging to the same seed stay in the same split. Split should be stratified on subfield and route-pair type where feasible.

---

## 7. F1 human construct audit — required before generation

F1 should have a calibration phase and then a certification phase.

### 7.1 Calibration sample

Take a source-only stratified sample spanning:

- R1–R4;
- several subfields;
- high/mid/low semantic relevance;
- easy and borderline seed leakage cases;
- matching-caliper boundary cases.

Human reviewers refine the rubric *without model proposal outcomes*.

### 7.2 What reviewers judge

For each seed-route block:

- seed is understandable without focal solution;
- seed does not prescribe one route;
- A relevance to seed;
- B relevance to seed;
- A scientific plausibility;
- B scientific plausibility;
- A/B distinguishability;
- non-subsumption;
- composability;
- whether a reasonable proposal can lean A, lean B, combine them, or choose neither.

Use at least two independent reviewers with sufficient ML/subfield literacy; adjudicate material disagreements. Exact pass thresholds are frozen after source-only calibration and before proposal generation.

### 7.3 Route-pair handling

Do **not** require R1–R4 to have equal final sample size.

The confirmatory target population is certified blocks, not a balanced taxonomy benchmark.

Report route-pair-specific effects and weights transparently. If R4 remains sparse after human validation, it can be absent from the confirmatory core without being replaced by an outcome-selected contrast.

---

## 8. Confirmatory treatment construction

### 8.1 Packet size

Confirmatory `k` must be divisible by four if using exact quarter mixtures:

`k in {4, 8, 12}`.

`k=6` remains a source-feasibility diagnostic, not a five-level confirmatory packet size.

Choose the final k at D0 using only:

- semantic/source balance;
- human validity;
- context length;
- certified seed breadth;
- ability to obtain multiple packet realizations.

Do not use model treatment effects.

### 8.2 Matched slots

For block `b`:

`slot_j = (A_j, B_j)`

where both papers are relevant to the same seed and differ in source-defined research route.

Match/diagnose on pre-treatment nuisance covariates such as:

- semantic relevance to seed;
- reranker relevance;
- abstract length;
- public date;
- problem/topic compatibility.

Do not force full-abstract semantic similarity so strongly that it removes the scientific route difference itself.

### 8.3 Packet policy

Core composition levels:

`alpha = 0, .25, .50, .75, 1`.

For k=8:

`0A/8B, 2A/6B, 4A/4B, 6A/2B, 8A/0B`.

Middle conditions use balanced/complementary slot assignments so particular slot identities are not systematically associated with alpha.

Document order is randomized with a predeclared balanced schedule.

### 8.4 Multiple packet realizations

The main within-bank randomization controls paper identity well, but does not by itself show generality beyond one selected bank.

Therefore require a packet-bank replication subset where source availability permits:

- construct two non-overlapping or minimally overlapping matched slot banks for the same seed-route block;
- repeat the endpoint or compact alpha experiment;
- estimate packet-bank identity variance.

Do not require two fully disjoint banks for every block if it destroys population breadth.

### 8.5 Source anonymization

Generator sees only ordered anonymous evidence excerpts/cards. It never sees:

- paper title;
- authors;
- venue name;
- citation count;
- URL;
- retrieval rank/score.

Since the evidence universe is ICLR 2025, venue/year prestige is naturally held nearly fixed.

---

## 9. Generator and model design

### Core model families

Use at least two independent open families with auditable cutoffs, currently Llama 3.1 and Gemma 3.

Instruction-tuned models are the primary scientific core because the task requires following a proposal-generation instruction.

Base-vs-instruction-tuned comparisons remain a later extension, not required for the core claim.

### Prompt

One proposal per generation. No ranking/refinement loop.

Neutral output contract:

1. scientific objective;
2. core research question/claim;
3. study design / technical approach;
4. key experiment or analysis;
5. evaluation and decision criteria;
6. expected scientific contribution.

Do not say "propose a new method", "design a benchmark", or include route labels.

Sampling parameters are frozen after D/P0 for engineering stability, not chosen to maximize treatment effects.

---

## 10. Outcome measurement

### 10.1 Primary raw label

For each output, human annotators see:

- the masked seed;
- neutral descriptions of routes A and B;
- the generated proposal.

They do **not** see evidence packet, alpha, document identities, or model condition where practical.

Primary categories:

`A_LEANING`
`B_LEANING`
`MIXED`
`NEITHER`
`INVALID`

Technical/API failures are tracked outside this scientific label.

### 10.2 Preserve the full distribution

For block/model/alpha, estimate:

`p(alpha) = [p_A, p_B, p_MIXED, p_NEITHER, p_INVALID]`.

Do not reduce the paper to a single ordinal score.

### 10.3 Primary directional estimand

Define:

`D(alpha) = P(A_LEANING | alpha) - P(B_LEANING | alpha)`.

Primary extreme contrast:

`Delta_route = D(1) - D(0)`.

Interpretation:

- positive: changing an all-B packet into an all-A packet shifts output mass toward A relative to B;
- zero: no net directional shift, but MIXED/NEITHER/INVALID may still change;
- negative: response runs opposite the intended evidence composition.

All categories remain in the denominator.

### 10.4 Secondary outcomes

- route engagement: `P(A)+P(B)`;
- MIXED probability;
- NEITHER probability;
- INVALID probability;
- direct method-copy indicator;
- source/finding uptake indicators;
- scientific validity/quality guardrail on an independently sampled subset.

Do not delete direct-copy outputs and re-estimate the primary effect; copying is a post-treatment outcome.

---

## 11. Inference and replication unit

The scientific population unit is the **unique seed**, with route blocks nested within seeds and generations nested within packets/blocks.

### Primary transparent analysis

Compute block-level `Delta_route`, then estimate the population mean with seed-clustered uncertainty / seed bootstrap.

Report:

- per-seed effects;
- per-route-pair summaries;
- per-model summaries;
- pooled target-population estimate only with explicit weighting.

### Secondary hierarchical model

Use a multinomial hierarchical model to retain MIXED/NEITHER/INVALID and model:

- model family;
- alpha;
- route pair;
- subfield;
- seed random effects;
- block random effects where needed.

Do not count thousands of generations as thousands of independent scientific units.

---

## 12. Baseline route propensity: downgrade from novelty claim to explanatory test

Treatment banks are frozen first.

Then collect two independent no-context batches for each seed/model to estimate baseline route choice and reliability.

Baseline directional propensity may be represented on a latent/log-odds scale, with uncertainty propagated.

### Critical null model

Before claiming baseline-dependent resistance, fit a simple response model where evidence has a fixed latent-scale effect and baseline changes only the intercept.

This model can already produce apparent probability-scale saturation and different zero-crossing thresholds.

### Stronger model

Add a pre-specified baseline × evidence term or constrained nonlinear response only if it improves:

- held-out likelihood / proper scoring rule;
- replicated seed-level prediction;
- or another predeclared out-of-sample criterion.

A probability-scale interaction alone is insufficient.

Because CLASH already reports preference-steerability correlation in another domain, our contribution is not generic baseline-dependent steerability. It would be a scientific-evidence response regularity under this controlled research-choice object.

---

## 13. Core robustness set

Do not create a giant robustness checklist. The core set should target the strongest alternative explanations.

### R-A — source identity nuisance

Already addressed in the primary design by anonymizing title/author/venue/URL/score and using one conference year.

Optionally verify on a small subset that adding source labels can change behavior; treat this as a nuisance diagnostic, not a main contribution.

### R-B — method/lexical priming

For a predeclared subset, create human-verified method-cue-reduced evidence cards preserving problem/finding/scope as faithfully as possible.

Interpretation is limited:

- survival strengthens the case that explicit method wording is not necessary;
- attenuation does **not** prove the RAW effect is trivial, because normalization also removes scientific information.

### R-C — document identity vs route composition

Compare:

- within-route matched replacement;
- cross-route matched replacement.

If cross-route effects reliably exceed within-route identity effects, the route-level abstraction has explanatory value beyond particular document identity.

### R-D — copy behavior

Measure direct-copy probability as an outcome. Do not post-treatment-filter the primary analysis.

### R-E — prompt/order

Use fixed prompt paraphrase and evidence-order robustness on a limited predeclared subset.

---

## 14. Natural-RAG validation

Reserve N seeds before scientific generation.

### Controlled fitting

Fit the response law using only controlled C-set data, then freeze all parameters/features.

### Natural retrieval

For each N seed/model:

1. run the frozen ordinary retrieval pipeline;
2. annotate the resulting packet under the already-frozen route system;
3. compute route-composition features;
4. generate proposals using the same source-anonymous evidence presentation where possible;
5. obtain blinded route labels.

### Predictive comparison

Compare proper scoring metrics for:

- N0: global distribution;
- N1: no-context baseline only;
- N2: natural evidence composition only;
- N3: baseline + evidence composition;
- N4: baseline + evidence + interaction, only if the interaction was pre-specified before N outcomes.

Primary question:

> Does natural evidence composition improve prediction beyond baseline choice distribution on untouched seeds?

A positive result upgrades ecological relevance. A negative result narrows the paper to controlled interventions.

---

## 15. Planned experiment sequence

### Stage F0 completion — now

Finish:

- missing ICLR 2026 abstracts;
- semantic retrieval/reranking;
- first-public dates;
- source-route audit;
- semantic matched-slot frontier.

No proposal generation.

### Stage F1 — construct certification

Human calibration + certification of seeds/routes/equipoise.

At end of F1 freeze D/C/N seed split and D0 source/treatment rules.

### Stage P0 — development/variance pilot

Use D only.

Compact treatment:

`alpha = 0, .5, 1`

Two model families.

Goals:

- invalid/API failure rate;
- human route-label reliability on actual outputs;
- generation variance;
- packet-bank variance;
- prompt/order noise;
- estimate precision inputs.

P0 effect magnitude cannot be used to cherry-pick confirmatory seeds/routes/models.

### D1 — confirmatory freeze

Using F1 validity + P0 variance, freeze:

- confirmatory sample size / fixed-N or valid sequential method;
- final k;
- five alpha levels;
- model checkpoints;
- number of generations per packet;
- packet-bank replication subset;
- human labeling plan;
- primary estimand;
- SESOI/ROPE if used;
- hierarchical model specification;
- C/N split hashes.

### P1 — confirmatory controlled experiment

Run the frozen five-level randomized intervention on C.

### P2 — targeted explanatory robustness

Run only if P1 produces a nontrivial interpretable phenomenon.

Priorities:

1. method-cue-reduced evidence;
2. cross-route vs within-route replacements;
3. copy outcome;
4. limited prompt/order robustness.

### P3 — held-out natural RAG

Run frozen predictive validation on N.

---

## 16. Figure plan

### Figure 1 — The experimental object

One scientific question → two human-certified routes → pairwise matched anonymous evidence slots → randomized alpha packets → proposal route distribution.

This must make the causal design understandable in 20 seconds.

### Figure 2 — Main response

Stacked or faceted route distributions across alpha:

A / B / MIXED / NEITHER / INVALID.

Overlay or separately plot `D(alpha)` with seed-clustered uncertainty.

### Figure 3 — Heterogeneity without overclaiming mechanism

Show:

- per-seed `Delta_route`;
- model-family effects;
- route-pair effects;
- comparison of fixed-response nonlinear null vs baseline-dependent model.

### Figure 4 — Alternative explanations

Compact panel:

- RAW vs method-cue-reduced;
- within-route vs cross-route replacement;
- copy-rate response;
- quality/invalid guardrail.

### Figure 5 — Natural RAG, if successful

Held-out predictive log-loss/Brier improvement of N1/N2/N3/N4.

If natural RAG fails, move it to a smaller panel/table and keep the claim controlled.

### Table 1 — Data / construct validity

- official denominator;
- semantic candidate bank;
- human-certified seeds;
- route-pair distribution;
- subfields;
- attrition reasons;
- final k / packet banks.

### Table 2 — Primary estimates

Per model and route-pair:

- `Delta_route`;
- route engagement;
- invalid rate;
- seed count;
- CI.

---

## 17. Reviewer red-team and required answers

### Attack 1: "You just prime models with method words."

Answer with source anonymity, method-cue-reduced robustness, copy-as-outcome, and document replacement tests.

### Attack 2: "A and B are not equally valid scientific routes."

Answer with source-defined candidate frame, human relevance/plausibility/equipoise certification, and full attrition.

### Attack 3: "Your result is just generic context steerability."

Answer: the contribution is the scientific choice object + matched literature intervention + distributional response under multiple valid routes, not the existence of steerability.

### Attack 4: "Baseline interaction is just sigmoid saturation."

Answer with latent-scale fixed-response null and out-of-sample model comparison.

### Attack 5: "Models prefer famous sources, not scientific content."

Answer with same-venue/year evidence and removal of title/authors/venue/source metadata.

### Attack 6: "You cherry-picked questions that work."

Answer with official focal-paper denominator, source-only eligibility, denominator-preserving attrition, and seed-level freeze before outcomes.

### Attack 7: "Thousands of outputs inflate your sample size."

Answer with seed as scientific replication unit and seed-clustered/hierarchical inference.

### Attack 8: "LLM judges define your result."

Primary route labels should be human-anchored. Automated annotation, if used for scale, must be frozen and validated against blinded humans; it cannot rescue low human reliability.

### Attack 9: "The controlled packets are artificial."

Answer with held-out ordinary-retrieval prediction if positive; otherwise explicitly scope to controlled literature interventions.

---

## 18. Success ladder

### Level 0 — not enough

RAW evidence changes wording or direct method copying only.

### Level 1 — publishable candidate phenomenon

Source-anonymous, relevance-matched evidence composition produces a replicated nontrivial shift in human-labeled high-level route distributions across multiple seeds and both model families, with no validity collapse.

### Level 2 — strong paper

Level 1 + the effect survives at least one strong anti-priming/document-identity test and shows a stable response law across models/route pairs.

### Level 3 — very strong paper

Level 2 + controlled response features improve held-out natural-RAG prediction, or another predeclared explanatory law adds genuine out-of-sample predictive power beyond simple nonlinear response.

### Kill / major downgrade

- human-certified multi-route bank collapses after semantic/equipoise audit;
- route labels on outputs are unreliable;
- apparent effect is explained by output invalidity/quality collapse;
- only RAW explicit method cues work and document-identity controls erase the effect;
- effect is precisely inside a predeclared practically trivial region;
- only a tiny hand-picked subset or one model produces the phenomenon.

---

## 19. Latest collision implication

Targeted September 2026 review found no work in the checked sources that combines all of:

1. open-ended scientific problems with multiple valid research routes;
2. source-anonymous, relevance-matched real-literature composition interventions;
3. route-distribution outcomes rather than proposal quality alone;
4. source-only treatment selection before model outcomes;
5. seed-level held-out natural retrieval prediction.

This is **not** an exhaustive novelty proof. The novelty claim remains provisional until submission-time literature review.

Recent works materially constrain claim language:

- Ideation Arena: shared-context expert evaluation already exists;
- Lit2Test: real-neighborhood falsifiable ideation benchmark already exists;
- MetaMuse: external-stimulus scientific/algorithmic ideation already exists;
- Spectrum Tuning: generic in-context steerability already exists;
- CLASH: preference-steerability correlation already exists in value dilemmas;
- Latent Source Preferences: source attribution can steer information selection/generation.

Therefore the paper must win on **controlled scientific evidence composition + construct validity + causal/predictive regularity**, not on generic ideation or steering terminology.

---

## 20. Immediate next action

Do not launch model proposals yet.

1. Complete F0 semantic/date/source validation.
2. Run F1 human construct certification.
3. Freeze D/C/N split and source/treatment bank.
4. Only then authorize a small D-set P0.

**Current paper viability assessment: promising but conditional.**

The project now has a coherent ICLR paper shape; the next bottleneck is no longer paper architecture. It is whether the large lexical candidate space survives semantic and human construct validation strongly enough to support a seed-level confirmatory experiment.