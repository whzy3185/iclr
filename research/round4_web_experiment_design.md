# Round 4 Web Research — Retrieval-Induced Scientific Idea Convergence

> Date: 2026-09-06  
> Role: web-side research lane running in parallel with Codex implementation  
> Status: **research design / no scientific results yet**

## Executive update

The web collision scan changes the strongest version of the P0 claim.

The broad claim **“LLMs generate homogeneous scientific ideas” is already crowded**. Recent work has documented scientific-idea diversity collapse, quality–diversity search, novelty-judge failures, and macro-level narrowing of science. We therefore should not submit a paper whose main claim is merely that LLM-assisted research becomes homogeneous.

The strongest remaining question is narrower and more causal:

> **Does the composition of retrieved literature act as a research prior that causally controls where LLM scientific ideation searches, and do relevance-optimized retrieval systems systematically concentrate or omit evidence that would support less conventional but still scientifically grounded directions?**

This creates a sharper paper story:

```text
relevance retrieval objective
        ↓
concentrated / familiar evidence exposure
        ↓
concentrated problem framing
        ↓
portfolio-level idea collision
```

A second, more ambitious mechanism is suggested by MUSES (2026-08-31): standard retrieval is much worse at retrieving author-endorsed *generative intellectual roots* than familiar future citations. This motivates a prospective downstream test:

```text
relevance ≠ discovery utility
```

The recommended research program is therefore:

1. keep the current top-k/MMR pilot as an engineering baseline;
2. add a **controlled-overlap dose–response experiment** that directly manipulates exposure overlap while matching relevance;
3. if the effect exists, use **MUSES/CiteRoots author-endorsed roots** for a stronger downstream causal experiment;
4. only then study LLM-judge selection pressure.

---

## 1. 2025–2026 collision map

### A. Scientific ideation diversity is already established

**Si et al., ICLR 2025 — _Can LLMs Generate Novel Research Ideas?_**  
Large-scale expert study; LLM ideas were judged more novel than expert ideas but slightly weaker in feasibility, while the authors explicitly identify self-evaluation failure and lack of generation diversity as open problems.

- https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html

**Deng et al., 2026 — _Examining and Addressing Barriers to Diversity in LLM-Generated Ideas_**  
Identifies fixation and lack of human-like knowledge partitioning as two mechanisms; shows CoT and ordinary personas can improve diversity.

- https://arxiv.org/abs/2602.20408

**Bao et al., 2026 — _Contemporary AI lacks the imagination to diverge or negate in science_**  
Large scientist-in-the-loop study: 6,749 scientists, 25,139 rating sets. Reports a narrow “hivemind” for non-reasoning models, broader hypothesis space for reasoning models, absence of spontaneous null hypotheses, weak agreement of automated evaluators with scientists, and only marginal gains from retrieval augmentation/persona prompting.

- https://arxiv.org/abs/2606.08251

**IDEAgent, 2026** treats scientific ideation explicitly as Quality–Diversity search and reports strong gains over baselines using lineage memory, explicit diversity comparison, repair, and refinement.

- https://arxiv.org/abs/2607.22375
- https://github.com/declare-lab/IDEAgent

**Heuresis, 2026** evaluates multiple autonomous research search strategies across quality, diversity and novelty; reports that fully original ideas remain rare and QD/search strategies do not expand the quality–novelty frontier.

- https://arxiv.org/abs/2606.25198

**Implication:** “LLMs lack diversity” or “quality-diversity search helps” cannot be our main novelty.

### B. Scientific novelty judging is already known to be unreliable

**RQ-Bench / Sinhahajari et al., 2026 — _On the Limits of LLM-as-Judge for Scientific Novelty Assessment_** reports a “novelty mirage”: LLM judges favor model-generated RQs while experts prefer author-anchored RQs; generated questions can be narrow/source-bound in ways judges miss.

- https://arxiv.org/abs/2606.12071

Generic LLM-as-judge bias (position, self-preference, prompt sensitivity) is also heavily documented in 2025–2026.

**Implication:** judge-induced portfolio narrowing can be an RQ/ablation, but not the headline by itself.

### C. Retrieval for scientific ideation is active, but mostly optimized as a quality tool

**Graph2Idea, 2026** structures retrieved literature into a graph and reports automated gains in novelty, quality and feasibility.

- https://arxiv.org/abs/2606.09105

**AI Scientist / Nature 2026** tightly integrates ideation with Semantic Scholar / web literature search and filters ideas that are judged too similar to existing work.

- https://www.nature.com/articles/s41586-026-10265-5

These systems treat retrieval primarily as grounding/novelty checking, not as a population-level causal variable controlling the distribution of research questions.

### D. MUSES creates a new opportunity: relevance may miss *generative roots*

**MUSES: A Benchmark for Prospective Intellectual-Roots Retrieval (2026-08-31)** evaluates retrieval against future citations and, crucially, author-endorsed generative inspirations.

Headline evidence from the paper/datasheet:

- fixed candidate pool: 2,330,779 papers;
- 1,038,780 MUSES instances;
- 1,518 author-attested `(focal paper, generative root)` pairs;
- 402 endorsement pairs are retrieval-evaluable in the released pool;
- best Hit@100 falls from 0.534 on CiteNext to 0.171 on author-endorsed roots;
- the authors frame conventional retrieval as favoring relevant/popular/familiar papers over less familiar works that later prove generative.

Sources:

- https://arxiv.org/abs/2609.00313
- https://huggingface.co/datasets/anon-muses-neurips/muses/blob/main/DATASHEET.md

This is especially valuable because the dataset provides **prospective/time-safe structure and author-endorsed labels**, reducing dependence on subjective LLM novelty judges.

### E. Macro-level relevance of the individual-vs-collective paradox

**Hao et al., Nature 2026 — _Artificial intelligence tools expand scientists’ impact but contract science’s focus_** analyzes 41.3M papers and reports that AI-augmented scientists individually publish/cite more while collective topic breadth contracts.

- https://doi.org/10.1038/s41586-025-09922-y

This is strong motivation, not a causal proof for our LLM retrieval mechanism.

---

## 2. Updated paper hypothesis

Avoid:

> LLMs make scientific ideas homogeneous.

Prefer:

> **Literature retrieval is not a neutral context provider. Under matched relevance and fixed generation conditions, changing shared evidence exposure causally shifts the distribution of research questions generated by LLMs. Standard relevance-oriented retrieval can act as a population-level research prior.**

Stronger follow-up if MUSES succeeds:

> **Retrieval optimized for relevance can underperform retrieval containing author-endorsed generative roots on downstream discovery utility, revealing an objective mismatch between relevance and scientific ideation.**

Candidate titles:

1. **Relevant but Redundant: How Literature Retrieval Shapes Scientific Idea Search**
2. **When Retrieval Becomes a Research Prior: Causal Evidence from LLM Scientific Ideation**
3. **Relevance Is Not Discovery Utility: Rethinking Literature Retrieval for AI-Assisted Science**
4. **Shared Evidence, Shared Ideas: Retrieval-Induced Convergence in Scientific Ideation**

Do not lock a title before experimental evidence.

---

# 3. Experiment hierarchy

## E0 — Existing preregistered baseline

Purpose: engineering sanity + first evidence.

Conditions already specified:

- no retrieval;
- top-k relevance;
- MMR/diversified retrieval.

Keep this as the first experiment because it is cheap and operationally useful.

However, **top-k vs MMR alone is not sufficient for the final causal claim**. The two source sets can differ in mean relevance, topic breadth, citation count, year distribution, and source quality. Reviewers can attribute any idea-diversity effect to those differences rather than exposure overlap itself.

---

## E1 — Controlled Exposure-Overlap Dose–Response (**recommended core experiment**)

### Research question

Holding retrieval quality approximately fixed, does independently manipulating the fraction of shared literature causally control downstream research-idea convergence?

### Why this is stronger than `top-k vs MMR`

It intervenes directly on the hypothesized mediator — **shared evidence exposure** — instead of comparing two retrieval algorithms with many simultaneous differences.

### Construction

For each domain/topic/query:

1. retrieve a relevance band, e.g. top `L=60` candidates;
2. stratify candidates by relevance-score bins, year and optionally citation/popularity bucket;
3. construct paper sets of fixed size `k=12`;
4. vary pair/group exposure overlap while keeping the marginal relevance distribution matched.

Required overlap levels:

```text
0%, 25%, 50%, 75%, 100%
```

For `k=12`, a practical discrete implementation is:

```text
shared papers = 0, 3, 6, 9, 12
unique papers fill the remainder
```

Unique replacements must come from the **same relevance strata** as the shared paper they replace.

### Unit of randomization

Use an `exposure_group` containing multiple independent generations. Do not define overlap only pairwise after generation.

Example:

```text
one topic
one model
one frozen base prompt
one relevance-band pool
5 overlap treatments
20 exposure groups / treatment
4 generations / group
```

This gives hierarchical data and allows group-level portfolio outcomes.

### Primary hypotheses

**H1a:** source-set overlap increases monotonically with assigned overlap treatment (manipulation check).

**H1b:** problem–method collision increases with assigned exposure overlap.

**H1c:** portfolio diversity growth decreases with assigned exposure overlap.

**H1d:** the dose–response persists after controlling for realized mean relevance, publication year and source popularity.

### Primary outcomes

Do not use a single embedding measure.

1. structured tuple collision:
   `(problem object, assumption/failure, method/intervention, evaluation target)`;
2. semantic pairwise distance of RQ + method;
3. cluster entropy / effective number of idea clusters;
4. diversity growth curve as N increases.

### Statistical model

Primary analysis should be hierarchical / clustered by topic and exposure group.

At minimum report:

- treatment-wise bootstrap confidence intervals;
- monotonic trend test or mixed-effects slope;
- effect replicated across model families and domains;
- sensitivity to tuple parser / embedding model.

### Decisive figure

```text
x-axis: assigned source-overlap dose
0   .25   .50   .75   1.0

y-axis 1: realized source overlap
y-axis 2: idea collision / effective cluster count
```

A clean monotonic curve is substantially more publishable than a binary MMR comparison.

### Kill criterion

Kill the retrieval-causality story if exposure overlap can be strongly manipulated but problem/method-level idea diversity does not move consistently across at least two model families and multiple domains.

---

## E2 — MUSES Generative-Root Injection (**highest scientific upside**)

### Research question

Does injecting a literature item that authors themselves later identify as a generative intellectual root change LLM scientific ideation more usefully than injecting a merely relevant matched paper?

### Dataset

Use the MUSES / CiteRoots-Endorsement retrieval-evaluable subset (402 pairs) where feasible.

The MUSES dataset is explicitly time-safe and author-disjoint, and releases structured root labels while requiring the user to join S2ORC for text/metadata.

### Experimental unit

For each eligible focal instance at time `t`:

- build context only from information available before the focal future paper;
- never expose the focal paper title/abstract/contribution to the generator;
- select an author-endorsed generative root `r+`;
- select a matched non-root `r-` with similar topic relevance, year, popularity and text length.

### Paired conditions

```text
A: base literature context + matched non-root r-
B: identical base context + endorsed generative root r+
C: base context only
```

Optional stronger control:

```text
D: base + random relevant paper from same relevance bin
```

### Outcome: prospective discovery utility

The main outcome should not be “LLM judge says novel.”

Use the held-out focal paper as an objective historical anchor.

Extract structured tuples from:

- generated idea;
- held-out focal paper.

Measure whether root injection improves recovery of the future paper’s:

- research problem;
- mechanism / gap;
- method family;
- key experiment;
- combination of problem × method.

This is not claiming the focal paper was the only good future idea. It is testing whether **author-endorsed roots have measurable downstream generative utility** compared with equally relevant non-roots.

### Secondary outcomes

- portfolio diversity across multiple generations;
- distance from already-existing literature at time `t`;
- feasibility/soundness via cross-family judge + human audit subset;
- proportion of ideas that recombine conventional anchors with a less familiar root.

### Key causal contrast

```text
Δ discovery utility = outcome(root injection) - outcome(matched relevance injection)
```

Because this is paired within focal instances, power can be substantially better than an unpaired study.

### Strong result

A particularly strong paper would show:

1. standard relevance retrieval rarely surfaces author-endorsed roots (replicate MUSES finding);
2. when such roots are experimentally inserted, downstream scientific ideas systematically change;
3. the change improves recovery of real future research directions and/or portfolio breadth;
4. simple diversity-aware retrieval is not equivalent to generative-root retrieval.

This would support the stronger claim:

> relevance and discovery utility are different retrieval objectives.

### Main risk

Reviewer: “Of course giving the model the paper that inspired the future work makes it closer to the future work.”

Mitigation:

- match root and non-root on semantic relevance;
- compare multiple root functional categories;
- remove direct lexical leakage where appropriate;
- analyze cases where root is semantically distant but mechanistically generative;
- evaluate whether the effect exceeds title/keyword copying and changes structured problem–method composition;
- include negative controls.

---

## E3 — Selection Bottleneck / Judge-Induced Convergence

Do this only after E1/E2 show a meaningful generation-stage effect.

### Research question

Given the **same candidate idea pool**, does LLM-based selection systematically reduce portfolio diversity or favor conventional/source-bound candidates?

### Fixed candidate pool

Generate a large candidate set once, then freeze it. This is essential: selection must not be confounded with generation.

### Conditions

1. random top-m selection;
2. same-family LLM judge;
3. cross-family LLM judge;
4. judge with explicit quality-only rubric;
5. judge with explicit quality + portfolio diversity rubric;
6. human expert subset if available.

### Outcomes

Before vs after selection:

- effective number of clusters;
- problem–method collision;
- source-neighborhood concentration;
- distance to existing literature;
- quality/soundness;
- rank agreement with human subset.

### Hypothesis

A plausible but unproven pattern is:

```text
individual judged quality ↑
portfolio diversity ↓
```

Do not assume it; test it.

### Important controls

- randomize candidate order;
- mask generator identity/model family;
- test self-preference by same-family vs cross-family judges;
- repeat judge calls to measure stability;
- use at least one human-calibrated subset because RQ-Bench and Bao et al. show weak novelty-judge validity.

---

## E4 — Research-Mode Taxonomy: Extension vs Falsification

Optional analysis inspired by Bao et al., not a main experiment.

Classify ideas into research modes:

```text
incremental extension
combination / transfer
measurement / evaluation
mechanism explanation
boundary / stress test
null / falsification
replication / robustness
```

Question:

> Does concentrated relevance exposure not only reduce semantic diversity, but also disproportionately collapse *research modes* toward incremental extensions?

This would make “idea diversity” scientifically richer than surface semantic spread.

Use a manually audited taxonomy. Do not make this a primary endpoint unless annotation reliability is high.

---

# 4. Required pre-run control: matched relevance

Before scientific generation, the pilot should record and compare for every retrieval condition:

- mean / distribution of retrieval similarity;
- year distribution;
- source popularity/citation proxy if available;
- token count of provided context;
- domain/cluster distribution.

For the core causal experiment, construct sets **within relevance strata** so exposure overlap is manipulated without simply feeding less relevant literature.

This is the most important methodological amendment from the web research lane.

---

# 5. Recommended execution order

```text
Phase A — Codex infrastructure
    existing Task 0–3

Phase B — cheap E0 baseline
    no retrieval / top-k / MMR

GATE 1
    if no measurable problem-method effect -> probably KILL

Phase C — E1 controlled-overlap dose response
    direct causal intervention

GATE 2
    if no monotonic effect -> KILL retrieval-monoculture mechanism

Phase D — E2 MUSES root injection
    strongest objective-mismatch / discovery-utility test

GATE 3
    if root injection adds no downstream utility beyond matched relevance -> keep only E1 or kill

Phase E — E3 selection pressure
    only if paper already has a strong generation/retrieval mechanism

Phase F — human audit + robustness + paper
```

The paper should ideally survive without E3. E3 is an explanatory extension, not a rescue experiment.

---

# 6. Reviewer red-team

## Objection 1 — “This is just prompt/retrieval diversity.”

Response design:

- E1 manipulates exact source overlap directly;
- relevance distributions are matched;
- same model, prompt, k, token budget;
- dose–response rather than one algorithm comparison.

## Objection 2 — “Semantic distance does not equal scientific diversity.”

Response design:

- structured problem–mechanism–method–evaluation tuples;
- research-mode taxonomy;
- multiple embeddings;
- blind human duplicate audit.

## Objection 3 — “More diverse ideas may just be worse.”

Response design:

- soundness/feasibility tracked separately;
- quality-diversity frontier, not diversity alone;
- MUSES E2 uses held-out real future research as an external anchor.

## Objection 4 — “You are rediscovering IDEAgent / generic creativity homogenization.”

Response design:

- headline is not a new diversity framework;
- contribution is causal evidence about **literature exposure as an upstream variable**;
- E1 matched-exposure intervention and E2 author-endorsed root injection are distinct from sequential-memory/QD search.

## Objection 5 — “MUSES already showed relevance retrieval misses roots.”

Response design:

MUSES studies **retrieval success**. Our E2 studies whether the missed roots have **downstream generative consequences for scientific ideation** under controlled paired intervention.

The distinction must be explicit in the introduction.

## Objection 6 — “Future-paper matching rewards imitation.”

Response design:

Use it only as one objective prospective-utility endpoint; pair it with diversity, existing-literature distance, structural recombination, and human soundness audit. Never claim the held-out focal paper is the only valid idea.

---

# 7. Decision criteria

## Strong CONTINUE

Continue if E1 shows a reproducible monotonic exposure-overlap → idea-convergence relationship across >=2 model families and >=2 domains, with structural metrics and human-audited subset agreeing.

Upgrade to a high-upside paper if E2 additionally shows author-endorsed root injection provides downstream utility beyond matched relevant non-roots.

## Weak / UNCLEAR

If only embedding diversity moves but structural problem/method diversity does not, treat as weak and likely kill.

If MMR helps but controlled overlap does not, interpret E0 as an algorithm-specific effect, not evidence for research monoculture.

## KILL

Kill the main claim if:

- exact source overlap changes substantially but idea structure does not;
- effects disappear under matched relevance;
- only one model/domain exhibits the effect;
- gains require low-quality/random irrelevant documents;
- conclusions depend on one LLM judge or embedding model.

---

# 8. Current recommended main claim ladder

Do not jump to the strongest claim. Earn it experimentally.

```text
Level 1:
Retrieved evidence composition changes generated research ideas.

Level 2:
Shared evidence exposure causally increases portfolio convergence.

Level 3:
Relevance-oriented retrieval systematically creates concentrated research priors.

Level 4:
Relevance and discovery utility diverge; author-endorsed generative roots produce downstream scientific value missed by relevance retrieval.
```

Target Level 3 for a solid paper. Level 4 would materially increase novelty and scientific interest.

---

# 9. Key sources from this web round

- Si, Yang, Hashimoto. _Can LLMs Generate Novel Research Ideas?_ ICLR 2025. https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html
- Bao et al. _Contemporary AI lacks the imagination to diverge or negate in science._ 2026. https://arxiv.org/abs/2606.08251
- Ruan et al. _Evaluating LLMs' divergent thinking capabilities for scientific idea generation with minimal context._ Nature Communications 2026. https://www.nature.com/articles/s41467-026-70245-1
- Deng et al. _Examining and Addressing Barriers to Diversity in LLM-Generated Ideas._ 2026. https://arxiv.org/abs/2602.20408
- Gumma et al. _IDEAgent: Agentic Quality-Diversity Search for Research Idea Generation._ 2026. https://arxiv.org/abs/2607.22375
- Antoniades et al. _Heuresis: Search Strategies for Autonomous AI Research Agents Across Quality, Diversity and Novelty._ 2026. https://arxiv.org/abs/2606.25198
- Sinhahajari et al. _On the Limits of LLM-as-Judge for Scientific Novelty Assessment._ 2026. https://arxiv.org/abs/2606.12071
- Li, Tu, Han. _Graph2Idea: Retrieval-Augmented Scientific Idea Generation with Graph-Structured Contexts._ 2026. https://arxiv.org/abs/2606.09105
- Pandey, Kwon, Yu. _MUSES: A Benchmark for Prospective Intellectual-Roots Retrieval._ 2026-08-31. https://arxiv.org/abs/2609.00313
- MUSES datasheet. https://huggingface.co/datasets/anon-muses-neurips/muses/blob/main/DATASHEET.md
- Lu et al. _Towards end-to-end automation of AI research._ Nature 2026. https://www.nature.com/articles/s41586-026-10265-5
- Hao et al. _Artificial intelligence tools expand scientists’ impact but contract science’s focus._ Nature 2026. https://doi.org/10.1038/s41586-025-09922-y
- Uzzi et al. _Atypical combinations and scientific impact._ Science 2013. https://pubmed.ncbi.nlm.nih.gov/24159044/

## Evidence boundary

This document is a targeted collision scan and experimental-design synthesis, not proof that no contemporaneous work exists. Re-run a 30-day collision scan immediately before claim freeze and submission.