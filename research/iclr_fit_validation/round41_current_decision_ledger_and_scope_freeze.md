# Research Round 41 — Current Decision Ledger and Scope Freeze

## 1. Purpose

After many collision/design rounds, the project has enough experimental depth. Continuing to add conditions without a decision hierarchy would reduce clarity and create researcher degrees of freedom.

This round consolidates what is ACTIVE, SECONDARY, HISTORICAL, FORBIDDEN, and what evidence is still missing.

No scientific treatment outcomes exist in the repository at this point.

---

# 2. Current project status

```text
Decision: KEEP / CONDITIONAL GO
Current execution stage: F0 SOURCE-ONLY FEASIBILITY
Scientific generation: NOT AUTHORIZED
```

The project is conceptually ICLR-shaped but empirically unvalidated.

---

# 3. Active core research question

> **For an open-ended ICLR research problem with multiple scientifically valid strategies, how does changing the composition of equally relevant real scientific literature change an LLM's high-level research choice, and can this response explain behavior under ordinary retrieval?**

Secondary mechanism question:

> Does the strength/direction of evidence-conditioned choice depend on the model × seed's independently measured no-context baseline route propensity?

---

# 4. Active core object

For model `M`, seed `x`, evidence packet `C_alpha`, open-ended proposal `Y`:

```text
Y ~ P_M(Y | x, C_alpha)
```

Primary measured variable:

```text
human-blinded ordinal A/B route score
S ∈ {-2,-1,0,+1,+2}
```

Primary causal intervention:

```text
alpha = fraction of Route-A evidence
        at fixed context amount and matched relevance
```

---

# 5. Active confirmatory hypotheses

## H1 — Evidence-conditioned scientific choice

Matched real scientific evidence composition changes high-level route choice.

## H2 — Baseline-conditioned response

The magnitude/geometry of the evidence response depends systematically on independently measured no-context route propensity.

## H3 — Controlled-to-natural generalization

A response model fitted on controlled evidence mixtures improves held-out prediction of the same LLM's route choices under ordinary top-k retrieval relative to baseline-only prediction.

H1 is foundational. H2/H3 elevate the work from context sensitivity to explanatory regularity.

---

# 6. Minimum viable ICLR paper

A main paper is viable only if the evidence chain includes:

```text
valid multi-route seeds
+
scientific equipoise
+
relevance-matched evidence
+
randomized/frozen route composition
+
blinded human outcome measurement
+
replication across >=2 model families
+
nontrivial route response or rigorous informative alternative
+
at least one strong anti-priming/mechanism result
+
held-out natural-RAG validation for the broad mechanism claim
```

Do not substitute a large number of raw generations for any missing link.

---

# 7. Required experiments — CORE

## Core E0 — Source feasibility / validity

Current bottleneck.

Must determine whether enough ICLR 2025 evidence and ICLR 2026 seeds support clean blocks.

## Core E1 — P0 variance/construct pilot

Only after F0/F1 approval.

Three alpha values:

```text
0, .5, 1
```

Purpose: validate output quality, annotation, packet variance, approximate effect/precision.

## Core E2 — Confirmatory five-level evidence mixture

```text
0, .25, .5, .75, 1
```

Multiple packets, multiple models, seed-clustered inference.

## Core E3 — No-context baseline

Measured only after treatments are frozen.

## Core E4 — Anti-priming control

At least one strong route-effect validation, preferably multiple:

- PF/PFL content normalization;
- direct-copy exclusion;
- cross-route > within-route document replacement.

## Core E5 — Held-out natural RAG prediction

Required for a strong general RAG/mechanism claim.

---

# 8. High-value secondary experiments

Run only if the core survives.

## S1 — Evidence component knockout

RAW / PF / PFM / PFL.

## S2 — Abstraction uptake profile

Source → concept → method → research route → problem framing.

## S3 — Same-family base vs instruction-tuned

Connect response behavior to post-training.

## S4 — Three-route simplex

Only if F0 finds many 3+ route seeds.

## S5 — Local matched document replacement / attribution bridge

Mechanism robustness.

## S6 — Frontier closed-model external validity

Not part of causal-clean core.

## S7 — MUSES generative-root extension

Potential separate/high-upside extension. Must not distract from primary paper.

---

# 9. Historical motivations — no longer main claims

The following remain useful background only:

```text
AI-assisted research monoculture
shared retrieval causes topic convergence
retrieval is a hidden inductive prior
generic context-vs-prior competition
LLMs have narrow scientific-method priors
grounding without steering
relevance is not discovery utility
```

Some are already covered by recent literature; others are too broad for the core ICLR paper.

---

# 10. Claims explicitly forbidden unless later evidence/literature radically changes

Do not claim:

- first scientific ideation with LLMs;
- first literature-grounded ideation;
- first shared-context research-idea evaluation;
- first evidence-grounded/corpus-first research discovery;
- first context-vs-prior study;
- first in-context steerability study;
- first proof LLMs have method priors;
- first demonstration external stimuli change ideas;
- first demonstration retrieval affects scientific proposals;
- first human evaluation of LLM research ideas;
- generic `RAG makes ideas diverse/homogeneous`.

---

# 11. Preferred pre-result terminology

Use:

```text
baseline route propensity
```

rather than intrinsic `scientific prior` in formal analysis.

Use:

```text
evidence-conditioned scientific choice response
```

rather than claiming a new form of steerability.

Use:

```text
matched scientifically plausible alternative routes
```

rather than `equivalent routes` unless human audit supports strong equipoise.

---

# 12. Current neutral working title

> **Same Relevance, Different Research Choices: How Scientific Evidence Shapes LLM Hypothesis Search**

Alternative:

> **Evidence-Conditioned Scientific Choice in Large Language Models**

Outcome-specific titles are not selected before data.

---

# 13. Core model plan

Causal core:

```text
Llama 3.1 family
Gemma 3 family
```

Common strict evidence date rule:

```text
first public > 2024-08-31
```

Pilot likely uses smaller/mid checkpoints; confirmatory may include larger family checkpoints if compute permits.

Closed frontier models remain external validity.

---

# 14. Generalization target

The paper does **not** target all scientific questions.

Primary target population:

> ICLR-like technical research problems for which contemporaneous literature supports at least two independently plausible, relevance-matchable scientific routes.

Report full attrition/eligibility rate.

Seed is the primary cluster/generalization unit when multiple route pairs share a seed.

---

# 15. Current paper-strength ladder

## Level 0 — Not publishable as intended

Raw abstracts cause lexical/method copying only.

## Level 1 — Controlled behavior

Matched evidence composition changes high-level route choice.

Interesting but potentially incremental.

## Level 2 — General regularity

Effect depends systematically on baseline, abstraction, or evidence component and survives anti-priming controls.

Strong ICLR candidate.

## Level 3 — Explanatory bridge

Controlled response predicts held-out natural-RAG choices.

Strong paper identity.

## Level 4 — Broader ML principle

Same-family post-training or multi-route geometry reveals a systematic model-property change.

High-upside extension, not required.

---

# 16. Current kill conditions

Kill or fundamentally pivot if any becomes clear:

1. real ICLR corpus cannot support enough source-valid/equipoise blocks;
2. seed route choice cannot be human-annotated reliably;
3. matched A/B alternatives are systematically unequal in scientific plausibility/relevance;
4. P0 precisely indicates a scientifically trivial high-level effect with no deeper pattern;
5. RAW effect disappears under all anti-priming controls;
6. result exists only in one family/hand-picked route type;
7. controlled response has no explanatory bridge to natural RAG and no strong model-behavior mechanism;
8. a direct contemporaneous paper occupies the combined causal question.

---

# 17. Research scope freeze rule

From this round onward, **do not add a new major experiment merely because it sounds interesting**.

A new experiment is justified only if it:

```text
A. resolves a critical reviewer objection;
B. tests a pre-existing core mechanism explanation;
C. provides necessary external validity;
D. is triggered by a material new collision/source-feasibility finding.
```

Otherwise defer it.

This rule prevents the project from becoming a collection of unrelated analyses.

---

# 18. Current next action

Wait for / complete:

```text
experiments/idea_collapse/feasibility_1/FEASIBILITY_RESULT.md
```

Then research lead performs PI review against Rounds 27/30/33/36 and authorizes either:

```text
F1 construct audit
or
KILL / redesign
```

No scientific generation is authorized yet.

## Decision

**SCOPE FROZEN AROUND H1–H3. CURRENT BOTTLENECK = SOURCE FEASIBILITY.**