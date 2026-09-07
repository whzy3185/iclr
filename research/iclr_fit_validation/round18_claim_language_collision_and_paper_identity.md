# Research Round 18 — Claim-Language Collision and Paper-Identity Refinement

## 1. Trigger

The latest direct/adjacent scan found 2026 work that makes `grounding without steering` and `grounded but prior-bound` less attractive as title-level novelty, even though our controlled experiment remains distinct.

This round separates:

- the **scientific object** we can still claim;
- outcome-dependent interpretation language;
- language that should not be presented as if newly coined by this project.

---

## 2. New adjacent evidence

### 2.1 Grounded autonomous research — 2026

*Grounded autonomous research: a fault-tolerant LLM pipeline from corpus to manuscript in frontier computational physics* reports that unscaffolded agents can cite literature without adequately confronting/calibrating against it, and uses explicit literature-based calibration checkpoints as an engineering mechanism.

Source:

- https://arxiv.org/abs/2607.02329

Collision level: **conceptual, not experimental**.

It does not perform our matched A/B scientific-route intervention, baseline-route measurement, or evidence-response modeling. But it weakens any broad novelty claim that `scientific agents can cite literature without letting it change scientific reasoning`.

### 2.2 Grounding Without Corrective Control — 2026

*Grounding Without Corrective Control: Truth-Tracking Profiles for Large Language Models* explicitly separates representational grounding from live corrective routes and argues that surface grounding can diverge from truth-tracking/corrective control.

Source:

- https://arxiv.org/abs/2608.14252

Collision level: **terminological/conceptual**.

This is not a scientific-ideation experiment, but `grounding without ...` is now clearly an occupied framing.

### 2.3 MetaMuse — ICLR 2026

MetaMuse already shows external stimuli can move LLM algorithm ideation away from familiar designs.

Source:

- https://proceedings.iclr.cc/paper_files/paper/2026/hash/85632be2cd69e9a0ef4ba054c096fac9-Abstract-Conference.html

Therefore, if our evidence packets produce a route shift, `external context steers ideas` remains insufficient.

### 2.4 Spectrum Tuning — ICLR 2026

Spectrum Tuning owns the general `in-context steerability` framing and explicitly studies overriding priors to reach novel output distributions.

Source:

- https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html

Thus our contribution must be a specific scientific-evidence response phenomenon, not a new definition of steerability.

---

## 3. Paper identity — what remains distinctive

The core paper should be identifiable without any of the following phrases:

- research monoculture;
- grounding without steering;
- scientific prior as a new concept;
- in-context steerability as a new concept;
- AI scientists ignore evidence.

The distinctive object is:

> **How the composition of equally relevant, real scientific literature changes an LLM's distribution over multiple valid research routes, with treatments frozen independently of model behavior and response modeled relative to an independently estimated no-context baseline.**

The distinctive validation is:

> **Controlled evidence-response estimates are tested for predictive value under held-out natural retrieval.**

This is the identity to preserve.

---

## 4. Preferred pre-result question

Use a neutral research question before outcomes:

> **How does scientific evidence composition affect LLM research-route choice under open-ended, multi-valid scientific problems?**

Secondary question:

> **Does the effect of the same evidence depend on the model's independently measured no-context route propensity?**

This wording is less likely to overclaim than `Can retrieval override scientific priors?` and makes both strong-response and weak-response outcomes valid.

---

## 5. Preferred pre-result working title

Current safest working title:

> **Same Relevance, Different Evidence: Controlled Literature Interventions for LLM Research-Route Choice**

Alternative:

> **How Scientific Evidence Composition Shapes LLM Research Choices**

Avoid freezing a result in the title before data exist.

---

## 6. Outcome-conditioned titles only after results

### Branch A — strong high-level response

Possible title:

> **Same Relevance, Different Science: Evidence Composition Redirects LLM Research Choices**

Required evidence:

- matched A/B route-response curves;
- multiple route pairs/models/seeds;
- effect survives anti-priming package;
- held-out natural-RAG prediction improves.

### Branch B — baseline-dominated / asymmetric response

Do not use `Grounded but Prior-Bound` as if it is novel terminology.

Possible title:

> **Reading Is Not Redirecting: Limits of Literature-Conditioned Research Choice in LLMs**

or

> **When Relevant Evidence Fails to Redirect LLM Research Choices**

Required evidence:

- verified source/concept uptake;
- weak/asymmetric high-level route displacement;
- stable relationship to independently measured baseline propensity;
- not explainable by invalid counter-route packets.

### Branch C — trivial priming/null

No paper identity should be manufactured.

---

## 7. Stronger novelty requirement after this round

Because neighboring work already covers:

- familiar-solution bias;
- external-stimulus steering;
- evidence neglect;
- context-vs-prior competition;
- grounding/corrective-control distinctions;

at least one of the following must become a central empirical contribution:

1. **baseline-dependent response law** — same evidence has systematically different leverage as a function of independent baseline route propensity;
2. **cross-abstraction response law** — source/concept/method/route/problem response follows a reproducible structure that predicts held-out behavior;
3. **controlled-to-natural prediction** — fitted response from artificial packets predicts ordinary top-k RAG route choices;
4. **metric dissociation** — standard ideation duplicate/diversity measures are nearly unchanged while high-level route distributions change materially;
5. **post-training/model-family regularity** — a consistent difference in route response across paired base/instruct or independent model families.

A simple positive treatment coefficient is no longer enough for an ambitious ICLR claim.

---

## 8. ICLR paper-shape analogy

The desired shape is closer to ICLR mechanism/behavior papers such as:

- Context-Parametric Inversion: surprising context reliance phenomenon + controlled studies + explanation;
- BiasBusters: controlled equivalent alternatives + source-of-bias isolation;
- Mixing Mechanisms: component phenomena + causal/predictive model;
- Does Writing with Language Models Reduce Content Diversity?: controlled population-level behavioral intervention.

Our paper should therefore have:

```text
clean behavior object
→ controlled intervention
→ nuisance elimination
→ response regularity
→ held-out prediction / mechanistic usefulness
```

not:

```text
new agent
→ better quality score
```

---

## 9. Direct-collision definition updated

A concurrent paper is now considered fatal/direct if it performs most of:

1. open-ended scientific ideation/research-route choice;
2. real literature context;
3. fixed quantity + matched relevance;
4. source-defined route contrast frozen before model output;
5. no-context baseline distribution measured independently;
6. dose-response evidence mixtures or equivalent counterfactual interventions;
7. high-level route/problem choice outcome;
8. anti-lexical/direct-copy controls;
9. baseline × evidence interaction or equivalent response law;
10. held-out natural retrieval prediction.

Papers covering one or two ingredients are strong neighbors but not direct collisions.

---

## 10. Codex status

No source-only feasibility deliverable is currently present.

No scientific generation is authorized.

The source-only feasibility task remains necessary because the largest remaining practical uncertainty is whether real ICLR 2025 evidence can provide enough high-relevance multi-route contrasts for unbiased ICLR 2026 seeds.

---

## 11. Decision

**KEEP / CONDITIONAL GO, with stricter novelty threshold.**

`Grounding without steering` is demoted from candidate paper identity to one possible interpretation of a specific response pattern.

The stable paper identity is now:

> **controlled, matched scientific-evidence interventions over open-ended LLM research-route choices, with independent baseline measurement and held-out natural-retrieval prediction.**
