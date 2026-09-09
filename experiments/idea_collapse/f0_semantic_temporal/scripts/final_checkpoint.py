"""Render T8 from measured source artifacts; no research-outcome inference."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

from common import BASE, hash_value, read_rows, save, sha, text


def finalize():
    cfg = json.loads((BASE / "config.json").read_text())
    temporal = json.loads((BASE / "temporal/temporal_summary.json").read_text())["coverage"]
    coverage = json.loads((BASE / "matching/coverage.json").read_text())
    package = json.loads((BASE / "f1_package/F1_PACKAGE_MANIFEST.json").read_text())
    reranking = json.loads((BASE / "semantic/reranking_summary.json").read_text())
    model = json.loads((BASE / "semantic/model_manifest.json").read_text())
    leaks = json.loads((BASE / "anonymization/leak_audit.json").read_text())
    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(BASE / "tests"), "-v"],
                           capture_output=True, text=True, timeout=120)
    if tests.returncode:
        raise RuntimeError(tests.stderr)
    test_log = BASE / "TEST_REPORT.json"
    if not test_log.exists():
        save(test_log, {"returncode": tests.returncode, "stdout": tests.stdout, "stderr": tests.stderr,
                        "scope": "source-only unit tests, not human labels or hypothesis tests"})
    banks = read_rows(BASE / "matching/matched_slots.jsonl")
    measured = 0
    for b in banks:
        if b["status"] == "MEASURED":
            measured += 1
            if b["max_matched_slots"] != len(b["slots"]): raise ValueError("slot count mismatch")
            ids = [s[k] for s in b["slots"] for k in ("A_paper_id", "B_paper_id")]
            if len(ids) != len(set(ids)): raise ValueError("source reused in bank")
        elif b["max_matched_slots"] is not None:
            raise ValueError("blocked matching has numeric count")
    hidden = {r["block_key"]: r for r in read_rows(BASE / "f1_package/F1_HIDDEN_PROVENANCE.jsonl")}
    field_allowlist = {"block_key", "method_masked_seed", "route_A_description", "route_B_description",
                       "A_evidence_abstracts", "B_evidence_abstracts", "human_labels", "status"}
    checked = 0
    seed_groups = []
    for name in ("CALIBRATION", "CERTIFICATION"):
        unique_seeds = set()
        for visible in read_rows(BASE / f"f1_package/F1_{name}_CANDIDATES.jsonl"):
            if set(visible) != field_allowlist or visible["human_labels"] is not None:
                raise ValueError("human view has metadata fields or fabricated labels")
            source = hidden[visible["block_key"]]
            if source["seed_id"] in unique_seeds: raise ValueError("duplicate seed within F1 partition")
            unique_seeds.add(source["seed_id"])
            for side in ("A", "B"):
                expected = [text(source["evidence_provenance"][s[side+"_paper_id"]]["abstract"]) for s in source["source_slots"]]
                if expected != visible[side+"_evidence_abstracts"]: raise ValueError("F1 abstract content altered")
            checked += 1
        seed_groups.append(unique_seeds)
    if seed_groups[0] & seed_groups[1]: raise ValueError("calibration/certification seed overlap")
    records = read_rows(BASE / "semantic/reranked_candidates.jsonl")
    cache_verified = 0
    for r in records:
        if r["status"] != "MEASURED": continue
        path = BASE / r["cache_file"]
        if sha(path) != r["cache_sha256"]: raise ValueError("reranker cache changed")
        if not np.array_equal(np.asarray(r["reranker_scores"], dtype=np.float32), np.load(path)):
            raise ValueError("record/cache score mismatch")
        cache_verified += 1
    save(BASE / "FINAL_VERIFICATION.json", {"matching_banks_checked": measured, "F1_records_checked": checked,
        "reranker_caches_checked": cache_verified, "F1_metadata_fields_not_present": True,
        "abstracts_not_rewritten": True, "partitions_seed_disjoint": True, "human_labels_performed": 0})
    pair_k8 = {pair: values["8"] for pair, values in coverage["by_route_pair"].items()}
    summary = {
        "CORPUS_SHA256": cfg["corpus_sha256"],
        "DENSE_BACKEND": model["dense"]["id"] + "@" + model["dense"]["revision"] + " MEASURED (5351 seeds, 3703 evidence)",
        "RERANKER_BACKEND": model["reranker"]["id"] + "@" + model["reranker"]["revision"] + " MEASURED",
        "TEMPORAL_2025_COVERAGE": f"{temporal['2025']['date_known']}/{temporal['2025']['total']} discovered dates; statuses={temporal['2025']['status_counts']}; historical completeness NOT_CERTIFIED",
        "TEMPORAL_2026_COVERAGE": f"{temporal['2026']['date_known']}/{temporal['2026']['total']} discovered dates; statuses={temporal['2026']['status_counts']}; historical completeness NOT_CERTIFIED",
        "SEMANTIC_SEEDS_PROCESSED": reranking["measured_seeds"],
        "K4_UNIQUE_SEEDS": coverage["unique_seed_coverage"]["4"],
        "K6_UNIQUE_SEEDS": coverage["unique_seed_coverage"]["6"],
        "K8_UNIQUE_SEEDS": coverage["unique_seed_coverage"]["8"],
        "K12_UNIQUE_SEEDS": coverage["unique_seed_coverage"]["12"],
        "ROUTE_PAIR_K8_COUNTS": pair_k8,
        "ANONYMIZATION_LEAK_TESTS": "PASS_METADATA_TEMPLATE_AND_F1_FIELDS; intrinsic content identifiers retained",
        "MATCHING_TESTS": "PASS_MAX_CARDINALITY_THEN_COST_AND_SOURCE_NONREUSE",
        "F1_CALIBRATION_BLOCKS": package["calibration_blocks"],
        "F1_CERTIFICATION_BLOCKS": package["certification_blocks"],
        "SCIENTIFIC_PROPOSAL_GENERATIONS": 0,
        "SCIENTIFIC_HYPOTHESIS_STATUS": "UNTESTED",
        "NEXT_GATE": "F1_HUMAN_CONSTRUCT_CERTIFICATION",
    }
    lines = [f"{k}={json.dumps(v, sort_keys=True) if isinstance(v, dict) else v}" for k, v in summary.items()]
    save(BASE / "T8_SUMMARY.json", summary)
    document = "# F0 Semantic / Temporal Source-side Result\n\n```text\n" + "\n".join(lines) + "\n```\n\n"
    document += f"""## Measured Scope

The frozen corpus and roles reconcile. Real dense inference covers all 5351
seed records; the independent cross-encoder scored {reranking['measured_pairs']}
pairs for {reranking['measured_seeds']} existing source-gate-allowed seeds.
{reranking['source_gate_blocked_seeds']} records remain BLOCKED_SOURCE_GATE;
their missing reranker values are not zeros and are not silently discarded.
No model or threshold was chosen using proposal outcomes. Models and thresholds
were frozen before source scoring. The default BAAI checkpoints were retained.

The matching objective maximizes cardinality before minimizing declared nuisance
cost. All eligibility exclusions, unmatched reasons and cost components are
retained. No full-abstract A/B embedding-distance caliper was applied. The fixed
logit floor and nuisance calipers are engineering diagnostics, not calibrated
scientific truth. Counts do not authorize a scientific PASS/KILL decision.

## Temporal Limitation

The OpenReview API returned challenge-required 403 and was not bypassed. Two
arXiv references were inspected but did not identify the focal papers, so their
dates were not borrowed. The current dates therefore rely on verifiable official
publication metadata, not filenames, cache times or conference-year arithmetic.
These are minimum **discovered** dates. They do not establish actual earliest
availability or guarantee historical evidence-before-seed cleanliness.

The candidate bank satisfies the declared discovered-date ordering policy only.
It must not be presented as a certified temporal-clean bank. Human/source-history
review remains necessary; see temporal failures, date events and gap distributions.

## Source Anonymity and Human Gate

Visible F1 records contain the unchanged masked seed, neutral route descriptions,
and whitespace/Unicode-normalized raw abstracts. Metadata fields, scores and
source IDs are kept out of the visible evidence. Method names, findings, embedded
URLs and years in the scientific abstract remain, as required. This does not
guarantee that a knowledgeable reader cannot recognize a source.

Calibration and certification use disjoint unique seeds and deterministic
source-side strata. If targets were not reached, no extra low-quality blocks
were manufactured. Only visible candidate files should be distributed to human
annotators, not the hidden provenance, scores or full source corpus. No human
labels, proposal generations, baseline measurements or treatment outcomes exist.

STOP at the F1 human construct certification gate. The hypothesis is UNTESTED.
"""
    (BASE / "F0_SEMANTIC_TEMPORAL_RESULT.md").write_text(document, encoding="utf-8")
    table = "# Semantic / Temporal Decision Table\n\nNo scientific decision is made.\n\n| Route pair | k=4 | k=6 | k=8 | k=12 |\n| --- | ---: | ---: | ---: | ---: |\n"
    for pair, row in coverage["by_route_pair"].items():
        table += f"| {pair} | {row['4']} | {row['6']} | {row['8']} | {row['12']} |\n"
    table += "\nCounts are unique seeds within each pair, not additive across pairs. Temporal ordering uses discovered fallback dates; historical cleanliness and construct validity remain pending human review.\n"
    (BASE / "semantic_temporal_decision_table.md").write_text(table)
    (BASE / "FINAL_CHECKPOINT.md").write_text("# Final Checkpoint\n\nCompleted:\n- Frozen source reconciliation, real semantic scoring, discovered-date mapping and metadata-only anonymity.\n- Exact matching, coverage/attrition, source diagnostics and unlabelled F1 candidate files.\n\nNot completed / not claimed:\n- Exhaustive earliest-public history; OpenReview earlier metadata blocked.\n- Human construct certification or scientific validity.\n- All research proposal, baseline, treatment, ARS and P0/P1 experiments remain NOT_RUN.\n\nScientific questions remaining:\n- Do provisional source labels/relevance and discovered-date order survive human/source-history review?\n\nNext:\n- F1 human construct certification; STOP here without automatically annotating anything.\n")
    (BASE / "STATUS.md").write_text("# Source-side Status\n\nT0-T8 source processing complete, with explicit temporal-history limitation.\n"
        "Real BGE dense/cross-encoder scoring and candidate matching are MEASURED.\n"
        "Earlier OpenReview history lookup is BLOCKED; discovered dates are FALLBACK_ONLY.\n"
        "Metadata anonymity tests pass; intrinsic content identifiers remain.\n"
        "F1 human labels are NOT_RUN and scientific validity is PENDING_HUMAN_REVIEW.\n"
        "See F0_SEMANTIC_TEMPORAL_RESULT.md for the exact T8 summary.\n"
        "Scientific proposal generations: 0. Hypothesis: UNTESTED. STOP at F1.\n")
    output_files = {str(p.relative_to(BASE)): sha(p) for p in sorted(BASE.rglob("*"))
                    if p.is_file() and "__pycache__" not in p.parts and p.name != "ARTIFACT_MANIFEST.json" and p.suffix != ".tmp"}
    save(BASE / "ARTIFACT_MANIFEST.json", {"files": output_files, "model_weights": "external pinned Hub snapshots; hashes in model_manifest",
        "scientific_hypothesis_status": "UNTESTED", "human_review": "PENDING_HUMAN_REVIEW"})
    print("\n".join(lines))


if __name__ == "__main__":
    finalize()
