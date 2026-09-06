# ICLR Research Project

Goal: build a defensible ICLR-level research contribution through a **research → falsifiable pilot → kill/continue → mechanism experiments → paper → reviewer red-team** workflow.

Current date: 2026-09-06.

## Current decision

The project is **not** pursuing the previous broad candidates (`model editing locality stress`, `multi-turn decomposition`, `causal agent memory`) as P0. The later broad framing `Shared-Retrieval Research Monoculture` is also no longer the primary claim; it remains motivation and historical provenance only.

### Current P0 — scientific-prior steerability

> **Can retrieved scientific literature override an LLM's default scientific-method / research-mode prior, and does evidence uptake weaken at higher abstraction levels?**

Candidate phenomenon:

> **Grounding without steering** — an LLM may visibly cite and use retrieved scientific concepts while remaining anchored to its no-retrieval prior in high-level methodology or problem framing.

This is a falsifiable hypothesis, not an assumed result. The opposite result — strong, predictable context steerability — is also a successful scientific branch if supported by controlled evidence.

Why the question changed:

- ICLR 2025 already reports that changing RAG paper count has little effect on a coarse near-duplicate scientific-idea metric.
- 2026 work finds frontier LLMs share concentrated default scientific-method choices under research-question-only prompting.
- ICLR 2025–2026 work on context reliance and `in-context steerability` provides a much stronger ML framing than a broad science-of-science monoculture claim.

## Mandatory read order before any scientific generation

1. [`research/iclr_fit_validation/round7_internal_validity_and_dataset_design.md`](research/iclr_fit_validation/round7_internal_validity_and_dataset_design.md)  
   **Latest hostile design review.** Cross-fitted priors, temporally clean models/corpus, anti-lexical-priming controls, mode-preserving negative control, natural-RAG held-out prediction.

2. [`experiments/idea_collapse/PRE_RUN_AMENDMENT_D.md`](experiments/idea_collapse/PRE_RUN_AMENDMENT_D.md)  
   **Latest preregistered experimental constraint.** Amendment D extends C with cross-fitting, temporal cleanliness and anti-priming controls. It was written before scientific outcomes existed.

3. [`research/iclr_fit_validation/round6_steerability_reframe.md`](research/iclr_fit_validation/round6_steerability_reframe.md)  
   Current scientific frame. Prior-vs-context question, grounding-without-steering hypothesis, framing-mixture design, outcome branches, reviewer attacks.

4. [`experiments/idea_collapse/PRE_RUN_AMENDMENT_C.md`](experiments/idea_collapse/PRE_RUN_AMENDMENT_C.md)  
   Primary steerability pilot contract: no-context prior, matched prior-congruent/counter-prior evidence, mixture dose response, L0–L4 context uptake.

5. [`research/iclr_fit_validation/related_work_matrix.md`](research/iclr_fit_validation/related_work_matrix.md)  
   Current ICLR/recent collision map and claims we must not make.

6. [`research/iclr_fit_validation/round5_iclr_specific_validation.md`](research/iclr_fit_validation/round5_iclr_specific_validation.md)  
   Earlier ICLR-specific validation that moved the project from generic RAG diversity to evidence-composition effects.

7. [`experiments/idea_collapse/PRE_RUN_AMENDMENT_B.md`](experiments/idea_collapse/PRE_RUN_AMENDMENT_B.md)  
   Historical preregistration amendment. Preserved for provenance.

8. [`experiments/idea_collapse/PRE_RUN_AMENDMENT_A.md`](experiments/idea_collapse/PRE_RUN_AMENDMENT_A.md) and [`experiments/idea_collapse/README.md`](experiments/idea_collapse/README.md)  
   Original pilot specification and matched-relevance constraint. Read for provenance and reusable infrastructure, but do not treat the old `top-k vs diversified retrieval` contrast as the current primary hypothesis.

9. [`CODEX_WORKFLOW.md`](CODEX_WORKFLOW.md)  
   Gated execution rules, anti-p-hacking discipline, reproducibility requirements, and hard scientific stop.

## Current experiment state machine

```text
P0-DISCOVERY: NO-CONTEXT PRIOR
Identify candidate model/seed priors
        ↓
FREEZE A/B FRAMING DEFINITIONS
        ↓
P0-CONFIRM: INDEPENDENT NO-CONTEXT PRIOR
Unbiased baseline; verify prior direction
        ↓
EVIDENCE MATCHING GATE
Matched relevance/date/length + temporal-clean corpus
        ↓
P1: MATCHED EVIDENCE INTERVENTION
Prior-congruent vs counter-prior scientific literature
        ↓
P2: FRAMING-MIXTURE DOSE RESPONSE
0 / 25 / 50 / 75 / 100% matched framing composition
        ↓
P3: HIERARCHICAL CONTEXT UPTAKE
L0 source grounding
→ L1 concept
→ L2 method
→ L3 research mode
→ L4 problem framing
        ↓
P4: CONTROLS
mode-preserving packet swap
prompt/order noise
lexical-priming diagnostic
sampling diversity
        ↓
P5: HELD-OUT NATURAL-RAG VALIDATION
prior-only predictor vs prior+evidence-composition predictor
        ↓
HARD SCIENTIFIC GATE
        ├─ strong steerability → CONTINUE-A
        ├─ grounded but prior-bound → CONTINUE-B
        └─ trivial/noisy/confounded → KILL
```

## Critical experimental rule

Do **not** start the confirmatory treatment run until the repository contains and validates:

```text
experiments/idea_collapse/TAXONOMY.md
experiments/idea_collapse/annotation_audit_pre_treatment.md
experiments/idea_collapse/taxonomy_version.json
experiments/idea_collapse/corpus_manifest.json
experiments/idea_collapse/model_cutoff_manifest.json
experiments/idea_collapse/seed_manifest.json
experiments/idea_collapse/P0_DISCOVERY_summary.json
experiments/idea_collapse/prior_definition_freeze.json
experiments/idea_collapse/P0_CONFIRM_summary.json
experiments/idea_collapse/evidence_matching_report.md
experiments/idea_collapse/preregistered_analysis.json
experiments/idea_collapse/STATUS.md
```

The universal research-mode taxonomy, temporal-clean subset, independent prior confirmation, and evidence matching must be validated **before treatment outcomes are inspected**.

## Current hard rules

- Do not write the paper before the controlled pilot passes.
- Do not build another end-to-end scientific-agent framework.
- Do not treat embedding similarity or an LLM novelty judge as primary ground truth.
- Do not change research-mode categories after seeing treatment effects.
- Do not use P0-DISCOVERY as the primary prior baseline; use the independent P0-CONFIRM batch.
- Do not weaken relevance in the counter-prior condition to manufacture diversity.
- Do not pool model families before reporting within-model context effects.
- Do not call lexical/method copying “scientific steerability.”
- Preserve all candidate seeds, failed prior replications, runs, parse failures, null results, hashes, configs, and deviations.
- A deadline is not a reason to keep a weak topic.

## Current success branches

### A — Strong steerability

> Matched evidence composition causally and predictably changes high-level scientific problem/method choices, even when coarse duplicate metrics miss the shift.

### B — Grounded but prior-bound

> Retrieved evidence is visibly used at source/concept levels but high-level method/problem choices resist counter-prior evidence, revealing hierarchical context reliance.

### Kill

Kill or substantially pivot if the effect reduces to keyword copying, prompt sensitivity, unmatched relevance, unreliable taxonomy, contamination, or a newly discovered direct collision.

## Reproducibility contract

Every scientific output must map to:

```text
git commit
corpus hash
model knowledge-cutoff metadata
seed manifest
prompt hash
model/version
retriever/version
evidence-packet IDs and matching diagnostics
random seed/run ID
annotation taxonomy/version
analysis config
```

Negative results remain in the repository.

## ICLR 2027 official references

- https://iclr.cc/Conferences/2027/CallForPapers
- https://iclr.cc/Conferences/2027/ReviewerGuidelines
- https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/
