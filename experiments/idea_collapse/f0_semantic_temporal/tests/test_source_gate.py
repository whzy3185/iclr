import hashlib
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import BASE, hash_value, render_evidence, text
from prepare_sources import parse_date
from build_bank import admissible, choose_f1, date_gap, exact_matching, percentile


class SourceGateTests(unittest.TestCase):
    def test_corpus_role_config(self):
        cfg = json.loads((BASE / "config.json").read_text())
        self.assertEqual(cfg["seed_year"], 2026)
        self.assertEqual(cfg["evidence_year"], 2025)
        self.assertEqual(cfg["candidate_k"], 200)
        self.assertFalse(cfg["matching"]["full_abstract_pair_embedding_caliper"])

    def test_date_uses_real_calendar_not_year_subtraction(self):
        self.assertEqual(date_gap("2025-01-01", "2024-12-31"), 1)
        self.assertIsNone(date_gap(None, "2025-01-01"))
        self.assertIsNone(parse_date("2025-99-01"))
        self.assertEqual(parse_date("2025/05/01"), "2025-05-01")

    def test_anonymity_removes_only_outer_metadata(self):
        abstract = "Method X from ICLR 2025 at https://example.org remains scientific content."
        rendered = render_evidence([{"abstract_text": abstract, "paper_id": "SECRET_ID", "title": "SECRET_TITLE", "rank": "SECRET_RANK"}])
        self.assertEqual(rendered, abstract)
        self.assertNotIn("SECRET_", rendered)

    def test_unicode_whitespace_transform_is_idempotent(self):
        original = "cafe\u0301  \n  method"
        self.assertEqual(text(text(original)), text(original))
        self.assertEqual(text(original), "caf\u00e9 method")

    def test_matching_objective_counterexample(self):
        result = exact_matching([("A0", "B0", 1), ("A0", "B1", 2), ("A1", "B0", 2)])
        self.assertEqual(len(result), 2)
        self.assertEqual(sum(e[2] for e in result), 4)

    def test_matching_cannot_reuse_source(self):
        with self.assertRaises(ValueError):
            exact_matching([("same", "same", 1)])

    def test_missing_covariate_not_zero_cost(self):
        cfg = json.loads((BASE / "config.json").read_text())["matching"]
        a = {"dense_percentile": .1, "reranker_percentile": .1, "tokens": 100, "date": None}
        b = {**a, "date": "2025-05-01"}
        cost, features, reasons = admissible(a, b, cfg)
        self.assertIsNone(cost)
        self.assertIn("MISSING_DATE", reasons)

    def test_route_content_not_a_cost_input(self):
        cfg = json.loads((BASE / "config.json").read_text())["matching"]
        a = {"dense_percentile": .1, "reranker_percentile": .1, "tokens": 100, "date": "2025-05-01", "abstract": "Build a method"}
        b = {**a, "abstract": "Diagnose a different failure mechanism"}
        self.assertEqual(admissible(a, b, cfg)[0], 0)

    def test_stable_rank_ties(self):
        self.assertEqual(percentile([1, 1, 0]).tolist(), [0, .5, 1])

    def test_f1_route_balance_and_seed_partition(self):
        blocks = []
        for i in range(500):
            for route in ("R1", "R2", "R3", "R4"):
                blocks.append({"seed_id": f"S{i}", "route_pair": route, "topic": "topic"+str(i%3),
                    "mean_reranker_score": 1., "mean_cost_units": 100000, "max_matched_slots": 4, "lexical_disagreement": "False"})
        calibration = choose_f1(blocks, 24, True)
        certification = choose_f1(blocks, 96, False)
        self.assertEqual(len({b["seed_id"] for b in calibration}), 24)
        self.assertEqual(len({b["seed_id"] for b in certification}), 96)
        self.assertFalse({b["seed_id"] for b in calibration} & {b["seed_id"] for b in certification})
        self.assertEqual({b["route_pair"] for b in calibration}, {"R1", "R2", "R3", "R4"})
        self.assertEqual(calibration, choose_f1(list(reversed(blocks)), 24, True))


if __name__ == "__main__":
    unittest.main()
