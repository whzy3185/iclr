# Codex Feasibility Task 1 — Source-Only ICLR Treatment Audit

> Status: AUTHORIZED
> Scope: SOURCE-ONLY FEASIBILITY
> Scientific outcomes: FORBIDDEN
> Research lead: ChatGPT / human

## 0. Purpose

Determine whether the current ICLR experiment is **actually constructible** before any model-prior estimation or treatment generation occurs.

The scientific design asks whether matched real scientific literature can steer an LLM among multiple valid research routes, with treatment packets frozen before observing model behavior.

This task does **not** test that hypothesis. It only tests whether the evidence/seed universe can support a clean experiment.

Read first:

1. `research/iclr_fit_validation/round12_collision_update_and_codex_feasibility_trigger.md`
2. `research/iclr_fit_validation/round11_route_pair_and_equivalence_design.md`
3. `research/iclr_fit_validation/round8_selection_independent_design.md`
4. `experiments/idea_collapse/PRE_RUN_AMENDMENT_E.md`
5. `research/iclr_fit_validation/taxonomy_design_draft.md`

If these files conflict, follow Round 12 and Amendment E as the newest scientific constraints. Do not silently resolve a material scientific conflict; record it.

---

# 1. Hard prohibition

During this task you MUST NOT:

- generate research ideas with any LLM;
- run no-context idea generation;
- estimate a model scientific prior;
- run evidence-conditioned idea generation;
- inspect any treatment outcome;
- optimize route definitions for an effect;
- change the research question;
- write an abstract/paper result;
- invent or tune a metric using model outcomes.

You may use deterministic scripts, metadata APIs, retrieval models, embeddings/rerankers, and source-paper annotation tooling solely to audit corpus feasibility.

If source annotation uses an LLM parser for scale, treat that as provisional. Preserve raw source text and parser output, and produce a human-audit sample. Do not treat parser labels as ground truth.

---

# 2. Source universe

## Evidence corpus

Primary target:

- ICLR 2025 accepted papers;
- prefer papers first public after `2024-08-31` for the temporally clean shared corpus;
- retain all candidates with explicit temporal-cleanliness status rather than silently dropping them.

For each paper record at minimum:

```json
{
  "paper_id": "...",
  "title": "...",
  "abstract": "...",
  "iclr_year": 2025,
  "proceedings_url": "...",
  "openreview_url": "...",
  "first_public_date": "YYYY-MM-DD|null",
  "earlier_public_version_found": true,
  "temporal_status": "CLEAN|POSSIBLE_EARLIER_VERSION|UNKNOWN|FAIL",
  "token_length": 0,
  "route_label_provisional": "...",
  "route_confidence": 0.0
}
```

Do not fabricate dates. `UNKNOWN` is valid.

## Seed universe

Candidate seeds should come from later ICLR work, initially ICLR 2026.

The seed must be a method-masked research question/problem statement, not the focal paper's method.

At feasibility stage, it is acceptable to build candidate seed metadata and a provisional method-masked seed draft, but do not use an LLM generator to solve the seed.

Exclude the focal paper itself from its evidence candidate pool.

---

# 3. Predeclared route contrasts

Audit these global route pairs first:

```text
R1 BUILD_IMPROVE                vs DIAGNOSE_STRESS_TEST
R2 BUILD_IMPROVE                vs MEASURE_EVALUATE
R3 BUILD_IMPROVE                vs EXPLAIN_MECHANISM_THEORY
R4 DIAGNOSE_STRESS_TEST         vs EXPLAIN_MECHANISM_THEORY
```

Do not remove a pair merely because it has poor coverage. Poor coverage is a result of this feasibility audit.

You may report additional route pairs as exploratory only; do not replace R1-R4 without research-lead approval.

The taxonomy draft is not frozen scientific truth. Use it as an auditable source-coding instrument.

---

# 4. Retrieval candidate construction

For each seed:

1. retrieve a generous candidate pool from the frozen evidence corpus;
2. calculate dense relevance;
3. if practical, add one independent reranker score;
4. record all candidate scores;
5. attach provisional route labels;
6. do not use route labels to change the seed query itself.

The retrieval stack/version/config must be frozen and recorded.

---

# 5. Route-pair matchability audit

For every `seed × route pair`:

compute:

```text
n_route_A_above_relevance_floor
n_route_B_above_relevance_floor
candidate relevance distributions
reranker relevance distributions
abstract/token-length distributions
year/date distributions
topic-cluster distributions
```

Then test whether fixed-size evidence packets can be constructed for both routes while preserving acceptable balance.

Audit at least:

```text
k = 6
k = 8
k = 12
```

This is a feasibility audit, not hyperparameter tuning for an outcome. Report how coverage changes with k; do not select k by future model behavior.

---

# 6. Matching diagnostics

For each feasible `seed × route pair × k`, attempt matching/stratification on:

- dense relevance;
- reranker relevance if available;
- token length;
- public date/year;
- coarse topic cluster;
- optional frozen popularity covariate only if consistently available.

Output standardized differences or another transparent balance diagnostic.

Do not label pairs “equivalent.” Use:

```text
scientifically plausible + relevance-matched alternative routes
```

because the paper does not need the routes to be normatively equal, only both valid responses to the same seed and not obviously mismatched in relevance/quality.

---

# 7. Provisional route-label audit

Sample source papers across all provisional route labels.

Produce a blind audit packet for human review containing only the source paper material needed to judge the primary scientific move.

Report:

- route-label frequency;
- ambiguity frequency;
- parser confidence if applicable;
- obvious lexical shortcuts;
- examples where the category boundary is genuinely unclear.

Test a trivial lexical classifier / keyword baseline if easy. If route labels are almost perfectly predictable from a few category words, flag this prominently. Do not hide it.

---

# 8. Required outputs

Create under:

```text
experiments/idea_collapse/feasibility_1/
```

at minimum:

```text
README.md
STATUS.md
corpus_manifest.jsonl
corpus_hash.txt
seed_candidates.jsonl
retrieval_config.json
route_label_summary.json
route_pair_coverage.csv
route_pair_matchability.csv
matching_diagnostics/
temporal_cleanliness_report.md
route_annotation_audit_packet.csv
FEASIBILITY_RESULT.md
```

`FEASIBILITY_RESULT.md` must answer only:

1. How many candidate seeds were audited?
2. How many seed × route pairs are feasible for R1-R4 at k=6/8/12?
3. Are both routes similarly relevant under the frozen retrieval stack?
4. Does temporal-clean filtering leave enough evidence?
5. Are route labels sufficiently auditable to justify a human annotation gate?
6. Which failure mode is dominant: route sparsity, relevance mismatch, temporal uncertainty, or taxonomy ambiguity?
7. Recommendation: `FEASIBLE`, `MARGINAL`, or `NOT_FEASIBLE`.

Do not recommend `CONTINUE` based on scientific effect; no effects are observed in this task.

---

# 9. Reproducibility

Record:

- git commit;
- exact commands;
- dependency versions;
- corpus sources;
- corpus hash;
- retrieval model/version;
- reranker model/version;
- seed-building rules;
- all exclusions and reasons.

No failed seed or route pair may be silently removed.

---

# 10. Stop condition

STOP after `FEASIBILITY_RESULT.md` is complete.

Do not proceed to no-context prior estimation or scientific generation even if the feasibility result is positive.

The research lead will review the source-only artifacts and decide whether to authorize the next phase.
