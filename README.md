# ICLR Research Project

Goal: produce a defensible ICLR contribution through **ICLR-specific research → source/construct validation → preregistered controlled experiment → mechanism/robustness → held-out natural-RAG validation → paper → reviewer red-team**.

Current date: 2026-09-07.

## Current decision

```text
KEEP / CONDITIONAL GO
Current stage: F0 SOURCE-ONLY FEASIBILITY
Scientific research-proposal generation: NOT AUTHORIZED
```

Previous broad ideas (`model editing locality`, `multi-turn decomposition`, `causal memory`, `Shared-Retrieval Research Monoculture`, generic `retrieval as a hidden prior`) are historical motivation only.

## Current core question

> **For an open-ended ICLR research problem with multiple scientifically valid strategies, how does changing the composition of equally relevant real scientific literature change an LLM's high-level research choice, and can this controlled response explain behavior under ordinary retrieval?**

Secondary mechanism question:

> Does evidence response depend systematically on the model × seed's independently measured **no-context baseline route propensity**?

Preferred terminology:

```text
baseline route propensity

evidence-conditioned scientific choice response

matched scientifically plausible alternative routes
```

Avoid generic claims that we introduce `scientific priors`, `in-context steerability`, or evidence-grounded scientific ideation; recent work already occupies those broader spaces.

## Read order — research lead / Codex

1. [`research/iclr_fit_validation/round41_current_decision_ledger_and_scope_freeze.md`](research/iclr_fit_validation/round41_current_decision_ledger_and_scope_freeze.md)  
   **Current scientific state and scope freeze.**

2. [`research/iclr_fit_validation/round33_staged_execution_and_hard_gates.md`](research/iclr_fit_validation/round33_staged_execution_and_hard_gates.md)  
   F0 → F1 → P0 → P1 → P2 → P3 execution/gate ordering.

3. [`research/iclr_fit_validation/round36_iclr_reviewer_matrix_and_must_have_evidence.md`](research/iclr_fit_validation/round36_iclr_reviewer_matrix_and_must_have_evidence.md)  
   ICLR reviewer attacks mapped to required evidence.

4. [`research/iclr_fit_validation/round40_data_schema_and_preregistered_analysis_contract.md`](research/iclr_fit_validation/round40_data_schema_and_preregistered_analysis_contract.md)  
   Provenance/data/analysis freeze contract.

5. [`research/iclr_fit_validation/round32_pre_result_paper_storyboard.md`](research/iclr_fit_validation/round32_pre_result_paper_storyboard.md)  
   Paper/figure branches defined before outcomes.

6. [`research/iclr_fit_validation/related_work_matrix.md`](research/iclr_fit_validation/related_work_matrix.md) and [`research/iclr_fit_validation/round34_last_30d_collision_update.md`](research/iclr_fit_validation/round34_last_30d_collision_update.md)  
   Collision boundary and prohibited novelty claims.

7. [`experiments/idea_collapse/PREREGISTRATION_V1.md`](experiments/idea_collapse/PREREGISTRATION_V1.md)  
   Historical/current operational preregistration foundation. Newer pre-outcome research rounds further tighten it; do not start scientific generation from this file alone.

Historical rounds/amendments remain for provenance. Do not delete or rewrite research history.

## Current Codex authorization

Codex is authorized **only** for source-only F0 feasibility.

Read:

- [`CODEX_FEASIBILITY_TASK_1.md`](CODEX_FEASIBILITY_TASK_1.md)
- [`CODEX_FEASIBILITY_TASK_1_AMENDMENT_A.md`](CODEX_FEASIBILITY_TASK_1_AMENDMENT_A.md)
- [`CODEX_FEASIBILITY_TASK_1_AMENDMENT_B.md`](CODEX_FEASIBILITY_TASK_1_AMENDMENT_B.md)

Required hand-back:

```text
experiments/idea_collapse/feasibility_1/FEASIBILITY_RESULT.md
```

Until that file is reviewed by the research lead, Codex must NOT:

- generate scientific research proposals;
- estimate no-context route propensity;
- run evidence-conditioned treatment generations;
- inspect treatment outcomes;
- select route pairs from model behavior;
- write results as if a phenomenon has been observed.

## Core experimental object

For model `M`, method-masked research seed `x`, matched evidence packet `C_alpha`, and free-form proposal `Y`:

```text
Y ~ P_M(Y | x, C_alpha)
```

For a source-selected, frozen A/B scientific route pair:

```text
alpha = fraction of Route-A evidence
        in a fixed-size, relevance-matched packet

alpha ∈ {0, .25, .5, .75, 1}
```

Routes are frozen from ICLR literature **before model outputs**.

A/B scientific alternatives must pass:

- seed validity/method neutrality;
- multi-route openness;
- source support;
- relevance matching;
- scientific plausibility/equipoise;
- distinguishability/non-subsumption;
- human annotatability.

## Primary outcome

Human-anchored, blinded ordinal route score:

```text
+2  STRONGLY_A
+1  LEANS_A
 0  MIXED
-1  LEANS_B
-2  STRONGLY_B
NA  NEITHER / INVALID
```

Annotators do not see model identity, evidence packet, alpha, or expected direction.

An LLM classifier may scale annotation only after human calibration; it does not define ground truth.

## Confirmatory hypotheses

### H1 — Evidence-conditioned scientific choice

Matched evidence composition changes high-level route choice.

### H2 — Baseline-conditioned response

The response depends on independently measured no-context baseline route propensity.

### H3 — Controlled-to-natural prediction

A response model fitted only on controlled evidence mixtures improves held-out prediction of the same model's route choices under ordinary top-k retrieval relative to baseline-only prediction.

## Required validity chain

A strong paper needs:

```text
source/seed validity
        ↓
route equipoise + relevance matching
        ↓
controlled evidence-mixture response
        ↓
blinded human measurement
        ↓
replication across model families
        ↓
anti-priming / copy controls
        ↓
baseline interaction or another nontrivial regularity
        ↓
held-out natural-RAG prediction
```

Raw `different papers → different proposal words` is explicitly insufficient.

## Anti-priming mechanism tests

Prioritized after the core response exists:

- content-normalized evidence cards (`PF`, `PFM`, `PFL`);
- direct/near method-copy exclusion;
- within-route vs cross-route matched document replacement;
- prompt/order nuisance controls;
- source → concept → method → route → problem-framing uptake profile.

If RAW abstracts show an effect but normalized/copy-controlled evidence does not, the main scientific claim should be killed or heavily downgraded.

## Held-out natural-RAG validation

Controlled intervention data fit a frozen response law.

Then on held-out seeds:

```text
ordinary top-k retrieval
→ frozen route-composition features
→ predict model's route distribution
```

Compare:

```text
M0 global/null
M1 baseline only
M2 evidence only
M3 baseline + evidence
M4 baseline + evidence + interaction
```

Natural-RAG outcomes evaluate the frozen prediction model; they do not refit it.

## Model plan

Causal core: open/auditable model families first.

```text
Llama 3.1 family  — documented cutoff Dec 2023
Gemma 3 family    — documented cutoff Aug 2024
```

Strict shared evidence subset:

```text
ICLR 2025 paper first public > 2024-08-31
and no discovered earlier public version before cutoff
```

Likely engineering pilot checkpoints:

```text
Llama-3.1-8B-Instruct
Gemma-3-12B-IT
```

Larger family checkpoints may be frozen for confirmatory replication if infrastructure supports them. Closed frontier APIs are external-validity extensions, not the temporal-clean causal core.

## Execution gates

```text
F0 SOURCE-ONLY FEASIBILITY          ← CURRENT
 ↓
F1 CONSTRUCT / HUMAN ANNOTATION AUDIT
 ↓
P0 ENGINEERING / VARIANCE PILOT
   alpha = 0,.5,1
 ↓
G0 FULL-STUDY AUTHORIZATION
 ↓
P1 CONFIRMATORY FIVE-LEVEL MIXTURE
 ↓
G1 NONTRIVIAL PHENOMENON?
 ↓
P2 MECHANISM / ANTI-PRIMING
 ↓
G2 MORE THAN PRIMING?
 ↓
P3 HELD-OUT NATURAL RAG
 ↓
G3 PAPER-LEVEL EXTERNAL VALIDITY
 ↓
P4 OPTIONAL EXTENSIONS
   base-vs-instruct / 3-route simplex / frontier / MUSES
```

No later stage is automatically authorized by an older prompt.

## Statistical discipline

- generation samples are Monte Carlo draws, not independent scientific replications;
- seed is the primary clustering/generalization unit when multiple route pairs share a seed;
- report within-model effects before pooled results;
- prioritize 30–40 independent seeds for a strong full study if F0 supports that breadth;
- final sample size / SESOI are frozen after construct/variance pilot and before confirmatory outcomes;
- do not stop when a p-value becomes significant.

## Current neutral paper identity

Working title:

> **Same Relevance, Different Research Choices: How Scientific Evidence Shapes LLM Hypothesis Search**

Alternative:

> **Evidence-Conditioned Scientific Choice in Large Language Models**

Outcome-specific titles remain unfrozen until data.

## Strong-paper ladder

```text
Level 0: lexical/method priming only → KILL
Level 1: robust matched-evidence high-level choice response
Level 2: response has a general regularity (baseline/component/abstraction)
Level 3: controlled response predicts held-out natural RAG
Level 4: post-training / multi-route geometry reveals broader ML property
```

## Hard kill conditions

Kill/pivot if:

- source feasibility cannot produce enough multi-route/equipoise blocks;
- route choice is not human-annotatable reliably;
- one route is systematically less relevant/plausible;
- precise effect is scientifically trivial;
- effects disappear under all anti-priming controls;
- result is one-model/hand-picked-seed only;
- controlled effect has no explanatory natural-RAG bridge and no strong mechanism;
- a direct concurrent paper occupies the combined causal question.

## Research history and AI-use provenance

Every meaningful research/design change is committed as a new round. Preserve:

```text
source URLs
research rounds
git commits
corpus / seed / treatment hashes
prompts / model versions
negative results / failed matching
human annotation provenance
deviation logs
```

This also supports the ICLR AI-use disclosure required for substantial LLM involvement in hypothesis/design/implementation/interpretation.

## Official ICLR references

- https://iclr.cc/Conferences/2027/CallForPapers
- https://iclr.cc/Conferences/2027/ReviewerGuidelines
- https://iclr.cc/Conferences/2027/AIPolicyForAuthors
- https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/
