# F0 Current Snapshot

This is an interrupted source-only F0 snapshot, pushed on user request before the corrected full rerun completed.

## Local Commit Prepared

`e3eb75948dcd6745eb77f1def0ad0898cb1c839b`

Local branch: `codex/f0-source-only-snapshot`

Remote marker branch: `codex/f0-source-only-snapshot-api`

## Completed Before Interruption

- Synced from latest `main` at `a36d1bb82a10b0e935371387b7ab915f65a367de`.
- Read `CODEX_F0_MASTER.md` and required F0 round documents.
- Confirmed hard boundary: no P0, no proposal generation, no no-context generation, no evidence-conditioned generation, no treatment-effect inspection.
- Downloaded official ICLR proceedings indexes:
  - ICLR 2025: 3703 Conference abstract links.
  - ICLR 2026: 5351 Conference abstract links.
- Cached source pages locally at interruption:
  - ICLR 2025: 3703/3703 abstract pages cached.
  - ICLR 2026: approximately 3737/5351 abstract pages cached.
- Implemented deterministic source-only audit script locally:
  - `experiments/idea_collapse/feasibility_1/scripts/f0_source_only_audit.py`
  - Standard-library only.
  - Proceedings ingestion, abstract parsing, provisional route/purity labeling, seed masking/leakage diagnostics, TF-IDF source retrieval, BM25-like reranker relevance, route-clear pairwise matching, packet balance simulation, and human-audit packet generation.

## Important Caveat

The first completed artifact set is not a final F0 result. It short-circuited matching because the initial automatic seed leakage gate marked all seeds as non-pass. The script has been corrected to send extractable but human-review-needed seeds into source-only retrieval/matching while preserving leakage flags. The corrected run was interrupted before it reached matching outputs.

## Local Artifact Files in Prepared Commit

- `README.md`
- `STATUS.md`
- `FEASIBILITY_RESULT.md`
- `corpus_manifest.jsonl`
- `corpus_hash.txt`
- `seed_candidates.jsonl`
- `retrieval_config.json`
- `route_label_summary.json`
- `route_pair_coverage.csv`
- `route_pair_matchability.csv`
- `matched_evidence_slots.csv`
- `packet_balance_simulation.csv`
- `multi_route_coverage.csv`
- `attrition_waterfall.csv`
- `seed_validity_audit_packet.csv`
- `route_equipoise_audit_packet.csv`
- `route_annotation_audit_packet.csv`
- `matching_diagnostics/retrieval_candidates.csv`
- `matching_diagnostics/unmatched_papers.csv`
- `temporal_cleanliness_report.md`
- `.gitignore` excluding `_source_cache/`

## Resume Command

From the local checkout:

```bash
python3 experiments/idea_collapse/feasibility_1/scripts/f0_source_only_audit.py
```

Then commit and push the regenerated completed artifacts.
