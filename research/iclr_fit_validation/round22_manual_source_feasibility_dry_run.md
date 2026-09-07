# Research Round 22 — Manual Source Feasibility Dry-Run

## 1. Trigger

The automated source-only feasibility audit has not yet produced `FEASIBILITY_RESULT.md`.

Before waiting on engineering, manually test a weaker necessary condition:

> Does the real ICLR 2025 literature contain multiple distinct scientific contribution routes within the same technical subfields, or is the proposed A/B treatment structure artificial?

This is **field-level dry-run evidence only**. It does not replace seed-specific relevance matching.

---

## 2. Long-context / retrieval subfield

ICLR 2025 contains multiple distinct contribution shapes addressing overlapping long-context problems.

### BUILD / IMPROVE / EFFICIENCY

- **A Little Goes a Long Way: Efficient Long Context Training and Inference with Partial Contexts (LongGen)** — proposes an efficient long-context architecture/training approach with substantial training/inference efficiency improvements.
- **DuoAttention** — proposes a KV-cache architecture separating retrieval and streaming heads for efficient long-context inference.
- **From Artificial Needles to Real Haystacks** — improves long-context retrieval/reasoning through synthetic-data finetuning.

### MEASURE / EVALUATE

- **HELMET** — argues current long-context evaluation is noisy/incomplete and introduces a broader application-centric benchmark.
- **SCBench** — reframes long-context method evaluation around the KV-cache lifecycle and shared-context deployment setting.

### EXPLAIN / MECHANISM

- **Retrieval Head Mechanistically Explains Long-Context Factuality** — identifies a sparse class of attention heads associated with long-context retrieval behavior.

### Implication

At a field level, a long-context seed can plausibly admit qualitatively different routes:

```text
A: build/optimize a long-context method
B: diagnose/evaluate the failure boundary
C: explain the underlying retrieval mechanism
```

Therefore a multi-route literature treatment is not inherently unnatural in this subfield.

### Remaining uncertainty

For a specific method-masked ICLR 2026 seed, the different 2025 route pools may not be equally relevant. Only seed-specific retrieval/matching can establish treatment validity.

---

## 3. Knowledge editing subfield

The literature is even more obviously multi-route.

### BUILD / IMPROVE

- **Precise Localization of Memories (FiNE)** — proposes fine-grained neuron-level editing to improve locality.
- **Everything is Editable (UnKE)** — proposes a new method for unstructured knowledge editing.

### MEASURE / EVALUATE

- **Can Knowledge Editing Really Correct Hallucinations? / HalluEditBench** — challenges whether standard editing evaluation actually measures correction of real hallucinations and introduces a holistic benchmark.
- **MQuAKE-Remastered** — audits corruption in a widely used multi-hop editing benchmark and shows evaluation artifacts can substantially distort conclusions.
- **MMKE-Bench** — expands multimodal knowledge-editing evaluation to more diverse visual knowledge types.

### DIAGNOSE / STRESS TEST + REPAIR

- **Uncovering Overfitting in Large Language Model Editing** — identifies Editing Overfit as a failure phenomenon, introduces EVOKE, and proposes a mitigation.

### Implication

A single broad question such as:

> How should LLM knowledge be reliably updated while preserving downstream behavior?

can support at least three scientifically legitimate high-level choices:

```text
build a better editor
vs
audit/repair evaluation
vs
diagnose a hidden failure mechanism
```

This is a promising source domain for seed-local A/B blocks.

---

## 4. LLM agents / planning

Field-level evidence also shows a strong evaluation/diagnostic route:

- **Robotouille** evaluates asynchronous planning and exposes a large synchronous-to-asynchronous performance drop.
- **Benchmarking Agentic Workflow Generation / WorfBench** evaluates sequence-vs-graph workflow planning and reports a substantial capability gap.
- **Agent Security Bench** reframes agent progress around security vulnerabilities and attacks/defenses.

The BUILD/IMPROVE pool needs a more targeted source audit before declaring a strong matched A/B design for this subfield.

### Implication

Agents may be feasible but should not be assumed as a primary source domain until matching is verified.

---

## 5. What this manual dry-run establishes

It supports only the following claim:

> ICLR 2025 contains genuine scientific-route diversity within at least some relevant ML subfields, so the treatment concept is not obviously artificial.

It does **not** establish:

- enough papers per route after temporal-clean filtering;
- route balance for any specific seed;
- relevance equivalence;
- annotation reliability;
- broad subfield coverage;
- final packet size k;
- treatment eligibility rate.

These remain Codex/source-audit questions.

---

## 6. Practical design update

The first source-only feasibility analysis should prioritize subfields in this order for diagnostic purposes, without selecting them based on outcomes:

1. knowledge editing / knowledge updating;
2. long-context / retrieval;
3. post-training / context reliance;
4. agents / planning;
5. interpretability / reasoning;
6. efficiency / optimization.

This ordering is **engineering diagnostic priority**, not a rule for inclusion in the eventual scientific sample.

Why prioritize the first two:

- manual inspection shows clear multiple contribution routes;
- route definitions are relatively interpretable;
- the literature contains method, evaluation, and mechanism papers in the same broad technical neighborhood.

If even these two fail seed-level relevance matching, the overall project should be reconsidered aggressively.

---

## 7. Candidate route contrasts suggested by the source literature

Do not freeze these until the formal source audit, but likely high-feasibility contrasts include:

### Knowledge editing

```text
BUILD/IMPROVE
vs
MEASURE/EVALUATE
```

and

```text
BUILD/IMPROVE
vs
DIAGNOSE/STRESS-TEST
```

### Long context

```text
BUILD/OPTIMIZE
vs
MEASURE/EVALUATE
```

and potentially

```text
BUILD/OPTIMIZE
vs
EXPLAIN/MECHANISM
```

### Why not force one universal contrast

A universal `BUILD vs DIAGNOSE` pair may reduce coverage unnecessarily. The primary seed-local A/B outcome plus preregistered contrast families remains preferable if treatment selection stays outcome-independent.

---

## 8. Strongest new design insight

The concept of route `equivalence` should be replaced by:

> **matched scientific admissibility under a shared seed problem**.

Two routes do not need equal expected scientific value. They need to be:

- relevant;
- plausible;
- supported by serious contemporaneous literature;
- non-dominated by obvious construction;
- matched on observable evidence quality/relevance.

The causal question is not which route is objectively better. It is whether changing the available admissible evidence changes the model's high-level choice distribution.

---

## 9. Decision

**KEEP / SOURCE FEASIBILITY LOOKS PLAUSIBLE AT FIELD LEVEL.**

The next hard gate is still seed-level, temporally clean, source-only matching. No treatment generation is authorized by this dry-run.
