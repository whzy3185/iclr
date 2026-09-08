# Recovered F0 Source Snapshot

Start with `F0_RESULT.md`, `research_decision_table.md`, and `FINAL_CHECKPOINT.md`.
Status is **F0_INCOMPLETE**, not scientific feasibility or a paper verdict.
The source-only lexical run and its replay are measured; scientific generation
and the later ARS pilot are NOT_RUN.

## Evidence Layout

- `legacy/`: exact preserved implementation/config, for inspection only.
- `runs/R0_20260908/`: verified cached-source manifest, normalized papers,
  deterministic pre-matching sample, and immutable first failed output archive.
- `runs/F0R-9f61bff4538465a7a96f/`: actual corrected source run, all seeds,
  annotations, retrieval candidates, matchings, missing cells and packet IDs.
- `runs/F0R-9f61bff4538465a7a96f-replay/`: independent deterministic rerun.
- Root CSV/report files: scripted exact copies or documented derivations.

## Reconstruct the Large Candidate Tables

The two `retrieval_candidates.csv.gz` files are byte-sharded for GitHub
transport. No rows were filtered or recomputed. All parts and their SHA256
manifests are committed. Restore them before running hash verification:

```sh
python3 experiments/idea_collapse/feasibility_1/scripts/artifact_parts.py restore experiments/idea_collapse/feasibility_1/runs/F0R-9f61bff4538465a7a96f/retrieval_candidates.csv.gz.parts
python3 experiments/idea_collapse/feasibility_1/scripts/artifact_parts.py restore experiments/idea_collapse/feasibility_1/runs/F0R-9f61bff4538465a7a96f-replay/retrieval_candidates.csv.gz.parts
```

This verifies every part and the assembled file, refusing to replace a
different existing artifact. The unsharded original remains in the local
working tree; `.gitignore` does not delete it or exclude observations.

## Exact Code Version

The source run used local commit
`78dbb1ebf7bb6a4b74fda96f86e951074ef9f857`, transported to GitHub as
`42dce017281a2a2b888405ccb12a87d0acb20b51` with an identical file tree.
R0 local `9a8ddb49b4ce6f3375b3ce2ee04f08dbc32b9513` likewise maps to remote
`748110d50126067091ae08d213d91b447048c292`. Server-side commit metadata changes
SHAs; raw traces were not relabeled. All normalized results carry input/code
hashes. The final reporter and byte-transport helper were added after matching.

For a fresh source-computation reproduction, use an independent worktree at
the published code commit `42dce017...`, install `networkx==3.6.1` with Python
3.12, and run the exact commands in `STATUS.md`. No raw-page redownload is
needed for this snapshot; the normalized R0 inputs are in that commit.
Legacy `main()` must not be executed: it contains historical overwrite and
mislabeling behavior preserved for audit, not current authority.

The original raw HTML cache was preserved without writes; its URLs, keys,
hashes and missingness are published. No unverified earliest-public dates,
purity probabilities, dense scores, human ratings or model ideas were invented.
