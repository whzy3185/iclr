"""Strict parsing preserves malformed outputs rather than repairing research ideas."""

import json
import math
import statistics


IDEA_FIELDS = ("research_question", "claimed_gap", "method_sketch",
               "key_experiment", "why_nontrivial")
CONDITIONS = ("topic_only_no_retrieval", "topk_relevance", "diversified_retrieval")
STATUSES = ("success", "parse_failure", "refusal", "provider_error")


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    def constant(value):
        raise ValueError("non-finite JSON value")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def parse_idea(raw):
    try:
        idea = strict_json(raw)
        if not isinstance(idea, dict) or set(idea) != set(IDEA_FIELDS):
            raise ValueError("expected exactly the five idea fields")
        if any(not isinstance(idea[k], str) or not idea[k].strip() for k in IDEA_FIELDS):
            raise ValueError("all idea fields must contain text")
        return {"parse_status": "success", "idea": idea, "parse_error": None}
    except (ValueError, TypeError) as error:
        return {"parse_status": "parse_failure", "idea": None,
                "parse_error": type(error).__name__}


def validate_retrieved(retrieved, condition, amended=False):
    if condition not in CONDITIONS or not isinstance(retrieved, list):
        raise ValueError("invalid condition/retrieval list")
    if condition == CONDITIONS[0] and retrieved:
        raise ValueError("C0 must contain no retrieved papers")
    seen = set()
    for rank, item in enumerate(retrieved, 1):
        basic = {"paper_id", "rank", "score", "title", "abstract"}
        extended = basic | {"year", "cluster_topic_id", "citation_popularity_proxy"}
        if set(item) not in (basic, extended) or (amended and set(item) != extended):
            raise ValueError("unexpected retrieval fields")
        if item["rank"] != rank or item["paper_id"] in seen:
            raise ValueError("invalid rank or duplicate source")
        if any(not isinstance(item[k], str) or not item[k] for k in ("paper_id", "title", "abstract")):
            raise ValueError("missing source text/ID")
        if isinstance(item["score"], bool) or not isinstance(item["score"], (int, float)) or not math.isfinite(item["score"]):
            raise ValueError("non-finite retrieval score")
        if "year" in item and item["year"] not in (2024, 2025, 2026):
            raise ValueError("missing/out-of-scope source year")
        seen.add(item["paper_id"])


def exposure_marginals(retrieved, context_token_count=None, tokenizer=None):
    scores = [paper["score"] for paper in retrieved]
    if not retrieved:
        context_token_count = 0
    if context_token_count is not None and (type(context_token_count) is not int or context_token_count < 0):
        raise ValueError("invalid context token count")
    return {
        "per_item_scores": scores,
        "mean_score": statistics.mean(scores) if scores else None,
        "median_score": statistics.median(scores) if scores else None,
        "publication_years": [paper["year"] for paper in retrieved],
        "paper_ids": [paper["paper_id"] for paper in retrieved],
        "cluster_topic_ids": [paper["cluster_topic_id"] for paper in retrieved],
        "citation_popularity_proxies": [paper["citation_popularity_proxy"] for paper in retrieved],
        "context_token_count": context_token_count,
        "tokenizer": tokenizer,
        "token_count_status": "no_context" if not retrieved else
                              ("measured" if context_token_count is not None and tokenizer else "unavailable"),
    }


def validate_trace(trace):
    from .provenance import object_hash
    required = {"run_id", "timestamp", "run_purpose", "git_commit", "git_dirty",
                "code_sha256", "config_sha256", "corpus_sha256", "prompt_sha256",
                "base_prompt_sha256", "analysis_config_sha256", "analysis_config",
                "domain", "condition", "seed", "model_provider", "model_family",
                "model_version", "resolved_model_version", "model_version_evidence",
                "generation_settings", "retrieval_query", "retriever_name",
                "retriever_version", "retriever_config", "retrieved", "prompt",
                "raw_response", "raw_provider_response", "status", "parse_error",
                "provider_error", "request_sha256", "request", *IDEA_FIELDS}
    version = trace.get("trace_schema_version", 1)
    if version == 2:
        required |= {"trace_schema_version", "retrieval_marginals"}
    elif version != 1:
        raise ValueError("unsupported trace schema version")
    if set(trace) != required:
        raise ValueError("trace schema fields do not match")
    if trace["run_purpose"] not in ("mock", "smoke_test", "scientific_pilot"):
        raise ValueError("unknown purpose")
    if trace["status"] not in STATUSES:
        raise ValueError("unknown status")
    for key in ("run_id", "code_sha256", "config_sha256", "corpus_sha256",
                "prompt_sha256", "base_prompt_sha256", "analysis_config_sha256", "request_sha256"):
        value = trace[key]
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError(f"invalid hash: {key}")
    if trace["status"] == "success":
        if any(not isinstance(trace[k], str) or not trace[k].strip() for k in IDEA_FIELDS):
            raise ValueError("successful trace missing parsed idea")
    elif any(trace[k] is not None for k in IDEA_FIELDS):
        raise ValueError("failed trace must not contain invented parsed fields")
    if not isinstance(trace["raw_response"], str):
        raise ValueError("raw response must be text")
    if trace["run_id"] != object_hash(trace["request"]) or trace["request_sha256"] != trace["run_id"]:
        raise ValueError("request identity mismatch")
    if any(trace.get(key) != value for key, value in trace["request"].items()):
        raise ValueError("trace differs from bound request")
    if trace["status"] == "success":
        parsed = parse_idea(trace["raw_response"])
        if parsed["idea"] != {key: trace[key] for key in IDEA_FIELDS}:
            raise ValueError("parsed fields do not match retained raw output")
    validate_retrieved(trace["retrieved"], trace["condition"], amended=version == 2)
    if version == 2:
        marginals = trace["retrieval_marginals"]
        expected = exposure_marginals(trace["retrieved"], marginals["context_token_count"], marginals["tokenizer"])
        if expected != marginals:
            raise ValueError("retrieval marginals differ from retained per-item data")


def require_pilot_traces(traces):
    if not traces:
        raise ValueError("no traces")
    for trace in traces:
        validate_trace(trace)
        if trace["run_purpose"] != "scientific_pilot":
            raise ValueError("mock/smoke data cannot enter scientific analysis")
        if trace["model_provider"] == "mock" or trace["model_version_evidence"] == "mock_fixture":
            raise ValueError("mock provider cannot supply scientific evidence")
        if trace.get("trace_schema_version") != 2:
            raise ValueError("scientific traces require Amendment A covariates")
        if trace["retrieval_marginals"]["token_count_status"] == "unavailable":
            raise ValueError("scientific context tokens have not been measured")
