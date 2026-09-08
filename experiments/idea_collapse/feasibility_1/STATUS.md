# F0 Recovery Status

F0_DATA_STATUS: F0_INCOMPLETE
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
SCIENTIFIC_PROPOSAL_GENERATIONS: 0

## R0 - Actual Snapshot Preserved

- Recovered the actual source checkout, script, original config, cached HTML and
  first-run outputs. No reset/clean/cache deletion or obsolete-P0 branch import.
- Verified 3703/3703 evidence abstracts and 3737/5351 focal abstracts locally.
- Preserved first failure as INCOMPLETE_GATE_SHORT_CIRCUIT; matching is NOT_RUN.
- Source inventory and raw/normalized hashes: `runs/R0_20260908/R0_MANIFEST.json`.
- Legacy tests: not found; recovery test results pending.
- Source commit: `049a313ed2900f1acd9c2d6673abd2124280b85f`.
- Baseline main: `b9cbbfdf0bafcf30adc7b8e261fdad6f08eb0ff8`.
- Next: publish this actual R0 code/data checkpoint, then correct/test seed gates,
  backend/date uncertainty, matching objectives and typed missingness.

## Exact Commands

From the preserved source checkout:

```sh
git status --short --branch
git log -5 --oneline
git worktree list --porcelain
git fetch /Users/muelsyse/Documents/Codex/2026-09-06/whzy3185-iclr-ars-skill-iclr/work/iclr-p0 refs/remotes/origin/main:refs/remotes/recovery/main
git worktree add -b codex/f0-recovery-20260908 /Users/muelsyse/Documents/Codex/2026-09-06/whzy3185-iclr-ars-skill-iclr/work/iclr-f0-recovery recovery/main
```

From the integration worktree:

```sh
/Users/muelsyse/.local/bin/python3.12 experiments/idea_collapse/feasibility_1/scripts/preserve_snapshot.py --source-root /Users/muelsyse/Documents/Codex/2026-09-07/whzy3185-iclr-f0-source-only-feasibility/work/iclr-f0/experiments/idea_collapse/feasibility_1 --output experiments/idea_collapse/feasibility_1/runs/R0_20260908
uv venv --python 3.12 experiments/idea_collapse/feasibility_1/.venv
uv pip install --offline --python experiments/idea_collapse/feasibility_1/.venv/bin/python -r experiments/idea_collapse/feasibility_1/requirements.txt
```

NetworkX 3.6.1 was installed from the existing package cache. No model weights,
corpus pages, or new dependency packages were downloaded during R0.
