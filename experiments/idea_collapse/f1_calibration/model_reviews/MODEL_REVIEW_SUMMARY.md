# F1 Calibration Model Pre-Review Summary

Status: **MODEL PRE-REVIEW / DIAGNOSTIC — VALIDATION PASS**

## Frozen input

- Repository/branch: `whzy3185/iclr` / `codex/f0-semantic-temporal-20260909`
- Reviewed package commit: `37f52f080aebd4fb806b1a8757eccb8b39c9e283`
- Task 1/package-generation commit: `cbf502ec173a69d11784a3df5e95dc1be1552263`
- F1 data-freeze commit recorded by `F1_INPUT_FREEZE.json`: `742c2a84819e122429cfa5b5973c173c734714b3`
- Reviewed rows: Seed 24, Paper 192, Block 24

## Label distributions

- Seed decisions: 5 PASS, 15 FAIL, 4 ADJUDICATION. All 24 were comprehensible and source-faithful; 15 had possible/present solution leakage, 11 were duplicated or malformed, and 11 were not multi-route open.
- Paper relevance: 30 DIRECT_RELEVANCE, 87 TRANSFER_ONLY, 75 OFF_TOPIC, 0 UNCLEAR. Confidence: 105 HIGH and 87 MEDIUM.
- Block usability: 17 YES, 3 UNCLEAR, 4 NO. Usable slot counts: 1×3, 2×4, 3×10, 4×7. Route relationship: 23 COMPLEMENTARY and 1 SUBSUMED.
- Seed ADJUDICATION count: 4. No Paper relevance UNCLEAR labels. Block equipoise: 17 YES, 6 UNCLEAR, 1 NO.

## Validation and blindness

- Validation: PASS with zero machine-detected errors.
- Original row IDs, row order, displayed text, A/B display order, source spans, reviewed slot scope, and all other frozen fields are unchanged field-for-field.
- All original reviewer-package files still match their manifest SHA-256 values.
- Every paper evidence sentence is a verbatim substring of its corresponding anonymous abstract.
- The 22 repeated-abstract groups have consistent scientific-contribution classifications; relevance was still judged per seed-paper pair.
- All `usable_slot_count` values are integers from 0 through 4; no k=6/8/12 claim was made.
- The three roles ran in isolated contexts and did not share verdicts. No private A/B mapping, hidden provenance, certification case, or external provenance lookup was accessed.

## Important ambiguities and human-review priorities

1. Review the four Seed ADJUDICATION rows first: blocks `0b45eca86417b0828be5ee61`, `14fd07d3eba29a1569a38a44`, `55b7ed5ebdb443a7ab940634`, and `aa4cc4ce24ed05e3d8ccff94`. Each remains route-open but may be anchored by source findings or a favored method family.
2. Review the seven blocks with non-YES intervention usability: `03d24e1f3f0d2e26d3310901`, `254f17109e7eaeb5bb6043da`, `3028da58e4e7fb9b0bf4d280`, `462fb658f17ec65a917d8229`, `4a6abaeabde5087f27e323b6`, `84a8473c90b77af4eb64cc4d`, and `f362ba379cce557f3755d6e8`.
3. Block `f362ba379cce557f3755d6e8` is the sole SUBSUMED/NO-equipoise case and deserves explicit human adjudication.
4. The 87 TRANSFER_ONLY paper pairs are all MEDIUM-confidence and are the highest-volume boundary class for targeted human sampling.
5. Rubric ambiguity: `reviewer_confidence` has no explicit enum in the instructions; this pre-review used HIGH/MEDIUM. The optional secondary contribution was left blank rather than inventing a label.

## Allowed next action and hard stop

Allowed next diagnostic action: run a non-importing Task 3 parser dry-run against copies of these model-review files, then produce a prioritized human-review queue emphasizing the items above.

These outputs do **not** change the original protocol state: `CALIBRATION_HUMAN_LABELS_IMPORTED=0`, `CERTIFICATION_BLOCKS_OPENED_FOR_RULE_ADJUSTMENT=0`, `SCIENTIFIC_PROPOSAL_GENERATIONS=0`, and `HARD_STOP=ACTIVE`.
