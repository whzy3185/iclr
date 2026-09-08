"""R1-R5 source-only recovery from the published R0 snapshot, never a generator."""

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import csv
from datetime import datetime, timezone
import gzip
import io
import itertools
import json
from pathlib import Path
import platform
import statistics
import sys
import time

import networkx as nx

from recovery_algorithms import BACKEND, PAIRS, annotate, coverage_cell, lexical_candidates, make_seed, match_lexical, packets
from recovery_common import BASE, ROOT, SPECS, digest, encoded, git, identity, legacy, read_jsonl, write_csv, write_json, write_jsonl


@contextmanager
def compressed_rows(path, fields):
    with Path(path).open("xb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="", compresslevel=6) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="raise", lineterminator="\n")
                writer.writeheader()
                yield writer


def audit_sample(seeds):
    strata = defaultdict(list)
    for seed in seeds:
        label = "structural" if seed["hard_errors"] else "repair" if seed["repair_reason"] else "flagged" if seed["risk_flags"] else "unflagged"
        strata[label].append(seed)
    rows = []
    for label, group in sorted(strata.items()):
        for seed in sorted(group, key=lambda s: identity(s["seed_id"]))[:5]:
            rows.append({"stratum": label, "seed_id": seed["seed_id"], "source_matching_allowed": seed["source_matching_allowed"],
                         "question": seed["method_masked_question"], "risk_flags": json.dumps(seed["risk_flags"]),
                         "hard_errors": json.dumps(seed["hard_errors"]), "source_spans": json.dumps(seed["source_spans"]),
                         "human_review": "", "human_notes": ""})
    return rows, {label: len(strata.get(label, [])) for label in ("structural", "repair", "flagged", "unflagged")}


def canonical_cells(seeds, config, run_id):
    for seed in seeds:
        for pair, temporal, regime, purity, k in itertools.product(
                PAIRS, config["temporal_tiers"], config["matching_regimes"], config["purity_thresholds"], config["k_values"]):
            state = "MISSING_COVARIATES" if seed["source_matching_allowed"] else "BLOCKED"
            yield {"run_id": run_id, "seed_id": seed["seed_id"], "route_pair_id": pair,
                   "temporal_tier": temporal, "retrieval_backend": BACKEND, "matching_regime": regime,
                   "purity_regime": purity, "purity_assessment_status": "NOT_ASSESSED", "k": k,
                   "n_A": None, "n_B": None, **coverage_cell(state),
                   "reason": "DENSE_DATE_MODEL_TOKEN_PURITY_UNAVAILABLE" if state == "MISSING_COVARIATES" else "SOURCE_GATE_OR_REPAIR"}


def run(config_path, replay=False):
    started = time.monotonic()
    config = json.loads(Path(config_path).read_text())
    if config["network_acquisition"] or config["scientific_generations"]:
        raise ValueError("this runner has no acquisition or proposal-generation path")
    snapshot = BASE / config["source_snapshot"]
    r0 = json.loads((snapshot / "R0_MANIFEST.json").read_text())
    for name, artifact in r0["artifacts"].items():
        if digest(snapshot / name) != artifact["sha256"]:
            raise ValueError("R0 artifact changed: " + name)
    config_hash = digest(config_path)
    code_hashes = {str(p.relative_to(ROOT)): digest(p) for p in sorted((BASE / "scripts").glob("*.py"))}
    code_hashes["legacy/f0_source_only_audit.py"] = digest(BASE / "legacy/f0_source_only_audit.py")
    run_id = "F0R-" + identity({"config": config_hash, "code": code_hashes,
                                "r0": digest(snapshot / "R0_MANIFEST.json")})[:20]
    output = BASE / "runs" / (run_id + ("-replay" if replay else ""))
    output.mkdir(exist_ok=False)
    initial_manifest = {"run_id": run_id, "run_purpose": "SOURCE_ONLY_RECOVERY", "git_commit": git("rev-parse", "HEAD"),
                        "git_dirty": bool(git("status", "--porcelain")), "config_sha256": config_hash,
                        "code_hashes": code_hashes, "r0_manifest_sha256": digest(snapshot / "R0_MANIFEST.json"),
                        "spec_hashes": {p: digest(ROOT / p) for p in SPECS}, "python": platform.python_version(),
                        "networkx": nx.__version__, "scientific_generations": 0,
                        "command": " ".join(sys.argv), "started_at": datetime.now(timezone.utc).isoformat()}
    write_json(output / "START_MANIFEST.json", initial_manifest)
    evidence_all = list(read_jsonl(snapshot / "iclr2025_papers.jsonl.gz"))
    focal_all = list(read_jsonl(snapshot / "iclr2026_papers.jsonl.gz"))
    evidence = [p for p in evidence_all if p["parse_status"] == "MEASURED"]
    seeds = [make_seed(p) for p in focal_all]
    allowed = [s for s in seeds if s["source_matching_allowed"]]
    annotations = {p["paper_id"]: annotate(p) for p in evidence}
    write_jsonl(output / "seed_candidates.jsonl.gz", seeds)
    write_jsonl(output / "seed_gate_audit.jsonl", ({k: s[k] for k in (
        "seed_id", "focal_paper_id", "source_spans", "extractable", "source_matching_allowed", "confirmatory_eligible",
        "risk_flags", "hard_errors", "review_state", "repair_reason")} for s in seeds))
    sample, strata = audit_sample(seeds)
    write_csv(output / "seed_gate_audit_sample.csv", sample, list(sample[0]))
    write_jsonl(output / "source_route_annotations.jsonl.gz", annotations.values())
    write_json(output / "route_label_summary.json", {"counts": dict(Counter(a["primary_route"] for a in annotations.values())),
        "qualitative_route_clear": dict(Counter(a["primary_route"] for a in annotations.values() if a["route_purity_descriptor"] == "ROUTE_CLEAR")),
        "numeric_purity_status": "NOT_ASSESSED", "human_review": "PENDING"})
    write_jsonl(output / "temporal_cleanliness.jsonl", ({"paper_id": p["paper_id"], "first_public_date": p["first_public_date"],
        "proceedings_date": p["proceedings_publication_date"], "status": p["temporal_status"], "search_coverage": p["date_search_coverage"]} for p in evidence_all))
    docs = [p["title"] + " " + p["abstract"] for p in evidence]
    _, idf, inverted = legacy.build_tfidf(docs)
    counters = [Counter(legacy.tokenize(doc)) for doc in docs]
    write_json(output / "retrieval_backend_manifest.json", {
        "backend": BACKEND, "vectorizer": "legacy lowercase unigram+bigram tf-idf, min_df=2, sublinear TF, L2",
        "idf_sha256": identity(idf), "vocabulary_sha256": identity(sorted(idf)), "candidate_pool_sha256": identity([p["paper_id"] for p in evidence]),
        "secondary_score": "legacy capped token-overlap score, normalized by within-query maximum; NOT independent semantic reranker",
        "dense_model": None, "dense_model_revision": None, "dense_relevance": None, "semantic_reranker": None,
        "config": config["lexical_diagnostic"], "purity_assessment": "NOT_ASSESSED"})
    retrieval_fields = ["seed_id", "paper_id", "rank", "retrieval_backend", "lexical_cosine", "lexical_bm25_like", "dense_relevance",
        "semantic_reranker_score", "numeric_route_purity", "first_public_date", "year", "lexical_length", "model_token_length",
        "subfield", "primary_route", "route_purity_descriptor", "above_legacy_lexical_floor", "query_sha256"]
    slot_fields = ["run_id", "bank_id", "seed_id", "route_pair_id", "matching_regime", "retrieval_backend", "slot_index",
                   "A_paper_id", "B_paper_id", "cost_units", "lexical_relevance_gap", "lexical_bm25_gap", "length_z_gap",
                   "subfield_disagreement", "date_gap_days", "dense_gap", "embedding_distance"]
    summaries, source_use = [], defaultdict(set)
    total_slots = total_candidates = packet_count = 0
    matched_fields = ["seed_id", "route_pair_id", "n_A", "n_B", "admissible_edges", "max_matched_slots",
                      "median_cost_units", "cell_status", "bank_id", "unmatched_count"]
    with compressed_rows(output / "retrieval_candidates.csv.gz", retrieval_fields) as retrieval_writer, \
         (output / "matched_evidence_slots.csv").open("x", encoding="utf-8", newline="") as slots_file, \
         compressed_rows(output / "unmatched_papers.csv.gz", ["seed_id", "route_pair_id", "paper_id", "reason"]) as unmatched_writer, \
         compressed_rows(output / "packet_assignments.csv.gz", ["seed_id", "route_pair_id", "bank_id", "k", "alpha", "assignment",
                         "A_slot_indices", "ordered_paper_ids", "exact_quarters_supported"]) as packet_writer:
        slot_writer = csv.DictWriter(slots_file, fieldnames=slot_fields, lineterminator="\n")
        slot_writer.writeheader()
        for index, seed in enumerate(allowed, 1):
            candidates = lexical_candidates(seed, evidence, annotations, idf, inverted, counters, config["lexical_diagnostic"])
            retrieval_writer.writerows(candidates)
            total_candidates += len(candidates)
            for pair, routes in PAIRS.items():
                matched, features, unmatched, summary = match_lexical(candidates, routes, config["lexical_diagnostic"])
                bank_id = identity({"seed": seed["seed_id"], "pair": pair, "slots": matched})
                row = {"seed_id": seed["seed_id"], "route_pair_id": pair, "n_A": summary["n_A"], "n_B": summary["n_B"],
                       "admissible_edges": summary["admissible_edges"], "max_matched_slots": len(matched),
                       "median_cost_units": statistics.median([c for a, b, c in matched]) if matched else None,
                       "cell_status": "MEASURED", "bank_id": bank_id, "unmatched_count": len(unmatched)}
                summaries.append(row)
                for j, (a, b, cost) in enumerate(matched, 1):
                    slot_writer.writerow({"run_id": run_id, "bank_id": bank_id, "seed_id": seed["seed_id"], "route_pair_id": pair,
                        "matching_regime": config["lexical_diagnostic"]["regime"], "retrieval_backend": BACKEND, "slot_index": j,
                        "A_paper_id": a, "B_paper_id": b, "cost_units": cost, **features[a, b]})
                    source_use[a].add((seed["seed_id"], bank_id))
                    source_use[b].add((seed["seed_id"], bank_id))
                total_slots += len(matched)
                unmatched_writer.writerows({"seed_id": seed["seed_id"], "route_pair_id": pair, **u} for u in unmatched)
                for k in config["k_values"]:
                    for packet in packets(matched, k):
                        packet_count += 1
                        packet_writer.writerow({"seed_id": seed["seed_id"], "route_pair_id": pair, "bank_id": bank_id,
                            **{name: json.dumps(value) if isinstance(value, list) else value for name, value in packet.items()}})
            if index % 100 == 0 or index == len(allowed):
                print(f"source matching {index}/{len(allowed)}, candidate rows={total_candidates}, slots={total_slots}", flush=True)
    write_csv(output / "lexical_matching_diagnostics.csv", summaries, matched_fields)
    print("Materializing typed coverage map (unavailable cells are not zeros)", flush=True)
    write_jsonl(output / "coverage_cells.jsonl.gz", canonical_cells(seeds, config, run_id))
    frontier = []
    for pair, temporal, regime, purity, k in itertools.product(PAIRS, config["temporal_tiers"], config["matching_regimes"], config["purity_thresholds"], config["k_values"]):
        frontier.append({"route_pair_id": pair, "temporal_tier": temporal, "matching_regime": regime, "purity_regime": purity,
                         "k": k, "retrieval_backend": BACKEND, "cell_status": "MISSING_COVARIATES", "eligible_unique_seeds": len(allowed),
                         "n_measured_blocks": 0, "unique_seed_coverage": None, "matched_blocks": None,
                         "reason": "DENSE_DATE_MODEL_TOKEN_PURITY_UNAVAILABLE"})
    for pair, k in itertools.product(PAIRS, config["k_values"]):
        rows = [r for r in summaries if r["route_pair_id"] == pair]
        coverage = {r["seed_id"] for r in rows if r["max_matched_slots"] >= k}
        frontier.append({"route_pair_id": pair, "temporal_tier": "T2_ALL_ACCEPTED", "matching_regime": config["lexical_diagnostic"]["regime"],
                         "purity_regime": "NOT_ASSESSED", "k": k, "retrieval_backend": BACKEND,
                         "cell_status": "MEASURED" if rows else "NOT_RUN", "eligible_unique_seeds": len(allowed),
                         "n_measured_blocks": len(rows), "unique_seed_coverage": len(coverage) if rows else None,
                         "matched_blocks": len(coverage) if rows else None,
                         "reason": "provisional source screen, not semantic/temporal validation"})
    write_csv(output / "coverage_balance_frontier.csv", frontier, list(frontier[0]))
    usable_by_k = {str(k): len({r["seed_id"] for r in summaries if r["max_matched_slots"] >= k}) for k in config["k_values"]}
    attrition = [
        {"stage": "official_focal_ids", "state": "measured", "count": len(focal_all), "unit": "unique_seed", "reason": "official index"},
        {"stage": "source_missing_or_structural_failure", "state": "measured", "count": sum(bool(s["hard_errors"]) for s in seeds), "unit": "unique_seed", "reason": "retained rows, not dropped"},
        {"stage": "extractable", "state": "measured", "count": sum(s["extractable"] for s in seeds), "unit": "unique_seed", "reason": "source-derived text exists"},
        {"stage": "explicit_solution_repair_queue", "state": "measured", "count": sum(bool(s["repair_reason"]) for s in seeds), "unit": "unique_seed", "reason": "not rehabilitated by warning policy"},
        {"stage": "provisional_source_matching_allowed", "state": "measured", "count": len(allowed), "unit": "unique_seed", "reason": "human review still pending"},
        {"stage": "lexical_matching_executed", "state": "measured", "count": len(summaries), "unit": "seed_route_block", "reason": "four contrasts per allowed seed"},
        *[{"stage": f"lexical_k{k}_coverage", "state": "measured", "count": usable_by_k[str(k)], "unit": "unique_seed", "reason": "at least one route block; provisional only"} for k in config["k_values"]],
        {"stage": "semantic_matching", "state": "not-run", "count": None, "unit": "seed_route_block", "reason": "backend/covariates unavailable"},
        {"stage": "human_approved_experimental_blocks", "state": "unknown", "count": None, "unit": "seed_route_block", "reason": "PENDING_REVIEW; not a measured zero"},
    ]
    write_csv(output / "attrition_waterfall.csv", attrition, list(attrition[0]))
    reuse = {"unique_seed_ids": len(seeds), "source_matching_seeds": len(allowed), "seed_route_blocks_measured": len(summaries),
             "nonempty_slot_banks": sum(r["max_matched_slots"] > 0 for r in summaries), "assignments_within_existing_banks": packet_count,
             "distinct_evidence_papers_in_banks": len(source_use), "matched_slots": total_slots,
             "sources_reused_across_banks": sum(len(uses) > 1 for uses in source_use.values()),
             "sources_reused_across_seeds": sum(len({s for s, bank in uses}) > 1 for uses in source_use.values()),
             "source_bank_use_counts": {p: len(uses) for p, uses in sorted(source_use.items())},
             "warning": "assignments are not independent banks; blocks are not independent seeds"}
    write_json(output / "source_reuse_summary.json", reuse)
    write_json(output / "matching_test_report.json", {"fixture": [["A0", "B0", 1], ["A0", "B1", 2], ["A1", "B0", 2]],
        "expected_cardinality": 2, "expected_cost": 4, "test_suite": "tests/test_recovery.py", "objective": config["matcher"],
        "suite_result": "see separately captured test log; source run does not invent a test execution"})
    write_json(output / "SUMMARY.json", {"run_id": run_id, "F0_DATA_STATUS": "F0_INCOMPLETE", "scientific_decision": "RESEARCH_LEAD_REQUIRED",
        "corpus_counts": r0["corpus_counts"], "audit_strata": strata, "source_matching_seeds": len(allowed),
        "flagged_but_matching_seeds": sum(bool(s["risk_flags"]) for s in allowed), "repair_seeds": sum(bool(s["repair_reason"]) for s in seeds),
        "structural_failure_seeds": sum(bool(s["hard_errors"]) for s in seeds), "lexical_candidate_rows": total_candidates,
        "matching_blocks_measured": len(summaries), "measured_zero_blocks": sum(r["max_matched_slots"] == 0 for r in summaries),
        "canonical_grid_cells": len(seeds) * 4 * 3 * 3 * 3 * 4,
        "canonical_matching_cells_measured": 0, "lexical_unique_seed_coverage": usable_by_k,
        "matched_slots": total_slots, "scientific_generations": 0, "human_reviews_performed": 0})
    artifact_manifest = {p.name: {"path": str(p.relative_to(ROOT)), "sha256": digest(p), "bytes": p.stat().st_size,
                                "status": "MEASURED_ARTIFACT_WITH_TYPED_CONTENT", "producing_command": " ".join(sys.argv)}
                         for p in sorted(output.iterdir()) if p.is_file()}
    manifest = {**initial_manifest, "finished_at": datetime.now(timezone.utc).isoformat(), "elapsed_seconds": time.monotonic() - started,
                "F0_DATA_STATUS": "F0_INCOMPLETE", "completed_scope": "cached ingestion and lexical source-only recovery",
                "incomplete_scope": ["missing focal abstracts", "dense semantic retrieval/matching", "first-public date resolution", "purity/F1 human audit"],
                "artifacts": artifact_manifest}
    write_json(output / "SOURCE_ONLY_RUN_MANIFEST.json", manifest)
    print(json.dumps({"output": str(output), "summary": json.loads((output / "SUMMARY.json").read_text())}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--replay", action="store_true", help="same frozen inputs into a new verification directory")
    args = parser.parse_args()
    run(args.config, args.replay)
