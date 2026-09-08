# F0 Recovery Status

F0_DATA_STATUS: F0_INCOMPLETE
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
SCIENTIFIC_PROPOSAL_GENERATIONS: 0

R0 published: `748110d50126067091ae08d213d91b447048c292`.
Actual source run: `F0R-9f61bff4538465a7a96f`.
Code commit: `78dbb1ebf7bb6a4b74fda96f86e951074ef9f857`.
Baseline main: `b9cbbfdf0bafcf30adc7b8e261fdad6f08eb0ff8`.
Implementation parent: `049a313ed2900f1acd9c2d6673abd2124280b85f`.

Completed: cached corpus inventory, seed-gate repair, provisional route annotations,
lexical retrieval candidates, exact matching, typed grid, source reuse, packet
assignment diagnostics, human-audit materials, F0 result and decision table.
Not complete: semantic matching, date resolution, missing focal abstracts and human audit.
Task 3/4: NOT_RUN; no model output or research effect was measured.

Run commands from integration worktree (no source acquisition):

```sh
experiments/idea_collapse/feasibility_1/.venv/bin/python -m unittest discover -s experiments/idea_collapse/feasibility_1/tests -v
experiments/idea_collapse/feasibility_1/.venv/bin/python experiments/idea_collapse/feasibility_1/scripts/run_recovery.py --config experiments/idea_collapse/feasibility_1/recovery_config.json
experiments/idea_collapse/feasibility_1/.venv/bin/python experiments/idea_collapse/feasibility_1/scripts/run_recovery.py --config experiments/idea_collapse/feasibility_1/recovery_config.json --replay
experiments/idea_collapse/feasibility_1/.venv/bin/python research/iclr_fit_validation/design_checks/round52/design_counterexamples.py --test
experiments/idea_collapse/feasibility_1/scripts/report_recovery.py --run experiments/idea_collapse/feasibility_1/runs/F0R-9f61bff4538465a7a96f --replay experiments/idea_collapse/feasibility_1/runs/F0R-9f61bff4538465a7a96f-replay
```

Tests: recovery suite PASS; independent Round 52 six design tests PASS; normalized
artifact replay PASS. See `matching_test_report.json` and `REPLAY_VERIFICATION.json`.
Artifacts/provenance: `SOURCE_ONLY_RUN_MANIFEST.json`; human audit CSVs at this root.
Every alteration from the legacy run is disclosed in `RECOVERY_INVENTORY.md`
and `recovery_config.json`. No outcome-dependent source/route/matching changes occurred.

Next: STOP for research-lead review of `FINAL_CHECKPOINT.md`, not a publication decision.
