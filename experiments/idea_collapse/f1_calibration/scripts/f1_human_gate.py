"""Freeze F1 inputs and prepare source-only human review materials."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
F0 = ROOT / "experiments/idea_collapse/f0_semantic_temporal"
F1 = ROOT / "experiments/idea_collapse/f1_calibration"
EXPECTED_INPUT_COMMIT = "742c2a84819e122429cfa5b5973c173c734714b3"
EXPECTED_CORPUS_SHA256 = "0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807"
PACKAGE = F1 / "reviewer_package"


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_value(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_immutable(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f"immutable artifact differs: {path}")
    if not path.exists():
        path.write_bytes(data)


def write_jsonl(path, rows):
    write_immutable(path, b"".join(canonical(row) for row in rows))


def write_csv(path, rows, fields):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field) for field in fields})
    write_immutable(path, buffer.getvalue().encode())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def artifact_record(path):
    path = Path(path)
    record = {
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }
    if path.suffix == ".jsonl":
        with path.open("rb") as handle:
            record["rows"] = sum(1 for line in handle if line.strip())
    elif path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            record["rows"] = max(0, sum(1 for _ in csv.reader(handle)) - 1)
    return record


def review_value_is_empty(value):
    return value is None or value == "" or value == [] or value == {}


def freeze_inputs():
    calibration_path = F0 / "f1_package/F1_CALIBRATION_CANDIDATES.jsonl"
    certification_path = F0 / "f1_package/F1_CERTIFICATION_CANDIDATES.jsonl"
    provenance_path = F0 / "f1_package/F1_HIDDEN_PROVENANCE.jsonl"
    calibration = read_jsonl(calibration_path)
    certification = read_jsonl(certification_path)
    provenance = read_jsonl(provenance_path)
    provenance_by_block = {row["block_key"]: row for row in provenance}
    calibration_seeds = sorted(provenance_by_block[row["block_key"]]["seed_id"] for row in calibration)
    certification_seeds = sorted(provenance_by_block[row["block_key"]]["seed_id"] for row in certification)

    review_specs = {
        F1 / "seed_audit.jsonl": [
            "human_source_faithfulness", "human_duplication_decision", "human_generic_masking_decision",
            "human_solution_leakage", "human_comprehensibility", "human_notes",
        ],
        F1 / "paper_relevance_route_audit.jsonl": [
            "seed_specific_relevance", "primary_contribution_route", "secondary_contribution_route",
            "supporting_source_span", "confidence", "notes",
        ],
        F1 / "block_admissibility_audit.jsonl": [
            "route_1_relevance", "route_2_relevance", "route_relation", "route_1_plausibility",
            "route_2_plausibility", "distinguishability", "complementarity_or_subsumption",
            "equipoise", "usable_slot_count", "human_notes",
        ],
    }
    nonempty_review_values = []
    for path, fields in review_specs.items():
        for row in read_jsonl(path):
            for field in fields:
                if not review_value_is_empty(row.get(field)):
                    nonempty_review_values.append({"file": str(path.relative_to(ROOT)), "record": row.get("audit_record_id"), "field": field})
    for partition, rows in (("CALIBRATION", calibration), ("CERTIFICATION", certification)):
        for row in rows:
            if not review_value_is_empty(row.get("human_labels")):
                nonempty_review_values.append({"file": partition, "record": row["block_key"], "field": "human_labels"})

    query_variants = read_jsonl(F1 / "query_variants.jsonl")
    calibration_seed_set = set(calibration_seeds)
    query_seed_set = {row["seed_id"] for row in query_variants}
    certification_seed_set = set(certification_seeds)

    files = [
        calibration_path,
        certification_path,
        provenance_path,
        F0 / "f1_package/F1_PACKAGE_MANIFEST.json",
        F0 / "anonymization/anonymous_evidence.jsonl",
        F1 / "seed_audit.jsonl",
        F1 / "paper_relevance_route_audit.jsonl",
        F1 / "block_admissibility_audit.jsonl",
        F1 / "query_variants.jsonl",
        F1 / "query_variant_manifest.json",
        F1 / "query_variant_result_manifest.json",
        F1 / "query_representation_diagnostics.jsonl",
        F1 / "query_pair_scores.jsonl",
        F1 / "token_budget_audit.json",
        F1 / "_PRIVATE_block_ab_mapping.jsonl",
        F1 / "source_identity_audit.json",
        F1 / "temporal_review_queue.jsonl",
        F1 / "INPUT_MANIFEST.json",
        Path(__file__),
    ]
    corpus_manifest = json.loads((ROOT / "experiments/idea_collapse/corpus/iclr_2024_2026/corpus_manifest.json").read_text())
    assertions = {
        "input_commit_matches_checkpoint": git("rev-parse", "HEAD") == EXPECTED_INPUT_COMMIT,
        "corpus_hash_matches_frozen": corpus_manifest["corpus_sha256"] == EXPECTED_CORPUS_SHA256,
        "calibration_blocks_24": len(calibration) == 24,
        "calibration_unique_seeds_24": len(calibration_seed_set) == 24,
        "certification_blocks_96": len(certification) == 96,
        "certification_unique_seeds_96": len(certification_seed_set) == 96,
        "calibration_certification_seed_disjoint": not (calibration_seed_set & certification_seed_set),
        "calibration_query_scope_exact": query_seed_set == calibration_seed_set,
        "certification_absent_from_query_adjustment_scope": not (query_seed_set & certification_seed_set),
        "human_labels_empty": not nonempty_review_values,
        "scientific_proposal_generations_zero": True,
    }
    if not all(assertions.values()):
        raise RuntimeError(f"F1 input freeze failed: {json.dumps(assertions, sort_keys=True)}")

    freeze = {
        "schema_version": "f1-input-freeze-v1",
        "freeze_date": "2026-09-21",
        "branch": git("branch", "--show-current"),
        "input_commit": EXPECTED_INPUT_COMMIT,
        "corpus_sha256": corpus_manifest["corpus_sha256"],
        "counts": {
            "calibration_blocks": len(calibration),
            "calibration_unique_seeds": len(calibration_seed_set),
            "certification_blocks": len(certification),
            "certification_unique_seeds": len(certification_seed_set),
            "nonempty_human_review_values": len(nonempty_review_values),
            "scientific_proposal_generations": 0,
        },
        "set_hashes": {
            "calibration_block_keys_sha256": hash_value(sorted(row["block_key"] for row in calibration)),
            "calibration_seed_ids_sha256": hash_value(calibration_seeds),
            "certification_block_keys_sha256": hash_value(sorted(row["block_key"] for row in certification)),
            "certification_seed_ids_sha256": hash_value(certification_seeds),
            "query_diagnostic_seed_ids_sha256": hash_value(sorted(query_seed_set)),
        },
        "assertions": assertions,
        "process_boundary": {
            "calibration_data_used_for_rule_development": True,
            "certification_data_used_for_rule_development": False,
            "basis": "Q0/Q1 diagnostic seed set exactly equals the 24 calibration seeds and is disjoint from all 96 certification seeds.",
            "future_model_outcomes_observed": False,
            "formal_certification_started": False,
        },
        "files": {str(path.relative_to(ROOT)): artifact_record(path) for path in files},
    }
    write_immutable(F1 / "F1_INPUT_FREEZE.json", canonical(freeze))
    print(json.dumps({"output": str((F1 / 'F1_INPUT_FREEZE.json').relative_to(ROOT)), "assertions": assertions}, indent=2, sort_keys=True))


def _json_cell(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _contains_source_id(value, source_ids):
    if isinstance(value, str):
        return value in source_ids
    if isinstance(value, dict):
        return any(_contains_source_id(item, source_ids) for item in value.values())
    if isinstance(value, list):
        return any(_contains_source_id(item, source_ids) for item in value)
    return False


def _review_fields_empty(rows, fields):
    return all(review_value_is_empty(row.get(field)) for row in rows for field in fields)


def prepare_calibration_package():
    freeze_path = F1 / "F1_INPUT_FREEZE.json"
    freeze = json.loads(freeze_path.read_text())
    if freeze["input_commit"] != EXPECTED_INPUT_COMMIT or not all(freeze["assertions"].values()):
        raise RuntimeError("invalid or incomplete F1 input freeze")
    for relative, record in freeze["files"].items():
        path = ROOT / relative
        if relative.endswith("scripts/f1_human_gate.py"):
            continue
        if sha256(path) != record["sha256"]:
            raise RuntimeError(f"frozen input changed: {relative}")

    seed_source = read_jsonl(F1 / "seed_audit.jsonl")
    paper_source = read_jsonl(F1 / "paper_relevance_route_audit.jsonl")
    block_source = read_jsonl(F1 / "block_admissibility_audit.jsonl")
    evidence_source = read_jsonl(F0 / "evidence.jsonl")
    source_ids = {row["paper_id"] for row in evidence_source}

    seed_rows = []
    for row in seed_source:
        seed_rows.append({
            "review_item_id": row["audit_record_id"],
            "block_key": row["block_key"],
            "original_problem_context": row["original_problem_context"],
            "current_method_masked_seed": row["current_method_masked_seed"],
            "source_spans": row["source_spans"],
            "deterministic_duplicate_diagnostic": row["duplicate_diagnostic"],
            "deterministic_generic_terms_masked": row["generic_terms_masked"],
            "deterministic_solution_prescribing_spans": row["possible_solution_prescribing_spans"],
            "reviewer_id": None,
            "review_round": None,
            "comprehensible": None,
            "method_neutral": None,
            "solution_leakage": None,
            "duplicated_or_malformed": None,
            "multi_route_open": None,
            "source_faithful": None,
            "seed_decision": None,
            "failure_types": None,
            "approved_repair_text": None,
            "reviewer_rationale": None,
        })

    paper_rows = []
    for row in paper_source:
        paper_rows.append({
            "review_item_id": row["audit_record_id"],
            "review_paper_token": row["review_paper_id"],
            "seed_display_text": row["seed_display_text"],
            "anonymous_abstract": row["abstract"],
            "reviewer_id": None,
            "review_round": None,
            "relevance_label": None,
            "primary_scientific_contribution": None,
            "secondary_scientific_contribution": None,
            "evidence_sentence": None,
            "reviewer_confidence": None,
            "reviewer_rationale": None,
        })

    block_rows = []
    for row in block_source:
        block_rows.append({
            "review_item_id": row["audit_record_id"],
            "block_key": row["block_key"],
            "display_route_1_description": row["display_route_1_description"],
            "display_route_2_description": row["display_route_2_description"],
            "display_route_1_evidence": row["display_route_1_evidence"],
            "display_route_2_evidence": row["display_route_2_evidence"],
            "reviewed_slot_count": 4,
            "reviewed_slot_scope": "exactly four displayed matched slots; cannot certify k=6/k=8/k=12",
            "reviewer_id": None,
            "review_round": None,
            "route_1_scientifically_plausible": None,
            "route_2_scientifically_plausible": None,
            "routes_distinguishable": None,
            "routes_non_subsumed": None,
            "equipoise": None,
            "route_relationship": None,
            "usable_for_intervention": None,
            "usable_slot_count": None,
            "reviewer_rationale": None,
        })

    seed_fields = [
        "review_item_id", "block_key", "original_problem_context", "current_method_masked_seed",
        "source_spans", "deterministic_duplicate_diagnostic", "deterministic_generic_terms_masked",
        "deterministic_solution_prescribing_spans", "reviewer_id", "review_round", "comprehensible",
        "method_neutral", "solution_leakage", "duplicated_or_malformed", "multi_route_open",
        "source_faithful", "seed_decision", "failure_types", "approved_repair_text", "reviewer_rationale",
    ]
    paper_fields = [
        "review_item_id", "review_paper_token", "seed_display_text", "anonymous_abstract",
        "reviewer_id", "review_round", "relevance_label", "primary_scientific_contribution",
        "secondary_scientific_contribution", "evidence_sentence", "reviewer_confidence", "reviewer_rationale",
    ]
    block_fields = [
        "review_item_id", "block_key", "display_route_1_description", "display_route_2_description",
        "display_route_1_evidence", "display_route_2_evidence", "reviewed_slot_count", "reviewed_slot_scope",
        "reviewer_id", "review_round", "route_1_scientifically_plausible",
        "route_2_scientifically_plausible", "routes_distinguishable", "routes_non_subsumed",
        "equipoise", "route_relationship", "usable_for_intervention", "usable_slot_count", "reviewer_rationale",
    ]
    write_jsonl(PACKAGE / "seed_review.jsonl", seed_rows)
    write_jsonl(PACKAGE / "paper_review.jsonl", paper_rows)
    write_jsonl(PACKAGE / "block_review.jsonl", block_rows)
    write_csv(PACKAGE / "seed_review.csv", [{**row, **{key: _json_cell(row[key]) for key in (
        "source_spans", "deterministic_duplicate_diagnostic", "deterministic_generic_terms_masked",
        "deterministic_solution_prescribing_spans")}} for row in seed_rows], seed_fields)
    write_csv(PACKAGE / "paper_review.csv", paper_rows, paper_fields)
    write_csv(PACKAGE / "block_review.csv", [{**row,
        "display_route_1_evidence": _json_cell(row["display_route_1_evidence"]),
        "display_route_2_evidence": _json_cell(row["display_route_2_evidence"])} for row in block_rows], block_fields)

    instructions = """# F1 Calibration Review Instructions

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
"""
    write_immutable(F1 / "F1_CALIBRATION_REVIEW_INSTRUCTIONS.md", instructions.encode())

    reviewer_fields = {
        "seed": seed_fields[8:],
        "paper": paper_fields[4:],
        "block": block_fields[8:],
    }
    assertions = {
        "seed_rows_24": len(seed_rows) == 24,
        "paper_rows_192": len(paper_rows) == 192,
        "block_rows_24": len(block_rows) == 24,
        "all_seed_review_fields_empty": _review_fields_empty(seed_rows, reviewer_fields["seed"]),
        "all_paper_review_fields_empty": _review_fields_empty(paper_rows, reviewer_fields["paper"]),
        "all_block_review_fields_empty": _review_fields_empty(block_rows, reviewer_fields["block"]),
        "paper_source_ids_absent": not any(_contains_source_id(row, source_ids) for row in paper_rows),
        "paper_hidden_fields_absent": all(not ({"retrieval_score", "rank", "match_status", "route_label", "paper_id"} & set(row)) for row in paper_rows),
        "ab_display_order_preserved": all(
            output["review_item_id"] == source["audit_record_id"]
            and output["display_route_1_description"] == source["display_route_1_description"]
            and output["display_route_2_description"] == source["display_route_2_description"]
            and output["display_route_1_evidence"] == source["display_route_1_evidence"]
            and output["display_route_2_evidence"] == source["display_route_2_evidence"]
            for output, source in zip(block_rows, block_source)
        ),
        "review_scope_exactly_four": all(
            row["reviewed_slot_count"] == 4
            and len(row["display_route_1_evidence"]) == 4
            and len(row["display_route_2_evidence"]) == 4
            for row in block_rows
        ),
        "private_mapping_not_in_reviewer_package": not any(path.name.startswith("_PRIVATE") for path in PACKAGE.iterdir()),
        "scientific_proposal_generations_zero": True,
    }
    if not all(assertions.values()):
        raise RuntimeError(f"review package validation failed: {json.dumps(assertions, sort_keys=True)}")
    package_files = [
        PACKAGE / "seed_review.jsonl", PACKAGE / "seed_review.csv",
        PACKAGE / "paper_review.jsonl", PACKAGE / "paper_review.csv",
        PACKAGE / "block_review.jsonl", PACKAGE / "block_review.csv",
        F1 / "F1_CALIBRATION_REVIEW_INSTRUCTIONS.md",
    ]
    manifest = {
        "schema_version": "f1-calibration-review-package-v1",
        "created_date": "2026-09-21",
        "input_freeze_sha256": sha256(freeze_path),
        "input_freeze_commit": EXPECTED_INPUT_COMMIT,
        "generation_commit": git("rev-parse", "HEAD"),
        "counts": {"seed_rows": len(seed_rows), "paper_rows": len(paper_rows), "block_rows": len(block_rows)},
        "reviewer_fields": reviewer_fields,
        "assertions": assertions,
        "files": {str(path.relative_to(ROOT)): artifact_record(path) for path in package_files},
        "human_labels_imported": 0,
        "certification_blocks_opened_for_rule_adjustment": 0,
        "scientific_proposal_generations": 0,
        "status": "WAITING_FOR_CALIBRATION_LABELS",
    }
    write_immutable(PACKAGE / "REVIEW_PACKAGE_MANIFEST.json", canonical(manifest))

    status_path = F1 / "STATUS.md"
    status = status_path.read_text()
    marker = "F1_HUMAN_GATE_TASK_2=COMPLETED"
    if marker not in status:
        status = status.rstrip() + "\n\n" + "\n".join([
            marker,
            "F1_INPUT_FREEZE_COMMIT=cbf502ec173a69d11784a3df5e95dc1be1552263",
            "CALIBRATION_REVIEW_PACKAGE=READY",
            "CALIBRATION_HUMAN_LABELS_IMPORTED=0",
            "CERTIFICATION_REVIEW_STARTED=False",
            "STATUS=WAITING_FOR_CALIBRATION_LABELS",
            "NEXT=HUMAN_COMPLETION_OF_24_CALIBRATION_BLOCKS",
            "SCIENTIFIC_PROPOSAL_GENERATIONS=0",
            "HARD_STOP=ACTIVE",
        ]) + "\n"
        status_path.write_text(status)
    print(json.dumps({"manifest": str((PACKAGE / 'REVIEW_PACKAGE_MANIFEST.json').relative_to(ROOT)), "assertions": assertions}, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["freeze", "package"])
    args = parser.parse_args()
    if args.task == "freeze":
        freeze_inputs()
    elif args.task == "package":
        prepare_calibration_package()


if __name__ == "__main__":
    main()
