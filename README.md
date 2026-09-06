# ICLR Research Project

Goal: produce a defensible ICLR contribution through **ICLR-specific research → preregistration → controlled pilot → kill/continue → mechanism/robustness → paper → reviewer red-team**.

Current date: 2026-09-06.

## Current P0

Previous broad ideas (`model editing locality`, `multi-turn decomposition`, `causal memory`, and later `Shared-Retrieval Research Monoculture`) are historical motivation only.

The current research question is:

> **Can retrieved scientific literature override an LLM's default scientific-method / research-mode prior, and does evidence uptake weaken at higher levels of scientific abstraction?**

Candidate phenomenon:

> **Grounding without steering** — the model may clearly use retrieved sources and concepts while remaining anchored to its no-retrieval prior in high-level method choice or problem framing.

The opposite outcome — strong and predictable high-level scientific steerability — is also a valid scientific branch.

## Single operational experiment contract

Read first:

1. [`experiments/idea_collapse/PREREGISTRATION_V1.md`](experiments/idea_collapse/PREREGISTRATION_V1.md)  
   **Current operational preregistration.** Where historical specs conflict, V1 wins.

2. [`research/iclr_fit_validation/round8_selection_independent_design.md`](research/iclr_fit_validation/round8_selection_independent_design.md)  
   Why treatment modes are selected from literature before observing model priors.

3. [`research/iclr_fit_validation/round7_internal_validity_and_dataset_design.md`](research/iclr_fit_validation/round7_internal_validity_and_dataset_design.md)  
   Temporal cleanliness, anti-priming controls, natural-RAG validation, model/corpus design.

4. [`research/iclr_fit_validation/round6_steerability_reframe.md`](research/iclr_fit_validation/round6_steerability_reframe.md)  
   ICLR scientific framing and outcome branches.

5. [`research/iclr_fit_validation/taxonomy_design_draft.md`](research/iclr_fit_validation/taxonomy_design_draft.md)  
   Research draft for the two-layer taxonomy; **not yet the frozen experiment taxonomy**.

6. [`research/iclr_fit_validation/outcome_conditioned_paper_blueprints.md`](research/iclr_fit_validation/outcome_conditioned_paper_blueprints.md)  
   What the paper should look like under strong-steerability, prior-bound, or kill outcomes.

7. [`research/iclr_fit_validation/related_work_matrix.md`](research/iclr_fit_validation/related_work_matrix.md)  
   Collision map and claims we must not make.

8. [`CODEX_WORKFLOW.md`](CODEX_WORKFLOW.md)  
   Historical execution discipline. Its scientific task details are superseded by `PREREGISTRATION_V1.md` where they conflict.

Historical research and Amendments A–D remain in the repository for provenance. Do not delete them.

## Current experiment ordering

```text
TEMPORAL-CLEAN ICLR CORPUS
ICLR 2025 evidence + ICLR 2026 method-masked seeds
        ↓
PRE-TREATMENT TAXONOMY AUDIT
freeze high-level scientific move + lower-level method taxonomy
        ↓
SELECTION-INDEPENDENT TREATMENTS
choose matchable literature framing pairs WITHOUT model outputs
freeze treatment-selection hash
        ↓
NO-CONTEXT PRIORS
independent P0-A / P0-B model generations
        ↓
MATCHED EVIDENCE MIXTURE
0 / 25 / 50 / 75 / 100% framing composition
        ↓
HIERARCHICAL CONTEXT UPTAKE
L0 source → L1 concept → L2 method → L3 scientific move → L4 problem framing
        ↓
NEGATIVE / NUISANCE CONTROLS
within-mode packet swap, prompt/order, lexical priming, sampling breadth
        ↓
HELD-OUT NATURAL-RAG VALIDATION
prior-only vs prior+evidence-composition prediction
        ↓
HARD SCIENTIFIC GATE
   ├─ CONTINUE A: strong high-level steerability
   ├─ CONTINUE B: grounded but prior-bound
   └─ KILL: trivial priming / noisy construct / confounded evidence / collision
```

## Why the question changed

ICLR 2025 already found that changing RAG paper count had little effect on a coarse near-duplicate scientific-idea metric, while model backbone had a large effect. 2026 work further finds strong shared narrowing in LLM-recommended scientific methodologies. Meanwhile ICLR 2025–2026 work establishes context-vs-prior reliance and **in-context steerability** as general ML problems.

Therefore the paper cannot be “RAG makes research ideas more/less diverse.” The ICLR-shaped question is **whether scientific evidence actually changes the model's high-level search distribution, and at what abstraction level context stops winning against the model prior.**

## Files required before confirmatory treatment generation

```text
experiments/idea_collapse/TAXONOMY.md
experiments/idea_collapse/annotation_audit_pre_treatment.md
experiments/idea_collapse/taxonomy_version.json
experiments/idea_collapse/corpus_manifest.json
experiments/idea_collapse/model_cutoff_manifest.json
experiments/idea_collapse/seed_manifest.json
experiments/idea_collapse/TREATMENT_MODE_SELECTION.md
experiments/idea_collapse/treatment_selection_hash.json
experiments/idea_collapse/evidence_matching_report.md
experiments/idea_collapse/P0_A_summary.json
experiments/idea_collapse/P0_B_summary.json
experiments/idea_collapse/preregistered_analysis.json
experiments/idea_collapse/STATUS.md
```

Treatment modes must be frozen before P0-A/P0-B outcomes under the strict selection-independent design.

## Hard rules

- Do not build another end-to-end scientific-agent framework.
- Do not use treatment outcomes to redefine the taxonomy or choose the treatment modes.
- Do not weaken relevance to manufacture a counter-direction effect.
- Do not call lexical/method copying “scientific steerability.”
- Do not rely on embedding diversity or an LLM novelty score as primary ground truth.
- Do not pool model families before reporting within-model effects.
- Preserve all candidate seeds, matching failures, nulls, parse failures, raw generations, hashes, configs, and deviations.
- Do not force a paper if the result is scientifically trivial.

## Paper outcome branches

### A — strong steerability

> Matched literature composition causally and predictably shifts high-level scientific choices, even when coarse duplicate metrics miss the shift.

Candidate title: **Same Relevance, Different Science**.

### B — grounded but prior-bound

> Models visibly use retrieved sources/concepts but resist counter-prior context at method/problem-framing levels, revealing hierarchical context reliance.

Candidate title: **Grounded but Prior-Bound**.

### Kill

If the honest summary is only “the model talks about the kind of method in its prompt,” or if matching/taxonomy/temporal cleanliness fails, stop the topic.

## Reproducibility contract

Every scientific result maps to:

```text
git commit
corpus hash
model cutoff metadata
seed manifest
treatment-selection hash
prompt hash
model/version
retriever/reranker versions
evidence packet IDs + matching diagnostics
random seed/run ID
taxonomy/version
analysis config
```

Negative evidence remains in the repository.

## ICLR official references

- https://iclr.cc/Conferences/2027/CallForPapers
- https://iclr.cc/Conferences/2027/ReviewerGuidelines
- https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/
