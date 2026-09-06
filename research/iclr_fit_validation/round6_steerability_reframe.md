# Round 6 — Can Retrieval Override Scientific Priors?

> Status: **PRIMARY ICLR RESEARCH FRAME**  
> Date: 2026-09-06  
> Scope: ICLR-only positioning and falsifiable experiment design.  
> Historical note: `experiments/idea_collapse/` keeps its original name for provenance; the scientific target has evolved.

---

## 0. Executive decision

The broad `AI-assisted topic monoculture` story should now be treated as **motivation, not the core ICLR claim**.

Two pieces of evidence materially change the best question:

1. **Si et al., ICLR 2025** already report that increasing the number of RAG papers from `k=0` to `5/10/20` barely changes their near-duplicate idea-diversity metric, while changing the LLM backbone changes diversity dramatically.
2. **Carlon et al., 2026** find that frontier LLMs given only research questions propose a much narrower methodology inventory than real papers, and different LLMs resemble one another more than they resemble the paper-derived reference inventory. Thus a shared **scientific-method prior** is already empirically plausible.

At the same time, **Spectrum Tuning, ICLR 2026** formalizes *in-context steerability* as the ability to use context to override a model prior and move toward a new output distribution.

These results yield a sharper ICLR question:

> **Can retrieved scientific literature actually override an LLM's default scientific-method / research-mode prior, or does retrieval mainly produce surface grounding while high-level hypothesis search remains prior-bound?**

This is a substantially stronger question than:

> “Does diversified retrieval produce diverse ideas?”

because it connects scientific ideation to a general ML property — distributional context reliance / in-context steerability — and admits symmetric, informative outcomes.

---

## 1. Proposed paper identity

### Working title — preferred if the prior-bound phenomenon appears

**Grounded but Prior-Bound: Can Retrieval Steer LLM Scientific Hypothesis Search?**

Alternatives:

- **Can Retrieval Override Scientific Priors? In-Context Steerability of LLM Research Ideation**
- **Grounded, Not Steered: Hierarchical Context Reliance in Scientific Hypothesis Generation**
- if evidence strongly steers the model instead: **Same Relevance, Different Science: Evidence Composition Steers LLM Hypothesis Search**

### One-sentence scientific object

We study the conditional distribution

```text
P_M(H | x, C)
```

where:

- `M` is a frozen language model;
- `x` is a scientific research question / problem statement;
- `C` is a controlled packet of retrieved scientific evidence;
- `H` is the generated research hypothesis / methodology, represented at several abstraction levels.

The main object is **not human scientists or the science ecosystem**. It is how an ML model changes its open-ended scientific-search distribution under controlled context interventions.

---

## 2. Why this is more ICLR-shaped than the monoculture framing

The ICLR connection is now direct:

### A. Context vs prior is already a core ICLR question

- *Context-Parametric Inversion* (ICLR 2025) shows that instruction tuning can reduce factual context reliance despite increasing general benchmark performance.
- *Controllable Context Sensitivity* (ICLR 2025) shows context-vs-prior reliance can be represented and controlled in a model subspace.
- *Spectrum Tuning* (ICLR 2026) explicitly distinguishes ordinary ICL from **in-context steerability**, where context must override prior behavior and induce a new output distribution.

Our contribution must therefore **not** be “models have priors” or “context can affect outputs.”

The missing object is:

> context-prior competition in **open-ended scientific hypothesis / methodology generation**, where many outputs are valid and the target is a distribution over research choices rather than one correct factual answer.

### B. Scientific ideation has a documented default-prior problem

Carlon et al. report a large contraction of methodological vocabulary under research-question-only prompting. That gives us a concrete prior to challenge experimentally.

### C. Retrieval-grounded scientific ideation is already crowded

Therefore we should not make a new agent, new generic RAG pipeline, or generic diversity algorithm the main contribution.

The paper should be a **behavioral mechanism / controlled evaluation paper**:

```text
prior measurement
   ↓
matched context intervention
   ↓
steerability / resistance curve
   ↓
hierarchical uptake analysis
   ↓
mechanistic prediction / simple diagnostic
```

---

## 3. Core phenomenon to test: Grounding Without Steering

### Hypothesis

A model may visibly use retrieved literature at low abstraction levels while remaining anchored to its parametric/default scientific prior at higher abstraction levels.

Define a hierarchy:

```text
L0 — source grounding
     cites/mentions supplied papers or specific entities

L1 — conceptual uptake
     adopts mechanisms, phenomena, constructs, or assumptions present in evidence

L2 — methodological uptake
     changes model/dataset/algorithm/experimental-method families

L3 — research-mode uptake
     changes the kind of scientific move it proposes:
     build/improve vs diagnose vs measure vs explain vs optimize, etc.

L4 — problem-framing uptake
     changes what it treats as the central scientific question / failure / causal target
```

The strongest prior-bound prediction is:

```text
context uptake(L0) > uptake(L1) > uptake(L2) > uptake(L3/L4)
```

or, more generally, that the model exhibits a **steerability gradient by abstraction level**.

This is not assumed to be true; it is the central falsifiable phenomenon.

### Why this would matter

RAG systems are often called “grounded” because generated text references supplied evidence. If high-level scientific choices remain dominated by the model's default prior, then source attribution / lexical grounding is an insufficient proxy for whether retrieval actually expands or redirects scientific search.

---

## 4. Alternative successful outcome: Strong Scientific Steerability

The paper remains viable if the opposite happens.

If carefully matched evidence mixtures produce strong, smooth, predictable shifts in high-level hypothesis modes, the central result becomes:

> scientific ideation is substantially steerable through evidence composition even when coarse duplicate metrics are almost unchanged.

Then the paper is about **where the model searches**, not merely how diverse the samples look.

This symmetry is important: the study is designed to learn whether models are context-steerable, not to manufacture a monoculture result.

---

## 5. Formalizing a scientific prior

For each model `M` and seed problem `x`, estimate a no-retrieval distribution over hypothesis categories:

```text
P0_M(H | x) = P_M(H | x, C=∅)
```

At minimum, estimate distributions over:

### 5.1 Research mode

A cross-ICLR taxonomy designed to be meaningful across subfields:

1. **Build / Improve** — propose a new model, module, training algorithm, architecture, system, or direct performance improvement.
2. **Diagnose / Stress-test** — find a failure mode, boundary condition, robustness problem, or hidden assumption violation.
3. **Measure / Evaluate** — improve or challenge evaluation, benchmark, metric, measurement protocol, or construct validity.
4. **Explain / Mechanism / Theory** — explain why a phenomenon occurs, derive mechanism/theory, characterize dynamics.
5. **Optimize / Efficiency** — compute/memory/sample/data efficiency, scaling, systems-aware reformulation.
6. **Replicate / Falsify / Null** — directly test a claimed effect, negative hypothesis, replication, or null result.

The sixth category may be sparse; sparsity itself is informative but it should be merged only by a pre-specified rule if annotation reliability is too low.

### 5.2 Methodological family

Subfield-specific, e.g. for LLM agents:

- memory/retrieval;
- planning/search;
- tool-use;
- post-training/RL;
- evaluation/benchmarking;
- mechanistic/interpretability;
- systems/efficiency.

These taxonomies must be defined from the **source corpus before reading generated outcomes**.

### 5.3 Problem / failure framing

Structured extraction:

```text
(problem object,
 assumed/observed failure,
 hypothesized mechanism,
 intervention family,
 evaluation target)
```

---

## 6. Core experimental idea: Prior-Congruent vs Counter-Prior Evidence

The most informative test is not generic `top-k vs MMR`.

For a seed problem `x`, first estimate the model's no-context scientific prior. Suppose the model strongly favors research mode `B` (e.g. Build/Improve) and rarely proposes `D` (e.g. Diagnose/Stress-test).

Create matched evidence packets that support both scientifically valid directions.

### Conditions

```text
C_prior     — evidence enriched for the model's default/favored mode
C_balanced  — balanced evidence across two or more modes
C_counter   — evidence enriched for a plausible but underrepresented counter-prior mode
C_none      — no retrieved evidence
```

All packets must be matched as closely as possible on:

- topical relevance to `x`;
- evidence count `k`;
- token length;
- year distribution;
- venue/quality tier;
- citation/popularity where available;
- source-document style;
- generator prompt and language;
- document order randomized across replicates.

### Key question

Does `C_counter` actually move high-level output modes away from `P0`, or does the model merely cite/mention the counter-prior evidence while still proposing the default methodology?

---

## 7. Stronger experiment: Framing-Mixture Dose–Response

A two-endpoint intervention is not enough. Build a continuous mixture.

Let `A` and `B` be two matched scientific framings for the same seed problem. For example:

- `A = Build / Improve`
- `B = Diagnose / Stress-test`

For fixed `k=12`, construct evidence packets with target mixture:

```text
α(A) = 0.00 / 0.25 / 0.50 / 0.75 / 1.00
```

Illustratively:

```text
0.00 -> 0 A + 12 B
0.25 -> 3 A +  9 B
0.50 -> 6 A +  6 B
0.75 -> 9 A +  3 B
1.00 ->12 A +  0 B
```

Every A paper should be paired/matched with a B paper from the same topical-relevance stratum as closely as feasible.

### Primary response curve

```text
α(A) → P(output research mode = A)
```

### Interpretation

- steep monotone response: high context steerability;
- weak/flat response near the model's no-context prior: prior-bound search;
- threshold/nonlinear response: evidence needs a critical mass before it redirects search;
- asymmetric response: prior-congruent evidence reinforces much more easily than counter-prior evidence overrides;
- model-dependent response: different post-training regimes create different scientific steerability.

The last three are especially interesting because they provide more than an obvious `same evidence → same output` result.

---

## 8. A useful quantitative model

For category `j`, seed problem `x`, model `m`, and evidence packet `c`, fit a hierarchical multinomial / logistic response model such as:

```text
logit P(H=j)
  = b_{m,x,j}
  + λ_{m,j} * q_j(c)
  + γ_{m,j} * prior_congruence(c)
  + interactions
```

where:

- `b_{m,x,j}` captures the model/problem prior;
- `q_j(c)` is the fraction/strength of evidence supporting mode `j`;
- `λ` captures evidence uptake / context susceptibility;
- `γ` measures whether prior-congruent evidence has asymmetric leverage.

Do not call `λ` a universal steerability score until model fit and category validity support that interpretation. Initially call it an **evidence-response coefficient**.

### Predictive requirement

A strong mechanism claim requires more than fitting the same data:

- learn response coefficients on training seed problems;
- predict output-mode shifts on held-out ICLR problems;
- report out-of-sample calibration / log likelihood / category prediction;
- test transfer across subfields and, if justified, across model families.

If the evidence-composition model predicts held-out behavior substantially better than a no-context-prior-only model, that strengthens the structured-prior story.

---

## 9. Hierarchical context-uptake measurement

Each generation should be evaluated at every abstraction level.

### L0 — Source grounding

- source IDs cited or clearly referenced;
- direct terminology/entity uptake;
- attributable statements.

### L1 — Conceptual uptake

- mechanisms/phenomena/assumptions appearing in evidence and adopted in generated rationale.

### L2 — Method uptake

- dataset family;
- model/algorithm family;
- experimental paradigm;
- evaluation type.

### L3 — Research-mode uptake

Use the universal mode taxonomy above.

### L4 — Problem-framing uptake

Blind annotators decide whether the central scientific problem/failure framing follows evidence packet A/B or neither.

### Candidate key figure

```text
context response
↑
| █████████  source/entity
| ███████    concept/mechanism
| ████       method
| ██         research mode
| █          problem framing
+--------------------------→ abstraction
```

Only use this visual if the data actually show a hierarchy.

---

## 10. Required controls

### 10.1 Prompt sensitivity noise floor

For each seed/context condition:

- paraphrase the task prompt several ways without changing semantics;
- randomize evidence order;
- vary harmless formatting.

The evidence-composition effect must exceed this nuisance variation.

### 10.2 Sampling breadth vs search direction

Use at least:

- standard temperature;
- higher temperature;
- one generation-diversity baseline if practical (STARS or a simpler established method).

Key distinction:

> generation-side diversity can broaden **within-context sampling**, while evidence composition changes **between-context search direction**.

If high temperature erases every apparent evidence effect, the mechanism is weak.

### 10.3 Model-family effects

Si et al. show backbone can dominate idea-diversity metrics. Therefore:

- never pool models before showing within-model effects;
- fit model × context interactions;
- require main effect in at least two model families for a broad claim.

### 10.4 Relevance matching

Use a pre-specified matching pipeline:

- candidate pool constrained by topic;
- dense/cross-encoder relevance;
- stratify into relevance bands;
- pair A/B evidence within band;
- check standardized mean differences for matching covariates.

If counter-prior packets are simply less relevant, the experiment is invalid.

### 10.5 Evidence quality matching

Where possible match:

- ICLR venue/year;
- acceptance type / review score if accessible and appropriate;
- citation/publication metadata only as secondary controls.

Do not hand-pick unusually weak papers to construct the counter-prior condition.

---

## 11. Corpus and seed design — ICLR only

The empirical universe should be ICLR papers, not arbitrary scientific domains, for the core paper.

### Proposed source corpus

ICLR 2023–2026 accepted papers and their public metadata/abstracts. Optional extended context corpus can include direct cited references only for a specific robustness analysis.

### Seed problems

Use 100–200 seed research questions spanning 4–6 ICLR-relevant areas, e.g.:

- LLM agents / tool use;
- retrieval / long context;
- post-training / optimization;
- interpretability / reasoning;
- model editing / continual knowledge;
- efficient training / inference.

The seed question should not reveal the actual method used by its source paper.

### Avoid circularity

If a seed is derived from an existing ICLR paper:

- strip title/method names/authors;
- use only the research question / problem statement;
- keep the source paper's actual methodology hidden from the generator;
- reserve the true paper methodology only as an optional descriptive reference, **not** as a normative gold answer.

Carlon et al. correctly note that real-paper methods are a reference inventory, not necessarily an optimal answer; preserve that distinction.

---

## 12. Scale if resources are not the constraint

A full paper-quality design could use:

```text
120 seed questions
× 4 model families
× 5 evidence-mixture levels
× 20 independent generations
= 48,000 generations
```

This is not a required starting point. The first scientifically meaningful pilot should be smaller but preserve the factorial structure.

A practical staged design:

### Pilot

```text
24 seed questions
× 3 subfields
(8 per subfield)
× 2 model families
× 5 α levels
× 10 generations
= 2,400 generations
```

### Full

Expand seeds/models/replicates only after annotation reliability and context matching are validated.

The exact scale should be chosen by statistical precision and cost, not by an arbitrary round number.

---

## 13. Statistical analysis plan

### Primary inferential unit

An independently sampled generation nested within:

```text
seed question × model × evidence packet
```

Do not treat the O(N²) pairwise similarity values as independent observations.

### Primary tests

1. mixed-effects / hierarchical multinomial regression of research mode on evidence mixture;
2. slope / dose-response uncertainty for `α → output_mode`;
3. context-vs-prior asymmetry interaction;
4. held-out predictive fit improvement versus prior-only baseline;
5. evidence condition mutual information with high-level output category;
6. hierarchical uptake differences across L0–L4.

### Robust uncertainty

- bootstrap over seed questions, not only generations;
- report confidence/credible intervals;
- report effect sizes and model heterogeneity;
- pre-specify main contrasts.

### Annotation reliability

Before scaling:

- manually annotate a stratified sample;
- measure inter-rater agreement;
- revise/merge ambiguous categories **before** inspecting treatment effects;
- freeze taxonomy version/hash.

An LLM may assist extraction at scale only after the schema is frozen and audited.

---

## 14. The decisive dissociation experiments

### Dissociation A — duplicate metric vs search distribution

Reproduce the logic of Si et al.:

```text
near-duplicate rate ≈ unchanged
```

while testing:

```text
research-mode / method distribution = shifted
```

If true, the paper identifies an evaluation blind spot.

### Dissociation B — grounding vs steering

Possible result:

```text
source/entity uptake       high
concept/mechanism uptake   high/moderate
method/research-mode shift low
```

This would be the strongest “Grounded but Prior-Bound” result.

### Dissociation C — diversity vs steerability

Possible result:

```text
high temperature / STARS:
within-context diversity ↑

but:
counter-prior context response remains weak
```

This shows generation diversity and scientific context steerability are distinct capabilities.

---

## 15. Reviewer attack matrix

### Attack 1 — “This is Spectrum Tuning on another domain.”

Required response:

Spectrum defines a general capability using tasks with known target distributions. Our scientific setting lacks a naturally specified target distribution and introduces a qualitatively different question: whether retrieved literature can redirect open-ended scientific problem/method search away from a model's empirically measured default prior. We additionally study hierarchy of evidence uptake and prior-congruence asymmetry.

If our paper merely computes a steerability score on scientific prompts, this attack wins. We need the prior/evidence causal intervention and high-level structural findings.

### Attack 2 — “Context-prior conflict is already known.”

Known mainly for factual or constrained answers. Our setting has many plausible outputs and no single factually correct target. The relevant outcome is redistribution of open-ended research choices.

### Attack 3 — “Carlon et al. already showed methodological narrowing.”

They deliberately use sparse RQ-only prompts to characterize initial defaults. We use this as a baseline and ask whether matched scientific literature can override the default; their paper does not conduct retrieval-context interventions.

### Attack 4 — “Prompt-language RAG already changes scientific proposals.”

It changes the retrieval query language, retrieval set, and generation language together in one domain. We directly manipulate matched evidence packets while generator language/prompt remain fixed, estimate a dose-response, and measure prior-vs-context competition.

### Attack 5 — “If I show the model papers about X, of course it talks about X.”

This is why the outcome cannot be keyword uptake. The core endpoints are high-level research mode/problem framing, prior-congruence asymmetry, matched relevance, and held-out prediction. The strongest result is a nontrivial hierarchy or nonlinear resistance curve, not mere topical copying.

### Attack 6 — “Your context mixture is artificial.”

Use actual ICLR papers; preserve realistic packet size/relevance; add a natural top-k retrieval condition and show where it lies on the controlled response curve.

### Attack 7 — “There is no normative target distribution.”

Agree. We do not claim the evidence mixture is the correct output distribution. The intervention estimates context response, not optimal calibration. Normative claims are limited unless supported by human/external evidence.

### Attack 8 — “This is only behavior, no mechanism.”

A behavioral ICLR paper can be strong if it reveals a robust, surprising mechanism-level regularity. Strengthen with held-out predictive modeling, prior-congruence asymmetry, base/instruct comparison, and optionally internal probes only if cleanly interpretable.

---

## 16. Optional mechanistic expansion: post-training and internal state

Do not start here.

If the behavioral phenomenon is robust, two deeper analyses become valuable.

### 16.1 Base vs instruction-tuned pair

Spectrum and Context-Parametric Inversion motivate:

> does post-training strengthen the model's default scientific prior or reduce counter-prior context uptake?

Use matched checkpoints if available.

Confound: base models may be worse at following the task format. Separate valid-output rate from steerability.

### 16.2 Activation/probe analysis

Only if open models show the phenomenon robustly:

- probe whether evidence framing can be decoded from intermediate states;
- compare evidence signal with final output mode;
- test whether evidence representation exists internally but is not expressed downstream.

A “represented but not acted on” effect would deepen grounding-without-steering, but it is not required for the first behavioral pilot.

---

## 17. MUSES / inspiration-retrieval extension

Keep separate from the core pilot.

MUSES and methodology-inspiration retrieval work suggest ordinary relevance may not identify the literature most useful for discovery.

If the core context-response phenomenon exists, ask a second question:

> Are author-endorsed intellectual roots more effective at steering high-level hypothesis search than relevance-matched non-root papers?

This is attractive but extremely vulnerable to training-data contamination. Require a separate temporal-leakage protocol before execution.

---

## 18. Paper-shaped outcome branches

### Outcome A — Strong steerability

**Title:** Same Relevance, Different Science

Main result:

> matched evidence composition causes strong and predictable shifts in scientific hypothesis modes, despite weak changes in coarse duplicate diversity.

Paper value:

- evidence composition matters more than RAG amount;
- scientific context is a powerful inference-time prior;
- common ideation-diversity metrics miss directional search-space effects.

### Outcome B — Grounded but prior-bound — potentially strongest

**Title:** Grounded but Prior-Bound

Main result:

> LLMs visibly ground on retrieved literature at the source/concept level but resist counter-prior evidence at the method/problem-framing level; the resistance is stronger in some post-trained models and is not fixed by ordinary sampling diversity.

Paper value:

- retrieval grounding does not imply scientific steerability;
- reveals hierarchical context reliance;
- connects scientific ideation failures to general post-training/context-prior behavior.

### Outcome C — Fully context-responsive with no hierarchy and no novel structure

If evidence effects are trivial, linear, and fully explained by keyword/topic copying, **kill or substantially pivot**. Do not write a paper around the obvious result.

### Outcome D — No context effect anywhere

Potentially interesting only if:

- evidence is strongly relevant and counter-prior;
- low-level grounding is verified;
- multiple models/topics show robust resistance;
- the result clearly exceeds Si's existing RAG-quantity null by demonstrating an abstraction-level failure.

Otherwise kill.

---

## 19. Hard gates before large-scale generation

Before any large run, require all of:

1. ICLR-only source corpus construction works and is frozen.
2. Universal research-mode taxonomy passes annotation reliability.
3. Evidence packets can be matched on relevance without obviously weakening counter-prior evidence.
4. At least several seed problems genuinely admit both prior-congruent and counter-prior scientific directions.
5. Treatment assignment and packet construction are outcome-blind.
6. Prompt/order nuisance design is pre-specified.
7. No new direct paper has already performed equivalent prior-congruent/counter-prior scientific-literature intervention.

---

## 20. Current verdict

### **GO TO CONTROLLED PILOT, but kill the old monoculture claim as the primary target.**

The best current ICLR question is:

> **Can retrieved literature override a language model's default scientific prior, and is context uptake weaker at higher levels of scientific abstraction?**

The strongest possible discovery is:

> **Grounding without steering:** a research agent can cite the right papers while continuing to search inside the same narrow methodological prior.

That question is less obvious, more directly tied to current ICLR work on context reliance and distributional steerability, and harder to collapse into “another scientific-agent framework.”

---

## 21. Key sources

ICLR primary sources:

- Si, Yang, Hashimoto, *Can LLMs Generate Novel Research Ideas?*, ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html
- Goyal et al., *Context-Parametric Inversion*, ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/aa27ac7aca4e462da1439b43ceebc04c-Abstract-Conference.html
- Sorensen et al., *Spectrum Tuning*, ICLR 2026: https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html
- Blankenstein et al., *BiasBusters*, ICLR 2026: https://proceedings.iclr.cc/paper_files/paper/2026/hash/a79875cc0d046ce7ce65f03f3affaa9e-Abstract-Conference.html
- Padmakumar & He, *Does Writing with Language Models Reduce Content Diversity?*, ICLR 2024: https://proceedings.iclr.cc/paper_files/paper/2024/hash/02dec8877fb7c6aa9a79f81661baca7c-Abstract-Conference.html

Direct recent neighbors:

- Carlon et al., *Thinking Like a Scientist? A Structural Study of LLM-Generated Research Methods*: https://arxiv.org/abs/2606.26130
- King, *Prompt language as a diversity lever*, DOI 10.31224/7520
- *On the Limits of LLM-as-Judge for Scientific Novelty Assessment*: https://arxiv.org/abs/2606.12071
- MUSES: https://arxiv.org/abs/2609.00313

The collision matrix in `related_work_matrix.md` should be updated continuously before each major experimental expansion.
