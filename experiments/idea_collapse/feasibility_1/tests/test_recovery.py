from fractions import Fraction
import itertools
from pathlib import Path
import random
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from recovery_algorithms import (annotate, coverage_cell, exact_matching, lexical_candidates,
                                 make_seed, packets, seed_gate, temporal_membership)
from recovery_common import digest, encoded, legacy, parse_source, write_jsonl


class RecoveryTests(unittest.TestCase):
    def source(self, text="Predicting distribution shift remains challenging for existing learning systems."):
        return {"paper_id": "FOCAL", "title": "A study of distribution shift", "abstract": text,
                "abstract_sha256": "test", "parse_status": "MEASURED", "hard_errors": []}

    def test_warning_permits_provisional_not_confirmatory(self):
        result = seed_gate(self.source(), "Generalization under shift", "Known limitations", ["distinctive_phrase_leak"])
        self.assertTrue(result["source_matching_allowed"])
        self.assertFalse(result["confirmatory_eligible"])
        self.assertIn("distinctive_phrase_leak", result["risk_flags"])

    def test_missing_source_retained_and_blocked(self):
        seed = make_seed({**self.source(), "abstract": None, "parse_status": "MISSING_SOURCE"})
        self.assertEqual(seed["seed_id"], "SEED_FOCAL")
        self.assertFalse(seed["extractable"])
        self.assertIn("MISSING_SOURCE_ABSTRACT", seed["hard_errors"])

    def test_solution_leak_not_rehabilitated(self):
        result = seed_gate(self.source(), "prior work discusses FocalNet for adaptation", "We propose FocalNet for adaptation")
        self.assertFalse(result["source_matching_allowed"])
        self.assertFalse(result["confirmatory_eligible"])
        self.assertEqual(result["repair_reason"], "EXPLICIT_FOCAL_SOLUTION_UNREPAIRED")

    def test_common_problem_vocabulary_is_not_hard_error(self):
        result = seed_gate(self.source(), "distribution shift generalization", "distribution shift generalization", ["focal_method_leak"])
        self.assertFalse(result["hard_errors"])
        self.assertTrue(result["source_matching_allowed"])

    def test_unknown_dates_stay_unknown(self):
        for value in (None, "UNKNOWN", "AMBIGUOUS", "2025-99-02"):
            self.assertEqual(temporal_membership(value, "T0_COMMON_STRICT"), "UNKNOWN")
        self.assertEqual(temporal_membership("2024-08-31", "T0_COMMON_STRICT"), "DISCOVERED_ON_OR_BEFORE_CUTOFF")
        self.assertEqual(temporal_membership("2024-09-01", "T0_COMMON_STRICT"), "DISCOVERED_AFTER_CUTOFF")

    def test_purity_descriptor_not_probability(self):
        row = annotate(self.source())
        self.assertIsNone(row["numeric_route_purity"])
        self.assertEqual(row["purity_assessment_status"], "NOT_ASSESSED")

    def test_lexical_backend_does_not_fill_semantic_columns(self):
        from collections import Counter
        papers = [{"paper_id": f"E{i}", "year": 2025, "first_public_date": None, "abstract": "distribution shift"} for i in range(2)]
        labels = {p["paper_id"]: {"subfield": "test", "primary_route": "BUILD_IMPROVE", "route_purity_descriptor": "ROUTE_CLEAR"} for p in papers}
        _, idf, inverted = legacy.build_tfidf(["distribution shift"] * 2)
        seed = {"seed_id": "S", "focal_paper_id": "F", "method_masked_question": "distribution shift"}
        rows = lexical_candidates(seed, papers, labels, idf, inverted, [Counter({"distribution": 1, "shift": 1})] * 2,
                                  {"candidate_pool_size": 300, "cosine_floor": .045, "bm25_like_floor": .08})
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["dense_relevance"] is None and r["semantic_reranker_score"] is None for r in rows))
        self.assertTrue(all(r["retrieval_backend"] == "LEXICAL_PROVISIONAL" for r in rows))

    def test_matching_is_max_cardinality_then_cost(self):
        result = exact_matching([("A0", "B0", 1), ("A0", "B1", 2), ("A1", "B0", 2)])
        self.assertEqual(len(result), 2)
        self.assertEqual(sum(cost for a, b, cost in result), 4)

    def test_exact_matcher_vs_exhaustive_small_graphs(self):
        rng = random.Random(17)
        for _ in range(30):
            edges = [(f"A{i}", f"B{j}", rng.randrange(6)) for i in range(3) for j in range(3) if rng.random() < .65]
            best = (0, 0)
            for mask in range(1 << len(edges)):
                chosen = [e for i, e in enumerate(edges) if mask & (1 << i)]
                if len({a for a, b, c in chosen}) != len(chosen) or len({b for a, b, c in chosen}) != len(chosen):
                    continue
                best = min(best, (-len(chosen), sum(c for a, b, c in chosen)))
            result = exact_matching(edges)
            self.assertEqual((-len(result), sum(c for a, b, c in result)), best)
            self.assertEqual(exact_matching(list(reversed(edges))), result)

    def test_no_replacement_and_no_same_source_two_sides(self):
        result = exact_matching([("A0", "B0", 1), ("A0", "B1", 2)])
        self.assertEqual(len(result), 1)
        with self.assertRaises(ValueError):
            exact_matching([("SAME", "SAME", 1)])

    def test_focal_exclusion(self):
        self.assertFalse(seed_gate(self.source(), "problem", "problem", evidence_ids=["FOCAL"])["source_matching_allowed"])
        papers = [{"paper_id": "FOCAL"}]
        seed = {"seed_id": "S", "focal_paper_id": "FOCAL", "method_masked_question": "distribution shift"}
        _, idf, inv = legacy.build_tfidf(["distribution shift", "distribution shift"])
        inv = {key: [(0, value) for idx, value in values if idx == 0] for key, values in inv.items()}
        self.assertEqual(lexical_candidates(seed, papers, {}, idf, inv, [{}], {"candidate_pool_size": 300}), [])

    def test_zero_vs_unrun(self):
        self.assertEqual(coverage_cell("MEASURED", len(exact_matching([])))["max_matched_slots"], 0)
        for state in ("NOT_RUN", "BLOCKED", "MISSING_COVARIATES", "PENDING_REVIEW"):
            self.assertIsNone(coverage_cell(state)["max_matched_slots"])
            with self.assertRaises(ValueError):
                coverage_cell(state, 0)

    def test_exact_packet_fractions_and_balance(self):
        slots = [(f"A{i}", f"B{i}", 1) for i in range(12)]
        for k in (4, 6, 8, 12):
            rows = packets(slots, k)
            if k == 6:
                self.assertNotIn("1/4", {r["alpha"] for r in rows})
                self.assertTrue(all(not r["exact_quarters_supported"] for r in rows))
            for alpha in {r["alpha"] for r in rows}:
                selected = [r for r in rows if r["alpha"] == alpha]
                for slot in range(k):
                    self.assertEqual(sum(slot in r["A_slot_indices"] for r in selected), int(Fraction(alpha) * k))
                self.assertTrue(all(len(set(r["ordered_paper_ids"])) == k for r in selected))

    def test_seed_bank_assignment_denominators_differ(self):
        blocks = [("s1", "R1"), ("s1", "R2"), ("s2", "R1")]
        self.assertEqual(len({seed for seed, pair in blocks}), 2)
        self.assertEqual(len(blocks), 3)
        self.assertNotEqual(len(packets([("A"+str(i), "B"+str(i), 1) for i in range(4)], 4)), len(blocks))

    def test_cached_parser_and_compressed_hash_stable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.html"
            path.write_text('<meta name="citation_title" content="Title"><meta name="citation_publication_date" content="2025-05-01"><p class="paper-abstract"><p>Source &amp; context.</p></p>')
            first = parse_source(path, "https://proceedings.iclr.cc/paper_files/paper/2025/hash/abc-Abstract-Conference.html", 2025)
            second = parse_source(path, first["proceedings_url"], 2025)
            self.assertEqual(first, second)
            self.assertIsNone(first["first_public_date"])
            self.assertEqual(first["abstract"], "Source & context.")
            for name in ("one.jsonl.gz", "two.jsonl.gz"):
                write_jsonl(Path(directory) / name, [first])
            self.assertEqual(digest(Path(directory) / "one.jsonl.gz"), digest(Path(directory) / "two.jsonl.gz"))

    def test_no_generation_clients_in_active_recovery(self):
        import ast
        scripts = Path(__file__).resolve().parents[1] / "scripts"
        for file in scripts.glob("*.py"):
            tree = ast.parse(file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    names = [a.name for a in node.names] + [getattr(node, "module", "") or ""]
                    self.assertFalse(any(any(p in name for p in ("openai", "anthropic", "generation.run", "transformers")) for name in names))


if __name__ == "__main__":
    unittest.main()
