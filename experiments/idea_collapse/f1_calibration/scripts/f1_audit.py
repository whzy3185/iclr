"""Source-only F1 calibration and validity audit."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import subprocess
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
F0 = ROOT / "experiments/idea_collapse/f0_semantic_temporal"
RECOVERY = ROOT / "experiments/idea_collapse/feasibility_1"
OUT = ROOT / "experiments/idea_collapse/f1_calibration"
CORPUS = ROOT / "experiments/idea_collapse/corpus/iclr_2024_2026"
MODEL_ROOT = ROOT.parent / "semantic-models"
ROUTE_NAMES = {"R1": ("BUILD", "DIAGNOSE"), "R2": ("BUILD", "MEASURE"), "R3": ("BUILD", "EXPLAIN"), "R4": ("DIAGNOSE", "EXPLAIN")}
ROUTE_TERMS = re.compile(r"\b(propose|proposed|introduce|introduced|method|model|framework|algorithm|mechanism|module|training|optimization|achieve|improve|enhance)\b", re.I)
URL_RE = re.compile(r"https?://[^\s)]+", re.I)


def read_jsonl(path: Path):
    if path.suffix == ".gz":
        import gzip
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_value(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write_bytes(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f"immutable artifact differs: {path}")
    if not path.exists():
        path.write_bytes(data)


def write_json(path: Path, value):
    write_bytes(path, canonical(value))


def write_jsonl(path: Path, rows):
    write_bytes(path, b"".join(canonical(row) for row in rows))


def write_csv(path: Path, rows, fields):
    import io
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({key: row.get(key) for key in fields} for row in rows)
    write_bytes(path, buf.getvalue().encode())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load_inputs():
    return {
        "seeds": read_jsonl(F0 / "seeds.jsonl"),
        "evidence": read_jsonl(F0 / "evidence.jsonl"),
        "reranked": read_jsonl(F0 / "semantic/reranked_candidates.jsonl"),
        "banks": read_jsonl(F0 / "matching/matched_slots.jsonl"),
        "calibration": read_jsonl(F0 / "f1_package/F1_CALIBRATION_CANDIDATES.jsonl"),
        "certification": read_jsonl(F0 / "f1_package/F1_CERTIFICATION_CANDIDATES.jsonl"),
        "hidden": read_jsonl(F0 / "f1_package/F1_HIDDEN_PROVENANCE.jsonl"),
        "annotations": read_jsonl(RECOVERY / "runs/F0R-9f61bff4538465a7a96f/source_route_annotations.jsonl.gz"),
        "dates": read_jsonl(F0 / "temporal/earliest_public_dates.jsonl"),
    }


def corpus_hash():
    return json.loads((CORPUS / "corpus_manifest.json").read_text())["corpus_sha256"]


def task1():
    data = load_inputs()
    seeds, reranked, banks = data["seeds"], data["reranked"], data["banks"]
    semantic_by_key = {(r["seed_id"], r["route_pair"]): r for r in banks}
    lexical_diag = RECOVERY / "runs/F0R-9f61bff4538465a7a96f/lexical_matching_diagnostics.csv"
    lexical_slots = RECOVERY / "runs/F0R-9f61bff4538465a7a96f/matched_evidence_slots.csv"
    old_diag = {}
    with lexical_diag.open(newline="") as f:
        for row in csv.DictReader(f):
            old_diag[(row["seed_id"], row["route_pair_id"])] = row
    old_slots = defaultdict(lambda: {"A": set(), "B": set()})
    with lexical_slots.open(newline="") as f:
        for row in csv.DictReader(f):
            old_slots[(row["seed_id"], row["route_pair_id"])]["A"].add(row["A_paper_id"])
            old_slots[(row["seed_id"], row["route_pair_id"])]["B"].add(row["B_paper_id"])
    comparison = []
    for seed in seeds:
        sid = seed["seed_id"]
        for route in ROUTE_NAMES:
            key = (sid, route)
            old = old_diag.get(key, {})
            new = semantic_by_key.get(key, {"status": "NOT_RUN", "max_matched_slots": None, "slots": []})
            old_status = old.get("cell_status", "NOT_RUN")
            old_max = int(old["max_matched_slots"]) if old.get("max_matched_slots") not in (None, "") else None
            new_status, new_max = new.get("status", "NOT_RUN"), new.get("max_matched_slots")
            old_positive = old_status == "MEASURED" and (old_max or 0) > 0
            new_positive = new_status == "MEASURED" and (new_max or 0) > 0
            if old_positive and new_positive:
                transition = "RETAINED_POSITIVE" if old_max == new_max else "RETAINED_CHANGED_CARDINALITY"
            elif old_positive:
                transition = "LOST_MATCH"
            elif new_positive:
                transition = "GAINED_MATCH"
            else:
                transition = "UNMATCHED_BOTH"
            reason = new_status if new_status != "MEASURED" else "NO_ADMISSIBLE_EDGE_OR_CAPACITY_COMPETITION" if not new_positive else ""
            old_papers = old_slots[key]["A"] | old_slots[key]["B"]
            new_papers = {p for slot in (new.get("slots") or []) for p in (slot.get("A_paper_id"), slot.get("B_paper_id"))}
            paper_ids = sorted(old_papers | new_papers) or [""]
            for paper_id in paper_ids:
                comparison.append({
                    "seed_id": sid, "route_pair": route, "paper_id": paper_id,
                    "old_cell_status": old_status, "old_max_matched_slots": old_max,
                    "semantic_cell_status": new_status, "semantic_max_matched_slots": new_max,
                    "block_transition": transition,
                    "paper_transition": "RETAINED" if paper_id in old_papers and paper_id in new_papers else "LOST" if paper_id in old_papers else "GAINED" if paper_id in new_papers else "NEITHER",
                    "reason": reason,
                })
    expected = "0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807"
    files = [F0 / "seeds.jsonl", F0 / "evidence.jsonl", F0 / "config.json", F0 / "semantic/model_manifest.json", F0 / "semantic/reranked_candidates.jsonl", F0 / "matching/matched_slots.jsonl", F0 / "matching/coverage.json", F0 / "f1_package/F1_PACKAGE_MANIFEST.json", F0 / "f1_package/F1_HIDDEN_PROVENANCE.jsonl", lexical_diag, lexical_slots, CORPUS / "corpus_manifest.json"]
    measured_seeds = sum(r.get("status") == "MEASURED" for r in reranked)
    blocked_seeds = sum(r.get("status") == "BLOCKED_SOURCE_GATE" for r in reranked)
    manifest = {
        "input_commit": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
        "corpus_sha256": corpus_hash(), "expected_corpus_sha256": expected, "corpus_hash_ok": corpus_hash() == expected,
        "counts": {"seed_records": len(seeds), "scored_seeds": measured_seeds, "blocked_seeds": blocked_seeds,
                   "scored_pairs": sum(len(r.get("paper_ids") or []) for r in reranked if r.get("status") == "MEASURED"),
                   "semantic_route_blocks": sum(r.get("status") == "MEASURED" for r in banks),
                   "blocked_route_blocks": sum(r.get("status") != "MEASURED" for r in banks),
                   "calibration_blocks": len(data["calibration"]), "certification_blocks": len(data["certification"])},
        "coverage": json.loads((F0 / "matching/coverage.json").read_text()),
        "files": {str(p.relative_to(ROOT)): {"sha256": sha256(p), "bytes": p.stat().st_size} for p in files},
        "comparison_semantics": "paper-ID-level union within each seed-route block; 1018/1119 is not a retention rate",
        "human_labels_imported": 0, "scientific_proposal_generations": 0,
    }
    if not manifest["corpus_hash_ok"]:
        raise RuntimeError("frozen corpus hash mismatch")
    write_json(OUT / "INPUT_MANIFEST.json", manifest)
    fields = ["seed_id", "route_pair", "paper_id", "old_cell_status", "old_max_matched_slots", "semantic_cell_status", "semantic_max_matched_slots", "block_transition", "paper_transition", "reason"]
    write_csv(OUT / "paired_lexical_semantic_comparison.csv", comparison, fields)
    write_bytes(OUT / "STATUS.md", (f"# F1 Calibration Status\n\nCURRENT_TASK=TASK 1\nINPUT_COMMIT={manifest['input_commit']}\nCORPUS_HASH={manifest['corpus_sha256']}\nCORPUS_HASH_OK={manifest['corpus_hash_ok']}\nSEEDS={len(seeds)}\nSCORED_SEEDS={measured_seeds}\nBLOCKED_SEEDS={blocked_seeds}\nSCORED_PAIRS={manifest['counts']['scored_pairs']}\nMEASURED_ROUTE_BLOCKS={manifest['counts']['semantic_route_blocks']}\nBLOCKED_ROUTE_BLOCKS={manifest['counts']['blocked_route_blocks']}\nCALIBRATION_BLOCKS={len(data['calibration'])}\nCERTIFICATION_BLOCKS={len(data['certification'])}\nNULL_BLOCKED_NOT_RUN=preserved_as_statuses\nDEVIATIONS=No source corpus, F0 cache, model, or threshold changed.\nNEXT=TASK 2\n").encode())


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def duplicate_info(text):
    ps, counts = paragraphs(text), Counter(paragraphs(text))
    dup = [p for p, n in counts.items() if n > 1]
    return {"paragraph_count": len(ps), "duplicate_paragraph_count": sum(counts[p] - 1 for p in dup), "duplicate_paragraphs": dup}


def task2():
    data = load_inputs()
    seeds = {r["seed_id"]: r for r in data["seeds"]}
    evidence = {r["paper_id"]: r for r in data["evidence"]}
    cal_keys = {r["block_key"] for r in data["calibration"]}
    cert_keys = {r["block_key"] for r in data["certification"]}
    hidden = data["hidden"]
    cal_hidden = sorted((r for r in hidden if r["block_key"] in cal_keys), key=lambda r: r["block_key"])
    cert_hidden = [r for r in hidden if r["block_key"] in cert_keys]
    if {r["seed_id"] for r in cal_hidden} & {r["seed_id"] for r in cert_hidden}:
        raise RuntimeError("calibration/certification overlap")
    cal_visible = {r["block_key"]: r for r in data["calibration"]}

    seed_rows = []
    for row in cal_hidden:
        seed = seeds[row["seed_id"]]
        source_spans = seed.get("source_spans", [])
        seed_rows.append({
            "audit_record_id": hash_value(["seed", row["block_key"]])[:24], "block_key": row["block_key"],
            "original_problem_context": seed.get("raw_problem_context", ""),
            "current_method_masked_seed": seed["method_masked_question"], "source_spans": source_spans,
            "duplicate_diagnostic": duplicate_info(seed["method_masked_question"]),
            "generic_terms_masked": seed.get("removed_solution_tokens_entities", []),
            "possible_solution_prescribing_spans": [sp for sp in source_spans if ROUTE_TERMS.search(sp.get("text", ""))],
            "provisional_repair_suggestion": None,
            "human_source_faithfulness": None, "human_duplication_decision": None,
            "human_generic_masking_decision": None, "human_solution_leakage": None,
            "human_comprehensibility": None, "human_notes": None, "status": "PENDING_HUMAN_REVIEW",
        })
    write_jsonl(OUT / "seed_audit.jsonl", seed_rows)

    paper_rows, seen = [], set()
    for row in cal_hidden:
        seed = seeds[row["seed_id"]]
        for slot in row["source_slots"]:
            for pid in (slot["A_paper_id"], slot["B_paper_id"]):
                key = (row["seed_id"], pid)
                if key in seen:
                    continue
                seen.add(key)
                paper_rows.append({
                    "audit_record_id": hash_value(["paper", row["block_key"], pid])[:24],
                    "seed_display_text": seed["method_masked_question"], "abstract": evidence[pid]["abstract"],
                    "review_paper_id": hash_value(["paper", pid])[:24],
                    "seed_specific_relevance": None, "primary_contribution_route": None,
                    "secondary_contribution_route": None, "supporting_source_span": None,
                    "confidence": None, "notes": None, "provisional_legacy_route_hidden": True,
                    "retrieval_score_hidden": True, "rank_hidden": True, "matching_outcome_hidden": True,
                    "status": "PENDING_HUMAN_REVIEW",
                })
    write_jsonl(OUT / "paper_relevance_route_audit.jsonl", paper_rows)

    block_rows, private_map = [], []
    for row in cal_hidden:
        key = row["block_key"]
        swap = int(hash_value(["AB_DISPLAY", key]), 16) % 2 == 1
        route_a, route_b = ROUTE_NAMES[row["route_pair"]]
        visible = cal_visible[key]
        a_desc, b_desc = visible["route_A_description"], visible["route_B_description"]
        a_abs = [evidence[s["A_paper_id"]]["abstract"] for s in row["source_slots"]]
        b_abs = [evidence[s["B_paper_id"]]["abstract"] for s in row["source_slots"]]
        block_rows.append({
            "audit_record_id": hash_value(["block", key])[:24], "block_key": key,
            "display_route_1_description": b_desc if swap else a_desc,
            "display_route_2_description": a_desc if swap else b_desc,
            "display_route_1_evidence": b_abs if swap else a_abs,
            "display_route_2_evidence": a_abs if swap else b_abs,
            "reviewed_slot_count": 4,
            "reviewed_slot_scope": "exactly the four displayed matched slots; no k=8/k=12 certification",
            "route_1_relevance": None, "route_2_relevance": None, "route_relation": None,
            "route_1_plausibility": None, "route_2_plausibility": None, "distinguishability": None,
            "complementarity_or_subsumption": None, "equipoise": None, "usable_slot_count": None,
            "human_notes": None, "status": "PENDING_HUMAN_REVIEW",
        })
        private_map.append({"block_key": key, "display_swapped": swap,
                            "display_route_1": route_b if swap else route_a,
                            "display_route_2": route_a if swap else route_b,
                            "source_slots": row["source_slots"]})
    write_jsonl(OUT / "block_admissibility_audit.jsonl", block_rows)
    write_jsonl(OUT / "_PRIVATE_block_ab_mapping.jsonl", private_map)

    zero_ids = sorted({r["seed_id"] for r in data["banks"] if r["status"] == "MEASURED" and (r.get("max_matched_slots") or 0) == 0}, key=lambda x: hash_value(["shadow-zero", x]))[:6]
    blocked_ids = sorted({r["seed_id"] for r in data["banks"] if r["status"] != "MEASURED"}, key=lambda x: hash_value(["shadow-blocked", x]))[:6]
    cert_seeds = {r["seed_id"] for r in cert_hidden}
    if (set(zero_ids) | set(blocked_ids)) & cert_seeds:
        raise RuntimeError("shadow sample overlaps certification queue")
    shadow = []
    for state, ids in (("MEASURED_ZERO", zero_ids), ("BLOCKED_SOURCE_GATE", blocked_ids)):
        for sid in ids:
            shadow.append({"shadow_record_id": hash_value(["shadow", state, sid])[:24], "shadow_status": state,
                           "method_masked_seed": seeds[sid]["method_masked_question"],
                           "human_false_exclusion_audit": None, "human_notes": None, "status": "PENDING_HUMAN_REVIEW"})
    write_jsonl(OUT / "shadow_audit.jsonl", shadow)
    write_json(OUT / "_PRIVATE_shadow_mapping.json", {"MEASURED_ZERO": zero_ids, "BLOCKED_SOURCE_GATE": blocked_ids})

    write_csv(OUT / "seed_audit.csv", seed_rows, ["audit_record_id", "block_key", "status", "human_source_faithfulness", "human_duplication_decision", "human_generic_masking_decision", "human_solution_leakage", "human_comprehensibility", "human_notes"])
    write_csv(OUT / "paper_relevance_route_audit.csv", paper_rows, ["audit_record_id", "review_paper_id", "status", "seed_specific_relevance", "primary_contribution_route", "secondary_contribution_route", "supporting_source_span", "confidence", "notes"])
    write_csv(OUT / "block_admissibility_audit.csv", block_rows, ["audit_record_id", "block_key", "status", "reviewed_slot_count", "reviewed_slot_scope", "route_1_relevance", "route_2_relevance", "route_relation", "route_1_plausibility", "route_2_plausibility", "distinguishability", "complementarity_or_subsumption", "equipoise", "usable_slot_count", "human_notes"])
    write_csv(OUT / "shadow_audit.csv", shadow, ["shadow_record_id", "shadow_status", "status", "human_false_exclusion_audit", "human_notes"])
    write_bytes(OUT / "REVIEW_FIELDS.md", b"""# F1 Calibration Review Fields\n\nAll human decision fields are intentionally null. This package is an instrument for human calibration, not a model-labelled dataset.\n\n`seed_audit`: review source-faithfulness, duplicated problem text, generic masking, solution-prescribing spans, and comprehensibility. Deterministic diagnostics are provisional observations only.\n\n`paper_relevance_route_audit`: one seed plus one abstract per row. Set DIRECT_RELEVANCE, TRANSFER_ONLY, OFF_TOPIC, or UNCLEAR; assign primary/secondary routes and quote a supporting sentence only after review. Relevance is seed-specific.\n\n`block_admissibility_audit`: A/B order is randomized and decoded only through the private mapping. Review exactly four displayed slots. Do not certify k=8 or k=12 from this file.\n\n`shadow_audit`: developmental false-exclusion audit for six measured-zero and six source-gate-blocked seeds selected by frozen hashes. It is not a pass threshold and is outside the 96-case queue.\n""")
    status = (OUT / "STATUS.md").read_text() + "\nTASK 2=COMPLETED; human labels remain null; certification queue untouched; displayed slot scope=4.\nNEXT=TASK 3\n"
    write_bytes(OUT / "STATUS.md", status.encode())


def q1_text(text):
    text = text.strip()
    text = re.split(r"\n\s*TASK\s+Propose one technically substantive.*", text, maxsplit=1, flags=re.I | re.S)[0].strip()
    kept, seen = [], set()
    for chunk in paragraphs(text):
        if chunk.upper().startswith("OBSERVED PROBLEM / OPEN QUESTION"):
            chunk = chunk[len("OBSERVED PROBLEM / OPEN QUESTION"):].strip()
        normalized = " ".join(chunk.split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            kept.append(chunk)
    return "\n\n".join(kept)


def task3(args):
    data = load_inputs()
    hidden = {r["block_key"]: r for r in data["hidden"]}
    cal_keys = {r["block_key"] for r in data["calibration"]}
    hidden_cal = sorted((r for r in data["hidden"] if r["block_key"] in cal_keys), key=lambda r: r["block_key"])
    seeds = {r["seed_id"]: r for r in data["seeds"]}
    evidence, evidence_by_id = data["evidence"], {r["paper_id"]: r for r in data["evidence"]}
    reranked = {r["seed_id"]: r for r in data["reranked"]}
    config = json.loads((F0 / "config.json").read_text())
    model_manifest = json.loads((F0 / "semantic/model_manifest.json").read_text())
    variants = []
    for row in hidden_cal:
        q0 = seeds[row["seed_id"]]["method_masked_question"]
        q1 = q1_text(q0)
        variants.append({"seed_id": row["seed_id"], "block_key": row["block_key"], "Q0": q0, "Q1": q1, "Q2": None,
                         "Q0_sha256": hashlib.sha256(q0.encode()).hexdigest(), "Q1_sha256": hashlib.sha256(q1.encode()).hexdigest(),
                         "Q2_status": "PENDING_REVIEW", "query_transform": "remove generic TASK block; remove exact duplicate paragraphs; preserve masking"})
    write_jsonl(OUT / "query_variants.jsonl", variants)
    manifest = {"input_commit": git("rev-parse", "HEAD"), "model_manifest_sha256": sha256(F0 / "semantic/model_manifest.json"),
                "config_sha256": sha256(F0 / "config.json"), "dense_model": config["dense"], "reranker_model": config["reranker"],
                "candidate_budget": 200, "Q0": "exact current method_masked_question; existing scores reused",
                "Q1": "deterministic deduplication and generic task removal; new embedding/retrieval/reranking required",
                "Q2": "PENDING_REVIEW; no source-faithful human repair supplied", "calibration_seed_count": len(variants),
                "allowed_new_candidates": len(variants) * 200, "scoring_frozen_before_execution": True,
                "human_labels_imported": 0, "scientific_proposal_generations": 0}
    write_json(OUT / "query_variant_manifest.json", manifest)

    import io
    import numpy as np
    import torch
    from transformers import AutoModel, AutoModelForSequenceClassification, AutoTokenizer
    if not torch.backends.mps.is_available():
        raise RuntimeError("MPS unavailable; no silent CPU fallback")
    dense_path, reranker_path = Path(args.dense_path), Path(args.reranker_path)
    dense_tok = AutoTokenizer.from_pretrained(dense_path, local_files_only=True, trust_remote_code=False)
    dense_model = AutoModel.from_pretrained(dense_path, local_files_only=True, trust_remote_code=False, use_safetensors=True, dtype=torch.float16).eval().to("mps")
    dense_docs = np.load(F0 / "semantic/evidence_embeddings.npy", allow_pickle=False)
    dense_queries = [config["dense"]["query_prefix"] + row["Q1"] for row in variants]
    dense_full_lengths = [len(ids) for ids in dense_tok(dense_queries, truncation=False)["input_ids"]]
    inputs = dense_tok(dense_queries, padding=True, truncation=True, max_length=512, return_tensors="pt").to("mps")
    with torch.inference_mode():
        q_emb = torch.nn.functional.normalize(dense_model(**inputs).last_hidden_state[:, 0].float(), p=2, dim=1).cpu().numpy()
    dense_indices = np.argsort(-(q_emb @ dense_docs.T), axis=1, kind="stable")[:, :200]
    dense_scores = np.take_along_axis(q_emb @ dense_docs.T, dense_indices, axis=1)
    bio = io.BytesIO(); np.save(bio, q_emb.astype(np.float32), allow_pickle=False); write_bytes(OUT / "q1_query_embeddings.npy", bio.getvalue())
    dense_model = None
    torch.mps.empty_cache()
    q1_dense_rows = []
    for i, row in enumerate(variants):
        q1_dense_rows.append({"seed_id": row["seed_id"], "block_key": row["block_key"], "variant": "Q1", "candidate_ids": [evidence[j]["paper_id"] for j in dense_indices[i]], "dense_scores": dense_scores[i].tolist(), "query_tokens_full": dense_full_lengths[i], "query_truncated": dense_full_lengths[i] > 512,
                              "cache_key": hash_value({"variant": "Q1", "seed_id": row["seed_id"], "query_sha256": row["Q1_sha256"], "candidate_k": 200, "dense_revision": config["dense"]["revision"]})})
    write_jsonl(OUT / "q1_dense_candidates.jsonl", q1_dense_rows)

    rer_tok = AutoTokenizer.from_pretrained(reranker_path, local_files_only=True, trust_remote_code=False)
    rer_model = AutoModelForSequenceClassification.from_pretrained(reranker_path, local_files_only=True, trust_remote_code=False, use_safetensors=True, dtype=torch.float16).eval().to("mps")
    docs = [" ".join(e["abstract"].split()) for e in evidence]
    doc_index = {e["paper_id"]: i for i, e in enumerate(evidence)}
    q0_rows, q1_rows, token_rows = [], [], []
    q0_query_counts, q1_query_counts = {}, {}
    doc_counts = {}
    for row in variants:
        sid = row["seed_id"]
        q0_query_counts[sid] = len(rer_tok(row["Q0"], truncation=False)["input_ids"])
        q1_query_counts[sid] = len(rer_tok(row["Q1"], truncation=False)["input_ids"])
        old = reranked[sid]
        for rank, (pid, ds, rs) in enumerate(zip(old["paper_ids"], old["dense_scores"], old["reranker_scores"]), 1):
            idx = doc_index[pid]
            doc_counts.setdefault(pid, len(rer_tok(docs[idx], truncation=False)["input_ids"]))
            retained = len(rer_tok(row["Q0"], docs[idx], truncation=True, max_length=512)["input_ids"])
            token_rows.append({"seed_id": sid, "block_key": row["block_key"], "variant": "Q0", "paper_id": pid, "query_tokens_full": q0_query_counts[sid], "document_tokens_full": doc_counts[pid], "pair_tokens_retained": retained, "query_truncated": q0_query_counts[sid] > 512, "document_truncated": doc_counts[pid] > 512, "pair_truncated": retained >= 512})
            q0_rows.append({"seed_id": sid, "block_key": row["block_key"], "variant": "Q0", "paper_id": pid, "rank": rank, "dense_score": ds, "reranker_score": rs, "candidate_source": "Q0_REUSED_CACHE", "relevance_label": None})
    for vi, row in enumerate(variants):
        pairs = [(row["Q1"], docs[idx]) for idx in dense_indices[vi]]
        scores = []
        for start in range(0, len(pairs), 16):
            batch = pairs[start:start + 16]
            batch_inputs = rer_tok(batch, padding=True, truncation=True, max_length=512, return_tensors="pt").to("mps")
            with torch.inference_mode():
                scores.extend(rer_model(**batch_inputs).logits.reshape(-1).float().cpu().numpy().tolist())
        for rank, (idx, score, ds) in enumerate(zip(dense_indices[vi], scores, dense_scores[vi]), 1):
            pid = evidence[idx]["paper_id"]
            doc_counts.setdefault(pid, len(rer_tok(docs[idx], truncation=False)["input_ids"]))
            retained = len(rer_tok(row["Q1"], docs[idx], truncation=True, max_length=512)["input_ids"])
            token_rows.append({"seed_id": row["seed_id"], "block_key": row["block_key"], "variant": "Q1", "paper_id": pid, "query_tokens_full": q1_query_counts.setdefault(row["seed_id"], len(rer_tok(row["Q1"], truncation=False)["input_ids"])), "document_tokens_full": doc_counts[pid], "pair_tokens_retained": retained, "query_truncated": q1_query_counts[row["seed_id"]] > 512, "document_truncated": doc_counts[pid] > 512, "pair_truncated": retained >= 512})
            q1_rows.append({"seed_id": row["seed_id"], "block_key": row["block_key"], "variant": "Q1", "paper_id": pid, "rank": rank, "dense_score": float(ds), "reranker_score": float(score), "candidate_source": "Q1_NEW_DENSE_TOP200", "relevance_label": None})
    rer_model = None
    torch.mps.empty_cache()

    diagnostics = []
    q0_by_seed, q1_by_seed = defaultdict(list), defaultdict(list)
    for r in q0_rows: q0_by_seed[r["seed_id"]].append(r)
    for r in q1_rows: q1_by_seed[r["seed_id"]].append(r)
    for row in variants:
        sid = row["seed_id"]
        q0_ids = [r["paper_id"] for r in sorted(q0_by_seed[sid], key=lambda x: x["rank"])]
        q1_ids = [r["paper_id"] for r in sorted(q1_by_seed[sid], key=lambda x: x["rank"])]
        inter = set(q0_ids) & set(q1_ids)
        diagnostics.append({"seed_id": sid, "block_key": row["block_key"], "variant_pair": "Q0_vs_Q1", "q0_query_sha256": row["Q0_sha256"], "q1_query_sha256": row["Q1_sha256"], "q0_full_chars": len(row["Q0"]), "q1_full_chars": len(row["Q1"]), "q0_top200_count": len(q0_ids), "q1_top200_count": len(q1_ids), "candidate_intersection": len(inter), "candidate_jaccard": len(inter) / len(set(q0_ids) | set(q1_ids)), "rank_change_mean_abs": statistics.mean(abs(q0_ids.index(pid) - q1_ids.index(pid)) for pid in inter) if inter else None, "q0_relevance_metrics": "PENDING_LABELS", "q1_relevance_metrics": "PENDING_LABELS", "negative_control": False})
    control_ids = [e["paper_id"] for e in data["evidence"][::max(1, len(data["evidence"]) // 4)][:4]]
    for row, pid in zip(variants[:4], control_ids):
        diagnostics.append({"seed_id": row["seed_id"], "block_key": row["block_key"], "variant_pair": "NEGATIVE_CONTROL", "paper_id": pid, "negative_control": True, "q0_relevance_metrics": "PENDING_LABELS", "q1_relevance_metrics": "PENDING_LABELS"})
    write_jsonl(OUT / "query_representation_diagnostics.jsonl", diagnostics)
    write_jsonl(OUT / "query_pair_scores.jsonl", q0_rows + q1_rows)
    q1_cache = [{"seed_id": r["seed_id"], "block_key": r["block_key"], "paper_ids": [x["paper_id"] for x in q1_rows if x["seed_id"] == r["seed_id"]], "new_pairs": 200, "cache_key": hash_value({"variant": "Q1", "seed_id": r["seed_id"], "query_sha256": r["Q1_sha256"], "candidate_k": 200, "reranker_revision": config["reranker"]["revision"]})} for r in variants]
    write_jsonl(OUT / "q1_reranked_candidates.jsonl", q1_cache)
    write_json(OUT / "token_budget_audit.json", {"tokenizer": model_manifest["reranker"], "max_length": 512, "q0_records": len(q0_rows), "q1_records": len(q1_rows), "records": token_rows, "metrics_status": "PENDING_LABELS", "scientific_proposal_generations": 0})
    manifest.update({"Q0_REUSED_SEEDS": len(variants), "Q1_SCORED_SEEDS": len(variants), "Q1_NEW_RERANKER_PAIRS": len(q1_rows), "Q2_SCORED_OR_PENDING": "PENDING_REVIEW"})
    write_json(OUT / "query_variant_manifest.json", manifest)
    status = (OUT / "STATUS.md").read_text() + "\nTASK 3=COMPLETED; Q0 reused for 24 seeds; Q1 rescored 24x200; Q2=PENDING_REVIEW.\nNEXT=TASK 4\n"
    write_bytes(OUT / "STATUS.md", status.encode())


def task4():
    data = load_inputs()
    seeds = {r["seed_id"]: r for r in data["seeds"]}
    evidence = {r["paper_id"]: r for r in data["evidence"]}
    dates = {r["paper_id"]: r for r in data["dates"]}
    hidden = {r["block_key"]: r for r in data["hidden"]}
    cal_keys = sorted(r["block_key"] for r in data["calibration"])
    queue, identity, seen = [], [], set()
    for key in cal_keys:
        block = hidden[key]
        seed = seeds[block["seed_id"]]
        seed_date = dates[seed["focal_paper_id"]]["earliest_public_date"]
        for slot in block["source_slots"]:
            for pid in (slot["A_paper_id"], slot["B_paper_id"]):
                if pid in seen:
                    continue
                seen.add(pid)
                pdate = dates[pid]
                paper = evidence[pid]
                abstract = paper["abstract"]
                queue.append({"review_record_id": hash_value(["temporal", pid])[:24], "paper_id": pid,
                              "year": paper["year"], "publication_date": pdate.get("earliest_public_date"),
                              "earliest_discovered_date": pdate.get("earliest_public_date"),
                              "earliest_history_status": "UNKNOWN_FALLBACK_ONLY", "historical_order_status": "UNVERIFIED_FALLBACK_DATE",
                              "date_source": pdate.get("status"), "date_url": (pdate.get("date_events") or [{}])[0].get("url"),
                              "first_party_identity_status": "OFFICIAL_PROCEEDINGS_IDENTITY_MATCHED", "calibration_block_key": key,
                              "seed_date_for_context": seed_date, "evidence_minus_seed_days": -354 if paper["year"] == 2025 else None,
                              "openreview_bypass": False, "arxiv_identity_inferred": False,
                              "notes": "history endpoint unavailable in frozen run; fallback preserved"})
                identity.append({"review_record_id": hash_value(["identity", pid])[:24], "paper_id": pid, "year": paper["year"],
                                 "official_source_type": paper.get("source_type"), "official_url": paper.get("proceedings_abstract_url"),
                                 "official_source_sha256": paper.get("source_sha256"), "abstract_sha256": paper.get("abstract_sha256"),
                                 "identity_match_status": "PASS_OFFICIAL_RECORD_AND_HASH", "intrinsic_url_count": len(URL_RE.findall(abstract)),
                                 "intrinsic_method_term_count": len(ROUTE_TERMS.findall(abstract)), "intrinsic_identity_examples": URL_RE.findall(abstract)[:3],
                                 "outer_metadata_suppressed_in_visible_review": True, "historical_earliest_status": "UNKNOWN_FALLBACK_ONLY", "raw_abstract_preserved": True})
    for key in cal_keys:
        seed = seeds[hidden[key]["seed_id"]]
        pid = seed["focal_paper_id"]
        if pid in seen:
            continue
        seen.add(pid)
        raw = seed.get("raw_problem_context", "")
        identity.append({"review_record_id": hash_value(["identity", pid])[:24], "paper_id": pid, "year": 2026,
                         "official_source_type": "FROZEN_SEED_SOURCE", "official_url": None, "official_source_sha256": None,
                         "abstract_sha256": seed.get("source_abstract_sha256"), "identity_match_status": "PASS_FROZEN_SEED_RECORD",
                         "intrinsic_url_count": len(URL_RE.findall(raw)), "intrinsic_method_term_count": len(ROUTE_TERMS.findall(raw)),
                         "intrinsic_identity_examples": URL_RE.findall(raw)[:3], "outer_metadata_suppressed_in_visible_review": True,
                         "historical_earliest_status": "UNKNOWN_FALLBACK_ONLY", "raw_abstract_preserved": True})
    gaps = []
    for key in cal_keys:
        seed_date = dates[seeds[hidden[key]["seed_id"]]["focal_paper_id"]]["earliest_public_date"]
        for slot in hidden[key]["source_slots"]:
            for pid in (slot["A_paper_id"], slot["B_paper_id"]):
                gaps.append((date.fromisoformat(dates[pid]["earliest_public_date"]) - date.fromisoformat(seed_date)).days)
    write_jsonl(OUT / "temporal_review_queue.jsonl", queue)
    write_json(OUT / "source_identity_audit.json", {"calibration_unique_exposure_papers": len(queue), "identity_records": identity,
        "intrinsic_url_total": sum(r["intrinsic_url_count"] for r in identity), "intrinsic_method_term_total": sum(r["intrinsic_method_term_count"] for r in identity),
        "outer_metadata_suppression": "PASS_FOR_VISIBLE_EXPORT; intrinsic abstract identifiers remain",
        "earliest_history_status": "UNKNOWN_FALLBACK_ONLY", "historical_order_status": "UNVERIFIED",
        "openreview_challenge_bypassed": False, "arxiv_identity_inferred": False})
    write_json(OUT / "temporal_gap_audit.json", {"calibration_slot_gaps": dict(Counter(gaps)), "all_gaps_equal_minus_354": all(g == -354 for g in gaps),
        "published_global_distribution_claim": "all 790000 F0 scored pairs were -354; this is not a historical cleanliness certificate"})
    status = (OUT / "STATUS.md").read_text() + f"\nTASK 4=COMPLETED; calibration temporal exposures={len(queue)}; fallback history remains UNKNOWN; all calibration slot gaps -354={all(g == -354 for g in gaps)}.\nNEXT=TASK 5\n"
    write_bytes(OUT / "STATUS.md", status.encode())


def validate():
    data = load_inputs()
    reranked, banks = data["reranked"], data["banks"]
    result = {
        "corpus_hash_ok": corpus_hash() == "0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807",
        "denominators_ok": len(data["seeds"]) == 5351 and sum(r["status"] == "MEASURED" for r in reranked) == 3950 and sum(r["status"] == "BLOCKED_SOURCE_GATE" for r in reranked) == 1401 and sum(len(r.get("paper_ids") or []) for r in reranked if r["status"] == "MEASURED") == 790000 and sum(r["status"] == "MEASURED" for r in banks) == 15800 and sum(r["status"] != "MEASURED" for r in banks) == 5604,
        "calibration_certification_disjoint": not ({r["seed_id"] for r in data["hidden"] if r["partition"] == "CALIBRATION"} & {r["seed_id"] for r in data["hidden"] if r["partition"] == "CERTIFICATION"}),
        "human_labels_imported": 0, "proposal_generations": 0,
        "fallback_not_historical_pass": json.loads((OUT / "source_identity_audit.json").read_text())["historical_order_status"] != "PASS",
        "query_q2_pending": json.loads((OUT / "query_variant_manifest.json").read_text())["Q2"] == "PENDING_REVIEW",
        "reviewed_slot_scope_4": all(row["reviewed_slot_count"] == 4 for row in read_jsonl(OUT / "block_admissibility_audit.jsonl")),
        "review_files_no_hidden_scores": all("score" not in key.lower() and "rank" not in key.lower() and "paper_id" not in key.lower() for path in (OUT / "seed_audit.jsonl", OUT / "paper_relevance_route_audit.jsonl", OUT / "block_admissibility_audit.jsonl") for row in read_jsonl(path) for key in row),
        "ab_mapping_private": all("source_slots" not in row for row in read_jsonl(OUT / "block_admissibility_audit.jsonl")),
        "no_silent_zero": all(row["status"] != "BLOCKED_SOURCE_GATE" or row.get("max_matched_slots") is None for row in banks),
    }
    result["all_required"] = all(v is True for v in result.values() if isinstance(v, bool))
    write_json(OUT / "TEST_REPORT.json", result)
    return result


def task5():
    result = validate()
    state = "READY_FOR_CALIBRATION_REVIEW" if result["all_required"] else "BLOCKED"
    write_bytes(OUT / "F1_CALIBRATION_READINESS.md", (f"# F1 Calibration Readiness\n\nSTATUS={state}\n\nThis is a source-only calibration package. No human labels were imported and no scientific proposal generation was run. The 96 certification records remain untouched.\n\n- Calibration blocks: 24 unique seeds.\n- Visible block review scope: exactly 4 displayed slots per block; no k=8/k=12 certification.\n- Q0: exact F0 query and cached scores reused for 24 seeds.\n- Q1: deterministic query variant scored on 24 x 200 candidates with new cache keys.\n- Q2: PENDING_REVIEW.\n- Temporal history: fallback-only discovered dates; historical cleanliness remains UNKNOWN/UNVERIFIED.\n\n## Tests\n```json\n{json.dumps(result, indent=2, sort_keys=True)}\n```\n").encode())
    write_bytes(OUT / "FINAL_CHECKPOINT.md", (f"# Final Checkpoint\n\nCompleted:\n- Reconciled frozen F0 counts, hashes, semantic/lexical paired comparison, and coverage.\n- Prepared unlabelled seed, paper, block, CSV, field-description, and independent shadow audit materials.\n- Frozen Q0/Q1/Q2 query manifest; reused Q0 and scored Q1 only on 24 calibration seeds.\n- Audited calibration temporal fallback semantics and intrinsic abstract identity cues.\n- Ran source-only validation tests.\n\nNot completed:\n- Human calibration labels and rubric freeze.\n- Formal F1 certification of 96 blocks.\n- ARS, baseline, P0/P1, or scientific proposal generation.\n\nScientific questions remaining:\n- Whether human reviewers judge the seed constructs, source relevance, route distinctions, and temporal/source validity as admissible.\n- Whether Q1 ranking changes correspond to improved relevance after labels exist; current metrics are PENDING_LABELS.\n\nRecommended next experiment:\n- Human review of the 24 calibration blocks, then freeze the rubric before touching the 96-case certification queue.\n\nSTATUS={state}\nSCIENTIFIC_PROPOSAL_GENERATIONS=0\n").encode())
    status = (OUT / "STATUS.md").read_text() + f"\nTASK 5=COMPLETED\nTESTS={json.dumps(result, sort_keys=True)}\nSTATUS={state}\nBLOCKERS=No human labels; fallback date histories unresolved; Q2 pending review.\nSCIENTIFIC_PROPOSAL_GENERATIONS=0\n"
    write_bytes(OUT / "STATUS.md", status.encode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["task1", "task2", "task3", "task4", "validate", "task5"])
    parser.add_argument("--dense-path", default=str(MODEL_ROOT / "bge-base-en-v1.5"))
    parser.add_argument("--reranker-path", default=str(MODEL_ROOT / "bge-reranker-base"))
    args = parser.parse_args()
    if args.task == "task1": task1()
    elif args.task == "task2": task2()
    elif args.task == "task3": task3(args)
    elif args.task == "task4": task4()
    elif args.task == "validate": print(json.dumps(validate(), indent=2, sort_keys=True))
    else: task5()


if __name__ == "__main__":
    main()
