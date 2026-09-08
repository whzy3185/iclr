"""Verify immutable F0 outputs and render bounded recovery/decision reports."""

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys

from recovery_common import BASE, ROOT, digest, encoded, git, identity, read_jsonl, write_csv, write_json


def retain_json(path, value):
    if path.exists():
        if path.read_bytes() != encoded(value):
            raise ValueError("existing derived JSON differs: " + str(path))
    else:
        write_json(path, value)


def retain_csv(path, rows, fields):
    expected = io.StringIO(newline="")
    writer = csv.DictWriter(expected, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    if path.exists():
        if path.read_bytes() != expected.getvalue().encode("utf-8"):
            raise ValueError("existing derived CSV differs: " + str(path))
    else:
        write_csv(path, rows, fields)


def verify(run, replay):
    manifest = json.loads((run / "SOURCE_ONLY_RUN_MANIFEST.json").read_text())
    checked = {}
    for name, entry in manifest["artifacts"].items():
        if digest(run / name) != entry["sha256"]:
            raise ValueError("artifact drift: " + name)
        if name != "START_MANIFEST.json":
            if digest(run / name) != digest(replay / name):
                raise ValueError("replay differs: " + name)
            checked[name] = entry["sha256"]
    summary = json.loads((run / "SUMMARY.json").read_text())
    with (run / "lexical_matching_diagnostics.csv").open() as handle:
        blocks = list(csv.DictReader(handle))
    if len(blocks) != summary["matching_blocks_measured"]:
        raise ValueError("block denominator mismatch")
    by_bank = {row["bank_id"]: row for row in blocks}
    seen = defaultdict(set)
    slots = Counter()
    with (run / "matched_evidence_slots.csv").open() as handle:
        for row in csv.DictReader(handle):
            bank = row["bank_id"]
            for key in ("A_paper_id", "B_paper_id"):
                if row[key] in seen[bank]:
                    raise ValueError("source reused within bank")
                seen[bank].add(row[key])
            if row["dense_gap"] or row["embedding_distance"] or row["date_gap_days"]:
                raise ValueError("lexical-only run populated unavailable semantic/date columns")
            slots[bank] += 1
    if sum(slots.values()) != summary["matched_slots"] or any(slots[bank] != int(row["max_matched_slots"]) for bank, row in by_bank.items()):
        raise ValueError("slot cardinalities do not reconcile")
    cells = Counter()
    for cell in read_jsonl(run / "coverage_cells.jsonl.gz"):
        cells[cell["cell_status"]] += 1
        if cell["max_matched_slots"] is not None or cell["n_A"] is not None or cell["n_B"] is not None:
            raise ValueError("unexecuted canonical cell contains a measured count")
    if sum(cells.values()) != summary["canonical_grid_cells"]:
        raise ValueError("coverage-grid denominator mismatch")
    return {"status": "PASS", "normalized_artifacts_replayed_identically": checked,
            "volatile_files_excluded": ["START_MANIFEST.json", "SOURCE_ONLY_RUN_MANIFEST.json"],
            "measured_blocks": len(blocks), "matched_slots": sum(slots.values()), "canonical_cell_statuses": dict(cells)}, blocks


def report(run, replay):
    run, replay = Path(run).resolve(), Path(replay).resolve()
    verification, blocks = verify(run, replay)
    summary = json.loads((run / "SUMMARY.json").read_text())
    manifest = json.loads((run / "SOURCE_ONLY_RUN_MANIFEST.json").read_text())
    seeds = list(read_jsonl(run / "seed_candidates.jsonl.gz"))
    seed_by_id = {s["seed_id"]: s for s in seeds}
    annotations = list(read_jsonl(run / "source_route_annotations.jsonl.gz"))
    retain_json(BASE / "REPLAY_VERIFICATION.json", verification)
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(BASE / "tests"), "-v"]
    if (BASE / "matching_test_report.json").exists():
        retained = json.loads((BASE / "matching_test_report.json").read_text())
        if retained["returncode"] != 0 or retained["exact_command"] != command:
            raise ValueError("retained test log is not a successful matching invocation")
    else:
        tested = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
        if tested.returncode:
            raise RuntimeError(tested.stdout + tested.stderr)
        write_json(BASE / "matching_test_report.json", {"status": "PASS", "exact_command": command,
            "returncode": tested.returncode, "stdout": tested.stdout, "stderr": tested.stderr,
            "suite_scope": "F0 recovery tests; not model science", "fixture_cardinality": 2, "fixture_cost": 4})
    for name in ("attrition_waterfall.csv", "matched_evidence_slots.csv", "coverage_balance_frontier.csv", "seed_gate_audit.jsonl",
                 "seed_gate_audit_sample.csv", "retrieval_backend_manifest.json", "source_reuse_summary.json"):
        if (BASE / name).exists():
            if digest(BASE / name) != digest(run / name):
                raise ValueError("existing copied artifact differs: " + name)
        else:
            shutil.copyfile(run / name, BASE / name)
    paired = {}
    for pair in ("R1", "R2", "R3", "R4"):
        subset = [b for b in blocks if b["route_pair_id"] == pair]
        paired[pair] = {str(k): len({b["seed_id"] for b in subset if int(b["max_matched_slots"]) >= k}) for k in (4, 6, 8, 12)}
    unmatched_counts = Counter()
    with gzip.open(run / "unmatched_papers.csv.gz", "rt") as handle:
        for row in csv.DictReader(handle):
            unmatched_counts[row["reason"]] += 1
    source_sample = []
    for route in ("BUILD_IMPROVE", "DIAGNOSE_STRESS_TEST", "MEASURE_EVALUATE", "EXPLAIN_MECHANISM_THEORY"):
        for boundary in (False, True):
            pool = [a for a in annotations if a["primary_route"] == route and (a["primary_route_strength_heuristic"] in (3, 4)) == boundary]
            for a in sorted(pool, key=lambda row: identity(row["paper_id"]))[:3]:
                source_sample.append({"paper_id": a["paper_id"], "boundary_sample": boundary, "source_text": a["input_text"],
                    "provisional_route": route, "source_spans": json.dumps(a["source_spans"]),
                    "numeric_purity": None, "human_route": "", "human_purity_descriptor": "", "human_notes": ""})
    retain_csv(BASE / "route_annotation_audit_packet.csv", source_sample, list(source_sample[0]))
    audit_blocks = []
    for pair in paired:
        # Source-support selection only; never use proposal outcomes or imagined effects.
        pool = [b for b in blocks if b["route_pair_id"] == pair and int(b["max_matched_slots"]) >= 4]
        for b in sorted(pool, key=lambda row: identity(row["seed_id"] + pair))[:5]:
            s = seed_by_id[b["seed_id"]]
            audit_blocks.append({"seed_id": s["seed_id"], "route_pair_id": pair, "bank_id": b["bank_id"],
                "matched_slots": b["max_matched_slots"], "masked_question": s["method_masked_question"],
                "risk_flags": json.dumps(s["risk_flags"]), "allowed_scope": "F1_SOURCE_REVIEW_CANDIDATE_ONLY",
                "ARS_eligible": False, "human_relevance": "", "human_equipoise": "", "human_non_subsumption": "", "human_notes": ""})
    retain_csv(BASE / "route_equipoise_audit_packet.csv", audit_blocks, list(audit_blocks[0]))
    table = "\n".join(f"| {pair} | {counts['4']} | {counts['6']} | {counts['8']} | {counts['12']} |" for pair, counts in paired.items())
    decision = f"""# F0 Research Decision Table

SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
Source run: `{summary['run_id']}`. No publication-readiness decision is made.

| Seed population | Count | State / interpretation |
| --- | ---: | --- |
| Official focal IDs | 5351 | measured denominator |
| Cached, parsed focal abstracts | 3737 | measured; not all 5351 |
| Source matching allowed | {summary['source_matching_seeds']} | provisional only |
| Flagged but matching allowed | {summary['flagged_but_matching_seeds']} | warnings preserved |
| Explicit solution repair queue | {summary['repair_seeds']} | blocked from primary candidate matching |
| Structural/cache-missing failures | {summary['structural_failure_seeds']} | retained, not negative model outcomes |
| Human-confirmed experimental blocks | unknown | pending review, not measured zero |

## Lexical Source Coverage - Unique Seeds Within Each Route Pair

| Pair | k=4 | k=6 | k=8 | k=12 |
| --- | ---: | ---: | ---: | ---: |
{table}

Across pairs, deduplicated unique-seed coverage is {summary['lexical_unique_seed_coverage']}.
Do not sum the route rows as independent seed counts.

## STRICT / BASE / RELAXED Frontier

All three canonical matching regimes, all T0/T1/T2 tiers, purity .60/.70/.80 and
k=4/6/8/12 are retained in `coverage_balance_frontier.csv` and the expanded typed
grid. Canonical semantic matching is **MISSING_COVARIATES**, not zero coverage.
Numeric purity is NOT_ASSESSED. T0/T1 date membership is UNKNOWN, not clean.
The additional `LEXICAL_LEGACY_NO_DATE_PROVISIONAL` regime is a separate
measured diagnostic; it is not a replacement for the canonical frontier.

## Largest Bottlenecks and Recommended Blocks

1. Semantic task compatibility, first-public dates and model-token length are
   not established; keyword purity is not a calibrated numeric probability.
2. 1614 focal abstracts were absent from the recovered cache. No missing title
   was turned into an invented abstract or a confirmed negative seed.
3. 965 focal-solution cases need repair/review; flagged cases remain provisional.
4. All four route contrasts have lexical audit candidates. The deterministic
   examples in `route_equipoise_audit_packet.csv` are recommended for **source
   review only**, not for ARS generation. No block is certified ARS eligible.
5. R4 remains a complementary/high-composability contrast requiring particular
   non-subsumption/equipoise review; it has not been dropped for poorer coverage.

No seed, route or matching parameter was selected using proposal effects.
"""
    (BASE / "research_decision_table.md").write_text(decision)
    result = f"""# F0 Recovery Result

F0_DATA_STATUS: F0_INCOMPLETE
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
SCIENTIFIC_PROPOSAL_GENERATIONS: 0

## Published Inputs and Execution

The actual R0 snapshot was published at `748110d50126067091ae08d213d91b447048c292`
before corrected matching. Original source commit `049a313ed2900f1acd9c2d6673abd2124280b85f`
and its caches were retained unchanged. Baseline main is
`b9cbbfdf0bafcf30adc7b8e261fdad6f08eb0ff8`. Source run `{summary['run_id']}` executed
code commit `{manifest['git_commit']}` with per-file code/config/spec hashes.
See the final run manifest for exact commands and source/transport provenance.

ICLR 2025: 3703/3703 cached title/abstract pairs verified. ICLR 2026: 3737/5351
verified. All 9054 official IDs remain in the acquisition manifest. No source
page was downloaded again; the missing 1614 remain an explicit incompleteness.

## Gate Recovery

First-run outputs are retained as INCOMPLETE_GATE_SHORT_CIRCUIT. Their empty
matching tables mean NOT_RUN. The legacy script had subsequently been edited,
so exact first-run code/output alignment is unknown rather than fabricated.

Corrected gate: {summary['source_matching_seeds']} source-matching candidates,
including {summary['flagged_but_matching_seeds']} flagged candidates; {summary['repair_seeds']}
explicit solution cases stay in repair; {summary['structural_failure_seeds']} structural
failures remain retained. Confirmatory eligibility is false pending human review.

## Matching Actually Performed

- Backend: LEXICAL_PROVISIONAL. TF-IDF and BM25-like scores are not dense scores.
- Candidate rows: {summary['lexical_candidate_rows']}.
- Exact source matchings solved: {summary['matching_blocks_measured']} seed-route blocks.
- Maximum-cardinality-then-minimum-declared-integer-cost slots: {summary['matched_slots']}.
- Measured zero blocks: {summary['measured_zero_blocks']}.
- Unmatched source rows by reason: {dict(unmatched_counts)}.
- Canonical typed cells: {summary['canonical_grid_cells']}; statuses: {verification['canonical_cell_statuses']}.

The declared lexical diagnostic inherits original lexical floors/gaps, uses
NetworkX 3.6.1 maximum-flow minimum-cost matching with deterministic tie rules,
and omits unavailable dates **explicitly**, not as zero. Costs use declared
micro-units. This is not calibrated semantic matching or scientific feasibility.
Full-abstract embedding-caliper comparisons were NOT_RUN because embeddings
were unavailable. Numeric purity .60/.70/.80 cells remain NOT_ASSESSED.

## Verification and Independence

Recovery unit tests passed, including the 3-edge fixture (cardinality 2, cost 4)
and 30 brute-force tiny-graph comparisons. The separate six Round 52 mathematical
tests passed; these are not LLM observations. All {len(verification['normalized_artifacts_replayed_identically'])}
normalized output artifacts replayed byte-identically. Volatile manifests are
separated; per-bank source non-reuse and table/grid counts reconcile.

`source_reuse_summary.json` distinguishes seeds, route blocks, source banks,
slots and packet assignments. Cyclic packet permutations are not new independent
banks. k=6 uses exact 0/0.5/1 fractions and does not claim quarter treatments.

## Remaining Scope and Stop

The cached-source lexical recovery is complete; full F0 is not. Missing focal
pages, semantic matching, first-public-date evidence and source/route audit remain.
The latest user permits ARS preparation/pilot after Task 1/2 completion, but the
complete source-feasibility prerequisite is not satisfied. Therefore no ARS
model selection, proposal generation, effect estimate or paper conclusion was
produced. Existing results are source measurements, not the proposed science.
"""
    (BASE / "F0_RESULT.md").write_text(result)
    (BASE / "FEASIBILITY_RESULT.md").write_text(result)
    final = f"""# Final Checkpoint

F0_DATA_STATUS: F0_INCOMPLETE
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED

Completed:
- Located and preserved actual F0 code, cached sources and first failed run.
- Published R0 before rerun; corrected seed gates and provenance/missingness.
- Executed lexical source retrieval and exact matching for {summary['source_matching_seeds']} seeds.
- Retained all failures, repaired-gate flags, measured zeros and unavailable grid cells.
- Replayed normalized artifacts exactly; prepared source audit packets and decision table.

Not completed:
- Complete Task 1 source feasibility: missing focal pages, semantic matching,
  date-resolution evidence and route/purity review remain incomplete.
- Task 2 final scientific block adjudication: table delivered, decisions remain with lead.
- Task 3 ARS setup and Task 4 5-10-seed/two-model pilot: NOT_RUN because prerequisites are incomplete.
- No pilot_report.md pretending to contain measurements; no full experiment or paper.

Scientific questions remaining:
- Which flagged seeds and provisional routes survive source-faithfulness/equipoise review?
- Which temporal and semantic matching cells can be supported by observed covariates?
- Does lexical source coverage survive semantic relevance validation, without changing route definitions?

Recommended next experiment:
- First finish source validation/repair on the deterministic audit packet and the missing
  covariates, then let the research lead choose the next permitted block scope.
- Only after full source feasibility is accepted, freeze the requested ARS state
  (seed + route pair + matched slots + model) and A0/A1/A2/A3 actions. Preserve
  the full route/validity/copy/missingness vector. Do not use source counts as a paper verdict.

STOP: no full experiment, MUSES, base-vs-instruct or three-route expansion.
"""
    (BASE / "FINAL_CHECKPOINT.md").write_text(final)
    (BASE / "STATUS.md").write_text(f"""# F0 Recovery Status

F0_DATA_STATUS: F0_INCOMPLETE
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
SCIENTIFIC_PROPOSAL_GENERATIONS: 0

R0 published: `748110d50126067091ae08d213d91b447048c292`.
Actual source run: `{summary['run_id']}`.
Code commit: `{manifest['git_commit']}`.
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
{' '.join(sys.argv)}
```

Tests: recovery suite PASS; independent Round 52 six design tests PASS; normalized
artifact replay PASS. See `matching_test_report.json` and `REPLAY_VERIFICATION.json`.
Artifacts/provenance: `SOURCE_ONLY_RUN_MANIFEST.json`; human audit CSVs at this root.
Every alteration from the legacy run is disclosed in `RECOVERY_INVENTORY.md`
and `recovery_config.json`. No outcome-dependent source/route/matching changes occurred.

Next: STOP for research-lead review of `FINAL_CHECKPOINT.md`, not a publication decision.
""")
    roots = [p for p in sorted(BASE.iterdir()) if p.is_file() and p.name not in ("SOURCE_ONLY_RUN_MANIFEST.json", ".gitignore")]
    combined = {"run_id": summary["run_id"], "F0_DATA_STATUS": "F0_INCOMPLETE", "scientific_decision": "RESEARCH_LEAD_REQUIRED",
        "source_run_manifest": str((run / "SOURCE_ONLY_RUN_MANIFEST.json").relative_to(ROOT)),
        "source_run_manifest_sha256": digest(run / "SOURCE_ONLY_RUN_MANIFEST.json"),
        "R0_manifest": "runs/R0_20260908/R0_MANIFEST.json", "script_sha256": digest(__file__),
        "code_commit_at_reporting": git("rev-parse", "HEAD"), "producing_command": " ".join(sys.argv),
        "artifacts": {p.name: {"path": str(p.relative_to(ROOT)), "sha256": digest(p), "status": "AVAILABLE_WITH_TYPED_CONTENT"} for p in roots}}
    retain_json(BASE / "SOURCE_ONLY_RUN_MANIFEST.json", combined)
    print(json.dumps({"verification": "PASS", "normalized_replay_files": len(verification["normalized_artifacts_replayed_identically"]),
                      "route_pair_coverage": paired, "state": "F0_INCOMPLETE"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    args = parser.parse_args()
    report(args.run, args.replay)
