# Research Round 50 — PI Audit of Codex Pushed Branch

## 1. Trigger

The user asked to inspect the pushed Codex work and assess the current project state.

Codex work was found on branch:

`codex/p0-task0-task1`

The current `main` branch is substantially newer and contains the F0 source-only design, matched-slot treatment construction, seed/equipoise gates, and latest ICLR-specific collision analysis.

## 2. Branch state

GitHub comparison shows the Codex branch diverged from `main` at merge base:

`93ebaf74f6d155b017c372211ca6b3078d828b3d`

Current Codex branch head:

`7fedda7f3dca906f91fc4404af8a174b907a892d`

Current main at time of audit:

`a36d1bb82a10b0e935371387b7ab915f65a367de`

The branch contains 8 commits not on main; main contains 66 commits after the merge base that are absent from the Codex branch.

Decision: **do not merge the Codex branch wholesale.** Reuse selected engineering assets after rebasing/reimplementation against current `main` and `CODEX_F0_MASTER.md`.

## 3. What Codex completed well

### 3.1 Reproducibility / fail-closed infrastructure

Codex implemented:

- canonical JSON serialization and content hashing;
- immutable/exclusive evidence writes;
- Git commit / dirty-state provenance;
- run IDs bound to outcome-affecting inputs;
- provider abstraction;
- retained raw/failure traces;
- cache/resume checks;
- mock/scientific run separation;
- strict schema validation;
- unit tests.

The branch status reports 28 tests passing after the latest amendment integration.

Most importantly, scientific execution was fail-closed: an attempted scientific invocation was rejected before any provider call/output creation.

This engineering discipline is reusable.

### 3.2 Official ICLR annual-index acquisition

Codex acquired official proceedings title indexes:

- ICLR 2024: 2260 records
- ICLR 2025: 3703 records
- ICLR 2026: 5351 records
- total: 11314 records

Each annual manifest preserves source URL, raw HTML SHA256, index SHA256, retrieval timestamp and count.

The parser explicitly labels these as title indexes rather than pretending they are an abstract corpus.

This is good provenance discipline and is reusable for F0.

### 3.3 No scientific contamination

There were:

- 0 scientific generations;
- 0 smoke scientific runs;
- only mock fixture traces;
- no PILOT_RESULT;
- no model-route estimates;
- no treatment outcomes.

Therefore the branch can be mined for engineering code without contaminating the current preregistered source-only F0 design.

## 4. What is obsolete under the current research design

The Codex branch was built around the older `Shared-Retrieval Research Monoculture / top-k vs MMR / 540 ideas` pilot.

Its implementation plan explicitly treats the old design as canonical, including:

- three old domains;
- top-k vs MMR arms;
- 540 idea generation plan;
- semantic/tuple diversity metrics;
- old quality instrument;
- old query-paraphrase issue.

Those are no longer the active scientific question.

Current main instead studies:

> matched scientific evidence composition -> high-level research-choice response,
> baseline-route-propensity interaction,
> and held-out natural-RAG prediction.

Therefore the following branch artifacts should **not** be treated as current scientific specifications:

- `experiments/idea_collapse/IMPLEMENTATION_PLAN.md`
- `experiments/idea_collapse/configs/pilot.draft.json`
- old scientific generation grid / old H1-H3 definitions
- old top-k/MMR-specific analysis assumptions

The general trace/provenance code may be reused, but its scientific schema must be updated to the current data model.

## 5. Current F0 gap

The pushed branch has **not** completed the actual currently-authorized F0 source-only feasibility task.

The following required artifacts do not yet exist on either main or the pushed branch:

- `experiments/idea_collapse/feasibility_1/FEASIBILITY_RESULT.md`
- temporal-clean abstract corpus with first-public dates;
- method-masked ICLR 2026 seed candidates;
- seed leakage/neutrality audit;
- source route annotation and route-purity audit;
- scientific equipoise audit packet;
- matched A/B evidence slots;
- k=6/8/12 matched-slot coverage;
- 3-route coverage;
- attrition waterfall;
- packet-balance simulation under the current matched-slot design.

Codex currently acquired only annual title indexes. The ICLR 2025 manifest explicitly reports:

`abstracts_acquired: 0`

and

`pilot_eligible: false`.

This is the central fact: **the current scientific F0 has not started yet; only reusable infrastructure and metadata-index acquisition exist.**

## 6. Reusable vs non-reusable assets

### Reuse / port forward

High priority:

- `generation/provenance.py`
- annual proceedings index parser + tests
- immutable write/hash utilities
- strict JSON/schema patterns
- mock/scientific separation
- fail-closed scientific guard pattern
- source manifests / raw source hashes
- selected corpus validation helpers after removing old hard-coded domains

Potentially reuse after adaptation:

- provider abstraction for later P0/P1
- trace journaling/caching
- run ID design

### Do not directly reuse as scientific contract

- old README on branch
- old implementation plan
- `pilot.draft.json`
- old generation prompt / five-field idea schema
- old top-k/MMR intervention logic
- old diversity metrics as primary outcomes
- old fixed three-domain taxonomy

## 7. Main engineering issue found

The old `build_corpus.py` hard-codes:

`model_editing`, `agents_tool_use`, `post_training_optimization`

and assumes OpenReview forum URLs plus the old domain-tag structure.

For current F0, corpus construction must instead support:

- ICLR 2025 evidence universe;
- first-public-date / temporal status;
- source route annotations, including multilabel/purity;
- coarse Artifact/Knowledge contribution family;
- seed-specific retrieval relevance;
- matched-slot source covariates;
- no old three-domain requirement.

Thus `build_corpus.py` is a pattern to refactor, not a file to merge unchanged.

## 8. Current PI verdict

### Scientific status

**CONDITIONAL GO remains unchanged.**

The pushed Codex branch provides no scientific evidence for or against H1-H3 because no current treatment or model outcomes exist.

### Engineering status

**Positive.** Codex demonstrated good reproducibility and fail-closed discipline. The ingestion/provenance foundation is useful.

### F0 status

**NOT YET EXECUTED.**

The next task should not be old TASK 2 or any model generation. It should be:

> create a fresh Codex branch from latest main, port selected engineering assets, and execute `CODEX_F0_MASTER.md` exactly.

## 9. Recommended branch strategy

Do not merge `codex/p0-task0-task1` into main.

Recommended workflow:

1. create a new branch from current `main`, e.g. `codex/f0-source-feasibility`;
2. selectively port/reimplement provenance + annual-index parser + useful tests;
3. record source branch/commit for every ported file;
4. execute only `CODEX_F0_MASTER.md`;
5. produce `feasibility_1/FEASIBILITY_RESULT.md`;
6. stop before all scientific proposal generation;
7. research lead performs PI review before authorizing P0.

This preserves clean scientific provenance and avoids importing stale experimental assumptions.

## 10. Decision

**KEEP project / KEEP Codex engineering / REBASE TASK / DO NOT MERGE OLD BRANCH WHOLESALE.**

The pushed work is useful infrastructure, not the requested F0 scientific-feasibility result.
