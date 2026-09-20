# Codex — F1 calibration and source-validity audit

Status: SOURCE-ONLY TASK AUTHORIZED. No ARS, research-proposal generation, baseline, P0/P1, paid API calls, or invented human judgments.

Continue existing work on `codex/f0-semantic-temporal-20260909`, whose reviewed snapshot is `e0fbbf27bae69030e9487fdf1958a27e84a18335`. Preserve uncommitted work and caches before synchronization; no reset, force push, whole-branch replacement or corpus reacquisition. If newer local/remote work exists, record its SHA and continue without overwriting it.

Fetch current main and read this task via `git show origin/main:CODEX_F1_CALIBRATION_SOURCE_AUDIT_TASK.md`. Also read Round 62 and the current experiment's `F0_SEMANTIC_TEMPORAL_RESULT.md`. Do not re-read sixty historical rounds. This task governs only the bounded next source audit; earlier generation gates stay closed.

Output root: `experiments/idea_collapse/f1_calibration/`. Existing F0 artifacts remain immutable.

## 1. Reconcile and preserve

Record input/code/config/model/corpus hashes and actual branch. Recompute counts from source rows: 5351 seed records = 3950 scored + 1401 blocked; 790000 scored pairs; 15800 measured route blocks and 5604 blocked blocks. Verify the published coverage, not only report text. Null/blocked/not-run must not become zero.

Export a paper-ID-level comparison to the lexical run: shared eligible seeds, newly available seeds, gained/lost/retained matches and reasons. Do not call 1018/1119 a retention rate. Do not require old/new counts to agree.

## 2. Prepare the existing 24 calibration blocks; keep the 96 queue unlabelled

Resolve the actual source IDs through hidden provenance. The current package displays four slots per block (eight seed-paper exposures): record reviewed slot scope explicitly and do not certify unshown k=8/12 slots.

Create separate review files:
- `seed_audit.jsonl`: original problem/source spans, current masked text, duplicated spans, generic terms masked, solution-prescribing spans, proposed source-faithful repairs; human decision null.
- `paper_relevance_route_audit.jsonl`: seed + one abstract, randomized neutral record ID; hide provisional route label, retrieval score, matching outcome and ranking. Human fields: DIRECT_RELEVANCE / TRANSFER_ONLY / OFF_TOPIC / UNCLEAR; primary/secondary contribution routes; supporting source span; confidence/notes.
- `block_admissibility_audit.jsonl`: neutral A/B descriptions and reviewed-source slots; randomize displayed A/B order with private mapping. Assess relevance, distinguishability, alternative/complementary/hierarchical relation, and usable slots. Human fields null.

Deduplicate identical paper annotations where legitimate, but retain seed-specific relevance judgments. Prepare a small, separately tagged shadow audit with up to six measured-zero and six source-gate-blocked seeds chosen by a frozen hash rule; this is a developmental exclusion audit, not a pass threshold. Do not draw the shadow sample from the 96 certification queue.

Anchor diagnostics must include calibration keys `345b55b6ef513c049c91d1e1` and `03d24e1f3f0d2e26d3310901`. Their flagged concerns are provisional, not prefilled human verdicts. Record all original calibration cases, not only easy ones.

## 3. Diagnose query construction and token truncation on the 24 only

Keep the BGE model revisions unchanged and reuse document embeddings/caches.

Q0 = exact current query, cached scores.
Q1 = deterministically deduplicate repeated problem text and remove generic proposal-generation TASK instructions; preserve substantive problem content and current masking.
Q2 = source-faithful masking repair only when a reviewed repair is supplied; otherwise PENDING_REVIEW, not an invented query or score.

Freeze query variants and an input manifest before new scoring. Up to 24 seeds x 200 candidates x two new variants are allowed with the existing local non-generative models; do not rerun all 790000 pairs. Changed queries require new query embeddings/retrieval and new cache keys; unchanged inputs reuse the old keys.

For every compared pair record full and retained query/document token counts, truncation flags, token limits, candidate IDs, scores and configuration. Use the same frozen evidence corpus and candidate budget; retain the union of candidates for later blinded review. Add a few clearly labelled negative-control pairs without mixing them into coverage statistics.

Output `query_representation_diagnostics.jsonl` and `token_budget_audit.json`. Ranking differences are not accuracy gains. Compute judged precision/ranking metrics only after real relevance labels are imported; before then return PENDING_LABELS. Do not select thresholds to maximize surviving block counts.

## 4. Date and metadata semantics, in parallel

Existing fallback dates stay preserved. Add fields distinguishing `publication_date`, `earliest_discovered_date`, `earliest_history_status` and `historical_order_status`; fallback-only must never become historical PASS. Confirm the published all-pair -354-day distribution and report per-year distinct dates and within-bank date variation.

Prioritize source-history lookup for calibration documents using accessible first-party pages/APIs and identity-checked title/author matches. Retain published and updated timestamps separately. Do not bypass OpenReview challenges or infer arXiv identity from topic similarity. Log unresolved cases; global earliest-history completeness is not a prerequisite for preparing F1.

Report intrinsic URLs/method names separately from outer metadata suppression. Preserve raw abstracts. Any future identity-suppressed representation needs its own version/change map, not silent rewriting.

## 5. Tests, reports and STOP

Add/run tests for: denominator reconciliation; no silent zero; calibration/certification disjointness; hidden label/score isolation in review exports; displayed A/B remapping; four-reviewed-slots cannot certify eight; query changes invalidate caches; pair token accounting; fallback dates cannot pass historical-clean tests; maximum-cardinality matching regressions. Report what actually ran.

Deliver:
`STATUS.md`, `INPUT_MANIFEST.json`, the review files above, `paired_lexical_semantic_comparison.csv`, `temporal_review_queue.jsonl`, `source_identity_audit.json`, `F1_CALIBRATION_READINESS.md` and `FINAL_CHECKPOINT.md`.

Return branch/commit, exact scored versus pending counts, new model-inference calls, actual human-label count, tests, unresolved validity issues, and `SCIENTIFIC_PROPOSAL_GENERATIONS=0`.

If humans have not supplied labels, final state is `READY_FOR_CALIBRATION_REVIEW`, not F1_COMPLETE or SCIENTIFICALLY_CERTIFIED. Commit and push each completed engineering checkpoint. STOP before the 96-case certification run or any scientific generation.
