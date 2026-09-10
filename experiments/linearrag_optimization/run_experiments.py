#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(args):
    print("+", " ".join(map(str, args)))
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    output = ROOT / "artifacts" / "synthetic_noise_summary.json"
    run([sys.executable, "-m", "pytest", "-q", "tests"])
    run([sys.executable, "benchmarks/tier_consistency_regression.py"])
    run([sys.executable, "benchmarks/multipath_backend_mismatch_demo.py"])
    run([sys.executable, "benchmarks/seed_disambiguation_demo.py"])
    run([sys.executable, "benchmarks/passage_scoring_benchmark.py"])
    run([
        sys.executable,
        "benchmarks/synthetic_noise_benchmark.py",
        "--trials", "100",
        "--top-k", "5",
        "--output", str(output),
    ])


if __name__ == "__main__":
    main()
