import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from experiments.idea_collapse.corpus.build_corpus import build, validate_records
from experiments.idea_collapse.generation.provenance import (
    canonical_bytes, export_jsonl, file_hash, input_path, object_hash, write_exclusive,
)
from experiments.idea_collapse.generation.providers import MockProvider, OpenAICompatibleProvider, ProviderFailure
from experiments.idea_collapse.generation.run import execute_request, run_mock
from experiments.idea_collapse.generation.schema import (
    CONDITIONS, IDEA_FIELDS, exposure_marginals, parse_idea, require_pilot_traces, validate_retrieved, validate_trace,
)


def request():
    prompt = "MOCK ONLY: one idea"
    analysis = {"purpose": "mock"}
    return {
        "run_purpose": "mock", "git_commit": "a" * 40,
        "code_sha256": "b" * 64, "config_sha256": "c" * 64,
        "corpus_sha256": "d" * 64, "base_prompt_sha256": "e" * 64,
        "analysis_config": analysis, "analysis_config_sha256": object_hash(analysis),
        "retriever_name": "mock", "retriever_version": "mock-v1", "retriever_config": {},
        "domain": "model_editing", "condition": CONDITIONS[0], "seed": 1,
        "model_provider": "mock", "model_family": "fixture_a", "model_version": "mock-a-v1",
        "generation_settings": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 256},
        "retrieval_query": "model editing", "retrieved": [], "prompt": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
    }


def paper():
    return {"paper_id": "UNIT_TEST_NOT_A_PAPER", "year": 2024,
            "title": "MOCK TITLE", "abstract": "MOCK ABSTRACT", "keywords": [],
            "openreview_url": "https://openreview.net/forum?id=UNIT_TEST_NOT_A_PAPER",
            "domain_tags": ["model_editing"],
            "provenance": {"source_url": "https://example.invalid/unit-test",
                           "retrieved_at": "2026-09-06", "topic_rule": "MOCK_ONLY"}}


class InfrastructureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_canonical_key_order(self):
        self.assertEqual(object_hash({"b": 2, "a": 1}), object_hash({"a": 1, "b": 2}))

    def test_raw_hash_and_no_overwrite(self):
        path = self.root / "evidence.json"
        write_exclusive(path, b"original")
        self.assertEqual(file_hash(path), hashlib.sha256(b"original").hexdigest())
        with self.assertRaises(FileExistsError):
            write_exclusive(path, b"replacement")
        self.assertEqual(path.read_bytes(), b"original")

    def test_nonfinite_hash_fails(self):
        with self.assertRaises(ValueError):
            object_hash({"value": float("nan")})

    def test_input_path_cannot_escape_repository(self):
        with self.assertRaises(ValueError):
            input_path("../outside", self.root)

    def test_valid_idea_preserves_text(self):
        idea = {key: "  wording must remain unchanged  " for key in IDEA_FIELDS}
        self.assertEqual(parse_idea(json.dumps(idea))["idea"], idea)

    def test_invalid_json_paths(self):
        for raw in ("not JSON", "```json\n{}\n```", "[]", "{}", '{"a":1,"a":2}', '{"x":NaN}'):
            with self.subTest(raw=raw):
                self.assertEqual(parse_idea(raw)["parse_status"], "parse_failure")

    def test_empty_or_extra_fields_are_not_repaired(self):
        idea = {key: "text" for key in IDEA_FIELDS}
        for altered in ({**idea, "extra": "x"}, {**idea, "claimed_gap": ""}):
            self.assertIsNone(parse_idea(json.dumps(altered))["idea"])

    def test_retrieval_roundtrip(self):
        rows = [{"paper_id": "MOCK", "rank": 1, "score": 0.4, "title": "t", "abstract": "a"}]
        validate_retrieved(json.loads(canonical_bytes(rows)), CONDITIONS[1])

    def test_amendment_marginals_and_unknown_tokens(self):
        rows = [{"paper_id": "MOCK", "rank": 1, "score": 0.4, "title": "t", "abstract": "a",
                 "year": 2024, "cluster_topic_id": None, "citation_popularity_proxy": None}]
        validate_retrieved(rows, CONDITIONS[1], amended=True)
        result = exposure_marginals(rows)
        self.assertEqual(result["mean_score"], 0.4)
        self.assertEqual(result["median_score"], 0.4)
        self.assertEqual(result["publication_years"], [2024])
        self.assertIsNone(result["context_token_count"])
        self.assertEqual(result["token_count_status"], "unavailable")
        self.assertEqual(exposure_marginals([])["context_token_count"], 0)
        self.assertEqual(exposure_marginals(rows, 12, "fixture-tokenizer-v1")["token_count_status"], "measured")

    def test_c0_rejects_context(self):
        with self.assertRaises(ValueError):
            validate_retrieved([{"paper_id": "MOCK"}], CONDITIONS[0])

    def test_duplicate_sources_and_bad_ranks_rejected(self):
        row = {"paper_id": "MOCK", "rank": 1, "score": 0.4, "title": "t", "abstract": "a"}
        for rows in ([row, {**row, "rank": 2}], [{**row, "rank": 2}], [{**row, "score": float("nan")}]):
            with self.assertRaises(ValueError):
                validate_retrieved(rows, CONDITIONS[1])

    def test_every_outcome_binding_changes_run_id(self):
        original = request()
        for key in ("seed", "git_commit", "code_sha256", "corpus_sha256", "prompt_sha256",
                    "model_version", "analysis_config_sha256", "condition", "retriever_version"):
            modified = {**original, key: "changed"}
            self.assertNotEqual(object_hash(original), object_hash(modified), key)

    def test_success_and_cache_do_not_regenerate(self):
        provider = MockProvider()
        first = execute_request(request(), provider, self.root)
        validate_trace(first)
        second = execute_request(request(), provider, self.root)
        self.assertEqual(provider.calls, 1)
        self.assertEqual(first, second)

    def test_all_failure_types_retained_and_cached(self):
        for mode, status in (("malformed", "parse_failure"), ("refusal", "refusal"), ("provider_error", "provider_error")):
            with self.subTest(mode=mode):
                provider = MockProvider(mode)
                first = execute_request(request(), provider, self.root / mode)
                second = execute_request(request(), provider, self.root / mode)
                self.assertEqual(first["status"], status)
                self.assertEqual(first, second)
                self.assertEqual(provider.calls, 1)
                self.assertTrue(first["raw_provider_response"])
                self.assertTrue(all(first[key] is None for key in IDEA_FIELDS))

    def test_incomplete_attempt_blocks_retry(self):
        provider = MockProvider()
        (self.root / (object_hash(request()) + ".attempt.jsonl")).write_text("{}\n")
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            execute_request(request(), provider, self.root)
        self.assertEqual(provider.calls, 0)

    def test_cache_tamper_is_detected(self):
        provider = MockProvider()
        trace = execute_request(request(), provider, self.root)
        path = self.root / (trace["run_id"] + ".json")
        changed = {**trace, "timestamp": "tampered"}
        path.write_bytes(canonical_bytes(changed))
        with self.assertRaisesRegex(ValueError, "checksum"):
            execute_request(request(), provider, self.root)
        self.assertEqual(provider.calls, 1)

    def test_copied_parsed_fields_cannot_replace_raw(self):
        trace = execute_request(request(), MockProvider(), self.root)
        trace["research_question"] = "post-hoc rewrite"
        with self.assertRaisesRegex(ValueError, "retained raw"):
            validate_trace(trace)

    def test_scientific_execution_and_mock_analysis_blocked(self):
        provider = MockProvider()
        with self.assertRaises(ValueError):
            execute_request({**request(), "run_purpose": "scientific_pilot"}, provider, self.root)
        self.assertEqual(provider.calls, 0)
        trace = execute_request(request(), provider, self.root)
        with self.assertRaisesRegex(ValueError, "mock/smoke"):
            require_pilot_traces([trace])

    def test_export_is_idempotent_and_no_duplicate_ids(self):
        trace = execute_request(request(), MockProvider(), self.root)
        path = self.root / "traces.jsonl"
        export_jsonl([trace], path)
        export_jsonl([trace], path)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            export_jsonl([trace, trace], self.root / "duplicate.jsonl")

    def test_transport_supports_two_models_without_logic_change(self):
        calls = []
        def transport(payload):
            calls.append(payload)
            return json.dumps({"model": payload["model"], "choices": [{"message": {"content": "{}"}}]})
        provider = OpenAICompatibleProvider(transport)
        for model in ("fixture-A-exact-v1", "fixture-B-exact-v2"):
            response = provider.generate({**request(), "model_version": model})
            self.assertEqual(response.resolved_model, model)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["messages"], calls[1]["messages"])

    def test_transport_cannot_override_model_identity(self):
        provider = OpenAICompatibleProvider(lambda _: self.fail("transport must not be called"))
        with self.assertRaises(ValueError):
            provider.generate({**request(), "generation_settings": {"model": "different"}})

    def test_bad_provider_envelope_preserves_raw(self):
        provider = OpenAICompatibleProvider(lambda _: "NOT JSON")
        with self.assertRaises(ProviderFailure) as caught:
            provider.generate(request())
        self.assertEqual(caught.exception.raw, "NOT JSON")

    def test_corpus_validation_and_freeze(self):
        source = self.root / "source.jsonl"
        source.write_bytes(canonical_bytes(paper()))
        output, manifest = self.root / "corpus.jsonl", self.root / "manifest.json"
        report = build(source, output, manifest)
        self.assertEqual(report["corpus_sha256"], file_hash(output))
        self.assertEqual(len(report["short_domains"]), 3)
        self.assertEqual(report["source_verification"], "not_performed_by_this_validator")
        with self.assertRaises(ValueError):
            build(source, output, manifest)

    def test_corpus_duplicates_and_scope_rejected(self):
        for rows in ([paper(), paper()], [{**paper(), "year": 2023}], [{**paper(), "abstract": ""}], []):
            with self.assertRaises(ValueError):
                validate_records(rows)

    def test_mock_end_to_end_and_resume(self):
        config = Path(__file__).resolve().parents[1] / "configs/mock.json"
        first = run_mock(config, self.root)
        second = run_mock(config, self.root)
        self.assertEqual(first["records"], 12)
        self.assertEqual(first["provider_calls"], 12)
        self.assertEqual(second["provider_calls"], 0)
        rows = [json.loads(line) for line in (self.root / "mock/traces.jsonl").read_text().splitlines()]
        for row in rows:
            self.assertEqual(row["trace_schema_version"], 2)
            if row["condition"] == CONDITIONS[0]:
                self.assertNotIn("MOCK ABSTRACT", row["prompt"])
                self.assertEqual(row["retrieved"], [])
                self.assertEqual(row["retrieval_marginals"]["token_count_status"], "no_context")
            else:
                self.assertEqual(row["retrieval_marginals"]["token_count_status"], "unavailable")
            self.assertEqual(row["run_purpose"], "mock")
        self.assertEqual(len({r["model_family"] for r in rows}), 2)


if __name__ == "__main__":
    unittest.main()
