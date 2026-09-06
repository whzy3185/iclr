# PREREGISTRATION V1 — Scientific-Prior Steerability in Literature-Grounded LLM Ideation

> Repository: `whzy3185/iclr`  
> Date frozen: 2026-09-06  
> Status: **CURRENT OPERATIONAL PREREGISTRATION**  
> Scope: ICLR-only core study.  
> Historical files `README.md` and Amendments A–D remain preserved as provenance, but this file supersedes them operationally where they conflict.

---

# 0. Freeze statement

No scientific treatment outcomes existed in the repository when the sequence of Amendments C/D and the selection-independent design was developed.

This preregistration freezes the current primary scientific question:

> **Can retrieved scientific literature override an LLM's default scientific-method / research-mode prior, and does evidence uptake weaken as the scientific abstraction level increases?**

Candidate phenomenon:

> **Grounding without steering** — retrieved literature may strongly affect source attribution and conceptual content while having much weaker influence on high-level method choice, scientific move, or central problem framing.

The opposite result — strong, predictable high-level context steerability — is also a successful scientific branch.

The experiment is designed to distinguish these outcomes rather than to produce a predetermined story.

---

# 1. Claims explicitly NOT under test as the main paper

The paper is not primarily testing:

- whether LLM-assisted science causes real-world scientific monoculture;
- whether RAG in general improves idea quality;
- whether adding more retrieved papers increases diversity;
- whether LLMs have any context sensitivity;
- whether retrieval is generically an inductive bias;
- whether LLMs have concentrated default scientific-method suggestions;
- whether another diversity-aware scientific-agent framework improves benchmarks.

All of these are either too broad, already studied, or insufficiently ICLR-specific.

---

# 2. Main scientific object

For a frozen model `M`, method-masked scientific seed question `x`, controlled evidence packet `C`, and generated proposal `H`:

```text
H ~ P_M(H | x, C)
```

We study how the distribution over structured scientific choices changes as `C` changes.

The main object is an ML model's inference-time conditional behavior, not human scientist behavior.

---

# 3. ICLR empirical universe

## 3.1 Primary evidence corpus

Use **ICLR 2025 accepted papers** from official proceedings/OpenReview metadata.

### Temporal-clean primary subset

For the clean causal analysis, require evidence papers to have a first-public date after:

```text
2024-08-31
```

and no discovered earlier public version before that date.

Rationale:

- Llama 3.1 official model card: pretraining cutoff Dec 2023;
- Gemma 3 official model card: knowledge cutoff Aug 2024.

The common post-Aug-2024 rule creates one conservative clean evidence subset.

Record arXiv/OpenReview/publication first-public dates and any earlier version found.

## 3.2 Seed questions

Prefer **ICLR 2026 accepted papers**.

For each seed:

- extract a research question/problem statement;
- remove title/authors;
- remove explicit focal method/solution names;
- remove introduced dataset/model names that reveal the solution;
- exclude the focal paper from retrieval/evidence;
- record focal first-public date;
- where feasible restrict evidence to papers available before focal first-public date.

The focal paper's actual method is never treated as an optimal gold answer.

## 3.3 Core ICLR subareas

Target at least three, and preferably 4–6, such as:

- LLM agents / tool use;
- retrieval / long context;
- post-training / optimization;
- interpretability / reasoning;
- model editing / knowledge updating;
- efficient training / inference.

Subarea list is frozen before treatment outcomes.

---

# 4. Core models

## 4.1 Causal-core families

Prioritize two independent open model families with documented cutoffs:

### Llama 3.1

Use an instruction-tuned checkpoint for the core; paired pretrained/base checkpoint is a pre-specified secondary comparison where feasible.

### Gemma 3

Use an instruction-tuned checkpoint for the core; paired pretrained/base checkpoint is a pre-specified secondary comparison where feasible.

Exact sizes must be frozen in `model_cutoff_manifest.json` before generation based on available inference infrastructure.

## 4.2 Frontier external-validity models

Closed/proprietary frontier models may be added only as separately reported external-validity results if their contamination status is not auditable enough for the clean causal subset.

Do not pool them with the temporal-clean causal estimate.

---

# 5. Two-layer scientific taxonomy

The final taxonomy must be audited and frozen before treatment generation.

Research draft: `research/iclr_fit_validation/taxonomy_design_draft.md`.

## 5.1 Layer A — high-level scientific move

Initial candidate categories:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
VERIFY_FALSIFY_REPLICATE
```

### Merge rule

Categories may be merged/redefined only during a pre-treatment annotation audit.

After the frozen taxonomy hash exists, no primary-category changes are allowed based on treatment outcomes.

## 5.2 Layer B — methodology inventory

Adapt established dimensions from Carlon et al. rather than claiming a novel method ontology:

- dataset/task properties;
- model/algorithm family;
- training paradigm;
- provider/openness/size where meaningful;
- evaluation metric type;
- normalized free method entities.

## 5.3 Layer C — problem-framing tuple

```text
(problem_object,
 failure_or_limitation,
 hypothesized_mechanism,
 intervention_family,
 evaluation_target)
```

Use primarily for audited structural-equivalence and transfer analysis.

---

# 6. Treatment selection is independent of model outputs

This is a critical design rule.

### First

Using only:

- seed question;
- frozen ICLR evidence corpus;
- frozen source-paper taxonomy;
- relevance/matching features;

identify which scientific-move treatments are feasible for each seed.

### Then freeze

Produce `TREATMENT_MODE_SELECTION.md` and a hashed selection table.

### Only afterward

Estimate no-context model priors.

Therefore `prior-congruent` / `counter-prior` are post-freeze descriptive labels, not criteria used to choose the treatment.

---

# 7. Seed and treatment eligibility

For each seed:

1. retrieve large candidate pool from clean ICLR evidence corpus;
2. classify source-paper Layer-A move;
3. apply frozen relevance floor;
4. identify modes with adequate evidence count;
5. test covariate matching feasibility between modes.

Record one of:

```text
ELIGIBLE_2_MODES
ELIGIBLE_3PLUS_MODES
INSUFFICIENT_MODE_COVERAGE
RELEVANCE_MATCH_FAILURE
TEMPORAL_CLEANLINESS_FAILURE
TAXONOMY_AMBIGUITY
```

No model generations are used for this eligibility decision.

### Treatment pair selection

Use a deterministic rule frozen before model outputs.

Recommended V1 rule:

1. enumerate all mode pairs passing evidence-count + matching gates;
2. choose the pair maximizing the minimum matched evidence count;
3. ties broken by a global frozen mode-priority order;
4. save all candidate pairs and the selected pair.

A fixed global pair is an acceptable simpler alternative if pre-treatment corpus analysis shows adequate coverage.

---

# 8. Evidence matching

For every candidate evidence paper record:

- dense relevance score;
- reranker relevance score;
- abstract/evidence token length;
- public date/year;
- topic cluster;
- ICLR status;
- optional frozen citation/popularity metadata;
- Layer-A mode label;
- Layer-B methodology labels.

Evidence packets must be matched/stratified on observables while differing in scientific-move composition.

### Required pre-treatment report

`evidence_matching_report.md` must show:

- means/medians/distributions;
- standardized mean differences where appropriate;
- overlap plots/tables;
- failed seeds and reasons.

Counter-direction evidence cannot be made “different” by relaxing topical relevance or selecting weaker papers.

---

# 9. No-context model prior

Treatments are already frozen when priors are measured.

Use two independent no-context batches for reliability:

```text
P0-A
P0-B
```

Both see only the method-masked seed question and the identical generation task.

### Primary prior estimate

Use the pooled or pre-specified combined estimator from P0-A/B after confirming batch consistency; exact estimator is frozen in `preregistered_analysis.json`.

### Prior variables

For every seed/model/mode:

- no-context probability;
- mode rank;
- entropy;
- prior strength / log-odds contrast.

### Important

P0 does not change the treatment assignment.

---

# 10. Controlled framing-mixture intervention

For the pre-frozen mode pair A/B, use fixed evidence count `k`.

Default:

```text
k = 12
alpha(A) = 0.00 / 0.25 / 0.50 / 0.75 / 1.00
```

Illustration:

```text
0.00 ->  0 A + 12 B
0.25 ->  3 A +  9 B
0.50 ->  6 A +  6 B
0.75 ->  9 A +  3 B
1.00 -> 12 A +  0 B
```

All packets:

- same generator prompt/language;
- same model/version;
- same decoding configuration;
- matched relevance distributions;
- approximately matched token budget;
- randomized evidence order across replicates.

No tuning of mixture levels after outcomes.

---

# 11. Primary treatment response

For mode A:

```text
response(alpha) = P(output primary scientific move = A | alpha)
```

Analyze separately by model and seed/subfield before pooled summaries.

### Core questions

1. Does evidence fraction produce a dose response?
2. Does response depend on no-context prior strength?
3. Is movement easier toward high-prior modes than low-prior modes under matched evidence?
4. Is response linear, thresholded, asymmetric, or model-dependent?

---

# 12. Hierarchical context uptake

Every treatment output is measured at multiple levels.

## L0 — source attribution

Does the proposal cite/reference supplied evidence or source-specific entities?

## L1 — conceptual evidence uptake

Does it use supplied findings, mechanisms, limitations, or assumptions?

## L2 — methodology uptake

Does method/dataset/model/evaluation family shift with context?

## L3 — scientific-move uptake

Does the proposal change among the frozen Layer-A scientific moves?

## L4 — central problem framing

Does the central scientific problem/failure/causal target follow the evidence framing?

### Candidate hierarchy

A possible result is:

```text
L0 > L1 > L2 > L3/L4
```

but no aggregate metric is allowed to impose this ordering.

---

# 13. Primary statistical model

Exact implementation is frozen in `preregistered_analysis.json` before outcomes.

Conceptual form for output category `j`:

```text
logit / multinomial P(Y=j)
 = intercept
 + evidence_support_j
 + prior_probability_j
 + evidence_support_j × prior_probability_j
 + model effects
 + subfield effects
 + seed random effects
 + pre-specified nuisance terms
```

### Main inferential targets

- evidence-response coefficient;
- evidence × prior interaction;
- between-model heterogeneity;
- abstraction-level response differences.

### Statistical discipline

- independent generation is nested in seed/model/context;
- bootstrap/hierarchical uncertainty over seeds;
- no O(N²) pairwise-similarity pseudo-replication;
- report effect sizes + intervals, not only p-values;
- mode labels and primary contrasts frozen before treatment outcomes.

---

# 14. Required negative / nuisance controls

## 14.1 Mode-preserving packet swap

Change document identities while preserving research-mode composition + relevance strata.

Purpose:

> distinguish framing-composition effects from arbitrary source-identity effects.

Strong structural evidence requires cross-mode shifts to exceed within-mode swap effects.

## 14.2 Evidence order

Randomize/permute document order.

## 14.3 Prompt paraphrase

Estimate semantically equivalent prompt variance as a noise floor.

## 14.4 Sampling breadth

At minimum compare standard vs high temperature on a subset.

Optional established generation-diversity method if cleanly reproducible.

Purpose:

> distinguish within-context sample breadth from between-context search direction.

---

# 15. Lexical-priming diagnostics

A paper cannot rest on “the model repeats words it saw.”

## 15.1 Exact method-copy score

Record whether a proposal directly reuses a supplied method/entity.

## 15.2 Treatment text separability

Measure how easily a lightweight lexical classifier predicts A/B from packet text.

## 15.3 Content-normalized robustness subset

For a pre-specified subset, generate audited standardized evidence cards preserving:

- scientific problem;
- empirical result;
- mechanism/limitation;

while removing:

- title/authors;
- explicit research-mode labels;
- direct future-work prescriptions;
- obvious boilerplate where feasible.

This normalization pipeline is frozen and manually audited before its treatment outputs.

Do not let an LLM summarizer silently introduce new scientific recommendations.

---

# 16. Coarse diversity compatibility analysis

Reproduce/approximate the logic of Si et al. (ICLR 2025):

```text
k = 0 / 5 / 10 / 20
```

with a compatible near-duplicate idea metric as a secondary analysis.

Potentially important dissociation:

```text
near-duplicate metric ~ flat
high-level scientific-mode distribution shifts
```

A flat duplicate metric alone does not kill this project.

---

# 17. Held-out natural-RAG validation

This is required for a strong mechanism claim.

### Training stage

Fit evidence-response relationships using **controlled treatment seeds only**.

### Freeze

Freeze the response model.

### Held-out stage

For new seed questions:

1. run ordinary natural top-k retrieval from the same clean ICLR corpus;
2. label retrieved packet composition with frozen taxonomy;
3. obtain no-context prior;
4. predict natural-RAG output distribution.

Compare:

```text
prior-only predictor
vs
prior + evidence-composition predictor
```

A meaningful held-out improvement is required to say controlled evidence composition explains ordinary RAG search behavior.

---

# 18. Base vs instruction-tuned secondary comparison

Where paired checkpoints are feasible:

- compare context response after controlling for valid-output rate;
- report task coherence separately;
- do not interpret incoherent base-model randomness as steerability.

Question:

> Does post-training strengthen scientific priors or reduce counter-prior context response, consistent with general ICLR steerability/context-reliance findings?

This is secondary, not required for the primary causal claim.

---

# 19. Annotation protocol

## Before treatments

1. develop taxonomy using source papers + no-context outputs only;
2. two independent annotators label a stratified sample;
3. report agreement/confusion/prevalence by category and abstraction level;
4. merge/redefine unreliable categories now;
5. freeze taxonomy hash.

## After freeze

- automatic LLM/parser classification is allowed for scale;
- parser model/version/prompt frozen;
- blind independent/human audit on treatment-stratified sample;
- report parser performance by category;
- downgrade unreliable L4 outcomes rather than hiding disagreement.

No generic LLM novelty judge is a primary endpoint.

---

# 20. Recombination diagnostics — exploratory

If reliable, label evidence use as:

```text
NO_UPTAKE
SOURCE_ATTRIBUTION
CONTENT_UPTAKE
COPY
COMBINE
TRANSFER
NEW_DIRECTION
```

These are not primary unless validated pre-treatment.

---

# 21. Pilot scale

First validate taxonomy, evidence matching, temporal cleanliness and generation pipeline with engineering smoke tests.

A scientifically meaningful first controlled pilot can target approximately:

```text
24 eligible seed questions
× 2 model families
× 5 mixture levels
× 10 independent generations
= 2,400 treatment generations
```

plus no-context priors and control subsets.

Exact pilot N is frozen before scientific treatment outcomes.

### Full-scale expansion

After the pilot estimates seed/model heterogeneity, choose and freeze either:

- fixed-N full design; or
- predeclared precision target + maximum budget.

No repeated significance peeking/stopping.

---

# 22. Result branches

## CONTINUE A — strong high-level steerability

Evidence composition produces reproducible high-level dose response across >=2 model families and >=3 ICLR subareas; effect exceeds nuisance controls and is supported by blind audit.

Best paper frame:

> **Same Relevance, Different Science** — evidence composition steers scientific hypothesis search; coarse diversity metrics miss directional search-space changes.

## CONTINUE B — grounded but prior-bound

Required pattern:

- strong L0/L1 evidence use;
- much weaker or asymmetric L3/L4 response;
- robustness to relevance matching, prompt/order, lexical controls and sampling breadth;
- replicated across >=2 model families/subareas.

Best paper frame:

> **Grounded but Prior-Bound** — literature grounding does not imply high-level scientific steerability.

## KILL C — trivial priming

High-level effect reduces to obvious lexical/method copying and disappears under proper controls.

## KILL D — construct failure

Scientific-move/problem-framing taxonomy cannot be reliably annotated.

## KILL E — matching failure

Scientifically valid A/B evidence cannot be relevance-matched.

## KILL F — direct collision

A newly discovered concurrent paper already provides comparable selection-independent matched-literature intervention + high-level scientific prior/context analysis.

---

# 23. Strong-paper requirement

The project is not worth an ICLR submission if the result can be accurately summarized as:

> “Models talk about the type of method described in their context.”

At least one deeper regularity must survive:

- evidence × prior interaction;
- prior-congruence asymmetry;
- abstraction-level uptake hierarchy;
- nonlinear/threshold response;
- post-training/model-family dependence;
- held-out natural-RAG prediction;
- structural effect invisible to duplicate-based metrics.

---

# 24. Required files before treatment generation

```text
TAXONOMY.md
annotation_audit_pre_treatment.md
taxonomy_version.json
corpus_manifest.json
model_cutoff_manifest.json
seed_manifest.json
TREATMENT_MODE_SELECTION.md
treatment_selection_hash.json
evidence_matching_report.md
P0_A_summary.json
P0_B_summary.json
preregistered_analysis.json
STATUS.md
```

`TREATMENT_MODE_SELECTION.md` must be frozen **before P0-A/P0-B model-prior outcomes** under the strict selection-independent design.

---

# 25. Literature anchors that motivated V1

Primary ICLR neighbors:

- Si, Yang & Hashimoto, *Can LLMs Generate Novel Research Ideas?*, ICLR 2025.
- Padmakumar & He, *Does Writing with Language Models Reduce Content Diversity?*, ICLR 2024.
- Goyal et al., *Context-Parametric Inversion*, ICLR 2025.
- Minder et al., *Controllable Context Sensitivity and the Knob Behind It*, ICLR 2025.
- Sorensen et al., *Spectrum Tuning*, ICLR 2026.
- Blankenstein et al., *BiasBusters*, ICLR 2026.
- Gur-Arieh et al., *Mixing Mechanisms*, ICLR 2026.

Direct scientific-ideation neighbors:

- Carlon et al., *Thinking Like a Scientist?*, 2026.
- ProjectionBench, 2026.
- LiveIdeaBench, Nature Communications 2026.
- SCI-IDEA, Machine Learning 2026.
- MoRI, ACL 2026.
- RQ-Bench / novelty-judge study, 2026.
- prompt-language RAG diversity study, 2026.

High-upside future extension:

- MUSES / intellectual-root retrieval, only after a separate contamination-safe design.

---

# 26. Operational rule from this point

Do not modify the primary question or treatment logic merely because pilot outcomes are weak.

Permitted pre-outcome changes after V1:

- implementation bug fixes;
- taxonomy changes required by the explicitly pre-treatment annotation audit;
- evidence matching thresholds needed to satisfy a predeclared balance criterion;
- direct-collision response if a newly published paper materially overlaps.

Any other substantive design change must be documented as `PREREGISTRATION_V2.md` **before the affected outcomes are generated**, with a precise reason unrelated to desired results.
