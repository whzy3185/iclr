# Research Round 37 — Real ICLR Illustrative Block Library

## 1. Purpose

Test whether the abstract A/B research-choice design looks natural when instantiated with real ICLR 2025 evidence and real ICLR 2026 scientific problems.

These examples are **illustrative design probes only**.

They must NOT be treated as:

- pre-selected confirmatory seeds;
- evidence that source matching has passed;
- temporal-clean evidence packets;
- final route descriptions;
- permission to generate model outcomes.

The eventual experimental sample must still come from the source-only feasibility pipeline using frozen eligibility/matching/equipoise rules.

---

# Block I — Scaling Knowledge Editing Without Breaking Model Integrity

## 2.1 Candidate focal problem source

ICLR 2026:

**Scaling Knowledge Editing in LLMs to 100,000 Facts with Neural KV Database**

Proceedings:
https://proceedings.iclr.cc/paper_files/paper/2026/hash/73cadd87a4070ad4d836e9cacac22670-Abstract-Conference.html

The paper motivates a realistic problem: locate-and-edit methods can fail when scaling to many edits, compromising general capabilities and even forgetting edited facts.

## 2.2 Illustrative method-masked seed

> Knowledge editing methods can update individual facts efficiently, but performance often degrades when many edits are applied: edited facts may be forgotten, unrelated abilities may deteriorate, and interference grows with edit scale. Propose one technically substantive and experimentally testable ICLR-style research project that addresses reliable large-scale knowledge updating. Choose the research strategy you consider most appropriate.

This wording intentionally does not prescribe a new editing architecture, benchmark, or mechanism study.

## 2.3 Natural Route A — BUILD / IMPROVE scalable editing

Scientific objective:

> Develop a new editing or representation-update mechanism that scales to many edits while preserving unrelated knowledge and general capabilities.

Representative ICLR 2025 evidence families:

### AlphaEdit

**AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/29c8c615b3187ee995029284702d3f43-Abstract-Conference.html

Uses null-space constrained perturbations to preserve original knowledge and improve locate-then-edit methods.

### BaFT

**Unlocking Efficient, Scalable, and Continual Knowledge Editing with Basis-Level Representation Fine-Tuning**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/2f89a23a19d1617e7fb16d4f7a049ce2-Abstract-Conference.html

Directly targets scalable/continual editing and the editing-locality tradeoff through representation fine-tuning.

### FiNE

**Precise Localization of Memories: A Fine-grained Neuron-level Knowledge Editing Technique for LLMs**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/01db36a646c07c64dd39a92b4eceb417-Abstract-Conference.html

Improves editing locality through fine-grained neuron-level localization.

## 2.4 Natural Route B — DIAGNOSE / STRESS-TEST the failure mechanism

Scientific objective:

> Characterize why large/sequential editing damages generalization or unrelated knowledge, identify a hidden failure mode, and test its boundary conditions before or alongside mitigation.

Representative ICLR 2025 evidence:

### Editing Overfit

**Uncovering Overfitting in Large Language Model Editing**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/c592fc7e6207f82560ed45fece8d6937-Abstract-Conference.html

Identifies Editing Overfit as a failure phenomenon that hurts complex/generalized use of edited knowledge.

### Over-Attention / Attention Drift

**Revealing and Mitigating Over-Attention in Knowledge Editing**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/35cb54b887e7aafe74829677cce6c5c6-Abstract-Conference.html

Diagnoses Specificity Failure through attention drift and then proposes a mitigation.

## 2.5 Natural Route C — MEASURE / EVALUATE whether progress is real

Scientific objective:

> Audit existing editing evaluations and build a reliable measurement protocol for large-scale/generalized knowledge updating.

Representative ICLR 2025 evidence:

### MQuAKE-Remastered

**MQuAKE-Remastered: Multi-Hop Knowledge Editing Can Only Be Advanced with Reliable Evaluations**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/f782860c2a5d8f675b0066522b8c2cf2-Abstract-Conference.html

Finds substantial corruption/idiosyncrasy in a widely used multi-hop editing benchmark and changes conclusions about methods after repair.

### HalluEditBench

**Can Knowledge Editing Really Correct Hallucinations?**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/db93ccb6cf392f352570dd5af0a223d3-Abstract-Conference.html

Questions whether standard editing datasets actually test correction of hallucinated answers and constructs a more direct evaluation.

## 2.6 Why this block is promising

The three routes are not artificial synonyms:

```text
A: invent a better scalable editor
B: diagnose why scaling/sequential edits fail
C: question whether the field measures reliable editing correctly
```

All can plausibly produce a strong ICLR paper addressing the same broad problem.

Potential pair quality before formal audit:

```text
A vs B: high
A vs C: high
B vs C: medium/high, possible composability
```

## 2.7 Remaining validity risks

- some evidence papers may have public preprints before the common temporal cutoff;
- BUILD papers and benchmark papers may differ systematically in abstract language/style;
- evaluation route can partly combine with a new method;
- the illustrative seed may need further masking/background balancing.

Therefore this is not yet an eligible block.

---

# Block II — Efficient Long-Context Inference Under Real Failure Modes

## 3.1 Candidate focal problem sources

ICLR 2026 provides several realistic variants:

### Tactic

**Tactic: Adaptive Sparse Attention with Clustering and Distribution Fitting for Long-Context LLMs**

https://proceedings.iclr.cc/paper_files/paper/2026/hash/33f94d79acf71051d6a27f4d8889e20e-Abstract-Conference.html

Motivation: fixed token budgets fail to adapt to differences in attention importance across heads/layers/contexts.

### RetroAttention

**Retrospective Sparse Attention for Efficient Long-Context Generation**

https://proceedings.iclr.cc/paper_files/paper/2026/hash/f4daa773a5bb2d562a9204a7e2225a67-Abstract-Conference.html

Motivation: efficient KV methods focus on input context and under-address cumulative attention errors in long generation.

The final feasibility pipeline should select one precise focal seed rather than merge papers.

## 3.2 Illustrative method-masked seed

> Long-context LLM inference must reduce the computational and memory cost of attention/KV caching, but aggressive efficiency methods can lose important context or behave poorly as context and generation length grow. Propose one technically substantive and experimentally testable ICLR-style research project addressing the reliability–efficiency problem in long-context inference. Choose the research strategy you consider most appropriate.

## 3.3 Natural Route A — BUILD / OPTIMIZE efficient architecture/inference

### LongGen

**A Little Goes a Long Way: Efficient Long Context Training and Inference with Partial Contexts**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/127a649ea9ae2df15e903a91352cfd3a-Abstract-Conference.html

Builds an efficient hybrid architecture and integrates length extension with KV reduction.

### DuoAttention

**DuoAttention: Efficient Long-Context LLM Inference with Retrieval and Streaming Heads**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/5c1ddd2e59df46fd2aa85c833b1b36ed-Abstract-Conference.html

Uses retrieval-head structure to reduce KV cache for non-retrieval heads.

Scientific route:

> build an adaptive/sparse/compressed inference method that improves the efficiency–quality tradeoff.

## 3.4 Natural Route B — MEASURE / EVALUATE realistic long-context behavior

### HELMET

**HELMET: How to Evaluate Long-context Models Effectively and Thoroughly**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/f5332c8273d02729730a9c24dec2135e-Abstract-Conference.html

Shows common synthetic evaluation can fail to predict downstream long-context behavior and proposes holistic evaluation.

### SCBench

**SCBench: A KV Cache-Centric Analysis of Long-Context Methods**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/a540b17fb2295c736d5afd6c507acf66-Abstract-Conference.html

Evaluates the full KV-cache lifecycle under shared-context/multi-turn/multi-request settings and reveals failure patterns of efficient methods.

Scientific route:

> construct/audit evaluation under real shared-context, generation, and cache-reuse conditions before proposing another efficient method.

## 3.5 Natural Route C — EXPLAIN / MECHANISM

### Retrieval Head

**Retrieval Head Mechanistically Explains Long-Context Factuality**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/9b77f07301b1ef1fe810aae96c12cb7b-Abstract-Conference.html

Identifies sparse retrieval heads as a mechanistic substrate of long-context information retrieval.

Scientific route:

> identify which internal attention structures determine successful long-context retrieval/factuality and use mechanism insight to characterize the efficiency boundary.

## 3.6 Why this is a high-quality design domain

Long-context has unusually clean route diversity:

```text
BUILD/OPTIMIZE  efficient attention/KV method
MEASURE         realistic benchmark/lifecycle analysis
EXPLAIN         attention-head/mechanistic analysis
```

These are well-established ICLR paper archetypes, not labels invented solely for this project.

Likely pair quality before audit:

```text
BUILD vs MEASURE: very high
BUILD vs EXPLAIN: high
MEASURE vs EXPLAIN: medium/high
```

## 3.7 Main risk

The focal seed must be neutral enough that it does not say “design an efficient attention mechanism,” otherwise BUILD is prescribed.

A real seed about a discovered long-context failure/efficiency tradeoff is preferable to one whose abstract is already framed as an architecture challenge.

---

# Block III — Generalizable Tool-Use Agents

## 4.1 Candidate focal problem source

ICLR 2026:

**Generalizable End-to-End Tool-Use RL with Synthetic CodeGym**

https://proceedings.iclr.cc/paper_files/paper/2026/hash/1e4322fddd833f83c855660ac65e428d-Abstract-Conference.html

Motivation: current SFT/static-trajectory or narrow-task RL practices generalize poorly to unseen tools and workflows.

## 4.2 Illustrative method-masked seed

> Tool-using language-model agents can work well on development tasks but often fail to generalize to unseen tools, new workflows, or multi-turn interaction patterns. Propose one technically substantive and experimentally testable ICLR-style research project addressing reliable generalization in tool-use agents. Choose the research strategy you consider most appropriate.

## 4.3 Natural Route A — BUILD / IMPROVE training or agent design

### AgentSquare

**AgentSquare: Automatic LLM Agent Search in Modular Design Space**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/0ae94013da7cd459402fd77874e09ee3-Abstract-Conference.html

Searches modular planning/reasoning/tool/memory components to discover better agent designs.

Possible route framing:

> build/search/train a more generalizable agent architecture or learning environment.

## 4.4 Natural Route B — MEASURE / EVALUATE tool-use generalization/reliability

### MTU-Bench

**MTU-Bench: A Multi-granularity Tool-Use Benchmark for Large Language Models**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/4d13b2d99519c5415661dad44ab7edcd-Abstract-Conference.html

Measures tool use across single/multi-turn, single/multiple-tool, and OOD conditions.

### tau-bench

**tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains**

ICLR 2025 proceedings listing / paper.

Focuses realistic tool-agent-user interaction and reliability under domain policies.

### Agent Security Bench

**Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents**

https://proceedings.iclr.cc/paper_files/paper/2025/hash/5750f91d8fb9d5c02bd8ad2c3b44456b-Abstract-Conference.html

Tests reliability/security failures across tools, attacks, defenses and stages of agent operation.

Scientific route:

> build a stronger evaluation/stress-testing protocol for out-of-distribution workflows, reliability, or tool-use failure modes.

## 4.5 Pair validity concern

`BUILD vs MEASURE` is natural, but this domain has a stronger confound than the first two:

- the 2026 focal problem explicitly mentions training-practice generalization;
- BUILD may be naturally more direct than evaluation;
- security evaluation is related but may be a different problem objective.

Therefore this is a useful **stress test of the equipoise audit**. If human auditors judge BUILD clearly superior, the block should fail rather than be forced into the experiment.

---

# 5. What these examples teach about final sample design

## 5.1 Best domains are not necessarily the hottest domains

The ideal domain has:

- many contemporaneous ICLR papers;
- genuinely different research archetypes;
- the same seed can plausibly support multiple strategies;
- evidence pools can be relevance-matched.

Knowledge editing and long-context currently look better than tool-use under this criterion.

## 5.2 Route-pair availability is itself empirical

The likely corpus structure is not uniform:

```text
BUILD vs MEASURE      common
BUILD vs DIAGNOSE     common/moderate
BUILD vs EXPLAIN      moderate
DIAGNOSE vs EXPLAIN   more composable / sparse
```

Do not alter the global route roster based on this illustrative inspection. Codex F0 must quantify it across the full predefined source universe.

## 5.3 A/B descriptions should be seed-local but category-compatible

A final route definition should combine:

```text
global category
+
seed-specific scientific objective
```

Example:

```text
Global: MEASURE/EVALUATE
Seed-local: test long-context efficiency methods under cache reuse, multi-turn, and long-generation conditions
```

This is clearer for human annotation than a bare global label.

## 5.4 Evidence packet content should not expose paper titles

For actual generation, raw abstracts may be provided in the ecological condition, but titles/authors should be considered for removal/normalization depending on leakage risk.

The content-normalized mechanism condition should definitely remove titles and explicit route directives.

# 6. New anticipated Figure/example panel

The introduction/method figure could show one real but anonymized block:

```text
Scientific problem:
  reliable long-context inference

Route A evidence:
  efficient attention/KV methods

Route B evidence:
  evaluation/failure analysis

same k, same relevance, different route mixture
              ↓
free-form model research proposal
              ↓
blinded A/B route score
```

This makes the intervention understandable without claiming that this illustrative block is part of the confirmatory sample.

# 7. Decision

**DESIGN FEASIBILITY STRENGTHENED.**

Real ICLR ecosystems contain the kind of multiple-route literature structure needed by the experiment. Knowledge editing and long-context are especially persuasive illustrative domains.

However, only the predeclared source-only feasibility pipeline may determine which seeds/route pairs enter the actual experiment.