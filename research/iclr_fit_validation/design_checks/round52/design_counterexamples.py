"""Deterministic design counterexamples, NOT LLM/ICLR experimental results.

Python >=3.10; standard library only; no networking, models, or repository data.
Run: python design_counterexamples.py --output design_counterexamples.json
Test: python design_counterexamples.py --test
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import unittest


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    exp_x = math.exp(x)
    return exp_x / (1.0 + exp_x)


def logit(p: float) -> float:
    if not 0.0 < p < 1.0:
        raise ValueError("logit requires a probability strictly between 0 and 1")
    return math.log(p / (1.0 - p))


def constant_logit_slope() -> list[dict[str, float | None]]:
    """p(A|b,alpha)=sigmoid(b + beta*(2*alpha-1)); beta=1 for ALL b."""
    beta = 1.0
    rows = []
    for b in (0.0, 1.0, 2.0, 3.0):
        low, high = sigmoid(b - beta), sigmoid(b + beta)
        crossing = 0.5 - b / (2.0 * beta)
        rows.append({
            "baseline_log_odds": b,
            "assumed_no_context_probability_A": sigmoid(b),
            "p_A_at_alpha_0": low,
            "p_A_at_alpha_1": high,
            "probability_difference": high - low,
            "log_odds_difference": logit(high) - logit(low),
            "beta_identical_across_baselines": beta,
            "algebraic_crossing": crossing,
            "crossing_in_unit_interval": crossing if 0 <= crossing <= 1 else None,
        })
    return rows


def post_treatment_selection() -> dict:
    """Toy counts: both arms have 50 A + 50 B; copying differs by arm/route."""
    arms = {
        "alpha_0": {"A": 50, "B": 50, "copy_A": 5, "copy_B": 25},
        "alpha_1": {"A": 50, "B": 50, "copy_A": 25, "copy_B": 5},
    }
    rows = {}
    for arm, counts in arms.items():
        retained_A = counts["A"] - counts["copy_A"]
        retained_B = counts["B"] - counts["copy_B"]
        rows[arm] = {
            **counts,
            "p_A_full_sample": counts["A"] / (counts["A"] + counts["B"]),
            "p_A_after_copy_exclusion": retained_A / (retained_A + retained_B),
        }
    return {
        "arms": rows,
        "full_sample_contrast": rows["alpha_1"]["p_A_full_sample"] - rows["alpha_0"]["p_A_full_sample"],
        "postselection_contrast": rows["alpha_1"]["p_A_after_copy_exclusion"] - rows["alpha_0"]["p_A_after_copy_exclusion"],
    }


def compressed_outcome() -> dict:
    """Equal p(A)-p(B) does not imply equal output distributions."""
    left = {"A": 0.4, "B": 0.4, "MIXED": 0.2, "NEITHER": 0.0, "INVALID": 0.0}
    right = {"A": 0.1, "B": 0.1, "MIXED": 0.8, "NEITHER": 0.0, "INVALID": 0.0}
    return {
        "alpha_0": left, "alpha_1": right,
        "directional_contrast": (right["A"] - right["B"]) - (left["A"] - left["B"]),
        "mixed_probability_change": right["MIXED"] - left["MIXED"],
        "total_variation_distance": 0.5 * sum(abs(left[k] - right[k]) for k in left),
    }


def matching_objective() -> dict:
    """Small counterexample: greedy min edge is not maximum cardinality.

    Production code needs max-cardinality then min-cost matching; this enumerator
    is intentionally only a tiny exact test fixture.
    """
    edges = [("A0", "B0", 1.0), ("A0", "B1", 2.0), ("A1", "B0", 2.0)]
    greedy, used_A, used_B = [], set(), set()
    for a, b, cost in sorted(edges, key=lambda e: (e[2], e[0], e[1])):
        if a not in used_A and b not in used_B:
            greedy.append((a, b, cost))
            used_A.add(a)
            used_B.add(b)
    candidates = []
    for mask in range(1 << len(edges)):
        chosen = [edge for i, edge in enumerate(edges) if mask & (1 << i)]
        if len({e[0] for e in chosen}) == len(chosen) == len({e[1] for e in chosen}):
            candidates.append(chosen)
    best = min(candidates, key=lambda c: (-len(c), sum(e[2] for e in c), c))
    optional_min_cost = min(candidates, key=lambda c: (sum(e[2] for e in c), c))
    return {
        "edges": edges,
        "greedy": greedy, "greedy_cardinality": len(greedy),
        "lexicographic_optimum": best, "maximum_cardinality": len(best),
        "minimum_cost_at_maximum_cardinality": sum(e[2] for e in best),
        "minimum_cost_without_cardinality_constraint": optional_min_cost,
    }


def quarter_feasibility() -> list[dict]:
    rows = []
    for k in (4, 6, 8, 12):
        rows.append({"k": k, "quarter_count": k / 4,
                     "supports_exact_quarters": k % 4 == 0})
    return rows


def build_report() -> dict:
    return {
        "artifact_type": "SYNTHETIC_DESIGN_COUNTEREXAMPLES_NOT_MODEL_RESULTS",
        "scientific_generations_performed": 0,
        "network_calls": 0,
        "assumptions": "User-specified toy distributions; no fitted values or real ICLR observations.",
        "constant_logit_slope": constant_logit_slope(),
        "post_treatment_selection": post_treatment_selection(),
        "compressed_outcome": compressed_outcome(),
        "matching_objective": matching_objective(),
        "quarter_feasibility": quarter_feasibility(),
    }


class DesignTests(unittest.TestCase):
    def test_identical_logit_effect_different_probability_effect(self):
        rows = constant_logit_slope()
        for row in rows:
            self.assertAlmostEqual(row["log_odds_difference"], 2.0)
        self.assertGreater(rows[0]["probability_difference"], rows[-1]["probability_difference"])

    def test_crossing_is_not_forced_inside_support(self):
        rows = constant_logit_slope()
        self.assertEqual(rows[0]["crossing_in_unit_interval"], 0.5)
        self.assertIsNone(rows[2]["crossing_in_unit_interval"])

    def test_copy_filter_creates_effect(self):
        result = post_treatment_selection()
        self.assertEqual(result["full_sample_contrast"], 0.0)
        self.assertAlmostEqual(result["postselection_contrast"], -2.0 / 7.0)

    def test_scalar_null_can_hide_distribution_change(self):
        result = compressed_outcome()
        self.assertEqual(result["directional_contrast"], 0.0)
        self.assertAlmostEqual(result["total_variation_distance"], 0.6)

    def test_cardinality_precedes_cost(self):
        result = matching_objective()
        self.assertEqual(result["greedy_cardinality"], 1)
        self.assertEqual(result["maximum_cardinality"], 2)
        self.assertEqual(result["minimum_cost_without_cardinality_constraint"], [])

    def test_k6_quarters_are_not_rounded(self):
        cases = {row["k"]: row for row in quarter_feasibility()}
        self.assertFalse(cases[6]["supports_exact_quarters"])
        self.assertTrue(cases[8]["supports_exact_quarters"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(DesignTests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if result.wasSuccessful() else 1)
    payload = json.dumps(build_report(), indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation avoids silently overwriting previous audit evidence.
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
