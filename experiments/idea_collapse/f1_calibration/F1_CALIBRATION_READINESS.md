# F1 Calibration Readiness

STATUS=READY_FOR_CALIBRATION_REVIEW

This is a source-only calibration package. No human labels were imported and no scientific proposal generation was run. The 96 certification records remain untouched.

- Calibration blocks: 24 unique seeds.
- Visible block review scope: exactly 4 displayed slots per block; no k=8/k=12 certification.
- Q0: exact F0 query and cached scores reused for 24 seeds.
- Q1: deterministic query variant scored on 24 x 200 candidates with new cache keys.
- Q2: PENDING_REVIEW.
- Temporal history: fallback-only discovered dates; historical cleanliness remains UNKNOWN/UNVERIFIED.

## Tests
```json
{
  "ab_mapping_private": true,
  "all_required": true,
  "calibration_certification_disjoint": true,
  "corpus_hash_ok": true,
  "denominators_ok": true,
  "fallback_not_historical_pass": true,
  "human_labels_imported": 0,
  "matching_objective_regression": true,
  "no_silent_zero": true,
  "proposal_generations": 0,
  "query_cache_invalidated": true,
  "query_q2_pending": true,
  "review_files_no_hidden_scores": true,
  "reviewed_slot_scope_4": true,
  "token_accounting_correct": true
}
```
