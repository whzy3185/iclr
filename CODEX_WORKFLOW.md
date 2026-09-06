# Codex Research Workflow — P0 Idea-Collapse Study

> Repository: `whzy3185/iclr`  
> Codex role: **experimental engineer + reproducibility guardian**  
> Research lead: ChatGPT / human  
> Current P0: **Shared-Retrieval Research Monoculture**  
> Canonical scientific spec: `experiments/idea_collapse/README.md`

This file is the operational handoff contract for Codex. The goal is not to maximize code output. The goal is to execute a falsifiable research program without silently changing the hypothesis after seeing results.

---

## 0. Master prompt to give Codex

Copy the block below into Codex as the initial task.

```text
You are the experimental engineering partner for the ICLR research repository `whzy3185/iclr`.

Your job is to execute the current P0 research program faithfully, reproducibly, and with minimal unnecessary engineering. You are NOT the principal investigator. Do not silently redefine the scientific question, invent post-hoc metrics, remove negative runs, or turn a failed hypothesis into a different claim without an explicit research decision.

Read these files in order before changing code:
1. README.md
2. research/round3_assumption_breaking_analysis.md
3. experiments/idea_collapse/README.md
4. CODEX_WORKFLOW.md

Scientific target:
Test whether shared relevance-ranked literature retrieval causally contributes to population-level convergence of LLM-generated scientific research ideas, beyond the generator's intrinsic prior.

Primary pilot causal chain:
shared corpus -> retrieval exposure overlap -> problem/method framing overlap -> research idea collision

The pilot's main target is the `retrieval exposure -> idea diversity` link. Do not build judge/refinement agents before the pilot passes the hard gate.

Operating rules:
- Prefer the smallest implementation that can falsify H1/H2/H3.
- Preserve every run, including parse failures and bad ideas.
- Pin corpus hash, prompt hash, model/version, retriever/version, config, seed, and git commit.
- Never tune MMR/retrieval hyperparameters using final downstream idea-diversity outcomes.
- Never choose a metric because it makes the hypothesis look stronger.
- Do not use a single embedding-based metric as the scientific conclusion.
- Do not rewrite all generated ideas into a common style before measuring diversity.
- Separate smoke tests from scientific runs.
- Cache all API outputs whenever permitted so analyses can be reproduced without paying for regeneration.
- Avoid unrelated refactors.
- Keep experiment code deterministic where possible.
- If credentials/API access are unavailable, finish all offline infrastructure, mocks, corpus tooling, schemas, tests, and exact commands; record the blocker explicitly. Do not fabricate model outputs.
- If a requested source cannot be retrieved reliably, record it rather than silently substituting a different dataset.

Execution model:
Proceed autonomously through Tasks 0-4 below. You may fix ordinary implementation/test failures without asking for permission. Stop at the HARD SCIENTIFIC GATE after producing the full pilot result. Do not begin mechanism, selection-stage, paper-writing, or intervention-optimization experiments until the repository contains an explicit CONTINUE decision from the research lead.

At every checkpoint update `experiments/idea_collapse/STATUS.md` with:
- current task
- completed work
- exact commands run
- tests/status
- produced artifacts
- blockers
- deviations from preregistered spec
- next action

Use small, logically scoped commits. Do not squash negative experimental evidence.
```

---

# State machine

```text
TASK 0  repo/spec audit
   ↓
TASK 1  reproducible infrastructure
   ↓
TASK 2  frozen corpus + retrieval conditions
   ↓
TASK 3  smoke test (engineering only)
   ↓
TASK 4  preregistered full pilot
   ↓
HARD SCIENTIFIC GATE
   ├── KILL      -> stop P0; preserve artifacts
   ├── UNCLEAR   -> stop; research lead decides one predeclared follow-up
   └── CONTINUE  -> TASK 5 mechanism experiments
                         ↓
                    TASK 6 selection/refinement
                         ↓
                    TASK 7 robustness + human audit
                         ↓
                    PAPER HANDOFF
```

Codex may autonomously proceed through Tasks 0–4. It must stop at the hard scientific gate.

---

# TASK 0 — Repository and specification audit

## Prompt

```text
TASK 0: Audit the repository and convert the preregistered pilot into an implementation checklist.

Do not implement the experiment yet.

Actions:
1. Read all four canonical files listed in the master prompt.
2. Inspect the existing repository tree and dependencies.
3. Identify every scientific requirement that must be represented in code/config/data.
4. Create `experiments/idea_collapse/STATUS.md`.
5. Create `experiments/idea_collapse/IMPLEMENTATION_PLAN.md` containing:
   - modules/files to create
   - CLI entry points
   - config schema
   - output schema
   - test plan
   - API/provider abstraction
   - reproducibility metadata
   - expected cost-bearing operations
   - known blockers
6. Map each preregistered hypothesis and metric to the code/output that will test it.
7. Explicitly list anything ambiguous. Resolve minor engineering ambiguity conservatively; do not alter scientific assumptions.

Definition of done:
- No experiment has run.
- Every preregistered requirement has a concrete implementation target.
- The plan distinguishes engineering smoke tests from scientific runs.
- STATUS.md says TASK 0 COMPLETE.

Then continue to TASK 1 automatically.
```

### Research-lead acceptance criteria

- No scientific claim changed.
- No new metric elevated to primary status.
- No unnecessary agent framework.
- Clear provenance schema.

---

# TASK 1 — Minimal reproducible infrastructure

## Prompt

```text
TASK 1: Implement the smallest reproducible experiment framework needed for the P0 pilot.

Required capabilities:
- frozen YAML/TOML/JSON experiment configs
- deterministic run IDs
- corpus SHA256
- prompt SHA256
- model/provider/version capture
- retriever name/version/config capture
- seed capture
- raw response preservation
- JSONL trace writing
- parse-failure retention
- resumable/cached runs
- analysis reads immutable traces rather than calling models

Suggested minimal tree (adapt only when justified):
experiments/idea_collapse/
  configs/
  corpus/
  retrieval/
  generation/
  metrics/
  runs/
  analysis/
  tests/

Implement provider interfaces so at least two model families can be configured without changing experiment logic. Do not hard-code secrets.

Add unit tests for:
- hashing/provenance
- trace schema
- retrieval result serialization
- structured response parser including failure path
- deterministic run-ID creation
- cache/resume behavior

Do not build paper figures yet.

Run tests and record exact commands/results in STATUS.md.

Definition of done:
- offline unit tests pass;
- one fake/mock end-to-end run writes a valid trace;
- no fabricated mock trace is mixed into scientific output directories;
- STATUS.md says TASK 1 COMPLETE.

Then continue to TASK 2 automatically.
```

---

# TASK 2 — Frozen corpus and retrieval interventions

## Prompt

```text
TASK 2: Build and freeze the pilot corpora, then implement preregistered retrieval conditions.

Domains:
1. model editing / knowledge updating
2. LLM agents / tool-use evaluation
3. post-training / optimization dynamics

Corpus target:
ICLR 2024–2026 titles + abstracts + metadata, approximately 200–500 relevant papers per domain where feasible.

Required output fields:
paper_id, year, title, abstract, keywords, openreview_url, domain tags/provenance.

Requirements:
- freeze the corpus before scientific generation;
- save raw acquisition metadata when legally/technically available;
- compute SHA256 for each frozen source table;
- never silently mutate a frozen corpus;
- if a domain has insufficient relevant papers, broaden the documented taxonomy rather than pad with irrelevant samples.

Implement conditions:
C0 topic_only_no_retrieval
C1 topk_relevance: fixed k=12, dense cosine retrieval, same candidate pool
C2 diversified_retrieval: same candidate pool + embedding model, preregistered MMR
Optional controlled variant only if cheap and clean: disjoint_neighborhood with a relevance floor.

Also implement the preregistered query-paraphrase control needed to distinguish deterministic identical-query exposure from ranking effects.

Before downstream generation, produce an exposure-only report showing:
- pairwise source Jaccard
- weighted overlap
- unique source coverage
- source HHI
- source Gini
for C1 vs C2.

This exposure report is an engineering/scientific sanity check, not yet evidence for H2.

Do not tune MMR using generated-idea diversity.

Definition of done:
- all corpora frozen and hashed;
- C0/C1/C2 retrieval paths tested;
- retrieval traces are inspectable;
- exposure metrics execute reproducibly;
- STATUS.md says TASK 2 COMPLETE.

Then continue to TASK 3 automatically.
```

---

# TASK 3 — Smoke test, not scientific evidence

## Prompt

```text
TASK 3: Run a small end-to-end smoke test solely to validate infrastructure.

Use at most 10 seeds per selected condition/domain as needed to catch engineering errors. Mark every output with `run_purpose=smoke_test`.

Validate:
- model calls work;
- exact model/version strings are captured;
- structured fields parse;
- parse failures are retained;
- retrieval context is exactly the intended context;
- caches/resume work;
- C0 truly receives no retrieved abstracts;
- C1/C2 use the same candidate corpus and embedding model;
- no condition leaks into another;
- analysis can run from saved traces offline.

Do NOT:
- calculate a final p-value and call it a result;
- choose hyperparameters based on which condition looks better;
- alter hypotheses because of smoke-test trends;
- present smoke outputs in PILOT_RESULT.md.

If engineering failures exist, fix them and rerun the minimum smoke checks required.

Before the full pilot, freeze:
- generation prompt text + hash
- structured output schema
- retrieval configs
- analysis config
- primary/secondary metric list

Save the frozen preregistration snapshot as:
`experiments/idea_collapse/runs/PILOT_LOCK.json`

Definition of done:
- pipeline is technically healthy;
- PILOT_LOCK.json exists;
- STATUS.md says TASK 3 COMPLETE.

Then continue to TASK 4 automatically.
```

---

# TASK 4 — Full preregistered pilot

## Prompt

```text
TASK 4: Execute the full preregistered P0 pilot using the frozen PILOT_LOCK.json.

Target design:
3 domains × 3 retrieval conditions × 2 model families × 30 independent runs = 540 ideas.

If provider cost/quota prevents the full design, do not silently reduce it. Record exactly what completed and why. A partial run can be analyzed descriptively but cannot be labelled the completed preregistered pilot.

Generation output per run:
- research_question
- claimed_gap
- method_sketch
- key_experiment
- why_nontrivial
plus full raw response and trace metadata.

Primary retrieval measurements:
- source Jaccard
- weighted overlap
- unique coverage
- HHI
- Gini

Idea-diversity measurements must include at least two non-equivalent families:
A. semantic: pairwise distance + cluster/effective-cluster behavior
B. structural: normalized tuple of
   (problem object, failure/assumption, intervention/method, evaluation target)
   with exact/partial/predefined-neighbor collision rates

Also plot/compute portfolio diversity growth with N.

Statistics:
- report effect sizes, not only p-values;
- use bootstrap confidence intervals for condition contrasts;
- analyze per-domain and per-model before pooled summaries;
- do not hide heterogeneous or reversed effects;
- label all exploratory analyses as exploratory.

Quality sanity check:
Measure feasibility/technical-depth proxies separately from diversity. Do not claim a diversity win if C2 simply produces incoherent/random ideas.

Produce exactly these research-facing artifacts:
1. `PILOT_RESULT.md`
2. `analysis/pilot_summary.json`
3. machine-readable metric tables
4. a small set of diagnostic figures, not publication polishing

`PILOT_RESULT.md` must contain:
- design actually completed
- deviations from PILOT_LOCK
- H1 result
- H2 result
- H3 quality sanity result
- model/domain heterogeneity
- metric agreement/disagreement
- strongest alternative explanations
- failed/negative evidence
- decision table against preregistered kill/continue criteria
- one final line containing exactly one provisional recommendation:
  `RECOMMENDATION: KILL`
  `RECOMMENDATION: UNCLEAR`
  or
  `RECOMMENDATION: CONTINUE`

Important: this is Codex's evidence-based recommendation, not authorization to continue.

HARD SCIENTIFIC GATE:
After committing PILOT_RESULT.md and all reproducible outputs, STOP. Do not start TASK 5. Wait for the research lead to place an explicit decision in `experiments/idea_collapse/DECISION.md`.
```

---

# HARD SCIENTIFIC GATE — Research lead only

Codex must not create the decision itself.

Expected file format:

```text
# P0 Decision

Decision: CONTINUE | KILL | ONE_FOLLOWUP
Date: YYYY-MM-DD

Evidence:
- ...

Reasoning:
- ...

Allowed next scope:
- ...

Forbidden post-hoc changes:
- ...
```

Rules:

- `KILL`: preserve all results; do not rescue the topic by renaming it.
- `ONE_FOLLOWUP`: one tightly scoped experiment resolves a specific ambiguity; no fishing expedition.
- `CONTINUE`: unlock Tasks 5–7.

---

# TASK 5 — Mechanism: where does diversity disappear?

Run only after explicit `Decision: CONTINUE`.

## Prompt

```text
TASK 5: Move from phenomenon to mechanism without changing the primary story.

Goal:
Decompose whether population convergence comes from:
1. generator prior,
2. shared source exposure,
3. relevance ranking concentration,
4. problem-framing mediation.

Required controlled interventions should include, where feasible:
- identical model + controlled source-overlap levels;
- fixed retrieved sources + prompt paraphrase;
- cross-model generation on identical exposure;
- matched-relevance but different-source neighborhoods;
- disjoint-neighborhood condition with relevance floor.

Key test:
Does manipulating source overlap while approximately holding relevance/quality constant change problem-method collision?

Do not merely regress idea similarity on source similarity and call that causal.

Produce:
- `MECHANISM_RESULT.md`
- mediation/intervention tables
- a figure tracing source exposure -> framing -> idea collision
- explicit alternative explanations that remain viable.

Stop if the effect cannot survive controlled source exposure manipulation. Do not compensate by adding a more complex agent.
```

---

# TASK 6 — Selection and refinement pressure

Run only if Task 5 leaves a credible retrieval-stage mechanism.

## Prompt

```text
TASK 6: Test whether scientific idea selection/refinement further compresses portfolio diversity.

Use a fixed candidate pool so generation is held constant.

Compare at minimum:
- random selection
- single LLM judge top-k
- cross-family LLM judge
- quality-diversity/MMR-style selection

Measure both:
- retained scientific quality/feasibility
- portfolio diversity/collision

Test whether same-family generator+judge produces stronger convergence than cross-family judging.

Do not frame this as 'LLM judges are bad' unless the experiment establishes that claim. The target is selection pressure on the research portfolio.

Produce `SELECTION_RESULT.md` and a combined stage-wise diversity curve:
generation -> retrieval-conditioned generation -> selection -> refinement.
```

---

# TASK 7 — Robustness and human audit

## Prompt

```text
TASK 7: Attempt to falsify the final claim before paper handoff.

Required robustness checks:
- >=3 research domains
- >=2 model families
- prompt paraphrase robustness
- alternative embedding representation
- at least one non-embedding structural diversity measurement
- stratified blind human audit for duplicate/distinct idea judgments
- inspect quality-diversity trade-off
- identify whether conclusions change under plausible metric choices

Actively search for counterexamples:
- domain where top-k increases diversity
- model family where effect disappears
- high-overlap sources that still yield diverse questions
- low-overlap sources that still converge

Report them; do not hide them.

Produce `ROBUSTNESS_RESULT.md` containing:
- what survived
- what failed
- scope conditions
- claims we are NOT entitled to make
- final evidence graph from each paper claim to experiment artifacts.

Then stop for research-lead paper handoff.
```

---

# Paper handoff contract

Codex should not write a polished paper before the evidence chain is frozen.

When requested after Task 7, Codex may prepare technical materials only:

- exact methods description from configs/code;
- dataset/corpus construction description;
- experiment tables;
- reproducibility appendix;
- artifact manifest;
- figure-generation scripts;
- limitations observed in runs.

Research lead owns:

- main scientific claim;
- novelty positioning;
- related-work interpretation;
- title/abstract/introduction;
- reviewer strategy;
- claims that go beyond direct experiment outputs.

---

# Mandatory anti-p-hacking rules

Codex must treat the following as hard constraints:

1. **No outcome-dependent metric substitution.**
   If a preregistered metric is noisy or broken, report that; a replacement is exploratory unless approved before inspecting its treatment result.

2. **No selective run deletion.**
   API errors, parse errors, refusals, and incoherent outputs receive explicit status codes and remain counted.

3. **No condition-dependent prompting.**
   Retrieval conditions differ only in preregistered evidence exposure unless a specific controlled experiment says otherwise.

4. **No hidden corpus mutation.**
   Corpus changes require a new hash and a new experiment version.

5. **No hyperparameter tuning on final hypothesis metrics.**
   Retrieval diversity parameters must be fixed before final idea measurements.

6. **No 'positive result' requirement.**
   A robust null result is acceptable and should trigger KILL if it invalidates P0.

7. **No automatic topic rescue.**
   A failed P0 remains failed until the research lead chooses a new research question.

---

# Codex checkpoint response format

At the end of each task, Codex should respond using this compact format:

```text
TASK: <n/name>
STATUS: COMPLETE | BLOCKED | PARTIAL
COMMIT: <sha>

DONE:
- ...

TESTED:
- command -> result

ARTIFACTS:
- path

DEVIATIONS/BLOCKERS:
- none | ...

SCIENTIFIC OBSERVATIONS:
- only observations justified at this stage

NEXT:
- next allowed task, or STOP AT GATE
```

This keeps ChatGPT/human review fast and prevents conversational summaries from replacing repository evidence.

---

# Recommended first Codex message

After the master prompt, the first command to Codex can simply be:

```text
Begin TASK 0 now. Work autonomously through TASK 4 unless genuinely blocked. Respect the HARD SCIENTIFIC GATE and stop after committing PILOT_RESULT.md. Do not begin judge/refinement experiments or paper writing before an explicit DECISION.md authorizes them.
```
