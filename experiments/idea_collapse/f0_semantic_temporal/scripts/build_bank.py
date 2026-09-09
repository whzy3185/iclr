"""T3/T5-T8 source-only diagnostics, exact matching and unlabelled F1 packets."""

import csv
from collections import Counter, defaultdict
from datetime import date
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import sys

import numpy as np
from scipy.stats import spearmanr
from transformers import AutoTokenizer

from common import BASE, RECOVERY, encode, hash_value, read_rows, render_evidence, save, sha, text
sys.path.insert(0, str(RECOVERY / "scripts"))
from recovery_algorithms import exact_matching


def percentile(values):
    order = np.argsort(-np.asarray(values), kind="stable")
    result = np.empty(len(order), dtype=float)
    result[order] = np.arange(len(order)) / max(1, len(order)-1)
    return result


def date_gap(later, earlier):
    if later is None or earlier is None:
        return None
    return (date.fromisoformat(later) - date.fromisoformat(earlier)).days


def admissible(a, b, cfg):
    dp = abs(a["dense_percentile"] - b["dense_percentile"])
    rp = abs(a["reranker_percentile"] - b["reranker_percentile"])
    ratio = max(a["tokens"], b["tokens"]) / max(1, min(a["tokens"], b["tokens"]))
    gap = abs(date_gap(a["date"], b["date"])) if a["date"] is not None and b["date"] is not None else None
    reasons = []
    if dp > cfg["dense_percentile_gap_max"]: reasons.append("DENSE_RELEVANCE_GAP")
    if rp > cfg["reranker_percentile_gap_max"]: reasons.append("RERANKER_RELEVANCE_GAP")
    if ratio > cfg["token_ratio_max"]: reasons.append("TOKEN_LENGTH_GAP")
    if gap is None: reasons.append("MISSING_DATE")
    elif gap > cfg["evidence_date_pair_gap_days_max"]: reasons.append("DATE_GAP")
    components = [dp, rp, abs(math.log(ratio)), gap]
    cost = round(1_000_000 * (dp + rp + components[2] + gap/365)) if not reasons else None
    return cost, components, reasons


def source_stratum(block):
    score = block["mean_reranker_score"]
    strength = "0_to_2" if score < 2 else "2_to_4" if score < 4 else "above_4"
    cost = block["mean_cost_units"] / 1_000_000
    difficulty = "low" if cost < .2 else "medium" if cost < .5 else "high"
    return (block["route_pair"], block["topic"], strength, difficulty, block["lexical_disagreement"])


def choose_f1(blocks, target, calibration):
    groups = defaultdict(list)
    for block in blocks:
        in_calibration = int(hash_value(block["seed_id"]), 16) % 5 == 0
        if in_calibration == calibration and block["max_matched_slots"] >= 4:
            groups[source_stratum(block)].append(block)
    for key in groups:
        groups[key].sort(key=lambda b: hash_value([b["seed_id"], b["route_pair"]]))
    topic_keys = defaultdict(list)
    for key in sorted(groups, key=str):
        topic_keys[key[:2]].append(key)
    route_topics = defaultdict(list)
    for route, topic in sorted(topic_keys):
        route_topics[route].append(topic)
    topic_cursors, stratum_cursors = Counter(), Counter()
    chosen, used = [], set()
    while len(chosen) < target:
        advanced = False
        for route in sorted(route_topics):
            topics = route_topics[route]
            picked = False
            for _ in range(len(topics)):
                topic = topics[topic_cursors[route] % len(topics)]
                topic_cursors[route] += 1
                keys = topic_keys[route, topic]
                for _ in range(len(keys)):
                    key = keys[stratum_cursors[route, topic] % len(keys)]
                    stratum_cursors[route, topic] += 1
                    while groups[key] and groups[key][0]["seed_id"] in used:
                        groups[key].pop(0)
                    if groups[key]:
                        b = groups[key].pop(0)
                        chosen.append(b)
                        used.add(b["seed_id"])
                        advanced = picked = True
                        break
                if picked: break
            if len(chosen) == target: break
        if not advanced: break
    return chosen


def build(args):
    cfg = json.loads((BASE / "config.json").read_text())
    seeds = read_rows(BASE / "seeds.jsonl")
    evidence = read_rows(BASE / "evidence.jsonl")
    ev = {e["paper_id"]: e for e in evidence}
    seedmap = {s["seed_id"]: s for s in seeds}
    time_rows = read_rows(BASE / "temporal/earliest_public_dates.jsonl")
    dates = {r["paper_id"]: r for r in time_rows}
    routes = json.loads((BASE / "route_definitions.json").read_text())
    annotations = {r["paper_id"]: r for r in read_rows(RECOVERY / "runs/F0R-9f61bff4538465a7a96f/source_route_annotations.jsonl.gz")}
    if set(annotations) != set(ev): raise ValueError("route annotation/corpus identity mismatch")
    token_counts = json.loads((BASE / "semantic/reranker_evidence_token_lengths.json").read_text())
    tok = AutoTokenizer.from_pretrained(args.reranker_path, local_files_only=True, trust_remote_code=False)
    seed_token_counts = {s["seed_id"]: len(ids) for s, ids in zip(seeds, tok([text(s["method_masked_question"]) for s in seeds], truncation=False)["input_ids"])}
    lexical = defaultdict(dict)
    lex_path = RECOVERY / "runs/F0R-9f61bff4538465a7a96f/retrieval_candidates.csv.gz"
    if lex_path.exists():
        with gzip.open(lex_path, "rt") as f:
            for r in csv.DictReader(f):
                lexical[r["seed_id"]][r["paper_id"]] = (float(r["lexical_cosine"]), int(r["rank"]))
    reranked_path = BASE / "semantic/reranked_candidates.jsonl"
    if not reranked_path.exists(): raise RuntimeError("complete T2 reranking is required; no partial bank is substituted")
    reranked = read_rows(reranked_path)
    if {r["seed_id"] for r in reranked} != set(seedmap): raise ValueError("missing T2 seed records")
    measured = [r for r in reranked if r["status"] == "MEASURED"]
    if len(measured) != sum(s["source_matching_allowed"] for s in seeds): raise ValueError("incomplete reranker scope")
    diagnostic, edge_rows, banks, unmatched_rows, source_exclusions, rejected_rows = [], [], [], [], [], []
    stage_counts = Counter()
    gap_counts = Counter()
    audit_candidates = defaultdict(list)
    for r in reranked:
        sid = r["seed_id"]
        seed = seedmap[sid]
        if r["status"] != "MEASURED":
            for pair in routes["pairs"]:
                banks.append({"seed_id": sid, "route_pair": pair, "status": "BLOCKED_SOURCE_GATE", "max_matched_slots": None, "slots": []})
            stage_counts["blocked_seed_gate"] += 1
            continue
        ids, scores, logits = r["paper_ids"], r["dense_scores"], r["reranker_scores"]
        if not len(ids) == len(scores) == len(logits) == cfg["candidate_k"]: raise ValueError("candidate lengths mismatch")
        if seed["focal_paper_id"] in ids or any(ev[i]["year"] != 2025 for i in ids): raise ValueError("evidence role contamination")
        dp, rp = percentile(scores), percentile(logits)
        rank_agreement = float(spearmanr(scores, logits).statistic)
        if not math.isfinite(rank_agreement): rank_agreement = None
        old = lexical.get(sid, {})
        old_top = {i for i, (value, rank) in old.items() if rank <= 20}
        overlap = len(old_top & set(ids[:20])) / 20 if old_top else None
        seed_date = dates[seed["focal_paper_id"]]["earliest_public_date"]
        candidates, excluded, candidate_date_gaps = [], [], []
        for index, pid in enumerate(ids):
            label = annotations[pid]
            value = dates[pid]["earliest_public_date"]
            gap = date_gap(value, seed_date)
            candidate_date_gaps.append(gap)
            if gap is None: gap_counts["UNKNOWN"] += 1
            else: gap_counts[str(gap)] += 1
            reasons = []
            if logits[index] < cfg["matching"]["reranker_logit_floor"]: reasons.append("BELOW_FIXED_RERANKER_FLOOR")
            if gap is None: reasons.append("MISSING_PUBLIC_DATE")
            elif gap > 0: reasons.append("EVIDENCE_DISCOVERED_DATE_AFTER_SEED")
            if label["route_purity_descriptor"] != "ROUTE_CLEAR": reasons.append("PROVISIONAL_ROUTE_NOT_CLEAR")
            if reasons:
                excluded.append({"paper_id": pid, "reasons": reasons})
            else:
                candidates.append({"id": pid, "route": label["primary_route"], "dense_percentile": float(dp[index]),
                    "reranker_percentile": float(rp[index]), "tokens": token_counts[pid], "date": value,
                    "logit": logits[index], "dense": scores[index]})
            disagreement = "high_lexical_low_semantic" if pid in old_top and logits[index] < 0 else "low_lexical_high_semantic" if old and pid not in old_top and logits[index] >= 2 else "ordinary"
            key = (disagreement, "positive" if logits[index] >= 0 else "negative")
            candidate = {"seed_id": sid, "paper_id": pid, "dense_score": scores[index], "reranker_score": logits[index],
                "lexical_score": old.get(pid, (None, None))[0], "stratum": disagreement}
            audit_candidates[key].append(candidate)
        stage_counts["reranker_measured_seeds"] += 1
        source_exclusions.append({"seed_id": sid, "excluded_sources": excluded})
        if any(x >= 0 for x in logits): stage_counts["has_semantic_candidates"] += 1
        if candidates: stage_counts["has_semantic_temporal_route_candidates"] += 1
        diagnostic.append({"seed_id": sid, "paper_ids": ids, "dense_scores": scores, "reranker_scores": logits,
            "reranker_ranks": (rp * (len(ids)-1) + 1).round().astype(int).tolist(),
            "lexical_scores": [old.get(i, (None, None))[0] for i in ids], "lexical_dense_overlap_at_20": overlap,
            "dense_reranker_spearman": rank_agreement, "seed_token_length": seed_token_counts[sid],
            "evidence_token_lengths": [token_counts[i] for i in ids],
            "title_free_abstract_hashes": [hashlib.sha256(text(ev[i]["abstract"]).encode()).hexdigest() for i in ids],
            "seed_date": seed_date, "evidence_dates": [dates[i]["earliest_public_date"] for i in ids],
            "evidence_minus_seed_days": candidate_date_gaps, "temporal_interpretation": "discovered dates; fallback-only history remains unresolved"})
        for pair, (route_a, route_b) in routes["pairs"].items():
            left = sorted([c for c in candidates if c["route"] == route_a], key=lambda c: c["id"])
            right = sorted([c for c in candidates if c["route"] == route_b], key=lambda c: c["id"])
            edges, components, rejected = [], {}, []
            compact = []
            for ai, a in enumerate(left):
                for bi, b in enumerate(right):
                    cost, features, reasons = admissible(a, b, cfg["matching"])
                    if reasons:
                        rejected.append([ai, bi, reasons])
                    else:
                        edges.append((a["id"], b["id"], cost))
                        components[a["id"], b["id"]] = features
                        compact.append([ai, bi, cost, *features])
            chosen = exact_matching(edges)
            used = {x for a, b, cost in chosen for x in (a, b)}
            has_edge = {x for a, b, cost in edges for x in (a, b)}
            edge_rows.append({"seed_id": sid, "route_pair": pair, "status": "MEASURED", "A_ids": [c["id"] for c in left],
                "B_ids": [c["id"] for c in right], "edge_fields": ["A_index", "B_index", "cost_units", "dense_percentile_gap", "reranker_percentile_gap", "abs_log_length_ratio", "evidence_date_gap_days"],
                "eligible_edges": compact, "rejected_edges_reference": "rejected_edges.jsonl.gz:"+sid+":"+pair,
                "source_exclusions_reference": sid})
            rejected_rows.append({"seed_id": sid, "route_pair": pair, "rows": rejected,
                                  "indices_reference": "eligible_edges.jsonl A_ids/B_ids"})
            unmatched_rows.append({"seed_id": sid, "route_pair": pair,
                "rows": [[side, i, 2 if c["id"] in has_edge else 1] for side, pool in [("A", left), ("B", right)]
                         for i, c in enumerate(pool) if c["id"] not in used],
                "schema": ["side", "candidate_index", "reason_code"],
                "indices_reference": "eligible_edges.jsonl A_ids/B_ids",
                "reason_codes": {"1": "NO_ADMISSIBLE_EDGE", "2": "CAPACITY_COMPETITION"}})
            bank = {"seed_id": sid, "route_pair": pair, "status": "MEASURED", "max_matched_slots": len(chosen),
                "slots": [{"A_paper_id": a, "B_paper_id": b, "cost_units": cost, "cost_components": components[a,b]} for a,b,cost in chosen],
                "mean_cost_units": statistics.mean(c for a,b,c in chosen) if chosen else None,
                "mean_reranker_score": statistics.mean(c["logit"] for c in left+right if c["id"] in used) if chosen else None,
                "topic": seed["subfield"], "lexical_disagreement": "UNKNOWN" if overlap is None else str(overlap < cfg["f1"]["lexical_disagreement_overlap_cut"]),
                "source_gate_flags": seed["risk_flags"], "human_certification": "PENDING_HUMAN_REVIEW",
                "temporal_scope": "DISCOVERED_DATE_ORDER_ONLY; earliest histories unverified"}
            banks.append(bank)
    def compressed_rows(path, rows):
        raw = gzip.compress(b"".join(encode(row) for row in rows), mtime=0)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if path.read_bytes() != raw: raise ValueError("compressed replay differs")
        else:
            path.write_bytes(raw)
    compressed_rows(BASE / "semantic/relevance_diagnostics.jsonl.gz", diagnostic)
    compressed_rows(BASE / "matching/source_exclusions.jsonl.gz", source_exclusions)
    compressed_rows(BASE / "matching/rejected_edges.jsonl.gz", rejected_rows)
    save(BASE / "temporal/evidence_minus_seed_distribution.json", {"candidate_pairs": sum(gap_counts.values()), "day_gaps": dict(gap_counts),
        "note": "actual differences of discovered source date fields, not conference-year subtraction"})
    audit = []
    for key, values in sorted(audit_candidates.items()):
        for row in sorted(values, key=lambda r: hash_value([r["seed_id"],r["paper_id"]]))[:20]:
            audit.append({**row, "seed": seedmap[row["seed_id"]]["method_masked_question"], "source_abstract": text(ev[row["paper_id"]]["abstract"]),
                          "purpose": "DEVELOPMENT_ONLY", "human_relevance": None, "human_notes": None})
    save(BASE / "semantic/development_relevance_audit.jsonl", audit, rows=True)
    ds = [x for d in diagnostic for x in d["dense_scores"]]
    rs = [x for d in diagnostic for x in d["reranker_scores"]]
    save(BASE / "semantic/relevance_summary.json", {"dense_quantiles": np.quantile(ds,[0,.1,.5,.9,1]).tolist(),
        "reranker_quantiles": np.quantile(rs,[0,.1,.5,.9,1]).tolist(),
        "rank_correlations": [d["dense_reranker_spearman"] for d in diagnostic],
        "lexical_comparison": "prior title+abstract TF-IDF; new dense is abstract-only; disagreement is not accuracy evidence",
        "stage_counts": dict(stage_counts), "human_labels_performed": 0})
    save(BASE / "matching/eligible_edges.jsonl", edge_rows, rows=True)
    save(BASE / "matching/matched_slots.jsonl", banks, rows=True)
    save(BASE / "matching/unmatched_rows.jsonl", unmatched_rows, rows=True)
    save(BASE / "matching/matching_manifest.json", {"config": cfg["matching"], "config_sha256": sha(BASE / "config.json"),
        "matched_file_sha256": sha(BASE / "matching/matched_slots.jsonl"), "model_manifest_sha256": sha(BASE / "semantic/model_manifest.json"),
        "source_code_sha256": sha(__file__), "date_map_sha256": sha(BASE / "temporal/earliest_public_dates.jsonl"),
        "reranked_candidates_sha256": sha(BASE / "semantic/reranked_candidates.jsonl"),
        "route_annotation_sha256": sha(RECOVERY / "runs/F0R-9f61bff4538465a7a96f/source_route_annotations.jsonl.gz"),
        "objective": "maximum cardinality first, minimum declared integer nuisance cost second; no global abstract-pair embedding caliper",
        "scope": "candidate banks, not certified relevance or true historical cleanliness", "human_certification": "PENDING_HUMAN_REVIEW"})
    measured_banks = [b for b in banks if b["status"] == "MEASURED"]
    coverage = {str(k): len({b["seed_id"] for b in measured_banks if b["max_matched_slots"] >= k}) for k in (4,6,8,12)}
    by_pair = {pair: {str(k): len({b["seed_id"] for b in measured_banks if b["route_pair"] == pair and b["max_matched_slots"] >= k}) for k in (4,6,8,12)} for pair in routes["pairs"]}
    save(BASE / "matching/coverage.json", {"unique_seed_coverage": coverage, "by_route_pair": by_pair,
        "measured_zero_blocks": sum(b["max_matched_slots"] == 0 for b in measured_banks),
        "blocked_blocks": len(banks)-len(measured_banks), "interpretation": "within frozen source-score and discovered-date policy"})
    chosen_cal = choose_f1(measured_banks, cfg["f1"]["calibration_target_unique_seeds"], True)
    chosen_cert = choose_f1(measured_banks, cfg["f1"]["certification_target_unique_seeds"], False)
    hidden = []
    for label, selected in [("CALIBRATION", chosen_cal), ("CERTIFICATION", chosen_cert)]:
        visible = []
        for b in selected:
            key = hash_value([label, b["seed_id"], b["route_pair"]])[:24]
            a_route, b_route = routes["pairs"][b["route_pair"]]
            sample = b["slots"][:4]
            a_text = [text(ev[s["A_paper_id"]]["abstract"]) for s in sample]
            b_text = [text(ev[s["B_paper_id"]]["abstract"]) for s in sample]
            visible.append({"block_key": key, "method_masked_seed": seedmap[b["seed_id"]]["method_masked_question"],
                "route_A_description": routes["definitions"][a_route], "route_B_description": routes["definitions"][b_route],
                "A_evidence_abstracts": a_text, "B_evidence_abstracts": b_text, "human_labels": None,
                "status": "PENDING_HUMAN_REVIEW"})
            hidden.append({"block_key": key, "seed_id": b["seed_id"], "route_pair": b["route_pair"], "partition": label,
                "stratum": list(source_stratum(b)), "source_slots": sample, "provisional_seed_flags": b["source_gate_flags"],
                "temporal_scope": b["temporal_scope"], "evidence_provenance": {pid: ev[pid] for s in sample for pid in (s["A_paper_id"],s["B_paper_id"])}})
        save(BASE / f"f1_package/F1_{label}_CANDIDATES.jsonl", visible, rows=True)
    if {b["seed_id"] for b in chosen_cal} & {b["seed_id"] for b in chosen_cert}: raise ValueError("F1 seed partitions overlap")
    save(BASE / "f1_package/F1_HIDDEN_PROVENANCE.jsonl", hidden, rows=True)
    save(BASE / "f1_package/F1_PACKAGE_MANIFEST.json", {"calibration_blocks": len(chosen_cal), "certification_blocks": len(chosen_cert),
        "calibration_unique_seeds": len({b["seed_id"] for b in chosen_cal}), "certification_unique_seeds": len({b["seed_id"] for b in chosen_cert}),
        "selection": cfg["f1"], "source_outcomes_only": True, "scientific_generator_outcomes": 0,
        "human_labels": "NOT_RUN", "scientific_validity": "PENDING_HUMAN_REVIEW", "target_is_not_guaranteed": True})
    attrition = [{"stage": "all_2026_seeds", "count": len(seeds), "unit": "unique_seed", "reason": "official source universe"},
        {"stage": "method_masked_records", "count": len(seeds), "unit": "unique_seed", "reason": "existing transform; all records retained"},
        {"stage": "source_gate_allowed", "count": len(measured), "unit": "unique_seed", "reason": "explicit solution/structural gates, not model-output selection"},
        {"stage": "has_reranker_positive_candidate", "count": stage_counts["has_semantic_candidates"], "unit": "unique_seed", "reason": "fixed logit>=0 diagnostic, not validated truth"},
        {"stage": "has_semantic_temporal_route_candidate", "count": stage_counts["has_semantic_temporal_route_candidates"], "unit": "unique_seed", "reason": "known discovered-date order and preserved provisional route filter"},
        *[{"stage": f"matched_k{k}", "count": coverage[str(k)], "unit": "unique_seed", "reason": "declared nuisance calipers and exact matching"} for k in (4,6,8,12)]]
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(attrition[0]), lineterminator="\n")
    writer.writeheader();writer.writerows(attrition)
    path = BASE / "attrition_waterfall.csv"
    raw = stream.getvalue().encode()
    if path.exists():
        if path.read_bytes() != raw: raise ValueError("attrition replay differs")
    else:
        path.write_bytes(raw)
    print(json.dumps({"coverage": coverage, "by_pair": by_pair, "F1_calibration": len(chosen_cal), "F1_certification": len(chosen_cert)}, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reranker-path", type=Path, required=True)
    build(parser.parse_args())
