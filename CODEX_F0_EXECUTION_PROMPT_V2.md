# CODEX F0 EXECUTION PROMPT V2 — ICLR-Style Engineering Contract

> Repository: `whzy3185/iclr`
> Status: **AUTHORIZED**
> Branch: `codex/f0-source-feasibility`
> Scientific proposal generation: **FORBIDDEN**
> This file is the highest operational authority for F0.

## 0. What changed from V1

This V2 supersedes `CODEX_F0_EXECUTION_PROMPT.md` where they conflict.

V1 correctly specified the engineering phases but used overly rigid source-count and raw-caliper thresholds. V2 keeps the engineering pipeline and replaces the decision logic with ICLR-style construct validity + controlled alternatives + pilot readiness.

Important:

- F0 does **not** decide full-paper sample size.
- F0 only decides whether there is enough auditable source structure for a construct/variance pilot.
- Full confirmatory N will be frozen after the pilot from block-level variance / annotation reliability / precision requirements.
- Do not optimize any F0 choice using future scientific outcomes.

Read before execution:

1. `README.md`
2. `CODEX_F0_EXECUTION_PROMPT_V2.md`
3. `CODEX_F0_MASTER.md`
4. `research/iclr_fit_validation/round51_iclr_style_gate_redesign.md`
5. `research/iclr_fit_validation/round27_route_equipoise_and_admissibility_audit.md`
6. `research/iclr_fit_validation/round30_seed_validity_method_masking_and_accessibility.md`
7. `research/iclr_fit_validation/round44_pairwise_matched_evidence_slot_design.md`
8. `research/iclr_fit_validation/round46_source_route_purity_and_mixed_contribution_handling.md`
9. `research/iclr_fit_validation/round50_codex_branch_pi_audit.md`
10. old `CODEX_F0_EXECUTION_PROMPT.md` only for non-conflicting implementation details.

Authority order:

```text
CODEX_F0_EXECUTION_PROMPT_V2.md
> CODEX_F0_MASTER.md
> Round 51 and latest relevant research rounds
> V1 execution prompt
> historical amendments/tasks
```

---

# 1. Mission

Determine whether real ICLR 2025/2026 literature supports a sufficiently clean bank of:

```text
method-neutral ICLR 2026 seed
×
scientifically plausible Route A / Route B
×
pairwise matched ICLR 2025 evidence slots
```

for a later controlled pilot.

F0 does not test whether evidence changes LLM research choices.

Do not generate scientific proposals.

---

# 2. Branch / migration contract

Start from latest `origin/main`.

```bash
git fetch origin main codex/p0-task0-task1
git switch --detach origin/main
git switch -c codex/f0-source-feasibility
```

Never merge `codex/p0-task0-task1` wholesale.

Permitted migration after inspection:

```text
canonical JSON / SHA256 utilities
git-state provenance
exclusive immutable writes
official ICLR proceedings parser
parser/provenance tests
```

Do not migrate as scientific authority:

```text
old top-k/MMR experiment
old fixed 3-domain schema
old 540-generation design
old pilot configs
old scientific generation runner settings
old diversity metrics / decision gates
```

Record every migrated function/file in:

```text
experiments/idea_collapse/feasibility_1/MIGRATION_LOG.md
```

---

# 3. Hard safety rails

F0 must perform exactly zero scientific proposal generations.

Forbidden:

- no-context research proposal generation;
- evidence-conditioned proposal generation;
- baseline route propensity estimation;
- treatment-effect estimation;
- outcome-aware seed/route/matching optimization;
- novelty/quality ranking of imagined proposals;
- paper results writing.

Allowed LLM use is limited to source transformation/classification, e.g. provisional paper-route annotation or method masking, with input/prompt/model/raw output/provisional status preserved and human audit packets emitted.

---

# 4. Active engineering layout

New F0 code:

```text
experiments/idea_collapse/f0/
    provenance.py
    schemas.py
    acquire_proceedings.py
    acquire_abstracts.py
    resolve_public_dates.py
    build_seed_candidates.py
    route_annotation.py
    retrieval.py
    matching.py
    packet_simulation.py
    reporting.py
    config/f0.json
```

Tests:

```text
experiments/idea_collapse/tests/f0/
```

Generated artifacts:

```text
experiments/idea_collapse/feasibility_1/
```

---

# 5. E0 — engineering migration

Port only audited reusable utilities.

Acceptance:

```text
no old experimental arm names in active F0 code
no hard-coded old 3-domain scientific schema
no scientific-generation imports in F0 modules
all migrated functions covered by tests
MIGRATION_LOG complete
```

Checkpoint commit:

```text
f0: migrate audited source-ingestion and provenance utilities
```

---

# 6. E1 — official ICLR source acquisition

Evidence universe:

```text
ICLR 2025 accepted papers
```

Seed universe:

```text
ICLR 2026 accepted papers
```

Canonical universe comes from official ICLR proceedings/OpenReview-linked metadata.

Acquire:

```text
paper_id
year
title
abstract
proceedings URL
PDF URL if available
OpenReview URL if available
authors/keywords/area if available
```

Preserve raw hashes and parse failures.

Target title+abstract coverage is >=95%, but this is a data-quality target, not an automatic scientific failure threshold.

If coverage <95%:

- characterize missingness;
- continue if the missing subset is small/non-systematic enough to audit;
- mark `ACQUISITION_INCOMPLETE`;
- never silently shrink the denominator.

If coverage <80%, stop normal execution and write `ENGINEERING_BLOCKED` unless a clearly justified official-source recovery path exists.

Required:

```text
raw_sources_manifest.jsonl
iclr2025_papers.jsonl
iclr2026_papers.jsonl
acquisition_failures.jsonl
corpus_hash.txt
```

---

# 7. E2 — temporal cleanliness

Primary causal-clean evidence subset:

```text
first_public_date > 2024-08-31
```

Resolve earliest confidently discovered public date from arXiv/OpenReview/official preprint metadata.

Statuses:

```text
CLEAN
FAIL_PRE_CUTOFF
UNKNOWN
AMBIGUOUS_MATCH
```

Never infer CLEAN from proceedings year/date alone.

Report clean/unknown/fail/ambiguous rates by topic/subfield if possible.

Temporal unknowns remain in the ledger and may be used only in clearly labeled sensitivity analyses later; they do not enter the primary clean F0 pool.

---

# 8. E3 — method-neutral seed candidates

Construct ICLR 2026 seed questions by masking the focal solution.

Required fields follow `CODEX_F0_MASTER.md`, including leakage diagnostics.

A seed is eligible for source retrieval only if it preserves a real technical problem while not prescribing a research route.

Do not automatically reject based on machine score. Emit status and a human-audit packet.

No seed may be solved during F0.

---

# 9. E4 — frozen source retrieval

Default dense model:

```text
BAAI/bge-base-en-v1.5
```

Default reranker:

```text
BAAI/bge-reranker-base
```

Pin exact revision. If unavailable, use an open substitute only with `DEGRADED` status.

For each seed:

1. dense retrieve top 200 CLEAN ICLR 2025 candidates;
2. rerank them when reranker is available;
3. preserve all scores/ranks;
4. do not rewrite queries using route labels.

## Primary relevance floor

Primary matching candidates:

```text
top 100 after reranking
```

If reranker is unavailable:

```text
top 100 dense
```

Sensitivity only:

```text
top 50
top 150
```

The purpose is to ensure alternatives come from a genuinely relevant neighborhood, not to maximize later effect size.

---

# 10. E5 — source-route annotation

Fine routes:

```text
BUILD_IMPROVE
DIAGNOSE_STRESS_TEST
MEASURE_EVALUATE
EXPLAIN_MECHANISM_THEORY
OPTIMIZE_EFFICIENCY
VERIFY_FALSIFY_REPLICATE
MIXED_UNCLEAR
```

Also annotate:

```text
secondary_routes
route_purity
opposite-route contamination
fine confidence
ARTIFACT / KNOWLEDGE / BOTH / UNCLEAR
rationale source span
backend/version
```

Primary source-route pool uses:

```text
primary_route != MIXED_UNCLEAR
route_purity >= .70
fine_route_confidence >= .70
```

Sensitivity:

```text
purity/confidence .60 / .70 / .80
```

These thresholds define audit strata; do not call .70 a universal scientific truth.

Run a simple lexical route baseline and report its predictability as a future priming-risk diagnostic.

---

# 11. E6 — fixed route contrasts

Audit exactly:

```text
R1 BUILD_IMPROVE        vs DIAGNOSE_STRESS_TEST
R2 BUILD_IMPROVE        vs MEASURE_EVALUATE
R3 BUILD_IMPROVE        vs EXPLAIN_MECHANISM_THEORY
R4 DIAGNOSE_STRESS_TEST vs EXPLAIN_MECHANISM_THEORY
```

Do not replace weak-coverage pairs with attractive post-hoc alternatives.

Report every seed × R1-R4 candidate, including failures.

Also report 3+ route coverage as exploratory source structure only.

---

# 12. E7 — pairwise matching, V2 primary policy

For each seed × route pair, form:

```text
slot_j = (A_paper_j, B_paper_j)
```

using deterministic minimum-cost bipartite matching without replacement.

## Matching features

Standardize within the seed's primary top-100 candidate pool:

```text
dense relevance
reranker relevance if present
log abstract token length
temporal position / public date
```

Also include topic embedding distance explicitly in pair cost.

Freeze the matching-cost formula/config before scientific outcomes exist.

Do not tune cost weights after seeing any treatment output.

## No universal raw STRICT/BASE/RELAXED calipers

V1 raw thresholds such as `topic cosine <= .20` or `date <=365 days` are no longer decision gates.

Preserve them only if useful as descriptive sensitivity diagnostics.

## Primary block balance criteria

For a proposed k-slot block, compare the all-A and all-B endpoint packets.

Label `PRIMARY_BALANCED` only when all hold:

```text
all A/B papers satisfy the primary top-100 relevance floor
abs(SMD dense relevance) <= .25
abs(SMD reranker relevance) <= .25 if reranker exists
abs(SMD log token length) <= .25
abs(SMD temporal position) <= .25
no scalar covariate abs(SMD) > .50
```

Additionally:

- compute optimal mean match cost;
- deterministically generate a null distribution from random cross-route pairings from the same candidate bank;
- require optimal mean match cost to be below the 25th percentile of that null distribution;
- report topic-distance median/p90 continuously rather than enforcing a universal cosine cutoff.

The `.25/.50` balance values are engineering diagnostics; all continuous values must be reported. They are not claims of a natural threshold.

If a scientifically reasonable block narrowly misses one diagnostic, preserve it as `NEAR_BALANCED` rather than silently deleting it. It does not count toward the primary pilot-readiness panel until human/PI review.

## k values

Audit:

```text
k=6
k=8
k=12
```

F0 does not force one global k.

---

# 13. E8 — equipoise audit packet

For every `PRIMARY_BALANCED` block with k>=6, emit a human review row.

Codex must not invent human ratings.

Required human fields:

```text
A relevance
B relevance
A scientific plausibility
B scientific plausibility
distinguishability
equipoise
non-subsumption
annotatability
composability
route dominance
notes
```

Important:

> A block can pass source matching and still fail scientific equipoise.

F0 readiness means `ready for F1 human construct audit`, not `ready for confirmatory generation`.

---

# 14. E9 — packet assignment simulation

For blocks with k>=8, simulate paper-ID-only packets at:

```text
alpha=0,.25,.5,.75,1
```

using the same matched slot bank and balanced/complementary slot assignments.

Report endpoint/middle-condition balance and number of independent packet realizations possible.

No LLM proposal calls.

---

# 15. E10 — F0 recommendation, V2

F0 categories now describe **pilot readiness**, not publication adequacy.

## READY_FOR_F1_CONSTRUCT_PILOT

All should hold:

```text
>=12 unique seeds have >=1 PRIMARY_BALANCED route pair at k>=6
>=8 of those unique seeds also support k>=8
>=2 of R1-R4 are represented by >=3 unique seeds each
source/purity/temporal attrition is fully reported
no systematic relevance imbalance is hidden by matching
human equipoise audit packets are ready
```

Subfield diversity is reported but is NOT a hard F0 pass/fail requirement.

Interpretation:

> Enough source structure exists to run a 12-seed construct/variance pilot. This does not authorize a full confirmatory study.

## LIMITED_PILOT_ONLY

Use when:

```text
6-11 unique seeds support PRIMARY_BALANCED k>=6
```

or >=12 exist but usable blocks are overwhelmingly concentrated in one route contrast or one very narrow scientific setting.

Interpretation:

> A small construct pilot is still informative, but broad ICLR claims are not yet supported.

## REDESIGN_REQUIRED

Use when:

```text
<6 unique seeds support PRIMARY_BALANCED k>=6
```

or clean matching requires clearly weak/off-topic evidence, or route purity / seed neutrality / temporal audit is too poor for an interpretable intervention.

Interpretation:

> Redesign corpus/treatment before scientific generation; possibly kill the topic.

## ENGINEERING_BLOCKED

Use when source/network/tooling failures prevent a meaningful F0 conclusion.

Do not mislabel engineering blockage as scientific source infeasibility.

---

# 16. Why 12 / 8 / 6 are used here

These are **not ICLR acceptance thresholds**.

They only define a practical pilot panel:

- ~12 independent seeds is enough to test annotation reliability, packet variance, route-response measurement, and gross heterogeneity before a full study;
- requiring some k=8 blocks verifies that the intended five-level evidence-mixture treatment is constructible without forcing every seed to support k=12;
- fewer than ~6 independent seeds provides too little source variation for a useful construct pilot and should trigger redesign.

After F1/P0, full-study sample size must be frozen using precision/variance, not these counts.

---

# 17. Full-run planning is explicitly out of scope for F0

Do not decide the final experiment has enough seeds because F0 passes.

After the construct pilot, the research lead will use:

```text
human annotation reliability
within-condition variance
between-seed heterogeneity
packet-realization variance
seed/route attrition
model-family heterogeneity
```

to freeze a full-run N and precision target.

No sequential stopping at p<.05.

---

# 18. Required outputs

Under:

```text
experiments/idea_collapse/feasibility_1/
```

produce at minimum:

```text
README.md
STATUS.md
MIGRATION_LOG.md
raw_sources_manifest.jsonl
iclr2025_papers.jsonl
iclr2026_papers.jsonl
acquisition_failures.jsonl
corpus_hash.txt
temporal_cleanliness.jsonl
temporal_cleanliness_report.md
seed_candidates.jsonl
seed_validity_audit_packet.csv
retrieval_config.json
retrieval_candidates.parquet or jsonl
source_route_annotations.jsonl
route_label_summary.json
route_annotation_audit_packet.csv
lexical_route_baseline.json
route_pair_coverage.csv
multi_route_coverage.csv
matched_evidence_slots.csv
matching_diagnostics/
route_equipoise_audit_packet.csv
packet_balance_simulation.csv
attrition_waterfall.csv
FEASIBILITY_RESULT.md
```

No candidate/failure may vanish from the denominators.

---

# 19. Tests

At minimum test:

```text
proceedings/abstract parsing
canonical hashes and exclusive writes
temporal cutoff/UNKNOWN/AMBIGUOUS
seed schema + focal-paper exclusion
route enum/purity behavior
retrieval deterministic tie handling
candidate relevance floor top50/top100/top150
matching deterministic / no replacement
standardization and SMD calculations
random-pairing null distribution reproducibility
PRIMARY_BALANCED classification
k6/k8/k12 counts
balanced alpha assignment
no duplicate paper within packet
attrition denominator preservation
F0 category classification
hard guard against scientific proposal generation
```

Run all tests and `git diff --check` at each checkpoint.

---

# 20. Commit discipline

Use phase commits and update `STATUS.md` with exact commands/counts/tests/blockers.

Recommended:

```text
f0: migrate audited source-ingestion utilities
f0: acquire official ICLR source corpus
f0: resolve temporal-clean evidence subset
f0: build neutral ICLR 2026 seed candidates
f0: freeze retrieval candidate pools
f0: annotate source routes with audit trail
f0: build balanced pairwise evidence slots
f0: emit equipoise and packet audit artifacts
f0: publish pilot-readiness feasibility result
```

---

# 21. Final handoff

Push `codex/f0-source-feasibility`.

Final response fields:

```text
BRANCH:
FINAL_COMMIT:
F0_RECOMMENDATION: READY_FOR_F1_CONSTRUCT_PILOT | LIMITED_PILOT_ONLY | REDESIGN_REQUIRED | ENGINEERING_BLOCKED
ICLR2025_TOTAL:
ICLR2025_ABSTRACT_COVERAGE:
TEMPORAL_CLEAN_EVIDENCE_COUNT:
ICLR2026_TOTAL:
METHOD_MASKABLE_SEEDS:
MULTI_ROUTE_SEEDS:
K6_PRIMARY_BALANCED_UNIQUE_SEEDS:
K8_PRIMARY_BALANCED_UNIQUE_SEEDS:
K12_PRIMARY_BALANCED_UNIQUE_SEEDS:
R1_R2_R3_R4_K6_COUNTS:
THREE_ROUTE_SEEDS:
SUBFIELD_DISTRIBUTION:
DOMINANT_BLOCKER:
HUMAN_REVIEW_FILES:
TEST_RESULT:
SCIENTIFIC_GENERATIONS_PERFORMED: 0
```

Then STOP.

Do not start baseline generation or treatment generation. The research lead will inspect the branch and issue the next contract.
