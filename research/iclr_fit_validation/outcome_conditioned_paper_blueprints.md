# Outcome-Conditioned ICLR Paper Blueprints

> Date: 2026-09-06  
> Purpose: define what a successful paper must look like **before** treatment outcomes exist.  
> Rule: none of the result statements below are claims about observed data. They are conditional paper shapes.

---

# 0. Why write the paper before running the experiment?

The project should not continue merely because some metric becomes significant. A useful test is whether each scientifically meaningful outcome can be converted into a coherent ICLR paper with:

1. one memorable question;
2. a non-obvious answer;
3. controlled evidence;
4. a general ML interpretation;
5. a clear relation to accepted ICLR work;
6. a result that survives the strongest obvious reviewer objection.

The current question is:

> **Can retrieved scientific literature override an LLM's default scientific-method / research-mode prior, and does evidence uptake weaken as scientific abstraction increases?**

There are three predeclared outcome branches.

---

# 1. Blueprint A — Strong Scientific Steerability

## 1.1 Candidate title

**Same Relevance, Different Science: Evidence Composition Steers LLM Hypothesis Search**

Alternative:

**Evidence as a Control Signal: In-Context Steerability of LLM Scientific Ideation**

## 1.2 One-sentence result, conditional

> Holding relevance, amount, prompt, and model fixed, changing the scientific framing composition of retrieved literature produces a strong and predictable shift in high-level research modes and problem/method choices, while common near-duplicate diversity metrics substantially understate the shift.

## 1.3 Why this is non-obvious

A weak observation would be:

> Models talk about papers they see.

The publishable result would instead require all of the following:

- matched topical relevance;
- fixed packet size and token budget;
- directional dose response across framing mixtures;
- effect larger than prompt/order noise;
- high-level mode/problem shift, not only keyword uptake;
- held-out natural-RAG behavior predicted from controlled response coefficients;
- effect replicated within multiple model families.

The surprising element would be a **metric dissociation**:

```text
coarse idea-duplicate rate       ~ flat
high-level search distribution   changes strongly
```

This explains why previous RAG-quantity experiments can look nearly null while retrieval still meaningfully steers where a model searches.

## 1.4 Abstract skeleton

### Motivation

Literature-grounded research agents increasingly retrieve papers before proposing hypotheses, but existing evaluations usually ask whether generated ideas are novel/diverse or whether retrieval improves quality. It remains unclear whether retrieved evidence actually changes the *distribution of scientific moves* an LLM explores.

### Gap

Prior ICLR work finds scientific ideation has limited generation diversity, while simply increasing RAG context has little effect on a coarse duplicate metric. Separately, distributional steerability work shows that post-trained models can struggle to override priors using context.

### Method

Estimate model-specific no-context scientific priors, then construct temporally clean ICLR evidence packets with matched relevance but controlled mixtures of research framings. Measure response at multiple abstraction levels and validate on held-out natural top-k retrieval.

### Conditional findings

Insert only if observed:

- smooth evidence-mixture dose response;
- robust high-level method/research-mode shift;
- coarse duplicate metric under-reacts;
- controlled response predicts natural RAG behavior;
- model/post-training heterogeneity.

### Conclusion

Retrieval is not merely a knowledge supplement; evidence composition is a controllable input to the distribution over open-ended scientific search choices.

## 1.5 Figure plan

### Figure 1 — Metric dissociation

Two panels for the same controlled intervention:

```text
A: Si-style near-duplicate rate
   weak/flat response

B: research-mode distribution
   strong evidence-mixture response
```

This figure should make the paper understandable without reading the method.

### Figure 2 — Evidence mixture dose response

For each model family:

```text
x = fraction of framing A in matched evidence packet
 y = P(output mode A)
```

Include no-context prior as horizontal reference.

### Figure 3 — Held-out natural RAG prediction

Observed vs predicted research-mode distribution on held-out seeds.

Compare:

```text
prior-only
prior + evidence composition
```

### Figure 4 — Abstraction hierarchy

Context response at L0–L4.

Even in strong-steerability branch, response may attenuate with abstraction.

### Figure 5 — Sampling breadth vs search direction

Temperature / generation-diversity method increases within-context breadth, but the evidence-conditioned directional shift remains.

## 1.6 Main contributions

Only claim those supported by data:

1. **Controlled evaluation:** a matched-evidence protocol for studying context-driven scientific search rather than generic idea quality.
2. **Empirical phenomenon:** evidence composition redistributes high-level scientific choices beyond prompt and source-identity effects.
3. **Measurement finding:** duplicate-based idea diversity can miss directional search-space steering.
4. **Predictive mechanism:** controlled evidence-response coefficients explain held-out natural-RAG behavior.
5. Optional: post-training changes scientific context steerability.

## 1.7 Reviewer #2 attack

> Of course a model follows the type of literature you show it.

### Paper must answer with data

- within-mode paper swaps produce much smaller high-level changes than cross-mode swaps;
- lexical-normalized contexts retain effect;
- relevance matched;
- response is nonlinear/asymmetric/model-dependent rather than trivial copying;
- controlled model predicts natural RAG.

If none of these deeper effects appear, do not use Blueprint A.

---

# 2. Blueprint B — Grounded but Prior-Bound

## 2.1 Candidate title

**Grounded but Prior-Bound: Can Retrieval Steer LLM Scientific Hypothesis Search?**

Alternative:

**Grounded, Not Steered: Hierarchical Context Reliance in Scientific Ideation**

This is currently the most distinctive possible paper shape.

## 2.2 One-sentence result, conditional

> LLMs reliably incorporate retrieved sources and concepts, yet counter-prior literature has disproportionately weak influence on high-level scientific methods and problem framing, revealing a hierarchy between evidence grounding and scientific steerability.

## 2.3 Why this could be strong

RAG systems are commonly described as grounded when generated text accurately uses external evidence. But for scientific discovery, grounding is not sufficient: the external literature must be able to change which hypotheses, methods, and failure modes are explored.

A strong result would expose a capability gap:

```text
retrieved paper is read        yes
retrieved facts are used       yes
retrieved mechanism is used    often
method choice changes          less
research mode changes          weakly
central question changes       weakest
```

This would connect scientific ideation to ICLR work on context-parametric inversion / in-context steerability while adding a new open-ended, hierarchical failure mode.

## 2.4 Abstract skeleton

### Motivation

Retrieval-augmented research agents are increasingly evaluated for citation accuracy, relevance, novelty, or final idea quality. These measures do not distinguish whether retrieved evidence merely grounds generated text or actually redirects high-level scientific search.

### Question

Can counter-prior literature move an LLM away from its default scientific methodology distribution?

### Method

Measure no-context research-mode priors using temporally clean post-cutoff ICLR questions, independently confirm those priors, and intervene with matched prior-congruent/counter-prior evidence mixtures. Measure context uptake from source attribution to problem framing.

### Conditional findings

Insert only if observed:

- L0/L1 uptake high;
- L3/L4 counter-prior response weak or thresholded;
- prior-congruent reinforcement > counter-prior override;
- hierarchy robust to lexical normalization, prompt/order and temperature;
- stronger resistance after instruction tuning or in specific model families;
- natural top-k retrieval sits in prior-bound regime.

### Conclusion

Literature grounding and scientific steerability are distinct capabilities; research-agent evaluation should measure both.

## 2.5 Figure plan

### Figure 1 — Grounding vs steering

The flagship figure:

```text
Context uptake
1.0 | █████████  L0 source
    | ████████   L1 concept
    | █████      L2 method
    | ███        L3 research mode
    | ██         L4 central framing
0.0 +------------------------------
```

Use actual uncertainty and model stratification; never force monotonicity in visualization.

### Figure 2 — Prior-congruence asymmetry

Compare equal-strength evidence:

```text
prior-congruent reinforcement
vs
counter-prior override
```

A strong asymmetry is more interesting than a global weak-context effect.

### Figure 3 — Dose-response / threshold

Counter-prior fraction vs high-level mode shift.

Show whether critical mass is required.

### Figure 4 — Base vs instruction-tuned pair

If valid:

```text
base / pretrained
vs
instruction tuned
```

Separate valid-output rate from context response.

### Figure 5 — Natural RAG

Show that ordinary top-k packets are genuinely grounded but their high-level influence is predictable from prior/context competition.

## 2.6 Contributions

1. Distinguish **scientific grounding** from **scientific steerability**.
2. Identify a hierarchy of context uptake across scientific abstraction levels.
3. Characterize prior-congruence asymmetry / threshold behavior.
4. Show whether post-training/model family changes that hierarchy.
5. Provide an evaluation protocol for retrieval-augmented research models that goes beyond citations and final quality scores.

## 2.7 Reviewer #2 attack

> This is just context-parametric inversion applied to research questions.

### Required answer

The scientific setting differs fundamentally:

- no single correct contextual answer;
- context encodes alternative valid scientific strategies, not counterfactual facts;
- target is a distribution over open-ended research modes;
- context uptake can be evaluated hierarchically;
- prior itself must first be estimated from repeated generation;
- natural-RAG prediction links controlled behavior to real retrieval pipelines.

If the paper only reports a single context-following percentage, this attack wins.

---

# 3. Blueprint C — Trivial / Null Result

## 3.1 No paper should be forced

Examples:

### C1 — trivial priming

Evidence condition predicts outputs only because explicit method words are copied.

### C2 — taxonomy failure

Human raters cannot reliably distinguish research modes/problem framing.

### C3 — relevance confound

Counter-prior evidence is systematically less relevant/valid.

### C4 — no robust context response and no grounding hierarchy

Neither high-level shift nor interesting resistance is reproducible.

### C5 — result only in one model / one subfield

No broad ICLR claim.

### C6 — direct collision appears

A new concurrent paper performs equivalent matched prior/counter-prior evidence intervention and obtains the same hierarchy.

## 3.2 What may still be reusable

- temporally clean ICLR ideation dataset;
- annotation taxonomy;
- evidence matching infrastructure;
- natural-RAG prediction pipeline;
- negative methodological findings.

But do not manufacture an ICLR submission solely from the infrastructure.

---

# 4. Result-free Introduction architecture

The opening can be drafted conceptually without assuming the answer.

## Paragraph 1 — Deployment reality

Research agents increasingly retrieve literature before generating hypotheses. Retrieval is therefore part of the model's inference-time environment, not merely a citation backend.

## Paragraph 2 — Missing distinction

Current evaluation tends to measure final quality, novelty, citation accuracy, or text diversity. These metrics do not tell us whether literature changes the high-level scientific search distribution.

## Paragraph 3 — Existing tension

- scientific ideation models exhibit strong generation priors / limited diversity;
- RAG quantity can have little effect on coarse duplicate measures;
- general ICLR research shows post-trained models can resist context when it must override strong priors.

## Paragraph 4 — Our question

> When retrieved evidence supports a scientifically valid direction that conflicts with an LLM's default research strategy, what changes?

## Paragraph 5 — Experimental idea

Estimate a no-context prior, then hold relevance/amount constant while varying framing composition of temporally clean ICLR literature.

## Paragraph 6 — Results

Do not write until observed. The entire paper must pivot honestly between Blueprint A/B/C.

---

# 5. Result-free Related Work architecture

### Scientific ideation quality/diversity

Si et al. 2025; LiveIdeaBench; SCI-IDEA; MoRI; other research-agent systems.

Message: these establish ideation as a serious evaluation object but do not isolate high-level prior-vs-context response.

### Context reliance / in-context steerability

Context-Parametric Inversion; Controllable Context Sensitivity; Spectrum Tuning.

Message: these establish generic context-prior competition; our setting is open-ended scientific choice distributions.

### Retrieval and scientific inspiration

SciPIP / Graph2Idea / MIR / ResearchBench / MUSES.

Message: these ask what to retrieve/how to generate; we causally test whether the generator *acts on* alternative but equally relevant scientific evidence.

### Diversity and selection bias

Padmakumar & He; STARS; BiasBusters.

Message: controlled population-level or matched-alternative interventions provide methodological precedents; our target is high-level scientific search direction.

---

# 6. What would make this look like an Outstanding-style ICLR paper?

Not required for acceptance, but useful as a quality target.

The strongest story would be a **simple distinction that explains several existing observations**:

> **Grounding ≠ steering.**

It could unify:

- why RAG paper count barely changes duplicate diversity;
- why scientific LLMs exhibit concentrated methodology choices;
- why systems can cite/use literature yet still generate conventional proposals;
- why generation-side diversity interventions may not change the direction of search;
- why post-training can improve instruction following while reducing distributional context flexibility.

Then a simple diagnostic — hierarchical context-uptake curves + counter-prior matched interventions — could become reusable outside scientific ideation.

This would be much stronger than inventing another agent.

---

# 7. Pre-mortem ICLR scores

These are not predictions of actual reviewer scores; they are quality gates.

## Blueprint A if executed weakly

- Soundness: 3/4
- Significance: 2/4
- Novelty: 2/4
- Main objection: obvious priming
- likely overall: borderline

## Blueprint A if held-out prediction + metric dissociation + controls succeed

- Soundness: 4/4
- Significance: 3/4
- Novelty: 3/4
- likely overall: strong accept territory depending execution

## Blueprint B if hierarchy is robust

- Soundness: 4/4
- Significance: 3–4/4
- Novelty: 3–4/4
- Main objection: extension of context-prior literature
- best defense: open-ended scientific distribution + hierarchical uptake + post-training / natural-RAG generalization

## Blueprint C

Do not submit merely because a deadline exists.

---

# 8. Current preferred paper target

Before data, prioritize the experimental design needed to distinguish A from B.

Do **not** optimize for the Grounded-but-Prior-Bound answer.

The ideal project is one in which either result teaches us something precise:

```text
If evidence strongly moves high-level research choices:
    quantify scientific steerability and show duplicate metrics miss it.

If evidence is read but fails to move high-level choices:
    establish grounding-without-steering and characterize the hierarchy.

If neither produces a deeper structure:
    kill the paper.
```

That is the current research contract.
