# Round 10 — Parallel ICLR Research, Core Estimand Refinement, and Codex Trigger Criteria

> Status: **ACTIVE RESEARCH — CODEX HOLD**  
> Scope: ICLR-only.  
> Principle: continue literature/collision/design research in parallel; do not ask Codex to implement until the scientific object and treatment construction are frozen enough that engineering cannot silently redefine the study.

---

## 0. Executive decision

The topic remains a **conditional GO**, but the paper should no longer be framed around generic monoculture, generic retrieval bias, or a new diversity metric.

Current strongest question:

> **When several scientifically plausible research strategies exist, can equally relevant real scientific literature implicitly steer an LLM among those strategies, and how does that response interact with the model's independently measured no-context scientific prior?**

The current paper object is the model distribution

```text
P_M(H | x, C)
```

where `x` is a scientific problem statement, `C` is a controlled packet of real scientific literature, and `H` is an open-ended hypothesis/proposal.

The novelty does **not** come from saying context affects output or context competes with priors. Accepted ICLR work already establishes these broadly:

- Context-Parametric Inversion, ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/aa27ac7aca4e462da1439b43ceebc04c-Abstract-Conference.html
- Controllable Context Sensitivity, ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/c9d780d1e2d57d4b70e807608a72501b-Abstract-Conference.html
- Spectrum Tuning, ICLR 2026: https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html

The plausible novelty boundary is the **combination**:

1. real scientific literature as the context signal;
2. open-ended multiple-valid-answer scientific choices rather than factual conflict;
3. fixed context amount and matched topical relevance;
4. treatment choice frozen before observing model outcomes;
5. independent no-context prior measurement;
6. high-level research-strategy response, not just lexical/source uptake;
7. context × prior interaction;
8. held-out natural-RAG prediction.

---

## 1. New direct-collision check

The closest relevant ICLR / recent work covers components separately.

### Scientific ideation

**Si et al., ICLR 2025 — Can LLMs Generate Novel Research Ideas?**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html

Establishes scientific ideation as an ICLR-relevant model capability and identifies generation diversity/self-evaluation problems. It does not isolate matched evidence-composition × prior interactions.

### Scientific discovery from inspirations

**MOOSE-Chem, ICLR 2025**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/51fd9a7d1706023cb9f8210cc6ac357c-Abstract-Conference.html

Decomposes discovery into inspiration retrieval, hypothesis generation, and ranking. This makes inspiration-conditioned generation an accepted ICLR object, but its target is rediscovery rather than causal context-prior competition among multiple valid strategies.

### General in-context steerability

**Spectrum Tuning, ICLR 2026**

Defines in-context steerability as using context to override model priors and move toward a new distribution. Therefore we must reuse this framing rather than claim it as new. Our distinction is ecological implicit steering by scientific evidence where there is no instructed target distribution.

### Context vs internal knowledge

**Context-Parametric Inversion / Controllable Context Sensitivity, ICLR 2025; LUMINA, ICLR 2026**

These establish context-prior tension and external-context/internal-knowledge utilization, mostly in factual or answer-oriented settings. They do not establish high-level scientific-method/problem-framing response under multiple valid choices.

### Selection-bias causal design archetype

**BiasBusters, ICLR 2026**

https://proceedings.iclr.cc/paper_files/paper/2026/hash/a79875cc0d046ce7ce65f03f3affaa9e-Abstract-Conference.html

Important methodological precedent: use functionally equivalent alternatives and controlled perturbations to isolate choice bias. Our experiment should aspire to the same logic using scientifically valid, relevance-matched literature framings.

### Scientific diversity/search

**Towards Diverse Scientific Hypothesis Search with LLMs, 2026**

https://arxiv.org/abs/2606.10587

Already addresses diversity collapse in hypothesis search and proposes a search algorithm. This reinforces that our paper must not become another diversity-generation method.

### Scientific discovery benchmark decomposition

**ResearchBench, ACL Findings 2026**

https://aclanthology.org/2026.findings-acl.644/

Separates inspiration retrieval, hypothesis composition, and ranking across disciplines. Again, our novelty must be behavioral/causal rather than another discovery benchmark.

### Current verdict

No direct collision found in this pass that simultaneously satisfies most of:

```text
real scientific literature
+ multiple valid scientific strategies
+ fixed evidence amount
+ matched relevance
+ treatment selected independent of model output
+ independently measured no-context prior
+ high-level strategy/problem response
+ evidence × prior interaction
+ natural-RAG held-out prediction
```

This is not proof of nonexistence; collision scanning remains active.

---

## 2. Important refinement: make the core result less taxonomy-dependent

The six-mode taxonomy is useful for cross-seed aggregation, but it should **not be the single point of failure**.

A reviewer can reasonably object that `BUILD`, `DIAGNOSE`, `MEASURE`, etc. have ambiguous boundaries and that an LLM-based classifier could manufacture the result.

### Revised primary estimand

For each seed `s`, freeze two scientifically valid evidence directions `A_s` and `B_s` using source-literature annotation only.

Examples:

```text
A = BUILD/IMPROVE
B = DIAGNOSE/STRESS-TEST
```

or

```text
A = MEASURE/EVALUATE
B = EXPLAIN/MECHANISM
```

The pair is selected before observing no-context model generations.

Construct relevance-matched mixtures:

```text
alpha(A) = 0, .25, .50, .75, 1.0
```

Then generate open-ended proposals with a fixed prompt.

### Primary output question

Instead of requiring perfect global taxonomy classification, blind annotators answer a local contrast:

> Is this proposal substantively closer to scientific direction A, direction B, both/mixed, or neither?

This is easier to audit and more directly connected to the intervention.

### Cross-seed secondary analysis

Map A/B directions to the frozen global taxonomy only after the local contrast is defined, allowing hierarchical pooled analysis.

This creates two validity layers:

```text
primary: seed-local A/B directional response
secondary: global scientific-move taxonomy
```

If global taxonomy reliability is mediocre but local A/B agreement is strong, the causal paper can still survive.

---

## 3. Core confirmatory design vNext

### Stage T0 — source-only treatment freeze

Using ICLR literature and the seed question only:

1. create seed-specific relevant candidate pool;
2. annotate candidate papers' scientific direction;
3. identify at least two scientifically plausible directions with enough evidence;
4. match packets on relevance, token length, date/year, topic cluster and available quality covariates;
5. select A/B pair via deterministic source-only rule;
6. freeze packet construction and hash manifests.

**No model prior output may be used in this selection.**

### Stage P0 — independent no-context prior

After treatment freeze, estimate repeated no-context generations:

```text
P0_M(H | x)
```

Measure the model's relative tendency toward frozen A/B directions and other modes.

This prior is a moderator, not a treatment selector.

### Stage T1 — evidence mixture dose response

For the same seed and frozen A/B pool:

```text
0% A / 100% B
25% A / 75% B
50% A / 50% B
75% A / 25% B
100% A / 0% B
```

Keep fixed:

- number of documents;
- relevance distribution;
- approximate context tokens;
- generator prompt;
- decoding parameters;
- document formatting;
- corpus snapshot.

### Primary statistical object

For seed-local A/B outcome `Y`:

```text
logit P(Y=A)
 = beta0
 + beta_evidence * alpha(A)
 + beta_prior * P0(A)
 + beta_interaction * alpha(A) * P0(A)
 + model/seed effects
```

Interpretation:

- `beta_evidence`: literature composition has directional leverage;
- `beta_prior`: model has a default scientific preference;
- interaction: context leverage depends on prior strength.

### Stage T2 — within-mode packet-swap negative control

Replace documents while preserving A/B composition and relevance strata.

Required contrast:

```text
cross-direction composition change
>
within-direction document-identity change
```

Otherwise the effect may merely be arbitrary document sensitivity.

### Stage T3 — lexical/priming robustness

For a subset, use content-normalized evidence summaries that preserve scientific problem/finding/mechanism but remove titles, explicit future-work prescriptions, and obvious mode labels.

The goal is not to eliminate all lexical signal; it is to determine whether the high-level effect survives beyond trivial category-word copying.

### Stage T4 — natural-RAG out-of-sample prediction

Fit response parameters only on controlled mixtures.

Freeze them.

For held-out seed questions:

1. run ordinary top-k retrieval;
2. annotate retrieved evidence composition;
3. estimate no-context prior independently;
4. predict generated A/B/global-mode distribution;
5. compare against actual generations.

Required comparison:

```text
prior-only predictor
vs
prior + evidence-composition predictor
```

This is the best defense against “artificial priming experiment.”

---

## 4. Three scientifically meaningful outcomes

The experiment is intentionally symmetric.

### Outcome A — strong steerability

Evidence mixtures smoothly and predictably redirect high-level research strategy.

Potential paper identity:

**Same Relevance, Different Science: Evidence Composition Steers LLM Hypothesis Search**

### Outcome B — grounded but prior-bound

Evidence strongly changes source/concept uptake but has much weaker leverage over high-level scientific choice, especially against a strong no-context prior.

Potential identity:

**Grounded but Prior-Bound: Can Retrieval Steer LLM Scientific Hypothesis Search?**

This remains the most distinctive candidate outcome.

### Outcome C — trivial/document-level priming or null

Only lexical/source copying changes; local A/B human annotation does not show robust high-level shift/resistance structure; natural-RAG prediction fails.

Decision: **KILL / major pivot** rather than rescue with extra metrics.

---

## 5. ICLR paper-shape check

The current design matches several accepted ICLR archetypes without duplicating their claims.

### Controlled population behavior

*Does Writing with Language Models Reduce Content Diversity?*, ICLR 2024, uses controlled assistance conditions to identify a population-level homogenization effect and attributes it to model-contributed text.

https://proceedings.iclr.cc/paper_files/paper/2024/hash/02dec8877fb7c6aa9a79f81661baca7c-Abstract-Conference.html

Lesson: a diversity/socially motivated phenomenon can fit ICLR when the ML intervention and attribution are controlled.

### Surprising context-prior failure

*Context-Parametric Inversion*, ICLR 2025, succeeds because it identifies a counterintuitive phenomenon, eliminates simple explanations, and connects it to training dynamics.

Lesson: if we find prior-bound scientific steering, merely measuring it is not enough; we need asymmetry/hierarchy/predictive structure.

### Controlled bias isolation

*BiasBusters*, ICLR 2026, controls functionally equivalent alternatives and isolates metadata/pretraining drivers.

Lesson: our A/B evidence should be scientifically equivalent in validity/relevance but differ in direction.

### Predictive mechanism archetype

*Mixing Mechanisms*, ICLR 2026, goes beyond observation and builds a causal model predicting behavior.

https://proceedings.iclr.cc/paper_files/paper/2026/hash/2eeff35664016c7f0f8aa704f0d9a83e-Abstract-Conference.html

Lesson: held-out natural-RAG prediction is strategically important.

---

## 6. ICLR review criterion mapping

ICLR 2027 Reviewer Guide asks reviewers to determine whether the submission brings sufficient value/new knowledge, and specifically asks:

1. What specific question/problem is tackled?
2. Is the approach well motivated and placed in literature?
3. Do experiments/theory support the claims rigorously?
4. What is the significance / new knowledge? SOTA is not required.

Source: https://iclr.cc/Conferences/2027/ReviewerGuidelines

Current answer target:

### Specific question

Can real scientific literature implicitly override model scientific priors in open-ended hypothesis search?

### Literature placement

Between scientific ideation, context-prior competition, distributional steerability, and RAG evidence utilization.

### Rigorous support

Outcome-independent treatment freeze + relevance matching + dose response + negative controls + blind local A/B annotation + held-out natural-RAG prediction.

### New knowledge

Either a predictable scientific steering law, or a grounding/steering capability gap and prior-resistance structure.

---

## 7. Codex trigger policy

**Do not start Codex yet.**

Codex should be invoked only when all research-side conditions below are satisfied.

### Trigger 1 — core estimand frozen

Primary endpoint wording is fixed as seed-local A/B directional response, with global taxonomy secondary.

### Trigger 2 — treatment-selection algorithm frozen

A deterministic source-only rule exists for seed eligibility and A/B selection, independent of model outcomes.

### Trigger 3 — taxonomy/local-annotation feasibility validated conceptually

We have an annotation protocol where blinded humans can distinguish A/B/mixture/neither without needing hidden model-chain reasoning.

### Trigger 4 — corpus/temporal policy frozen

Exact ICLR years, first-public-date checks, seed/evidence exclusion rules, and model cutoff policy are specified.

### Trigger 5 — no unresolved preregistration contradiction

Amendments A–E and later design documents are reconciled into one current authoritative preregistration before generation.

### Trigger 6 — one more high-recall collision sweep passes

Search specifically for papers combining scientific literature intervention, model prior measurement, and high-level method/hypothesis steering.

Only after these six conditions hold should Codex receive an engineering task.

### First Codex task when triggered

Codex should **not generate hypotheses first**.

Its first task should be purely infrastructure/data:

```text
1. build temporally audited ICLR corpus manifest
2. build seed manifest
3. implement source-only candidate retrieval
4. implement evidence matching diagnostics
5. generate treatment-selection manifest + hashes
6. produce annotation packets for human pre-treatment audit
```

Generation begins only after those artifacts pass research review.

---

## 8. Current open research questions before Codex

1. Can A/B scientific directions be defined locally enough that annotation is reliable while still generalizing across ICLR subfields?
2. What exact deterministic rule should choose A/B pairs without selecting only unusually easy seeds?
3. How should "scientifically plausible/equally relevant" be operationalized beyond embedding relevance?
4. Which ICLR subfields produce enough same-question, different-scientific-move literature to construct matched packets?
5. Should base-vs-instruct remain secondary, or can it become a mechanistic extension only after the core effect is established?
6. What is the cleanest natural-RAG prediction target when top-k packets contain mixed/ambiguous modes?

These are research-design questions, not coding questions. They remain on the ChatGPT research side for now.

---

## 9. Current decision

**Continue research. Hold Codex.**

The topic is now sufficiently ICLR-shaped to justify deeper design work, but the greatest marginal value still comes from reducing construct ambiguity and treatment-selection bias rather than generating data.

The next research milestone is a single authoritative `EXPERIMENT_FREEZE_V1.md` that reconciles Round 6–10 + Amendments A–E. Codex should only be activated after that freeze document is defensible.