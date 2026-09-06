# Nearest-Neighbor Novelty Boundary

> Date: 2026-09-06  
> Purpose: force the paper to articulate a contribution that is not already contained in its nearest ICLR/2026 neighbors.

---

## 1. Comparison matrix

| Work | Setting | Context intervention | Output object | Explicit target distribution / answer? | Measures model prior? | Scientific hypothesis/method search? | Main gap left for us |
|---|---|---|---|---|---|---|---|
| **Context-Parametric Inversion** (ICLR 2025) | factual/context conflict | context contradicts parametric fact | factual answer | yes / effectively binary | implicit context-vs-parametric | no | open-ended multi-valid scientific choices; distributional rather than factual reliance |
| **Controllable Context Sensitivity** (ICLR 2025) | factual context-vs-prior | explicit instruction to follow context or prior | factual answer | yes / binary | yes, context/prior | no | implicit scientific-evidence steering without telling model which distribution to follow; high-level abstraction hierarchy |
| **Spectrum Tuning** (ICLR 2026) | conditional distribution modeling | demonstrations/context specify novel distribution | samples from known/constructible distribution | yes | yes conceptually | no specific scientific-literature mechanism | scientific evidence as an *implicit* control signal; no normative target distribution; prior×evidence interaction; natural RAG |
| **Carlon et al., Thinking Like a Scientist?** (2026) | research methodology recommendation | minimal RQ-only prompt; BM25 calibration | datasets/models/metrics/pipeline | paper inventory is descriptive reference, not optimal target | characterizes default methodological concentration | yes | no retrieval-context intervention; does not ask whether literature can override the measured default |
| **ProjectionBench** (2026) | scientific hypothesis projection | progressively disclose null hypothesis / experiment | predicted focal-paper results | yes, focal paper conclusions | minimal-context baseline | yes, mostly materials science outcomes | holds information amount *not* fixed; context becomes focal experiment itself; no alternative valid scientific-mode distribution / prior competition |
| **Prompt-language diversity lever** (2026) | scientific RAG ideation | query language changes retrieval and possibly generation | generated proposals | no | no | yes | intervention bundles query/retrieval/language; one domain; no relevance-matched packet randomization; no prior interaction/hierarchy |
| **Si et al. scientific ideation** (ICLR 2025) | NLP research ideas | RAG quantity / generation pipeline | research idea | no | backbone-level diversity measured | yes | RAG amount nearly null under duplicate metric; composition and high-level search distribution not isolated |
| **BiasBusters** (ICLR 2026) | tool choice | controlled equivalent tool metadata/order | discrete tool selection | equivalent valid tools | bias inferred from choices | no | methodological design precedent; scientific open-ended context remains unstudied |

---

# 2. What we can legitimately claim as novel — conditional on results

## Claim N1 — Open-ended scientific prior/context competition

> We study context-vs-prior behavior where the alternatives are **multiple scientifically plausible research strategies rather than a correct context fact or a known target output distribution**.

Why this matters:

In scientific ideation, there is generally no oracle saying that a 75% `DIAGNOSE` evidence packet should yield exactly 75% diagnostic proposals. The evidence mixture is an intervention, not a normative label distribution.

Therefore our question is about **response to evidence** and prior resistance, not distributional accuracy.

---

## Claim N2 — Evidence as implicit, not explicit, steering signal

Spectrum-style tasks can give examples that directly define the desired output distribution; Context Sensitivity explicitly tells the model whether to use context or prior.

Our generator prompt remains fixed and does not say:

> “Choose DIAGNOSE rather than BUILD.”

Only the scientific literature changes.

Thus we measure the strength of **ecological/implicit in-context steering by evidence composition**.

---

## Claim N3 — Hierarchical context uptake

We distinguish:

```text
source attribution
conceptual uptake
method-family uptake
scientific-move uptake
central problem framing
```

The publishable phenomenon would be a systematic difference across these abstraction levels — especially **grounding without high-level steering**.

None of the nearest neighbors above establishes this hierarchy for literature-grounded scientific ideation.

---

## Claim N4 — Treatment independent of model prior

Treatment modes are selected/matched from the ICLR corpus before observing model-prior outputs.

We then test whether the same frozen evidence treatment has different leverage depending on independently measured model prior strength.

This gives a causal interaction:

```text
context evidence × model prior
```

rather than selecting a counterfactual tailored to the model's observed behavior.

---

## Claim N5 — Controlled-to-natural RAG prediction

Controlled evidence-mixture experiments fit a response model; held-out natural top-k retrieval is then predicted from:

```text
no-context prior + natural evidence composition
```

This is a stronger bridge to realistic research agents than a benchmark-only context manipulation.

---

# 3. Claims we must explicitly avoid

Do not write any of the following in the abstract/introduction:

- “We introduce in-context steerability.”
- “We are the first to study context versus model prior.”
- “We are the first to show scientific LLMs have method biases.”
- “We are the first to reveal retrieval changes scientific proposals.”
- “We show RAG reduces idea diversity.”
- “We introduce the first benchmark for scientific ideation.”
- “We show the true/optimal scientific method distribution.”

They are false, overly broad, or unsupported.

---

# 4. Best one-sentence novelty statement

Before results:

> **Unlike prior context-sensitivity work with factual conflicts or known target distributions, we test whether real, equally relevant scientific literature can implicitly redirect an LLM among multiple valid research strategies, and whether that influence survives from source grounding to high-level method and problem choice.**

If the prior-bound branch succeeds:

> **We identify a hierarchy of scientific context reliance: retrieved literature is strongly represented in source and conceptual content yet is systematically weaker at overriding high-level research-method and problem-framing priors.**

If strong steerability succeeds:

> **We show that evidence composition acts as a quantitatively predictable control signal over high-level scientific search, despite being invisible to coarse duplicate-based idea-diversity measures.**

---

# 5. What would invalidate the novelty claim

A new paper is a direct collision if it simultaneously does most of the following:

1. literature-grounded scientific hypothesis/method generation;
2. multiple valid scientific strategies rather than a known answer;
3. measures a no-context model prior;
4. chooses context treatments independently of those model outputs;
5. matches context alternatives on scientific relevance/quality;
6. manipulates evidence composition at fixed context amount;
7. measures high-level method/research-mode/problem-framing response;
8. tests prior × context interaction or hierarchical uptake;
9. validates on natural retrieval or multiple realistic domains/models.

A paper matching only “retrieval affects ideas” is not sufficient collision.

---

# 6. Current novelty verdict

**Conditional GO.** The direct-collision search up to 2026-09-06 has found strong adjacent work on every component separately, but not the combined causal question above.

This is a double-edged situation:

- positive: the question has clear grounding in current ICLR research;
- negative: novelty depends on the *combination and rigor* of the controlled experiment, not on a flashy new term.

A weak implementation will look incremental. A strong prior×evidence interaction / hierarchy / held-out natural-RAG prediction can be a genuine ICLR contribution.
