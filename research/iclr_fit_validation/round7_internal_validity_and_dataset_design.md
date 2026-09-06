# Round 7 — Internal Validity, Temporal Cleanliness, and Reviewer-Proof Experimental Design

> Date: 2026-09-06  
> Purpose: attack Round 6 before spending on large-scale generation.  
> Scope: ICLR-only empirical universe and ML claims.

---

## 0. Executive conclusion

Round 6 yields a promising ICLR question, but a naive implementation would still be easy to reject.

The four most dangerous false-positive mechanisms are:

1. **Winner's-curse prior estimation** — using noisy no-context outputs to pick a “strong prior” and then comparing against the same estimate.
2. **Relevance confounding** — counter-prior literature may simply be weaker / less relevant than prior-congruent literature.
3. **Lexical/method imitation** — the model may copy words or methods explicitly present in the context; that is not a deep search-space effect.
4. **Training-data contamination** — the generator may already know the seed/evidence papers, making “context uptake” hard to interpret.

The experiment should therefore become a **cross-fitted, temporally clean, matched-context intervention** with a natural-RAG validation stage.

---

## 1. Use two model families with documented knowledge cutoffs for the causal core

### Family A — Llama 3.1

Meta's model card reports a **December 2023** pretraining data cutoff for Llama 3.1.

Useful checkpoints:

- `Llama-3.1-8B` / `Llama-3.1-8B-Instruct`
- `Llama-3.1-70B` / `Llama-3.1-70B-Instruct` if inference resources permit.

Advantages:

- documented cutoff;
- base/instruct pair;
- long context;
- widely studied, reviewer-recognizable family.

### Family B — Gemma 3

Google's Gemma 3 model card reports an **August 2024** knowledge cutoff and provides pretrained / instruction-tuned variants.

Useful sizes:

- 12B / 27B depending resources.

Advantages:

- later but documented cutoff;
- base/instruct comparison aligns directly with Spectrum Tuning's post-training question;
- second independent architecture/training family.

### Frontier closed models

Use one or more frontier APIs only as **external-validity extensions**, not as the only causal evidence, because training cutoffs/corpora may be incomplete or hard to audit.

---

## 2. Temporally clean ICLR corpus

For the causal core, construct evidence from ICLR papers first publicly available **after the latest causal-core model cutoff**.

Conservative global cutoff:

```text
2024-08-31
```

### Preferred source corpus

ICLR 2025 accepted papers satisfying:

- submission/preprint first-public date > 2024-08-31;
- no evidence of an earlier public version before cutoff;
- title + abstract + public metadata available;
- topic can be assigned to one of selected subfields;
- research-mode annotation is auditable.

Optional ICLR 2026 papers can expand evidence later, but use ICLR 2025 first for a clean, simple temporal story.

### Why not use ICLR 2023–2024 as the primary evidence corpus?

Llama 3.1 may not know 2024 papers after December 2023, but Gemma 3 can have knowledge through August 2024. A unified post-August-2024 evidence corpus avoids model-specific contamination rules.

---

## 3. Seed-question construction

### Preferred seed source

ICLR 2026 accepted papers or 2025–2026 public submissions whose research questions postdate the model cutoff.

For each focal paper:

1. extract a **method-agnostic research question / problem statement**;
2. remove title, authors, dataset/model names introduced by the focal paper, and explicit solution description;
3. never expose the focal paper's abstract/method to the generator;
4. exclude the focal paper from all evidence candidates;
5. preferably restrict evidence to material publicly available before the focal paper's first-public date for a realistic “what could have been read” condition.

### Important semantic rule

The real paper's method is **not a gold-standard optimal answer**. It can be used only as a descriptive reference / contamination diagnostic.

---

## 4. Cross-fitted prior estimation

Do not use one noisy no-context batch for both selecting priors and estimating treatment displacement.

For each `model × seed`:

### P0-DISCOVERY

Generate an initial no-context batch and estimate the candidate dominant research mode(s).

Purpose:

- determine whether a usable prior exists;
- select prior-congruent and candidate counter-prior framing.

### P0-CONFIRM

Generate a fresh, independent no-context batch **after the A/B definition is frozen but before treatment outcomes**.

Purpose:

- provide an unbiased prior baseline;
- verify that the apparent prior reproduces.

### Eligibility rule

A seed enters the confirmatory treatment set only if:

- the dominant/underrepresented mode relationship reproduces directionally in P0-CONFIRM; AND
- both A/B directions have sufficiently relevant real ICLR evidence.

Seeds failing this rule remain in the repository and are reported as `prior_not_stable` or `evidence_not_matchable`; they are not quietly deleted.

### Analysis implication

Use P0-CONFIRM, never P0-DISCOVERY, as the no-context comparator in the primary causal effect.

---

## 5. Avoid choosing only extreme/easy seeds

Selecting only seeds with enormous prior skew may make the paper about a cherry-picked subset.

Use two strata:

```text
STRONG_PRIOR
MODERATE_PRIOR
```

and report eligibility rate among all candidate seeds.

Prefer a continuous `prior_strength` variable in the hierarchical analysis rather than only a hard threshold.

Key test:

> Is counter-prior context response weaker when the model's pre-existing prior is stronger?

This prior-strength × evidence interaction is more informative than a simple average effect.

---

## 6. Evidence-packet matching — formal design

For each seed `x`, generate a candidate evidence pool from the frozen ICLR corpus.

### Step 1 — relevance floor

Use a retrieval stack such as:

```text
dense retrieval → top-N candidate pool → cross-encoder/reranker relevance
```

Freeze retriever/reranker versions before outcomes.

### Step 2 — mode annotation

Annotate every candidate paper's primary research mode using only its public paper content, independent of generated outcomes.

### Step 3 — propensity/matching features

For each candidate paper record:

- dense relevance;
- reranker relevance;
- abstract token length;
- year;
- topic cluster;
- venue (ICLR fixed for primary corpus);
- public status/date;
- optional citation count only if measured at one frozen date;
- evidence research mode.

### Step 4 — pair/match

For A/B packet construction, optimize balance on the above covariates subject to mode contrast.

Report standardized mean differences and overlap plots before scientific generation.

### Hard matching gate

Do not proceed for a seed if A/B packets cannot achieve an acceptable pre-specified relevance overlap.

---

## 7. Prevent trivial lexical priming from becoming the whole result

If a packet contains twelve papers repeatedly saying “benchmark/evaluate” and the model then proposes a benchmark, a reviewer can call it lexical imitation.

Use four complementary protections.

### 7.1 High-level endpoints

Primary outcome is research-mode / problem-framing shift, not keyword overlap.

### 7.2 Exact-method copying diagnostic

Measure whether generated methods are exact/near matches to methods in supplied evidence.

Strong result:

> research mode changes even when exact method copying is low.

### 7.3 Content-normalized evidence robustness

For a subset, build a standardized evidence representation that preserves:

- problem;
- empirical finding;
- mechanism/limitation;

while removing:

- paper title/authors;
- explicit “future work” prescriptions;
- boilerplate section language;
- direct research-mode labels.

The normalization pipeline must be frozen and manually audited before generation.

If high-level steering persists under content-normalized context, it is harder to dismiss as superficial imitation.

### 7.4 Category-word sensitivity audit

Quantify whether treatment classification can be predicted merely from a small lexicon (`benchmark`, `improve`, `failure`, `mechanism`, etc.).

If a trivial bag-of-words classifier nearly perfectly distinguishes A/B packets, report it and use the content-normalized condition as the stronger result.

Do not pretend lexical cues do not exist.

---

## 8. Natural-RAG validation — crucial external-validity stage

Controlled mixtures are intentionally artificial. The strongest validation is to predict behavior under a real retriever.

### Procedure

1. Fit evidence-response relationships using only controlled A/B mixture experiments.
2. Freeze the model.
3. For held-out seed questions, run natural top-k retrieval from the same ICLR corpus.
4. Annotate the naturally retrieved packet's mode composition.
5. Predict the generated research-mode distribution from the packet composition + no-context prior.
6. Compare predicted vs observed natural-RAG outputs.

### Why this is important

If controlled packet composition predicts real top-k RAG behavior, the mechanism generalizes beyond an artificial treatment setup.

This is likely one of the most valuable experiments in the paper.

---

## 9. Hierarchical uptake should distinguish imitation from reasoning

Refine L0–L4:

### L0 ATTRIBUTION

Does the output refer to supplied sources/entities?

### L1 EVIDENCE CONTENT

Does it use supplied findings/phenomena accurately?

### L2 METHOD FAMILY

Does the intervention/method family change?

### L3 SCIENTIFIC MOVE

Does the proposal switch among Build / Diagnose / Measure / Explain / Optimize / Falsify?

### L4 CENTRAL QUESTION

Does the core problem/failure/causal target change?

### Additional diagnostic: Novel recombination

Classify whether the idea:

- copies a source method;
- combines source components;
- transfers a source framing to a new target;
- proposes a high-level direction absent from any one paper.

This helps distinguish context following from simple retrieval copying.

---

## 10. Negative controls

### 10.1 Evidence-order control

Permute document order. No substantive change should be attributed to mode composition if order dominates.

### 10.2 Prompt-paraphrase control

Estimate task-prompt sensitivity as a noise floor.

### 10.3 Mode-preserving packet swap

Swap papers within the same research mode and relevance stratum.

Expected:

- some low-level/source changes;
- much smaller high-level research-mode change than cross-mode packet swaps.

This is an excellent control because it separates **document identity effects** from **framing-composition effects**.

### 10.4 Natural top-k

Not a negative control, but establishes where ordinary RAG lies relative to the experimental curve.

---

## 11. Sampling diversity control

Scientific search direction and sample diversity are distinct.

Within selected contexts run:

```text
T_low
T_standard
T_high
```

Optionally include one established generation-diversity intervention.

Report two axes:

```text
within-context breadth
between-context directional shift
```

Possible strong finding:

> high temperature increases breadth but does not eliminate a strong default research-mode prior or context-response asymmetry.

This would directly separate our phenomenon from STARS-style generic mode-collapse mitigation.

---

## 12. Base vs instruction-tuned comparison

This is a high-value secondary experiment because ICLR 2025/2026 work suggests post-training can alter context reliance / steerability.

For Llama 3.1 and Gemma 3, compare paired pretrained vs instruction-tuned checkpoints.

### Separate validity from steerability

Base models may produce invalid/unstructured answers more often.

Report:

- valid-output rate;
- task relevance;
- steerability conditional on valid output;
- unconditional outcome as sensitivity analysis.

Do not interpret “base model changes more” as better if it is simply less task-coherent.

---

## 13. Annotation strategy

### Stage 1 — manual schema development

Use source corpus + no-context outputs only, no treatment outcomes.

### Stage 2 — independent audit

Two independent annotators on a stratified sample.

### Stage 3 — scalable parser

After schema freeze, use an LLM parser/classifier if needed.

### Stage 4 — blinded outcome audit

Human/independent annotation of a treatment-stratified sample with condition labels hidden.

### Reliability principle

Report agreement separately for each abstraction level. If L4 central-question framing has low reliability, do not hide this under an aggregate score; downgrade L4 to exploratory.

---

## 14. Statistical model improvements

### Cross-fitted baseline

Use P0-CONFIRM as prior comparator.

### Example high-level model

For output mode `j`:

```text
logit P(Y=j)
 = β_j
 + u_seed,j
 + u_model,j
 + βmix,j * evidence_fraction_j
 + βprior,j * prior_strength_j
 + βint,j * evidence_fraction_j × prior_strength_j
 + nuisance/order terms
```

### Natural-RAG prediction

Out-of-sample compare:

```text
Prior-only model
vs
Prior + evidence-composition model
```

Use held-out seed questions.

### Generalization target

The meaningful target is average behavior over ICLR research questions, not thousands of correlated generations from a few prompts.

Use seed-level bootstrap / hierarchical uncertainty.

---

## 15. Precision-based scaling rather than arbitrary sample counts

The first 24-seed × 2-model pilot is for validating treatment construction and estimating variance.

After pilot, determine full sample size using a pre-specified precision target, e.g.:

> expand until the 95% interval for the average high-level counter-prior treatment effect is narrower than a fixed scientifically meaningful tolerance, subject to a predeclared maximum budget.

Do not repeatedly peek and stop when significance is reached.

If a fixed-N design is operationally easier, freeze it before full-scale outcomes.

---

## 16. Quality / validity guardrail

A counter-prior idea must still be a plausible answer to the seed question.

Blindly audit:

- relevance to seed;
- internal coherence;
- testability;
- feasibility at a coarse level;
- whether the proposal is actually supported by the supplied evidence.

The paper does not need to prove that counter-prior outputs are *better*, but it must rule out the possibility that apparent steerability is merely loss of scientific validity.

---

## 17. Contamination protocol

For every causal-core model record:

- official knowledge/data cutoff;
- evidence paper first-public date;
- focal/seed paper first-public date;
- any earlier arXiv/workshop version found.

### Primary clean subset

Require evidence and seed paper public dates after the latest documented model cutoff used in the clean causal analysis.

### Contamination diagnostics

Before context treatment, ask models controlled questions about identifying titles/methods from masked descriptions only as an exploratory memorization check.

Do not rely solely on self-reported “I have not seen this paper.”

### Frontier models

Report separately as external-validity results, not pooled with the clean subset.

---

## 18. Strongest possible Figure 1 design

A figure with two paired panels could make the paper immediately understandable.

### Left — evidence visibly enters the answer

```text
counter-prior evidence fraction ↑
source/concept uptake ↑ strongly
```

### Right — high-level scientific move

Possible prior-bound outcome:

```text
counter-prior evidence fraction ↑
research-mode shift ↑ only weakly / thresholded
```

or steerable outcome:

```text
research-mode shift follows a calibrated dose-response
```

This exposes the difference between **being grounded** and **being steered**.

---

## 19. Reviewer-proof claim hierarchy

### Minimum publishable claim

> Matched literature context causes robust changes in high-level scientific choices beyond prompt/order noise, and existing duplicate metrics do not capture the effect well.

### Stronger claim

> The magnitude/direction of context response is predictable from evidence composition and the model's no-context prior on held-out ICLR questions.

### Strong prior-bound claim

> Context response decreases with scientific abstraction and is asymmetric against strong default method priors, despite verified source/concept grounding.

### Strongest extension

> Post-training systematically strengthens the prior-bound hierarchy or reduces counter-prior scientific steerability across paired checkpoints.

Do not jump to the stronger language without corresponding evidence.

---

## 20. Updated decision

The topic survives another hostile design review.

However, **the experiment is only worth doing if we execute the cross-fitted prior, matched evidence, temporal-clean subset, mode-preserving negative control, and natural-RAG prediction.**

Without those elements, a skeptical ICLR reviewer can plausibly reduce the story to:

> “Models are primed by the papers in their prompt.”

With them, the paper tests a substantially deeper property:

> **how strongly and at what abstraction levels can scientific evidence move an LLM away from its learned/default research prior?**

---

## Sources added in this round

- Meta Llama 3.1 official model card — knowledge cutoff December 2023: https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md
- Google Gemma 3 official model card — knowledge cutoff August 2024: https://ai.google.dev/gemma/docs/core/model_card_3
- Carlon et al., *Thinking Like a Scientist?*: https://arxiv.org/abs/2606.26130
- Spectrum Tuning, ICLR 2026: https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html
