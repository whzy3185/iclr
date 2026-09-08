"""Explicit seed gates, temporal uncertainty and exact source-only matching."""

from collections import Counter
from datetime import date
from fractions import Fraction
import math
import re
import statistics
from types import SimpleNamespace

import networkx as nx

from recovery_common import identity, legacy

BACKEND = "LEXICAL_PROVISIONAL"
PAIRS = legacy.R_PAIRS
TIERS = {"T0_COMMON_STRICT": date(2024, 8, 31), "T1_LLAMA_CLEANER": date(2023, 12, 31)}


def temporal_membership(first_public, tier):
    if tier == "T2_ALL_ACCEPTED":
        return "INCLUDED_CONTAMINATION_UNCERTAIN"
    if first_public is None or first_public in ("UNKNOWN", "AMBIGUOUS"):
        return "UNKNOWN"
    try:
        value = date.fromisoformat(first_public)
    except (TypeError, ValueError):
        return "UNKNOWN"
    return "DISCOVERED_AFTER_CUTOFF" if value > TIERS[tier] else "DISCOVERED_ON_OR_BEFORE_CUTOFF"


def seed_gate(source, masked, raw_context, warning_flags=(), evidence_ids=()):
    errors = list(source.get("hard_errors", []))
    if not source.get("abstract"):
        errors.append("MISSING_SOURCE_ABSTRACT")
    if source["paper_id"] in evidence_ids:
        errors.append("FOCAL_SELF_INCLUSION")
    extractable = bool(source.get("abstract") and masked.strip()) and not errors
    explicit = bool(re.search(r"\b(?:we|our (?:paper|work))\s+(?:propose|introduce|develop|present)\b",
                              raw_context, re.I)) and bool(re.search(
                                  r"\b(?:we propose|we introduce|we present|we develop|prior work discusses|our method)\b",
                                  masked, re.I))
    flags = sorted(set(warning_flags) | ({"EXPLICIT_FOCAL_SOLUTION_UNREPAIRED"} if explicit else set()))
    return {"extractable": extractable, "source_matching_allowed": extractable and not explicit,
            "confirmatory_eligible": False, "risk_flags": flags, "hard_errors": sorted(set(errors)),
            "review_state": "REVIEW_PENDING" if extractable else "NOT_REVIEWED",
            "repair_reason": "EXPLICIT_FOCAL_SOLUTION_UNREPAIRED" if explicit else None}


def make_seed(source):
    p = SimpleNamespace(paper_id=source["paper_id"], title=source["title"] or "", abstract=source["abstract"] or "",
                        extraction_status="OK" if source["parse_status"] == "MEASURED" else "MISSING",
                        subfield_source_tags=legacy.classify_subfield((source["title"] or "") + " " + (source["abstract"] or "")),
                        first_public_date="UNKNOWN")
    old = legacy.make_seed_rows([p])[0]
    flags = [name for name in ("focal_method_leak", "distinctive_phrase_leak", "too_broad", "too_narrow")
             if old[name] == "True"]
    spans = []
    for sentence in legacy.sentence_split(p.abstract):
        if sentence in old["raw_problem_context"]:
            start = p.abstract.find(sentence)
            spans.append({"start": start, "end": start + len(sentence), "text": sentence})
    return {"seed_id": old["seed_id"], "focal_paper_id": p.paper_id, "subfield": p.subfield_source_tags,
            "raw_problem_context": old["raw_problem_context"], "method_masked_question": old["method_masked_question"],
            "source_spans": spans, "source_abstract_sha256": source["abstract_sha256"],
            "removed_solution_tokens_entities": old["removed_solution_tokens/entities"].split(";") if old["removed_solution_tokens/entities"] else [],
            "legacy_heuristics_uncalibrated": old,
            **seed_gate(source, old["method_masked_question"], old["raw_problem_context"], flags)}


def annotate(source):
    text = (source["title"] or "") + " " + (source["abstract"] or "")
    primary, strength, secondary, confidence, scores, descriptor = legacy.classify_route(text)
    spans = []
    for route, terms in legacy.ROUTE_KEYWORDS.items():
        for term in terms:
            match = re.search(r"\b" + re.escape(term) + r"\b", text, re.I)
            if match:
                spans.append({"route": route, "term": term, "start": match.start(), "end": match.end(), "text": match.group()})
    return {"paper_id": source["paper_id"], "input_text": text, "source_spans": spans,
            "primary_route": primary, "secondary_routes": secondary,
            "route_purity_descriptor": descriptor, "numeric_route_purity": None,
            "purity_assessment_status": "NOT_ASSESSED", "primary_route_strength_heuristic": strength,
            "raw_parser_output": {"scores": scores, "legacy_confidence_uncalibrated": confidence},
            "coarse_family": legacy.classify_coarse(primary, secondary, strength),
            "annotation_backend": "KEYWORD_PROVISIONAL", "annotation_version": "preserved_legacy_keywords_v1",
            "review_state": "REVIEW_PENDING", "subfield": legacy.classify_subfield(text)}


def exact_matching(edges):
    """Maximum cardinality then minimum declared integer cost, stable graph order."""
    if not edges:
        return []
    if len({(a, b) for a, b, cost in edges}) != len(edges):
        raise ValueError("duplicate edge")
    if any(type(cost) is not int or cost < 0 for _, _, cost in edges):
        raise ValueError("nonnegative integer matching costs required")
    graph = nx.DiGraph()
    graph.add_nodes_from(["s", "t"])
    left = sorted({a for a, _, _ in edges})
    right = sorted({b for _, b, _ in edges})
    if set(left) & set(right):
        raise ValueError("same source cannot occupy both route partitions")
    for a in left:
        graph.add_edge("s", ("A", a), capacity=1, weight=0)
    for b in right:
        graph.add_edge(("B", b), "t", capacity=1, weight=0)
    ordered = sorted(edges)
    # Secondary rank cannot outweigh one unit of the declared primary cost.
    multiplier = min(len(left), len(right)) * max(1, len(ordered)) + 1
    for rank, (a, b, cost) in enumerate(ordered):
        graph.add_edge(("A", a), ("B", b), capacity=1, weight=cost * multiplier + rank)
    flow = nx.max_flow_min_cost(graph, "s", "t")
    return [(a, b, cost) for a, b, cost in ordered if flow[("A", a)].get(("B", b), 0) == 1]


def lexical_candidates(seed, evidence, annotation, idf, inverted, doc_counts, config):
    query = seed["method_masked_question"]
    qvector = legacy.vectorize_query(query, idf)
    scores = legacy.cosine_scores(qvector, inverted)
    top = sorted(((i, v) for i, v in scores.items() if evidence[i]["paper_id"] != seed["focal_paper_id"]),
                 key=lambda pair: (-pair[1], evidence[pair[0]]["paper_id"]))[:config["candidate_pool_size"]]
    query_counts = Counter(legacy.tokenize(query))
    raw_bm = [sum(min(2.0, doc_counts[i].get(term, 0)) * (1 + math.log(n)) for term, n in query_counts.items()) /
              (len(query_counts) + 4) for i, score in top]
    maximum = max(raw_bm, default=0)
    rows = []
    for rank, ((i, score), bm) in enumerate(zip(top, raw_bm), 1):
        source = evidence[i]
        labels = annotation[source["paper_id"]]
        bm_normalized = bm / maximum if maximum else 0.0
        rows.append({"seed_id": seed["seed_id"], "paper_id": source["paper_id"], "rank": rank,
                     "retrieval_backend": BACKEND, "lexical_cosine": score, "lexical_bm25_like": bm_normalized,
                     "dense_relevance": None, "semantic_reranker_score": None, "numeric_route_purity": None,
                     "first_public_date": source["first_public_date"], "year": source["year"],
                     "lexical_length": len(legacy.tokenize(source["abstract"])), "model_token_length": None,
                     "subfield": labels["subfield"], "primary_route": labels["primary_route"],
                     "route_purity_descriptor": labels["route_purity_descriptor"],
                     "above_legacy_lexical_floor": score >= config["cosine_floor"] and bm_normalized >= config["bm25_like_floor"],
                     "query_sha256": identity(query)})
    return rows


def match_lexical(candidates, routes, config):
    pool = [c for c in candidates if c["above_legacy_lexical_floor"] and c["route_purity_descriptor"] == "ROUTE_CLEAR"]
    left = sorted([c for c in pool if c["primary_route"] == routes[0]], key=lambda c: c["paper_id"])
    right = sorted([c for c in pool if c["primary_route"] == routes[1]], key=lambda c: c["paper_id"])
    lengths = {p["paper_id"]: z for p, z in zip(left + right, legacy.standardize([c["lexical_length"] for c in left + right]))}
    edges, features = [], {}
    exclusions = Counter()
    for a in left:
        for b in right:
            delta = abs(a["lexical_cosine"] - b["lexical_cosine"])
            bm_delta = abs(a["lexical_bm25_like"] - b["lexical_bm25_like"])
            if delta > config["cosine_gap"] or bm_delta > config["bm25_like_gap"]:
                exclusions["LEXICAL_GAP_CALIPER"] += 1
                continue
            topic = int(a["subfield"] != b["subfield"])
            length_delta = abs(lengths[a["paper_id"]] - lengths[b["paper_id"]])
            cost = round((0.35 * delta + 0.25 * bm_delta + 0.15 * length_delta + 0.15 * topic) * 1_000_000)
            edges.append((a["paper_id"], b["paper_id"], cost))
            features[(a["paper_id"], b["paper_id"])] = {"lexical_relevance_gap": delta, "lexical_bm25_gap": bm_delta,
                "length_z_gap": length_delta, "subfield_disagreement": topic, "date_gap_days": None,
                "dense_gap": None, "embedding_distance": None}
    chosen = exact_matching(edges)
    used = {p for a, b, cost in chosen for p in (a, b)}
    connected = {p for a, b, cost in edges for p in (a, b)}
    unmatched = [{"paper_id": c["paper_id"], "reason": "CAPACITY_COMPETITION" if c["paper_id"] in connected else "NO_ADMISSIBLE_EDGE"}
                 for c in left + right if c["paper_id"] not in used]
    return chosen, features, unmatched, {"n_A": len(left), "n_B": len(right), "admissible_edges": len(edges),
                                       "rejected_edges": dict(exclusions), "max_matched_slots": len(chosen)}


def coverage_cell(status, maximum=None):
    allowed = {"MEASURED", "NOT_RUN", "BLOCKED", "MISSING_COVARIATES", "PENDING_REVIEW"}
    if status not in allowed or (status == "MEASURED") != (maximum is not None):
        raise ValueError("measured values and typed missingness must remain distinct")
    if maximum is not None and (type(maximum) is not int or maximum < 0):
        raise ValueError("invalid matching cardinality")
    return {"cell_status": status, "max_matched_slots": maximum}


def packets(slots, k):
    if len(slots) < k:
        return []
    selected = slots[:k]
    fractions = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)] if k % 4 == 0 else [Fraction(0), Fraction(1, 2), Fraction(1)]
    rows = []
    for alpha in fractions:
        count = alpha * k
        if count.denominator != 1:
            raise ValueError("unsupported exact packet fraction")
        for shift in range(k):
            chosen_A = {(shift + j) % k for j in range(int(count))}
            order = [(shift + j) % k for j in range(k)]
            paper_ids = [selected[j][0 if j in chosen_A else 1] for j in order]
            if len(set(paper_ids)) != k:
                raise ValueError("source reused within packet")
            rows.append({"k": k, "alpha": str(alpha), "assignment": shift, "A_slot_indices": sorted(chosen_A),
                         "ordered_paper_ids": paper_ids, "exact_quarters_supported": k % 4 == 0})
    return rows
