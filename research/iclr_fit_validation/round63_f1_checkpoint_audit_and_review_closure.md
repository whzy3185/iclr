# Round 63 — F1 checkpoint audit and review closure

Date: 2026-09-20
Audited implementation: `742c2a84819e122429cfa5b5973c173c734714b3`
Branch: `codex/f0-semantic-temporal-20260909`
Research main observed before this audit: `512386e7672f275fb59fe909636b1c02a2475c8e`
Decision: KEEP the collected data and scores; repair diagnostics and start actual calibration review. Do not start formal certification or scientific generation yet.

## 1. Scope and evidence status

Read the pinned readiness report, checkpoint, test commands, F1 implementation, relevant F0 scoring implementation, all 24 Q0/Q1 diagnostic rows, and the first four seed/variant records. This is a code-and-artifact audit, NOT a rerun of the 4,800 Q1 pairs or the 790,000 F0 pairs. The full large token ledger was not loaded into the local runtime. Reported upstream test passes remain reported test results, not independently rerun passes.

Four small deterministic source-logic checks were run locally: pair truncation despite each component being under the length limit; exact-fit versus truncation; dense versus reranker order; prefixed duplicate text escaping literal duplicate detection. These are synthetic audit checks, not model experiments or human labels.

Published state correctly preserves human_labels_imported=0, Q2=PENDING_REVIEW, no formal 96-block certification, and scientific proposal generations=0. The phrase 'reviewed slot scope=4' denotes displayed coverage ONLY: no human slots have been certified.

## 2. Quantitative result actually supported by the checkpoint

Source: `experiments/idea_collapse/f1_calibration/query_representation_diagnostics.jsonl`, blob `acec5c2ae1e8e81af985dfb28195ffbc65959e81`, first 24 Q0_vs_Q1 rows; exclude the four negative-control markers.

The 24 top-200 intersection sizes in file order are:
`[177,188,177,185,184,181,177,147,165,163,168,157,164,173,181,178,184,177,172,185,160,175,184,178]`.

Derived statistics (arithmetic recomputed, not new inference):
- Mean Q0 query characters: 854.7083; Q1: 567.2083.
- Pooled character reduction: 33.6372%.
- Mean intersection: 174.1667 out of 200; 4,180 seed-document intersections total.
- Mean fraction of candidates replaced: 12.9167% (range 6.0%–26.5%).
- Mean Jaccard: 0.7746561 (range 0.5810277–0.8867925).
- Seed-specific candidate union: 5,420 pairs, NOT 5,420 unique papers.
- Mean of the 24 reported common-document absolute rank shifts: 21.1279 positions. This is dense candidate rank, not reranker rank.

Conclusion: deterministic query cleanup changes the candidate sets and their dense ordering on this fixed calibration panel. No evidence yet establishes better relevance, better route validity, or LLM research-choice effects. Do not extrapolate this selected panel to all ICLR papers. No claim that all change is caused solely by irrelevant words: some queries include duplicate removal and the numerical serving path needs normal reproducibility checks.

## 3. Three repairs before using the diagnostics scientifically

### 3.1 Actual joint-input truncation, not standalone-length flags

`task3` records query_truncated=(standalone query length>512), document_truncated=(standalone document length>512), and pair_truncated=(retained pair length>=512). `validate` checks the same formulas. This is consistency with the recording formula, not proof of actual per-sequence retention.

A 300-token query and 300-token document can require joint truncation while neither standalone length exceeds 512. A pair that exactly fits 512 can have zero removed tokens. Add original and retained token counts by sequence, using the actual tokenizer, exact inference text normalization, padding mask, and special-token treatment. With a fast tokenizer, sequence_ids distinguishes query/document and special tokens; use an explicitly tested alternative if unavailable. Keep max_length, model revisions, scoring inputs and all old score artifacts unchanged. Run CPU tokenizer diagnostics only; no model scoring is needed.

Reference: Hugging Face tokenizer API, https://huggingface.co/docs/transformers/main_classes/tokenizer (sequence_ids and truncation parameters).

### 3.2 Preserve dense and reranker rank as different fields

F0 `rerank_all` preserves the dense candidate array order while attaching reranker scores. F1 `task3` similarly enumerates the dense top-200 list. Its `rank` and rank_change_mean_abs therefore measure dense retrieval order. The scoring work is still useful; the diagnostic names need precision.

Create dense_rank and reranker_rank separately, reranker_rank sorted by descending reranker score with declared deterministic tie-break. Compute both diagnostics from saved scores. When comparing top-10 results, label whether they refer to dense or reranked lists. Do not rerun inference merely to sort scores.

### 3.3 The old matched evidence audit is not the Q0/Q1 quality evaluation pool

`task2` builds the paper relevance forms from the original displayed slots, before Q1 retrieval. Those forms are useful for auditing existing blocks but do not guarantee labels for Q1-only retrieved documents.

Add a bounded, blinded relevance pool for each of the 24 seeds: union of Q0 reranker top-10, Q1 reranker top-10, and the eight existing displayed papers, deduplicated by (seed_id,paper_id). Maximum 672 pairs before deduplication; publish the actual size. Preserve originating systems/ranks/scores only in the private mapping. This pool supports predeclared top-10 precision after judging, not full-corpus recall. Unjudged records remain null. TRANSFER_ONLY is a separate label, not silently merged with DIRECT_RELEVANCE.

The neutral scientific need must be approved before relevance judgments. Do not make Q1 the definition of relevance and then conclude Q1 is better. Do not sample based on favorable scores or repair outcomes. The four current NEGATIVE_CONTROL rows are unlabeled candidates, not verified negatives; retain or relabel their status accordingly.

## 4. Four source-inspection observations — AI provisional, NOT human certification

These are the first four file records, not a representative error-rate estimate. None grants permission to run Q2.

| block_key | Observation | Required decision |
|---|---|---|
| 03d24e1f3f0d2e26d3310901 | Q1 removes repetition but still contains a prescribed teacher/student unsupervised environment-design setting. | Decide whether UED is essential task scope or a solution prescription; do not automatically delete the setting and broaden the scientific question. |
| 0b45eca86417b0828be5ee61 | Q1 retains a description of the focal benchmark and its measured results after masking the benchmark name. | Decide whether the task is a pre-contribution research question or a post-publication follow-up. Split background from focal solution/results explicitly. |
| 0c6669318c4b2016c0db9d95 | Dynamic Time Warping and DTW are masked although the source spans identify them as established background; a generic unresolved-limitation sentence is not anchored to the displayed source spans. | Restore background terminology only after source checking; recover the actual limitation from the source or mark INSUFFICIENT_SOURCE. Do not invent a new gap. |
| 14fd07d3eba29a1569a38a44 | Q1 retains the focal experimental plan and three results while masking broad terms including LLM/TTS/Verification. | Preserve necessary background terms and explicitly decide whether focal results are allowed for the task. |

Also, the first seed's literal duplicate_diagnostic reports zero because one repeated paragraph has an extra heading. Q1 correctly strips that heading and removes the duplicate; normalize headings consistently in the duplicate diagnostic too. This is a diagnostic issue, not evidence that Q1 failed its assigned cleanup.

## 5. Validation and provenance caveats

- The F1 matching regression enumerates a toy graph without calling the production solver. It is a useful oracle, but add a test comparing the actual production matcher to that oracle; do not infer production correctness solely from the toy enumeration. The separate F0 suite is reported as passing and should be retained.
- Hidden-field booleans and filename prefixes do not by themselves establish blind delivery. Reviewer-facing HTML/JSON must not contain private maps, original scores, source identifiers, or embedded side-channel metadata. Preserve private mappings elsewhere; do not include them in the reviewer export.
- human_labels_imported=0 and proposal_generations=0 are currently literals in the validator. Audit the actual label import and run ledgers when those stages become active; do not treat constants as general future execution guards.
- Task 4 mainly organizes existing fallback metadata. It does not establish new historical first-public dates. Its queue hardcodes evidence_minus_seed_days=-354 for 2025, although a separate gap audit computes differences. Derive date gaps from records in both places; unresolved fallback is not a failure of the research hypothesis.

## 6. Operational decision: close engineering gaps, then obtain decisions

No more corpus expansion, full reranking, threshold grids, or venue re-positioning in this checkpoint.

Allow only: cache-only diagnostic corrections; a source-grounded Q2 repair proposal table with explicit provenance and null approvals; export/import tooling for the existing calibration panel. Use an offline review page or self-contained sheets that display the text and collect answers. Existing CSV files primarily contain answer fields and identifiers, so a usable display layer is needed.

Model-assisted source review is allowed as a clearly marked suggestion layer if separately authorized; it is neither a human label nor ground truth. This chat's four observations are not blind judgments and must not count toward human agreement. For independent evaluation, reviewers must not see suggestion labels or system identity before recording their own decisions.

Historical completeness remains necessary only for historical/novel-knowledge claims. Contemporary retrieval evaluation and current-context behavior can proceed with transparent limitations; do not block all construct review waiting for every historical date.

Actual progress milestone after this audit: approved problem text and completed relevance/route decisions, not another report saying READY. Then freeze the rubric and move to certification. Keep 96 certification seeds untouched by calibration tuning. P0/ARS/proposal generation remains unapproved.

## 7. Evidence ledger

All repository paths below refer to the audited commit, under `experiments/idea_collapse/`:
- `f1_calibration/F1_CALIBRATION_READINESS.md`
- `f1_calibration/FINAL_CHECKPOINT.md`
- `f1_calibration/TEST_COMMANDS.md`
- `f1_calibration/scripts/f1_audit.py` (blob `1171022b8c0ee363e55d044668a2cd743e96c309`)
- `f1_calibration/query_representation_diagnostics.jsonl`
- `f1_calibration/query_variants.jsonl`
- `f1_calibration/seed_audit.jsonl`
- `f0_semantic_temporal/scripts/semantic_compute.py` (blob `291cd64e1ca387271356d22d12cbef08af0b7dcc`)

No new scientific model outputs, human labels, paid API calls, or certification decisions were produced by this audit.
