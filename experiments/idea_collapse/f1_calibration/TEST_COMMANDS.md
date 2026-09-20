# Test Commands and Results

All commands were run from the repository root on branch `codex/f0-semantic-temporal-20260909`.

## Source-only validation

```text
uv run --python 3.12 python experiments/idea_collapse/f1_calibration/scripts/f1_audit.py validate
```

Result: passed. `TEST_REPORT.json` records all required checks as true.

```text
uv run --python 3.12 python experiments/idea_collapse/f1_calibration/scripts/f1_audit.py task5
```

Result: passed. Generated `F1_CALIBRATION_READINESS.md` and `FINAL_CHECKPOINT.md` with `READY_FOR_CALIBRATION_REVIEW`.

## Existing F0 regression suite

```text
uv run --python 3.12 --with 'torch==2.9.1' --with 'transformers==4.57.6' --with 'numpy==2.5.2' --with networkx --with scipy python -m unittest discover -s experiments/idea_collapse/f0_semantic_temporal/tests -v
```

Result: 10 tests passed, including matching cardinality/cost ordering, no source reuse, missing-date handling, anonymity, and F1 partition checks.

## Dependency bootstrap note

An initial unpinned test attempt failed before test collection because `networkx` was not present in the bare environment. No scientific artifact was changed. The pinned dependency command above completed the same suite successfully.
