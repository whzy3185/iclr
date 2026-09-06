# PRE-RUN AMENDMENT D — Cross-Fitting, Temporal Cleanliness, and Anti-Priming Controls

> Date: 2026-09-06  
> Status: **PRE-SCIENTIFIC-RUN AMENDMENT**  
> Repository state check immediately before writing: no `STATUS.md`, generated-outcome files, or `PILOT_RESULT.md` were present.  
> Purpose: strengthen Amendment C against prior-selection bias, training-data contamination, relevance imbalance, and trivial lexical imitation.

---

## 1. Cross-fit the no-context prior

The no-context prior must be estimated in two independent batches.

### P0-DISCOVERY

Used only to:

- identify candidate dominant / underrepresented research modes;
- determine whether a seed appears usable for prior-vs-context intervention;
- define candidate A/B evidence framing.

### P0-CONFIRM

Generated after A/B framing definitions are frozen and before treatment outcomes.

Used to:

- confirm prior direction;
- estimate the primary no-context baseline;
- calculate `prior_strength` used in confirmatory analysis.

### Rule

Primary treatment displacement must be calculated relative to **P0-CONFIRM**, not P0-DISCOVERY.

All failed prior replications remain recorded.

---

## 2. Temporally clean causal-core models

Prioritize models with documented cutoffs:

### Llama 3.1 family

Official pretraining cutoff: **December 2023**.

Use base/instruct pairs where feasible.

### Gemma 3 family

Official knowledge cutoff: **August 2024**.

Use pretrained/instruction-tuned pairs where feasible.

### Primary temporal-clean corpus rule

For the clean causal subset, source evidence papers must have first-public dates after:

```text
2024-08-31
```

and no discovered earlier public version before that date.

Prefer ICLR 2025 accepted papers that satisfy this rule.

Frontier/proprietary APIs with unclear contamination status may be included only as separate external-validity results.

---

## 3. Temporally clean seed problems

Prefer method-masked research questions derived from ICLR 2026 papers.

For each seed:

- remove title/authors;
- remove solution/method introduced by focal paper;
- exclude focal paper from retrieval corpus;
- record focal first-public date;
- where feasible restrict evidence to papers public before the focal paper.

The actual focal method is descriptive reference only, not a normative gold answer.

---

## 4. Prior selection must not cherry-pick only extremes

Track all candidate seeds and classify:

```text
stable_strong_prior
stable_moderate_prior
unstable_prior
insufficient_counterprior_evidence
```

Report eligibility rate.

Use continuous prior strength in analysis.

Do not quietly exclude moderate-prior seeds simply because effect sizes are smaller.

---

## 5. Evidence balance gate

Before treatment generation, produce `evidence_matching_report.md` showing condition balance on:

- dense relevance;
- reranker relevance;
- token length;
- public year/date;
- topic cluster;
- any optional popularity/quality covariate.

A seed cannot enter the confirmatory treatment run if A/B evidence is obviously separated in relevance or quality.

---

## 6. Mode-preserving packet-swap negative control

Add a key control:

> swap evidence documents while preserving the same research-mode composition and relevance strata.

This estimates document-identity sensitivity.

Expected interpretation:

```text
cross-mode packet swap effect
   >
within-mode packet swap effect
```

is evidence that framing composition matters beyond arbitrary document identity.

---

## 7. Lexical-priming diagnostics

### Exact-copy diagnostic

Record exact/near method overlap between supplied evidence and generated proposal.

### Bag-of-words treatment predictability

Train/evaluate a simple treatment classifier from packet text using pre-specified lexical features or a lightweight text baseline.

If A/B framing is trivially separable from words such as `benchmark`, `improve`, `failure`, `mechanism`, do not hide this.

### Content-normalized robustness subset

For a pre-specified subset, create standardized evidence summaries preserving:

- scientific problem;
- empirical finding;
- mechanism/limitation;

while removing:

- titles/authors;
- explicit future-work prescriptions;
- explicit research-mode labels;
- boilerplate method-section language where possible.

Freeze and manually audit the normalization pipeline before outcome generation.

This condition is secondary but important if lexical priming is strong.

---

## 8. Natural top-k RAG becomes a held-out validation target

Do not use natural top-k merely as another baseline.

### Procedure

1. Fit the evidence-response model on controlled framing-mixture treatments only.
2. Freeze model/analysis.
3. Run natural top-k retrieval for held-out seed questions.
4. Annotate natural packet composition using the frozen taxonomy.
5. Predict downstream research-mode distribution from:
   - no-context prior;
   - evidence composition.
6. Compare with observed natural-RAG generations.

### Key comparison

```text
prior-only predictor
vs
prior + evidence-composition predictor
```

A material held-out improvement is required for a strong “structured context prior” mechanism claim.

---

## 9. Source hierarchy endpoints

Retain Amendment C L0–L4, but explicitly add:

```text
COPY
COMBINE
TRANSFER
NEW_DIRECTION
```

as an exploratory recombination label indicating whether the model:

- copies supplied methodology;
- combines supplied components;
- transfers evidence framing to a new target;
- creates a direction not directly contained in one source.

Do not aggregate this into the primary endpoint unless annotation reliability is established.

---

## 10. Base-vs-instruct is secondary but pre-specified

If both checkpoint types are available:

- report valid-output rate separately;
- analyze context response conditional on valid scientific output;
- include unconditional sensitivity analysis;
- do not interpret incoherent base-model variability as superior steerability.

This comparison is motivated by ICLR context-reliance / Spectrum findings but is not required for the core claim.

---

## 11. Full-run sample size must be fixed by a predeclared rule

The first controlled pilot estimates variance and annotation reliability.

Before expanding to full run, choose one:

### Fixed-N

Freeze exact seeds/models/replicates.

OR

### Precision rule

Freeze a confidence-interval-width target and maximum budget before full outcomes.

Do not repeatedly inspect p-values and stop once significant.

---

## 12. New hard gate before treatment generation

The following must exist and pass review:

```text
TAXONOMY.md
annotation_audit_pre_treatment.md
corpus_manifest.json
model_cutoff_manifest.json
seed_manifest.json
P0_DISCOVERY_summary.json
prior_definition_freeze.json
P0_CONFIRM_summary.json
evidence_matching_report.md
preregistered_analysis.json
```

Only then may the confirmatory framing-mixture treatment be run.

---

## 13. Updated reviewer-proof criterion

The project should continue to a paper only if the result cannot reasonably be summarized as:

> “The model mentions the kind of method that appears in the papers it was shown.”

At least one deeper regularity is required:

- prior-congruence asymmetry;
- abstraction-level uptake hierarchy;
- nonlinear/threshold context-response curve;
- post-training-dependent resistance;
- held-out natural-RAG prediction from controlled response coefficients;
- structural effect hidden by coarse duplicate metrics.

Otherwise kill or downgrade the project.
