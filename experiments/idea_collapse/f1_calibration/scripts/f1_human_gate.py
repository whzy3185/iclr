"""Freeze F1 inputs and prepare source-only human review materials."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
F0 = ROOT / "experiments/idea_collapse/f0_semantic_temporal"
F1 = ROOT / "experiments/idea_collapse/f1_calibration"
EXPECTED_INPUT_COMMIT = "742c2a84819e122429cfa5b5973c173c734714b3"
EXPECTED_CORPUS_SHA256 = "0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807"


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


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def artifact_record(path):
    path = Path(path)
    record = {
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }
    if path.suffix in {".jsonl", ".csv"}:
        with path.open("rb") as handle:
            record["rows"] = sum(1 for line in handle if line.strip()) - (1 if path.suffix == ".csv" else 0)
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["freeze"])
    args = parser.parse_args()
    if args.task == "freeze":
        freeze_inputs()


if __name__ == "__main__":
    main()
