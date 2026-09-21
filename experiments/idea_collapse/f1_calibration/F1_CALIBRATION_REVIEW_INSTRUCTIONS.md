# F1 Calibration Review Instructions

## Scope and gate

This package covers 24 calibration blocks only. It is for rubric calibration and source/construct review, not formal certification. The 96 certification blocks must remain unopened for rule adjustment until the calibration labels are imported and `F1_RUBRIC_FREEZE.md` is committed.

Reviewers must work independently from the visible files in `reviewer_package/`. Do not open `_PRIVATE_block_ab_mapping.jsonl`, retrieval/reranker files, provisional route annotations, or source provenance while assigning blind labels. Make one copy of each CSV per reviewer and edit only reviewer fields. Do not alter IDs or displayed source text.

All deterministic diagnostics are advisory review targets, not prefilled human decisions. Every reviewer field is intentionally blank.

## A. Seed review

For each row in `seed_review.csv`, judge:

- `comprehensible`: YES / NO / UNCLEAR.
- `method_neutral`: YES only if the seed does not privilege a particular solution or route.
- `solution_leakage`: NONE / POSSIBLE / PRESENT.
- `duplicated_or_malformed`: NO / YES / UNCLEAR.
- `multi_route_open`: YES only if at least two scientifically defensible, nontrivial routes remain open.
- `source_faithful`: YES only if the masked seed preserves the source problem without adding a new claim.
- `seed_decision`: PASS / FAIL / ADJUDICATION.
- `failure_types`: semicolon-separated values from SEED_LEAKAGE, SEED_NOT_OPEN, DUPLICATED_OR_MALFORMED, SOURCE_UNFAITHFUL, INCOMPREHENSIBLE, or OTHER.

Use `approved_repair_text` only when a source-faithful repair is necessary. A proposed repair is not approved until reviewers explicitly supply or accept it.

## B. Paper review

Each row in `paper_review.csv` contains one seed and one anonymous abstract. Existing route labels, source IDs, retrieval scores, ranks, and matching outcomes are hidden.

Here, anonymous means outer source metadata is suppressed. The scientific abstract is preserved verbatim, so intrinsic URLs, method names, project names, or other identity cues may remain. Reviewers should record relevance from the provided content and must not use those cues to recover hidden provenance.

Set `relevance_label` to exactly one of:

- `DIRECT_RELEVANCE`: directly addresses the seed's scientific problem or a necessary component of it.
- `TRANSFER_ONLY`: scientifically meaningful transfer or analogy, but not direct evidence for the seed problem.
- `OFF_TOPIC`: no defensible scientific relevance to the seed problem.
- `UNCLEAR`: insufficient information or genuine ambiguity.

Set `primary_scientific_contribution` and optional `secondary_scientific_contribution` to BUILD, DIAGNOSE, MEASURE, EXPLAIN, MIXED, OTHER, or UNCLEAR. Quote an exact abstract sentence in `evidence_sentence`. Paper contribution classification may be reused when the identical abstract recurs, but relevance must be judged separately for every seed-paper pair.

## C. Block review

The displayed Route 1/Route 2 order is deterministically randomized and must not be decoded during review. Judge:

- whether each route is scientifically plausible;
- whether routes are distinguishable and non-subsumed;
- whether genuine equipoise exists;
- `route_relationship`: COMPLEMENTARY / COMPETING / HIERARCHICAL / SUBSUMED / UNCLEAR;
- whether the block is usable for an evidence-composition intervention.

Only four slots are displayed. Set `usable_slot_count` from 0 through 4. This package cannot certify k=6, k=8, or k=12. Additional slots require separate blind review.

## Missingness and disagreement

Never convert blank, unclear, or failed review into a negative zero. Preserve each reviewer's row independently. Disagreement is analyzed only after real reviewer files are returned. No model-generated label may be entered as a human label.

## Stop condition

After reviewers complete the three CSVs, return the labelled copies for Task 3 import. Do not access the 96 certification cases or begin P0 before calibration analysis and rubric freeze.
