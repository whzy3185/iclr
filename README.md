# ICLR Research Project

Goal: build a defensible ICLR-level research contribution through a **research → falsifiable pilot → kill/continue → mechanism experiments → paper → reviewer red-team** workflow.

Current date: 2026-09-06.

## Current decision

The project is **not** pursuing the previous broad candidates (`model editing locality stress`, `multi-turn decomposition`, `causal agent memory`) as P0. A 2026 collision scan found substantial overlap with recent work.

Current P0:

> **Shared-Retrieval Research Monoculture** — test whether literature-grounded LLM ideation pipelines cause population-level research-question convergence because independent runs are exposed to overlapping relevance-ranked literature, and causally identify which pipeline stage drives the loss of diversity.

This is intentionally framed as **failure discovery + causal decomposition**, not as another scientific-agent framework.

## Read order

1. [`research/round3_assumption_breaking_analysis.md`](research/round3_assumption_breaking_analysis.md)  
   Research rationale, ICLR award-paper reverse analysis, collision checks, related-work positioning, P0 selection.

2. [`experiments/idea_collapse/README.md`](experiments/idea_collapse/README.md)  
   Pre-registered 24–48h pilot, hypotheses, controls, metrics, kill criteria, and exact Codex implementation contract.

## Current hard rule

Do **not** write the paper or build a complex agent before the P0 pilot passes.

First decision:

```text
P0 pilot
  ↓
Does controlled literature exposure affect problem/method-level idea diversity
across multiple models/areas without obvious quality collapse?
  ├─ no  → KILL / search next topic
  └─ yes → mechanism + selection-stage experiments
```

## Codex handoff

Codex should begin from:

```text
experiments/idea_collapse/README.md
```

and implement only the reproducible pilot infrastructure specified there.

Expected first outputs:

- frozen ICLR 2024–2026 title/abstract corpora for three areas;
- `no_retrieval`, `topk_relevance`, and `diversified_retrieval` generations;
- full retrieval/generation traces;
- bootstrap confidence intervals for source exposure and idea-diversity differences;
- problem × method collision analysis;
- a one-page `PILOT_RESULT.md` ending in `KILL` or `CONTINUE`.

## Research discipline

Every scientific claim should map to evidence. Every experiment should retain:

```text
git commit
corpus hash
prompt hash
model version
retriever version
seed/run id
analysis config
```

Negative results must remain in the repository.

## ICLR 2027 timing

Official deadlines currently relevant to this project:

- Abstract submission: **2026-09-18 11:59 PM AoE**
- Full paper submission: **2026-09-25 11:59 PM AoE**

A deadline is not a reason to keep a weak topic. If the pilot does not produce a clear, robust, scientifically interpretable signal, switch to a quality-first later submission rather than manufacture a paper-shaped result.

Official pages:

- https://iclr.cc/Conferences/2027/CallForPapers
- https://iclr.cc/Conferences/2027/ReviewerGuidelines
- https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/
