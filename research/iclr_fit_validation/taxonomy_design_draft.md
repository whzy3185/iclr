# Taxonomy Design Draft — Scientific Move vs Method Inventory

> Date: 2026-09-06  
> Status: **RESEARCH DRAFT, NOT THE FROZEN EXPERIMENT TAXONOMY**  
> Purpose: design a taxonomy that can separate high-level scientific search direction from low-level methodology substitution.  
> Do not copy this file verbatim to `experiments/idea_collapse/TAXONOMY.md` until a pre-treatment annotation audit is complete.

---

## 0. Design principle

The paper should not rely on one monolithic “idea category.”

We need at least two conceptually different layers:

```text
Layer A — WHAT SCIENTIFIC MOVE IS THE PROPOSAL MAKING?
          high-level goal / framing

Layer B — WHAT CONCRETE METHODOLOGY DOES IT USE?
          datasets / model families / training / metrics / experimental design
```

This distinction is crucial because retrieval may cause:

```text
low-level substitution without high-level steering
```

For example, a model could replace Llama with Qwen or change one benchmark while still proposing the same familiar “build a better module and improve accuracy” research strategy.

Carlon et al. (2026) already provide a useful structural methodology taxonomy at Layer B, including dataset task type, model architecture/provider/training paradigm/openness/size, and metric evaluation type. We should reuse or adapt established dimensions instead of inventing arbitrary low-level labels.

Our novel measurement burden is primarily Layer A.

---

# 1. Layer A — Scientific Move

## A1 BUILD_IMPROVE

### Definition

The central scientific objective is to create or modify a model, algorithm, training procedure, system, representation, or inference method to directly improve task capability/performance.

### Positive signals

- “We propose a new architecture/training objective/module…”
- success is primarily measured by improved task performance / capability.
- even if analysis is included, the main claim is an improved method.

### Examples of ICLR-style papers

- STARS if viewed through its mitigation/construction contribution;
- REGENT;
- many new training/inference algorithms.

### Exclusions

- a new method whose primary purpose is to test a scientific mechanism rather than win performance;
- a diagnostic benchmark with only a small repair baseline.

---

## A2 DIAGNOSE_STRESS_TEST

### Definition

The primary objective is to reveal a failure mode, boundary condition, robustness issue, hidden assumption violation, bias, vulnerability, or mismatch between expected and observed behavior.

### Positive signals

- “We find that…” followed by an unexpected failure;
- controlled stress conditions;
- main value remains even if no mitigation exists.

### Examples

- Context-Parametric Inversion;
- BiasBusters;
- failure-mode / robustness studies.

### Exclusions

- benchmark construction where measurement protocol itself is the main contribution;
- mechanistic explanation where the central question is “why,” not “where does it fail.”

---

## A3 MEASURE_EVALUATE

### Definition

The primary contribution is a new or corrected measurement of capability/behavior, benchmark/protocol/metric, construct-validity analysis, or evaluation reframe.

### Positive signals

- “existing benchmark/metric fails to measure X”;
- systematic capability evaluation;
- new benchmark with scientific conclusions about model behavior.

### Examples

- DiscoveryBench;
- scientific ideation benchmark papers;
- content-diversity measurement studies when evaluation design is central.

### Exclusions

- a benchmark used mainly to validate a new method;
- diagnostic studies with a standard metric but novel failure mechanism.

---

## A4 EXPLAIN_MECHANISM_THEORY

### Definition

The primary objective is to explain why a model/algorithm/phenomenon behaves as observed, derive a theory, identify an internal/computational mechanism, or unify observations under a predictive explanation.

### Positive signals

- causal/mechanistic decomposition;
- theoretical model predicts behavior;
- explanation generalizes beyond the motivating case.

### Examples

- Mixing Mechanisms;
- mechanistic interpretability / optimization-dynamics papers.

### Exclusions

- purely descriptive failure taxonomy;
- method paper with superficial post-hoc explanation.

---

## A5 OPTIMIZE_EFFICIENCY

### Definition

The central objective is to reduce compute, memory, samples, data, latency, communication, or other resource costs while preserving or improving behavior.

### Positive signals

- resource metric is first-class objective;
- algorithm is motivated by computational constraints;
- scaling/efficiency trade-off is central.

### Examples

- efficient training/inference, quantization, sample-efficient search.

### Exclusions

- generic method improvement that happens to be faster;
- theory paper whose efficiency result is secondary.

---

## A6 VERIFY_FALSIFY_REPLICATE

### Definition

The central goal is to independently test whether an existing empirical/theoretical claim holds, explicitly test a null/counter-hypothesis, reproduce a result under controlled conditions, or falsify a claimed generalization.

### Why keep this separate initially

Scientific ideation systems may systematically underproduce direct falsification/null-hypothesis projects. Recent ideation evidence suggests this category may be sparse, and sparsity itself is potentially scientifically meaningful.

### Exclusions

- discovering a new failure mode without directly testing a pre-existing claim (A2);
- generic benchmarking of many models (A3).

### Merge rule

If pre-treatment human annotation shows A6 is too sparse or cannot be reliably separated from A2/A3, merge it using a rule frozen **before treatment outcomes**. Do not preserve A6 solely because it gives an interesting result.

---

# 2. Multi-label vs primary-label rule

Many papers genuinely perform multiple moves.

Recommended annotation structure:

```json
{
  "primary_move": "DIAGNOSE_STRESS_TEST",
  "secondary_moves": ["EXPLAIN_MECHANISM_THEORY", "BUILD_IMPROVE"],
  "confidence": 0.85,
  "rationale": "..."
}
```

### Primary move definition

Ask:

> If the implementation/method were removed, what scientific contribution would the authors most want the reader to remember?

and:

> Which claim motivates the experimental design rather than merely appearing as a downstream consequence?

Do not infer primary move from paper-section counts or title keywords alone.

### Primary analysis

Use `primary_move` for the cleanest dose-response model.

### Robustness

Use multi-label marginals to verify that results are not artifacts of forced single-label classification.

---

# 3. Layer B — Method Inventory

Adapt dimensions from Carlon et al. rather than inventing a new full ontology.

## B1 Dataset / task properties

Potential dimensions:

- modality: text / image / audio / video / time series / graph / multimodal;
- task type: classification / regression / generation / QA / reasoning / retrieval / ranking / etc.;
- domain;
- size / granularity where relevant.

## B2 Model / algorithm properties

- architecture family;
- training paradigm;
- provider / source;
- open vs closed;
- parameter-size bucket;
- retrieval/RAG usage;
- fine-tuning / RL / prompting / inference-time search.

## B3 Evaluation properties

- accuracy/capability;
- ranking/retrieval;
- robustness;
- safety;
- efficiency/latency;
- fairness;
- explainability;
- uncertainty/calibration;
- user/human evaluation.

## B4 Free method entities

Preserve normalized entity names separately:

```text
specific dataset
specific model
specific metric
specific method name
```

This allows us to distinguish:

```text
entity substitution
from
category-level methodology shift
from
high-level scientific-move shift
```

---

# 4. Layer C — Problem-Framing Tuple

For a subset / high-quality parser, extract:

```text
(problem_object,
 failure_or_limitation,
 hypothesized_mechanism,
 intervention_family,
 evaluation_target)
```

This is not necessarily a categorical ontology.

Use it for:

- pairwise substantive-equivalence audit;
- treatment-condition divergence;
- source→proposal transfer mapping.

Do not treat raw LLM extraction as ground truth without audit.

---

# 5. Layer D — Context-Uptake / Recombination

Separate how the proposal uses supplied evidence.

## D0 NO_UPTAKE

No meaningful supplied evidence trace.

## D1 SOURCE_ATTRIBUTION

Explicitly cites/mentions source or source-specific entity.

## D2 CONTENT_UPTAKE

Uses a supplied finding/mechanism/limitation.

## D3 COPY

Proposal directly reuses a supplied method/experiment with minimal adaptation.

## D4 COMBINE

Combines components from multiple supplied sources.

## D5 TRANSFER

Transfers a supplied idea/framing/method to a materially different target/problem.

## D6 NEW_DIRECTION

High-level proposal is not directly contained in any one supplied source but can reasonably be interpreted as conditioned by the evidence packet.

These are exploratory until annotation reliability is demonstrated.

---

# 6. Why this taxonomy helps identify Grounding Without Steering

A model can score high on:

```text
D1 source attribution
D2 content uptake
B-level entity substitution
```

while remaining nearly unchanged in:

```text
A-level scientific move
C-level central problem framing
```

That is exactly the phenomenon the paper needs to distinguish.

Conversely, strong steerability requires not just method-name changes but systematic A/C-level changes with evidence composition.

---

# 7. Source-paper taxonomy and output taxonomy must use the same high-level codebook

For controlled evidence mixtures:

1. label ICLR source papers using Layer A;
2. build matched A/B context packets;
3. generate proposals;
4. label proposals with the same Layer A definitions, blinded to treatment;
5. estimate treatment transfer.

This creates a transparent mapping:

```text
fraction of context labeled A
      ↓
probability generated proposal labeled A
```

The classifier used for source papers and outputs may see different text fields, but definitions must be identical.

---

# 8. Pre-treatment audit design

Before any treatment output exists, sample:

- ~100 ICLR source-paper abstracts across years/subfields;
- ~100 no-context generated ideas across models/seeds.

Two independent annotators apply Layer A + a small Layer B subset.

Report:

- raw agreement;
- Cohen/Fleiss κ or an appropriate alternative;
- confusion matrix;
- category prevalence;
- confidence distribution.

### Revision rules

Allowed before treatment:

- merge confusing categories;
- rewrite definitions;
- add examples;
- clarify priority rules.

Forbidden after treatment outcomes are visible:

- redefining categories because one condition produces inconvenient labels;
- changing primary/secondary rules to amplify a treatment effect.

---

# 9. Automatic annotation strategy

After taxonomy freeze:

1. have blinded human gold labels for a stratified subset;
2. compare several automatic parsers/classifiers;
3. select parser based on pre-treatment validation only;
4. freeze parser model/version/prompt;
5. report accuracy/F1/confusion by category;
6. propagate uncertainty / run sensitivity analyses if error is nontrivial.

Do not use the same LLM generator as the only classifier if avoidable.

A simple supervised classifier trained on audited labels may be preferable if sample size is sufficient.

---

# 10. Taxonomy-related kill conditions

Kill or redesign the high-level experiment if:

- Layer A agreement is too poor for interpretable inference;
- source papers systematically require multiple equal primary moves such that mixtures are not constructable;
- A/B evidence packets are trivially separable by topic rather than research move;
- automatic label error is large and strongly condition-dependent;
- treatment effects vanish under multi-label robustness analysis.

---

# 11. Current recommendation

Use **Layer A scientific move** as the main high-level treatment/outcome variable, but make the paper's explanatory power come from the *contrast across layers*:

```text
source/entity grounding
method inventory
scientific move
problem framing
```

The scientifically interesting question is not whether retrieval changes text.

It is:

> **At what level of abstraction does retrieved scientific evidence stop being able to move the model?**

That is the taxonomy's purpose.

---

## Relevant source

Carlon et al., *Thinking Like a Scientist? A Structural Study of LLM-Generated Research Methods*, arXiv:2606.26130. Their methodology taxonomy includes dataset dimensions (e.g. modality/task type), model dimensions (architecture/training paradigm/provider/openness/size), and metric evaluation type. Their work motivates reusing structured method dimensions for our Layer B instead of presenting them as our novel taxonomy.
