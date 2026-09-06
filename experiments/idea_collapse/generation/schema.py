"""Strict parsing preserves malformed outputs rather than repairing research ideas."""

import json
import math


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


def validate_retrieved(retrieved, condition):
    if condition not in CONDITIONS or not isinstance(retrieved, list):
        raise ValueError("invalid condition/retrieval list")
    if condition == CONDITIONS[0] and retrieved:
        raise ValueError("C0 must contain no retrieved papers")
    seen = set()
    for rank, item in enumerate(retrieved, 1):
        if set(item) != {"paper_id", "rank", "score", "title", "abstract"}:
            raise ValueError("unexpected retrieval fields")
        if item["rank"] != rank or item["paper_id"] in seen:
            raise ValueError("invalid rank or duplicate source")
        if any(not isinstance(item[k], str) or not item[k] for k in ("paper_id", "title", "abstract")):
            raise ValueError("missing source text/ID")
        if isinstance(item["score"], bool) or not isinstance(item["score"], (int, float)) or not math.isfinite(item["score"]):
            raise ValueError("non-finite retrieval score")
        seen.add(item["paper_id"])


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
    validate_retrieved(trace["retrieved"], trace["condition"])


def require_pilot_traces(traces):
    if not traces:
        raise ValueError("no traces")
    for trace in traces:
        validate_trace(trace)
        if trace["run_purpose"] != "scientific_pilot":
            raise ValueError("mock/smoke data cannot enter scientific analysis")
        if trace["model_provider"] == "mock" or trace["model_version_evidence"] == "mock_fixture":
            raise ValueError("mock provider cannot supply scientific evidence")
