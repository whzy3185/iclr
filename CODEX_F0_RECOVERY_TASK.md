# Codex F0 Recovery — Publish, Diagnose, Resume

Version: 1. Date: 2026-09-08.
Authorization: source-only recovery and deterministic tests. Scientific proposal generation: NOT AUTHORIZED.

## 0. Execute this task, not a fresh research program

Read only these current entry points first:

1. `CODEX_F0_EXECUTION_PROMPT.md`;
2. this file;
3. `CODEX_F0_MASTER.md` v2 for source fields and the descriptive sensitivity map;
4. Round 52, sections 1 and 6–12, for the identified validity issues.

For this recovery task, this file overrides conflicting migration, seed-gate, matching and completion instructions in historical F0 prompts. It does not unlock later scientific stages. Do not read fifty historical rounds before resuming ingestion.

Known remote marker: `codex/f0-source-only-snapshot-api` at `5ee1a014e03f5f1dd2543c5c8de0b3ccd553e1c9`.
Its marker reports local branch `codex/f0-source-only-snapshot`, local commit `e3eb75948dcd6745eb77f1def0ad0898cb1c839b`, a local script and cached abstracts. These are leads to verify, not guaranteed local paths.

The immediate objective is an inspectable corrected source-only snapshot. Do not promise a feasible experiment, maximize passing seeds, or run research-idea generation.

## 1. Preserve current work before synchronization

Inspect `git status --short`, `git branch --show-current`, `git log -5 --oneline`, and available worktrees. Record the results without exposing credentials.

Do NOT execute reset --hard, clean -fd, force-push, or delete caches. Do not discard an interrupted F0 branch simply because it has a different name from an earlier prompt.

Preserve uncommitted F0 work in a reviewed commit or separate safe worktree; never automatically commit secrets or raw cache directories. Fetch current main, then integrate the CURRENT F0 instruction files into the preserved F0 branch, or create an integration worktree that selectively imports the NEW F0 implementation and artifacts. Do not wholesale import the obsolete p0 study. Do not require rewriting reusable F0 code into a new layout before it can be audited.

Record `baseline_main_sha`, `implementation_parent_sha`, active branch, actual code paths, and SHA256 of the three active instructions. Pin this snapshot for the run; do not continuously change specs mid-run.

## 2. R0 — Publish what actually exists

Before another full rerun, publish an inspectable checkpoint containing:

- F0 script/module source;
- actual configuration;
- tests that exist, with honest test status;
- raw-source cache index with URLs, byte hashes, retrieval/parse status and local cache keys;
- parsed-corpus manifests/counts;
- first-run seed-gate diagnostics;
- a small deterministic audit excerpt, selected before inspecting matching success.

Retain the first failed run in an immutable run directory. Mark it `INCOMPLETE_GATE_SHORT_CIRCUIT`, not NOT_FEASIBLE. Corrected runs use new run IDs/config hashes.

The existing local path reported by the marker is:
`experiments/idea_collapse/feasibility_1/scripts/f0_source_only_audit.py`.
Verify that it exists before using it. Existing equivalent modules are acceptable. Record actual entry points; do not invent commands already executed.

Do not claim that a local commit or a remote text marker publishes the underlying artifacts. A handoff needs an accessible commit with code plus manifests and audit excerpts. Large raw caches may stay excluded; give their hashes, retrieval/rebuild instructions and licensing notes. Never upload credentials.

If transport fails, retain the prepared commit and a structured blocker, and publish through an already authorized alternative only if available. No credentials or paid services may be invented.

## 3. R1 — Make seed gating explicit and unit-testable

Replace a single `seed_pass` Boolean with at least:

```text
extractable: bool
source_matching_allowed: bool
confirmatory_eligible: bool
risk_flags: list[str]
hard_errors: list[str]
review_state: NOT_REVIEWED | REVIEW_PENDING | REVIEWED
```

Recovery policy:

- missing/empty source abstract, corrupted identity, or focal-paper self-inclusion: structural error; retain row and exclude the broken object from applicable matching;
- nonempty source-derived seed with similarity/ambiguity warnings: allow PROVISIONAL source matching, preserve every flag, keep confirmatory_eligible=false;
- explicit unrepaired focal solution encoded in the seed: retain and route to repair/diagnostic queue, not the primary candidate analysis;
- human review absent: never fabricate PASS/FAIL; confirmatory eligibility remains false;
- expected common problem vocabulary is not automatically solution leakage;
- do not disable all leakage flags just to recover coverage.

Emit `seed_gate_audit.jsonl`: seed ID, source span, every triggered rule, extractability, source-matching decision, exclusion/repair reason. Emit a deterministic human sample of flagged AND unflagged seeds, including boundary cases. Sampling rules must not depend on future proposal outcomes.

All-seed rejection is an anomaly requiring diagnostics, not permission to label the source universe impossible.

## 4. R2 — Preserve backend and temporal uncertainty

Backend enum:

```text
DENSE_WITH_RERANKER
DENSE_ONLY
LEXICAL_PROVISIONAL
UNAVAILABLE
```

TF-IDF and BM25-like retrieval may be used for a cheap provisional screen; do not name their scores `dense_relevance` or treat them as independent semantic validation. Keep backend-specific score columns and absent scores null. Record formula/version/vocabulary/candidate-pool hash. Do not run dense calipers against lexical scores.

For source annotation retain input text, evidence spans, qualitative labels, backend and raw parser output where applicable. Self-reported purity/confidence is uncalibrated. If a backend does not produce a meaningful purity descriptor, emit NOT_ASSESSED for those grid cells; do not synthesize 0.70 from a keyword hit.

Resolve earliest DISCOVERED public dates, with record-identity match evidence and search coverage. Temporal tiers describe observed publication timing, not proof that a model never saw a paper. UNKNOWN is not PRE_CUTOFF and is not POST_CUTOFF. Mixed known/unknown dates require distinct report rows.

Preserve the v2 T0/T1/T2 descriptive map when the required fields exist. A missing date/backend/annotation can block a grid cell without blocking unrelated ingestion.

## 5. R3 — Correct matching and zero/missing semantics

The reported `max_matched_slots` must mean maximum admissible disjoint pair count, not the result of a greedy approximation.

Objective, in this exact order:

1. maximize admissible matching cardinality;
2. minimize cost among maximum-cardinality solutions;
3. deterministic tie-breaking.

Implement using an appropriate bipartite matching/min-cost-flow method. If a heuristic is temporarily used, report `HEURISTIC_LOWER_BOUND` and never label it maximum. A full pair assignment that forces inadmissible edges is also forbidden.

Required tiny regression fixture:

```text
A0-B0 cost=1
A0-B1 cost=2
A1-B0 cost=2
```

Expected maximum cardinality=2, minimum cost at cardinality 2=4. Greedy lowest-edge matching returns only 1; unconstrained optional minimum cost returns empty. The report must not confuse these objectives.

Keep existing STRICT/BASE/RELAXED as descriptive regimes, not acceptance truth. For matching features distinguish problem/task compatibility, nuisance length/date variables, and intended route contrast. Full-abstract embedding distance is a diagnostic unless an audited primary rule explicitly uses it. Add a clearly labeled comparison with/without that caliper only when embeddings exist; do not select a winner by proposal effects.

No automatic numerical gate defines scientific feasibility. A complete sensitivity map reports measurements and unavailable cells honestly.

Coverage cell schema:

```json
{
  "run_id": "...",
  "seed_id": "...",
  "route_pair_id": "R1",
  "temporal_tier": "T0_COMMON_STRICT",
  "retrieval_backend": "LEXICAL_PROVISIONAL",
  "matching_regime": "...",
  "purity_regime": "NOT_ASSESSED",
  "k": 8,
  "cell_status": "NOT_RUN",
  "n_A": null,
  "n_B": null,
  "max_matched_slots": null,
  "reason": "..."
}
```

Allowed cell_status: MEASURED, NOT_RUN, BLOCKED, MISSING_COVARIATES, PENDING_REVIEW.
A real zero uses MEASURED and a numeric 0. An unexecuted matcher never writes 0. Human eligibility is separate from measured source counts.

## 6. R4 — Packet and independence diagnostics only

For measured banks, retain descriptive k=4/6/8/12 coverage. Do not round k=6 into exact quarter treatments: use exact feasible fractions or mark quarter design unsupported.

Report separately:

- unique seeds;
- seed-route blocks;
- distinct source papers;
- slot banks;
- assignments within each bank;
- source reuse between banks and seeds.

Permuting the same documents is not a new independent source bank. Multiple contrasts of one seed are not independent seeds. A/B assignment must balance slot identities and packet order according to a deterministic recorded schedule. These are paper-ID manifests, not proposal generations.

Do not create a full factorial computation explosion unnecessarily: cache embeddings/annotations and reuse admissible-edge computations. Every planned grid cell must have an explicit status, even when not executed.

## 7. R5 — Deliver a bounded source-only report

Required outputs under the existing `feasibility_1/` root or a versioned subdirectory, with pointers from STATUS:

```text
RECOVERY_INVENTORY.md
SOURCE_ONLY_RUN_MANIFEST.json
seed_gate_audit.jsonl
seed_gate_audit_sample.csv
retrieval_backend_manifest.json
coverage_balance_frontier.csv
matching_test_report.json
source_reuse_summary.json
FEASIBILITY_RESULT.md
STATUS.md
```

Reuse v2 corpus/route/temporal artifacts rather than duplicating files. The run manifest maps each output to path, SHA256, status, producing command and config/code hash. CSV/JSON counts must reconcile to their source rows.

FEASIBILITY_RESULT must distinguish: independently inspectable artifacts, locally reported-but-unpublished artifacts, measured zeros, unrun stages, lexical-screen results, calibrated semantic results, and human-review-pending claims.

State only F0_COMPLETE / F0_INCOMPLETE / F0_BLOCKED, plus `SCIENTIFIC_DECISION=RESEARCH_LEAD_REQUIRED`. Completion concerns the declared source-only scope; do not mark full F0 complete when semantic matching is unexecuted and only a lexical screen is complete.

## 8. Acceptance tests, not arbitrary scientific count thresholds

Add tests using the existing test runner; do not change frameworks just for this task:

1. similarity warning on an extractable seed preserves flags and permits provisional matching;
2. missing source text retains a row and records a structural failure;
3. explicit solution leakage does not become confirmatory eligible;
4. unknown public date is not classified as known post-cutoff;
5. lexical backend never fills semantic score columns;
6. unrun grid cells use null, while measured empty matchings use zero;
7. the three-edge fixture returns maximum cardinality 2;
8. no source is used twice within a without-replacement matching;
9. focal source is excluded from its own evidence pool;
10. k=6 never claims exact 25%/75% packet fractions;
11. distinct seed counts differ from block/assignment counts where expected;
12. rerun from cached inputs preserves normalized data hashes, with volatile timing metadata separated;
13. no recovery path invokes a research-proposal generator.

The design-only counterexamples can additionally run with:

```bash
python research/iclr_fit_validation/design_checks/round52/design_counterexamples.py --test
```

Passing that script does NOT establish that the F0 pipeline tests pass.

## 9. Final handoff format and stop

```text
BRANCH:
REMOTE_COMMIT:
BASELINE_MAIN_SHA:
SPEC_HASHES:
CODE_AND_CONFIG_PUBLISHED:
F0_DATA_STATUS:
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
ABSTRACT_COUNTS_VERIFIED_FROM_PUBLISHED_MANIFEST:
SOURCE_MATCHING_SEEDS:
FLAGGED_BUT_PROVISIONALLY_MATCHED_SEEDS:
STRUCTURAL_FAILURE_SEEDS:
RETRIEVAL_BACKEND:
MATCHER_OBJECTIVE:
MEASURED_ZERO_CELLS:
UNRUN_OR_UNKNOWN_CELLS:
UNIQUE_SEEDS_VS_ROUTE_BLOCKS:
TEST_COMMAND_AND_RESULT:
REMAINING_BLOCKERS:
HUMAN_AUDIT_PATHS:
SCIENTIFIC_PROPOSAL_GENERATIONS: 0
```

STOP after publishing the corrected source-only snapshot. Do not implement P0/P1 statistics, run research-proposal generation, select model families by imagined effects, train a new retriever, or write paper results.

The next research-lead action is code/data review followed by REPAIR_PIPELINE, PREPARE_F1, REVISE_SOURCE_DESIGN, or REQUEST_MISSING_ARTIFACTS. This task file is an execution specification, not evidence that a Codex session has been launched.
