# Round 9 — Independent ICLR Validation and Pre-Experiment Freeze

> Status: **CONDITIONAL GO — PROOF-OF-DESIGN AUTHORIZED, FULL CLAIM NOT YET AUTHORIZED**  
> Scope: ICLR-only scientific positioning.  
> Purpose: independently validate Rounds 5–8 against current literature, settle the paper identity, and specify the smallest experiment that can genuinely falsify the proposed contribution.  
> Important: this document is written before observing treatment outcomes. It must not be retrofitted to whichever result looks best.

---

## 0. Executive decision

The project has now moved through three distinct hypotheses:

```text
H0 (abandoned as main paper)
AI-assisted research may create idea monoculture

H1 (too generic to be novel)
retrieval/context acts as an inference-time prior

H2 (current ICLR question)
real scientific literature is an implicit control signal whose ability to redirect
open-ended scientific choices competes with an LLM's independently measured prior,
and this context response may differ sharply across levels of scientific abstraction
```

The current research should **not** claim that retrieval is a prior, that context competes with parametric knowledge, or that LLM scientific ideas are insufficiently diverse. All are already established or strongly adjacent to accepted/recent work.

The defensible ICLR object is narrower:

> **Given multiple scientifically valid ways to attack the same research problem, can equally relevant real literature implicitly shift an LLM's distribution over high-level scientific moves, methods, and problem framings; and is that response predictable from evidence composition and the model's independently measured no-context prior?**

This question survives the current direct-collision scan.

The most distinctive possible phenomenon remains:

> **Grounding without steering** — the model accurately uses retrieved papers and concepts, but high-level scientific choices remain disproportionately anchored to its default prior.

The opposite outcome is also scientifically valuable:

> **Calibrated scientific steerability** — matched evidence mixtures causally and predictably redistribute high-level scientific choices, including under held-out natural RAG.

The experiment must be outcome-symmetric. A null/trivial result must kill the paper rather than trigger post-hoc reframing.

---

# 1. Independent verification of the nearest ICLR boundary

## 1.1 Spectrum Tuning — ICLR 2026

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html

Spectrum Tuning explicitly defines **in-context steerability** as the ability to use context to override model priors and move toward a novel data-generating distribution. It studies conditional distributional coverage and finds that post-training can reduce this capability.

### Consequence for us

We cannot claim:

- first study of in-context steerability;
- first context-vs-prior competition study;
- first observation that post-training can reduce contextual flexibility.

### Gap left for us

Spectrum tasks have an explicit/constructible target distribution. Our scientific setting has:

- multiple valid scientific strategies;
- no single correct contextual answer;
- no normative target saying a 75% evidence mixture should produce exactly 75% outputs;
- real literature as an **implicit ecological steering signal**, not an explicit instruction to adopt a distribution.

This distinction is substantial only if the experiment measures a distribution over high-level scientific choices rather than generic text similarity.

---

## 1.2 Context-Parametric Inversion — ICLR 2025

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2025/hash/aa27ac7aca4e462da1439b43ceebc04c-Abstract-Conference.html

This work shows that instruction fine-tuning can eventually reduce context reliance when context conflicts with parametric knowledge.

### Consequence

A simple observation that a model resists retrieved context is not novel.

### Difference required

Our context does not state a false/counterfactual fact against a correct parametric fact. Instead, both evidence treatments must encode scientifically valid alternative research strategies. The dependent variable is therefore not factual correctness but a distribution over open-ended scientific choices.

---

## 1.3 Controllable Context Sensitivity — ICLR 2025

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2025/hash/c9d780d1e2d57d4b70e807608a72501b-Abstract-Conference.html

This paper identifies a low-dimensional mechanism associated with choosing context versus prior in factual conflicts.

### Consequence

We should use `context sensitivity`, `prior`, and `steerability` carefully as inherited concepts rather than branding them as ours.

### Gap

The paper does not study how implicit scientific evidence composition changes a multi-valid, open-ended methodology/search distribution.

---

## 1.4 Si et al. scientific ideation — ICLR 2025

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html

This is the most important accepted ICLR neighbor because it establishes scientific research ideation itself as a legitimate evaluation object. It finds strong per-idea novelty but substantial lack of generation diversity and weak self-evaluation.

Their RAG ablations also make the original project story unsafe: changing the number of retrieved papers has little effect on their near-duplicate metric compared with large model-backbone effects.

### Consequence

Do not test `RAG vs no RAG` or `more papers vs fewer papers` as the paper's main question.

### Required advance

Our primary contrast must manipulate **composition at fixed amount/relevance**, and the outcome must be structural scientific choice rather than only a near-duplicate text threshold.

A particularly strong result would be:

```text
Si-style coarse duplicate metric       ~ weak change
high-level scientific-mode distribution  strong change
```

This would expose a measurement blind spot rather than contradict Si et al.

---

## 1.5 Does Writing with LMs Reduce Content Diversity? — ICLR 2024

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2024/hash/02dec8877fb7c6aa9a79f81661baca7c-Abstract-Conference.html

This establishes an ICLR precedent for a controlled population-level homogenization phenomenon, but it also makes generic `LLMs cause homogenization` substantially less novel.

### Use for us

Paper-shape precedent only. The current project should not be sold as another content-diversity study.

---

## 1.6 BiasBusters — ICLR 2026

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/a79875cc0d046ce7ce65f03f3affaa9e-Abstract-Conference.html

BiasBusters uses functionally equivalent alternatives and controlled perturbations to reveal LLM selection bias.

### Use for us

This is an excellent **experimental-design archetype**. Our analog is not functionally equivalent tools but scientifically valid, relevance-matched evidence packets representing alternative scientific moves.

The paper reinforces the need for controlled alternatives rather than observational diversity metrics.

---

## 1.7 RAG context attribution/interference — ICLR 2026

Primary sources:

- Attributing Response to Context:
  https://proceedings.iclr.cc/paper_files/paper/2026/hash/ed67dff7cb96e7e86c4d91c0d5db49bb-Abstract-Conference.html
- Resisting Contextual Interference:
  https://proceedings.iclr.cc/paper_files/paper/2026/hash/4dbcd4ba82866fdefc7ea0d15e9a72f2-Abstract-Conference.html
- Frustratingly Simple Retrieval:
  https://proceedings.iclr.cc/paper_files/paper/2026/hash/114273bb8d7969c60ab2a97adad609e1-Abstract-Conference.html

These papers confirm that retrieved context selection, attribution, source diversity, and parametric/context competition are active ICLR topics.

### Consequence

Generic statements such as `retrieval changes behavior`, `models may ignore context`, `source diversity matters`, or `context can conflict with priors` are not enough.

Our contribution must be specific to **open-ended scientific choice distributions** and supported by causal/predictive evidence.

---

# 2. Current non-ICLR direct neighbors that constrain novelty

These papers may not define ICLR novelty alone, but they make weak formulations untenable.

## 2.1 Thinking Like a Scientist? (Carlon et al., 2026)

https://arxiv.org/abs/2606.26130

The study prompts multiple strong LLMs with 1,000 computer-science research questions and finds much narrower methodology inventories than paper-derived references; different LLMs also resemble one another strongly.

### Consequence

Do not claim first discovery of a narrow/shared scientific-method prior.

### Opportunity

Use this as evidence that an independently measurable prior is plausible, then ask the causal next question:

> can real literature override it?

---

## 2.2 Prompt language as a diversity lever (2026 preprint)

DOI: https://doi.org/10.31224/7520

The paper shows that changing query language changes retrieved papers and downstream scientific proposals in one mechanobiology system.

### Consequence

`different retrieval -> different proposals` is already too weak.

### Required distinction

We directly intervene on the evidence packet while holding generator prompt language fixed; match relevance/amount/covariates; use multiple ICLR domains/models; and measure high-level scientific move rather than lexical/content diversity alone.

---

## 2.3 MIR — ACL 2025

https://aclanthology.org/2025.acl-long.1390/

Methodology Inspiration Retrieval explicitly argues that the nature of retrieved literature matters and seeks inspiring methodology beyond semantic similarity.

### Consequence

Do not make `relevance is not inspiration` the main novelty claim unless downstream causal evidence is unusually strong.

---

## 2.4 ResearchBench — Findings ACL 2026

https://aclanthology.org/2026.findings-acl.644/

ResearchBench decomposes discovery into inspiration retrieval, hypothesis composition, and ranking.

### Consequence

Do not create another generic scientific-discovery benchmark.

### Possible use

External validation / dataset inspiration after the ICLR-only core is stable.

---

## 2.5 ProjectionBench (2026 preprint)

https://arxiv.org/abs/2605.30284

ProjectionBench progressively reveals information from focal scientific experiments and measures how hypotheses approach the focal paper's conclusions.

### Difference

Our amount of context is fixed while composition changes; alternatives are multiple valid research modes; there is no single focal-paper answer treated as the desired target.

---

## 2.6 SCI-IDEA / MoRI / CHIMERA and other ideation systems

Representative sources:

- SCI-IDEA: https://doi.org/10.1007/s10994-026-07036-8
- MoRI: https://aclanthology.org/2026.acl-long.1609/
- CHIMERA: https://aclanthology.org/2026.acl-long.85/

### Consequence

The algorithm/system space is highly crowded. We should not turn the project into another framework whose main contribution is better novelty/quality scores.

A mechanism/evaluation paper is strategically safer.

---

# 3. The exact research question to freeze

## Primary question

For frozen LLM `M`, research problem `x`, and evidence packet `C`, define the generated scientific choice representation `H`.

Study:

```text
P_M(H | x, C)
```

where `C` varies only in predeclared scientific framing composition while amount, relevance, temporal validity, and major covariates are controlled.

The confirmatory question is:

> **Does changing the framing composition of equally relevant real ICLR literature causally redistribute high-level scientific choices, and does the magnitude/asymmetry of that response depend on the model's independently measured no-context prior?**

## Secondary hierarchy question

> **Does evidence influence attenuate as the output variable moves from source/content uptake to method/research-mode/problem-framing choice?**

## External-validity question

> **Can a response model learned under controlled evidence mixtures predict model behavior under held-out natural top-k retrieval?**

These three questions are sufficient for an ICLR mechanism/evaluation paper. Do not add another main question unless the first three are answered cleanly.

---

# 4. What the paper is *not*

It is not:

- a paper about whether real human science is becoming monocultural;
- another RAG architecture;
- another scientific-agent framework;
- another idea-generation benchmark;
- another generic diversity metric;
- a claim that there is one optimal scientific method;
- a factual context-conflict benchmark;
- a paper whose conclusion relies only on LLM-as-judge novelty scores.

The population-monoculture motivation may appear in the introduction, but the empirical object is a frozen ML model under context intervention.

---

# 5. Confirmatory experiment architecture

## Stage A — Taxonomy audit before treatment outputs

Freeze a cross-ICLR Layer-A scientific-move taxonomy only after human/auditable annotation of real ICLR papers demonstrates acceptable separability.

Candidate modes from the current draft:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
VERIFY_FALSIFY_REPLICATE
```

Rules:

- primary label + optional secondary labels;
- merge sparse/unreliable categories only using a pre-treatment rule;
- do not look at treatment outcomes while changing taxonomy;
- Layer A is primary; low-level method inventory is secondary.

### Gate A

If independent annotators cannot reliably distinguish the major modes, the main experiment must stop or use a more defensible outcome representation. A taxonomy that exists only because an LLM parser can output labels is not sufficient.

---

## Stage B — ICLR-only temporally clean corpus

Use open models with documented cutoff dates for the causal core:

- Meta Llama 3.1: documented knowledge cutoff December 2023;
- Gemma 3: documented training-data knowledge cutoff August 2024.

Official model-card sources:

- https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md
- https://ai.google.dev/gemma/docs/core/model_card_3

Construct the primary evidence corpus from ICLR papers first publicly available after the latest core cutoff. A conservative candidate is post-2024-08-31 ICLR 2025 literature, but **each paper needs an individual first-public-date check**; conference year alone is not a contamination guarantee.

Use later ICLR questions as seed problems only after removing solution/method leakage and verifying temporal cleanliness.

### Gate B

A seed/evidence paper whose first-public date cannot be verified is excluded from the clean causal subset and may only enter a sensitivity analysis.

---

## Stage C — Treatment selection independent of model outcomes

Adopt Round 8's strongest design.

Before any no-context model generation:

1. retrieve large relevance pools for each seed;
2. annotate source-paper research modes;
3. impose a frozen relevance floor;
4. identify mode pairs with enough relevant evidence;
5. match packet covariates;
6. select treatment pair by a deterministic rule independent of model outputs;
7. write and hash `TREATMENT_MODE_SELECTION.md` / manifest.

No model prior is used to choose the treatment.

This removes the strongest winner's-curse/cherry-picking critique.

---

## Stage D — Matched evidence packets

For each eligible seed and chosen mode pair A/B, construct packets with identical `k` and approximately matched:

- dense relevance;
- reranker relevance;
- token length;
- year / first-public date;
- topical cluster;
- document style where feasible;
- evidence quality/status;
- ordering randomized independently.

Primary mixture:

```text
alpha(A) = 0.00, 0.25, 0.50, 0.75, 1.00
```

For `k=12`, a natural implementation is 0/3/6/9/12 papers of A, with B filling the remainder.

### Gate D

Do not run a treatment for a seed if the A/B relevance distributions fail the predeclared balance gate. Report the failure rate.

---

## Stage E — Independently estimate the no-context prior

Only after treatment packets are frozen, generate repeated no-context samples for each `model × seed` and estimate:

```text
P0_M,seed(mode)
```

Use this as a modifier/predictor, not a treatment selector.

Important quantities:

- prior probability of each treated mode;
- prior log-odds;
- prior entropy;
- prior difference A vs B.

This enables the main interaction:

```text
evidence composition × prior strength
```

---

## Stage F — Treatment generation

Give the **same frozen evidence packets** to both core model families.

Keep constant within model family:

- system/task prompt;
- decoding parameters;
- max output length;
- context formatting;
- packet size;
- seed question.

Save raw outputs. No result is discarded for being bad or unparsable.

The generator should propose one coherent research direction, not a list, to avoid within-sample portfolio confounding.

---

# 6. Primary and secondary outcome hierarchy

## Primary endpoint — L3 scientific move

This is likely the best compromise between scientific meaning and annotation reliability.

Measure the probability distribution over Layer-A research modes.

Main dose-response example:

```text
x = fraction of A-mode evidence
 y = P(generated proposal has primary move A)
```

## Secondary endpoint — Layer-B methodology

Ask whether concrete method family changes even when high-level move does not.

## Exploratory / higher-risk endpoint — L4 problem framing

Use the structured tuple:

```text
(problem object,
 failure/limitation,
 hypothesized mechanism,
 intervention family,
 evaluation target)
```

L4 must not be a primary claim unless human annotation reliability is strong.

## Context-uptake endpoints

Separate:

```text
L0 source attribution
L1 evidence/content uptake
L2 method-family uptake
L3 scientific-move uptake
L4 central problem framing
```

The paper must report the actual shape; do not force monotonicity.

---

# 7. Controls that are mandatory for a credible ICLR paper

## C1 — Mode-preserving packet swap

Swap paper identities within the same scientific mode and relevance stratum.

Purpose: distinguish scientific framing composition from document-identity effects.

## C2 — Evidence order randomization

Purpose: detect positional effects.

## C3 — Prompt paraphrase noise floor

Purpose: quantify ordinary prompt-induced variability and require treatment effects to exceed it.

## C4 — Lexical-priming audit

Check whether simple category words can trivially predict treatment packet identity.

For a stratified subset, create content-normalized evidence that preserves the scientific finding/limitation but removes titles, explicit mode labels, future-work imperatives, and obvious template wording.

If the entire L3 effect disappears after lexical normalization, the stronger scientific-steering story is weakened substantially.

## C5 — Exact-method copying

Measure overlap/near-copy between supplied methods and generated method proposal.

A high-level mode shift is much more interesting when exact-method copying is low.

## C6 — Temperature/sampling breadth

At selected conditions run low/standard/high sampling temperature.

Separate:

```text
within-context sample breadth
from
between-context directional shift
```

If temperature greatly broadens samples but does not erase evidence-conditioned direction, the phenomenon is not generic sampling mode collapse.

---

# 8. The most valuable external-validity experiment: controlled -> natural RAG prediction

This should be treated as a must-have for the full paper if the causal core works.

Procedure:

1. fit an evidence-response model on controlled A/B mixtures only;
2. freeze the model;
3. on held-out ICLR seed questions, run a natural top-k retriever from the same corpus;
4. annotate the natural packet's scientific-mode composition;
5. combine natural evidence composition with independently estimated no-context prior;
6. predict output mode allocation;
7. compare prediction with observed natural-RAG generations.

Compare at least:

```text
prior-only predictor
vs
prior + evidence-composition predictor
```

Why this matters:

Without this stage, reviewers can argue that the controlled mixture experiment is an artificial priming demonstration. Out-of-sample natural-RAG prediction converts the controlled intervention into a mechanism with ecological relevance.

---

# 9. Main statistical object

A simple confirmatory model for treated mode `j` can take the form:

```text
logit P(Y=j)
  = beta0
  + beta_evidence * evidence_fraction_j
  + beta_prior * prior_probability_j
  + beta_interaction * evidence_fraction_j * prior_probability_j
  + seed/model effects
  + predeclared nuisance/order terms
```

For the multi-class outcome, use an appropriate hierarchical multinomial/softmax formulation or predeclared binary contrasts per frozen treatment pair.

Primary uncertainty should reflect **seed-level generalization**, not only thousands of correlated generation samples.

Use seed-level bootstrap / hierarchical uncertainty.

Do not peek and stop when p-values become favorable.

---

# 10. Predeclared outcome branches

## Branch A — Strong steerability

Evidence needed:

- clear dose response at L3, not just L0/L1;
- effect survives relevance matching, mode-preserving swaps, order/prompt controls;
- lexical normalization preserves substantial effect;
- response varies systematically with independent prior;
- controlled response predicts held-out natural RAG better than prior-only.

Paper identity:

**Same Relevance, Different Science: Evidence Composition Steers LLM Hypothesis Search**

ICLR contribution:

Real scientific literature is a quantitatively useful implicit control signal over open-ended model search, and existing coarse diversity metrics can miss directional redistribution.

---

## Branch B — Grounded but prior-bound

Evidence needed:

- strong L0/L1 context uptake verifies the model is actually reading/using the packet;
- L3/L4 response is substantially weaker or thresholded;
- matched evidence reinforces high-prior choices more easily than equally strong low-prior choices, with treatment modes selected independently of prior;
- result replicates across seeds/models;
- natural RAG is predictable as a prior/context competition regime.

Paper identity:

**Grounded but Prior-Bound: Can Retrieval Steer LLM Scientific Hypothesis Search?**

This is currently the most distinctive branch because it distinguishes `retrieval grounding` from `scientific steerability`.

---

## Branch C — Kill / insufficient

Kill the main paper if any of the following dominates:

- only surface keywords/source names move;
- L3 scientific-move taxonomy is unreliable;
- matched relevance cannot be achieved for enough seeds;
- treatment effects are comparable to prompt/order noise;
- effect is one-model or one-subfield only with no interpretable reason;
- generated counter-mode ideas are systematically incoherent/irrelevant;
- results depend on one embedding metric or one LLM judge;
- no natural-RAG predictive value and no other deeper mechanism emerges;
- a new direct collision performs essentially the same matched, prior-independent scientific evidence intervention.

Do not rescue Branch C by inventing a new metric after outcomes.

---

# 11. What the first proof-of-design should answer

Before large-scale generation, the first implementation should test **design viability**, not paper significance.

Minimum proof-of-design questions:

1. Can real ICLR papers be annotated into Layer-A scientific moves with acceptable human agreement?
2. For enough seed questions, do at least two scientific modes contain relevance-matched evidence?
3. Can packets be matched without obvious lexical/covariate separation?
4. Are model outputs coherent enough that L3 can be annotated reliably?
5. Do no-context priors show non-degenerate variation across models/seeds?
6. Is treatment effect magnitude distinguishable from prompt/order noise on a small blinded sample?

If 1–5 fail, do not scale.

Question 6 is exploratory in the proof-of-design; it should not be used to tune the treatment to significance.

---

# 12. Strongest possible Figure 1

The paper should be designed around a figure that tells the result without relying on `idea diversity` rhetoric.

Preferred Branch-B version:

```text
             verified context uptake
1.0 |  source  █████████
    | concept  ████████
    | method   █████
    | move     ███
    | framing  ██
0.0 +-------------------------
          abstraction level

matched evidence amount is identical;
no-context prior shown as reference;
uncertainty by seed/model
```

Preferred Branch-A version:

```text
P(output mode A)
1.0 |                     ●
    |                ●
    |           ●
    |      ●
    | ●
0.0 +--------------------------
      0  .25  .50  .75  1.0
       fraction A-mode evidence

same relevance, same k, same prompt
```

The natural-RAG prediction figure should be the strongest validation figure, not an appendix afterthought.

---

# 13. Why this is ICLR rather than science-of-science

The causal unit is an ML model inference distribution.

We manipulate:

```text
scientific context C
```

and measure:

```text
P_M(H | x, C)
```

under a frozen model, matched input distributions, and controlled interventions.

The work speaks to general ICLR questions:

- context reliance;
- conditional generation;
- in-context steerability;
- post-training effects;
- retrieval augmentation;
- distributional behavior under many-valid-answer tasks;
- robustness of model decisions to external evidence.

Real-world scientific monoculture is only a motivation/possible implication and must not be causally claimed from the model experiment.

---

# 14. ICLR 2027 reviewer criterion mapping

Official guide:
https://iclr.cc/Conferences/2027/ReviewerGuidelines

The paper must have a clear answer to the guide's four core questions.

## Specific question

Can real, matched literature implicitly redirect open-ended scientific choices against a model's prior?

## Literature placement

Directly linked to accepted work on scientific ideation, context sensitivity, context-parametric competition, and in-context steerability.

## Claim support

Treatment selection independent of model outcomes; relevance matching; temporal cleanliness; dose response; negative controls; human audit; natural-RAG out-of-sample prediction.

## Significance / new knowledge

The strongest knowledge contribution is a newly characterized distinction between **being grounded in evidence** and **having high-level scientific search redirected by evidence**, or alternatively a quantitative demonstration that real evidence composition acts as an implicit control signal over open-ended scientific search.

This is more defensible under ICLR's stated emphasis on correctness + significance than a marginal improvement in ideation scores.

---

# 15. AI-use disclosure requirement

ICLR 2027 requires authors to disclose substantial LLM use in research and writing. The official policy explicitly lists hypothesis refinement, methodology/experiment design, implementation, result interpretation, literature analysis/topic discovery, and related tasks.

Official source:
https://iclr.cc/Conferences/2027/AIPolicyForAuthors

This project is intentionally using ChatGPT and Codex in many of those roles. Therefore:

- preserve an auditable record of AI contributions in the repository;
- do not conceal LLM use;
- maintain human verification of claims, citations, code, and statistical conclusions;
- prepare an accurate disclosure section when/if a manuscript is written.

This requirement is not a problem for the project, but it makes provenance discipline especially important.

---

# 16. Final Round-9 verdict

## Decision: CONDITIONAL GO

The current topic is sufficiently ICLR-shaped to justify a **proof-of-design and causal pilot**, but not yet a full-scale paper commitment.

The paper's identity is now:

> **scientific context steerability / prior competition under real, relevance-matched literature**

not:

> scientific monoculture

and not:

> retrieval is a hidden prior.

The strongest confirmatory design is the Round-8 selection-independent treatment plus Round-7 temporal/matching/negative-control discipline.

### What should happen next

Before running expensive treatment generation, freeze and validate:

```text
1. ICLR-only corpus + temporal manifest
2. Layer-A taxonomy + human reliability audit
3. eligible seed set
4. relevance/matching gate
5. treatment-mode selection algorithm
6. frozen evidence packets and hashes
7. annotation protocol
8. analysis specification
```

Only after these artifacts exist should no-context priors and treatment outcomes be generated.

### Most important anti-p-hacking rule

The scientific modes, evidence packets, eligibility rules, primary L3 endpoint, and main statistical contrast must be frozen **before model outcomes are observed**.

If the causal result is weak, the correct outcome is to learn that this paper shape does not work — not to reinterpret arbitrary output differences as a new discovery.

---

## 17. Direct-collision watch list

Continuously monitor only the closest lanes, rather than repeatedly broad-searching all AI-for-science work:

1. ICLR/NeurIPS/ICML work on in-context steerability / context-prior competition;
2. scientific ideation papers with explicit retrieval composition interventions;
3. scientific-method-prior studies;
4. inspiration/generative-root retrieval with downstream hypothesis-generation experiments;
5. benchmarks that introduce hierarchical scientific-choice/context-uptake measures.

A true direct collision is not a paper that says `retrieval changes ideas`. It is one that independently measures scientific priors and performs relevance-matched, fixed-amount, high-level evidence-composition interventions with comparable causal analysis.
