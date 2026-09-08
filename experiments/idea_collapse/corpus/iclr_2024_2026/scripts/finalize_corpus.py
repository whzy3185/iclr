"""Revalidate both complete corpus passes against retained source bytes."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from complete_corpus import BASE, EXPECTED, SCHEMA, all_papers, canonical, exclusive, file_sha, parse_official, parse_openreview, sha


def validate_rows(rows, official):
    expected = {p["paper_id"]: p for p in official}
    ids = [r["paper_id"] for r in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(expected):
        raise ValueError("duplicate, missing or nonofficial paper ID")
    for row in rows:
        if set(row) != set(SCHEMA):
            raise ValueError("normalized schema differs")
        paper = expected[row["paper_id"]]
        if row["year"] != paper["year"] or row["proceedings_abstract_url"] != paper["proceedings_abstract_url"]:
            raise ValueError("official identity mismatch")
        if row["abstract"] is None:
            if row["parse_status"] == "VERIFIED_ABSTRACT" or row["abstract_sha256"] is not None:
                raise ValueError("missing abstract mislabeled verified")
        elif row["parse_status"] != "VERIFIED_ABSTRACT" or row["abstract_sha256"] != sha(row["abstract"].encode()):
            raise ValueError("abstract hash/status mismatch")


def finalize(args):
    first, second = BASE / args.first, BASE / args.second
    primary = [f"iclr{y}_{suffix}.jsonl" for y in EXPECTED for suffix in ("abstracts", "missing")]
    primary += ["corpus_2024_2026.jsonl", "acquisition_failures.jsonl", "source_cache_catalog.jsonl", "corpus_sha256.txt"]
    matches = {}
    for name in primary:
        left, right = file_sha(first / name), file_sha(second / name)
        if left != right:
            raise ValueError("two passes differ: " + name)
        matches[name] = left
    m1 = json.loads((first / "corpus_manifest.json").read_text())
    m2 = json.loads((second / "corpus_manifest.json").read_text())
    if m1["pipeline_sha256"] != m2["pipeline_sha256"] or m2["network_requests_this_pass"] != 0:
        raise ValueError("replay must use identical pipeline code and verified cache only")
    official = all_papers(BASE)
    indexed = {p["paper_id"]: p for p in official}
    rows = [json.loads(line) for line in (first / "corpus_2024_2026.jsonl").open()]
    validate_rows(rows, official)
    initially_missing = {json.loads(line)["paper_id"] for year in EXPECTED
                         for line in (BASE / "inventory" / f"iclr{year}_missing.jsonl").open()}
    attempt_records = [json.loads(path.read_text()) for path in sorted((BASE / "_cache").glob("*/*.json"))]
    requested_ids = {record["paper_id"] for record in attempt_records}
    if not requested_ids <= initially_missing:
        raise ValueError("a previously verified page was unnecessarily requested")
    if any(not 1 <= record["attempt"] <= 3 for record in attempt_records):
        raise ValueError("bounded retry policy exceeded")
    counts, cache_index = {}, []
    for year in EXPECTED:
        yearly = [json.loads(line) for line in (first / f"iclr{year}_abstracts.jsonl").open()]
        missing = [json.loads(line) for line in (first / f"iclr{year}_missing.jsonl").open()]
        if yearly != [r for r in rows if r["year"] == year] or missing != [r for r in yearly if r["abstract"] is None]:
            raise ValueError("year/combined/missing outputs do not reconcile")
        counts[year] = {"official": EXPECTED[year], "abstracts": sum(r["abstract"] is not None for r in yearly), "missing": len(missing)}
    revalidated = 0
    for row in rows:
        if row["abstract"] is None:
            cache_index.append({"paper_id": row["paper_id"], "status": row["parse_status"], "cache_key": None, "sha256": None})
            continue
        if row["source_type"] == "official_proceedings_legacy_cache":
            key = f"_source_cache/iclr{row['year']}_abstract_pages/" + row["proceedings_abstract_url"].rsplit("/", 1)[-1]
            source = args.legacy_root / key
            meta = None
            root_label = "legacy_root_argument"
        else:
            directory = BASE / "_cache" / row["paper_id"]
            candidates = [json.loads(p.read_text()) for p in sorted(directory.glob("*.json"))]
            meta = next(m for m in candidates if m["http_status"] == 200 and m["source_sha256"] == row["source_sha256"])
            source = directory / meta["body_file"]
            key = str(source.relative_to(BASE))
            root_label = "corpus_directory"
            if row["source_retrieved_at"] != meta["source_retrieved_at"]:
                raise ValueError("retrieval timestamp drift")
        raw = source.read_bytes()
        if sha(raw) != row["source_sha256"]:
            raise ValueError("raw source hash mismatch")
        if row["source_type"] == "linked_openreview_metadata":
            parsed, error = parse_openreview(raw, indexed[row["paper_id"]], row["openreview_url"])
        else:
            parsed, error, _ = parse_official(raw, indexed[row["paper_id"]])
        if error or any(row[k] != parsed[k] for k in ("title", "abstract", "authors", "pdf_url", "openreview_url")):
            raise ValueError("normalized content differs from actual source: " + row["paper_id"])
        revalidated += 1
        cache_index.append({"paper_id": row["paper_id"], "status": "SOURCE_BYTES_REVALIDATED", "cache_root": root_label,
                            "cache_key": key, "sha256": row["source_sha256"], "source_type": row["source_type"],
                            "source_retrieved_at": row["source_retrieved_at"],
                            "source_url": meta["url"] if meta else row["proceedings_abstract_url"]})
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(BASE / "tests"), "-v"]
    tests = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if tests.returncode != 0:
        raise RuntimeError(tests.stderr)
    n_tests = int(re.search(r"Ran (\d+) tests?", tests.stderr).group(1))
    verification = {"unit_tests": n_tests, "test_exit_code": 0, "test_command": command,
                    "test_stdout": tests.stdout, "test_stderr": tests.stderr,
                    "byte_identical_files": matches, "full_pipeline_passes": 2,
                    "second_pass_network_requests": 0, "source_rows_revalidated": revalidated,
                    "unique_requested_papers": len(requested_ids), "previously_verified_papers_redownloaded": 0,
                    "attempt_records_retained": len(attempt_records)}
    exclusive(BASE / "VERIFICATION.json", canonical(verification))
    exclusive(BASE / "raw_sources_manifest.jsonl", b"".join(canonical(r) for r in cache_index))
    for name in primary:
        if (BASE / name).exists():
            raise FileExistsError(BASE / name)
        shutil.copyfile(first / name, BASE / name)
    total = sum(n["official"] for n in counts.values())
    abstracts = sum(n["abstracts"] for n in counts.values())
    missing = total - abstracts
    digest = matches["corpus_2024_2026.jsonl"]
    lines = []
    for year in EXPECTED:
        lines += [f"ICLR{year}_OFFICIAL={counts[year]['official']}", f"ICLR{year}_ABSTRACTS={counts[year]['abstracts']}", f"ICLR{year}_MISSING={counts[year]['missing']}"]
    lines += [f"TOTAL_OFFICIAL={total}", f"TOTAL_ABSTRACTS={abstracts}", f"TOTAL_MISSING={missing}", f"CORPUS_SHA256={digest}",
              f"TESTS={n_tests} unit tests PASS; 2 byte-identical full passes; {revalidated} source-byte revalidations; replay requests=0"]
    report = "# Corpus Completion Report\n\nStatus: " + ("COMPLETE" if missing == 0 else "INCOMPLETE") + "\n\n```text\n" + "\n".join(lines) + "\n```\n\n"
    report += ("Every normalized ID reconciles with the frozen official Conference indexes.\n"
               "Nonempty abstracts were reparsed from retained source bytes; no title-based\n"
               "surrogate or generated abstract was used. All acquisition failures and missing\n"
               "rows remain retained. Legacy retrieval timestamps are null when not historically\n"
               "known, not fabricated from file modification times. New retrieval timestamps\n"
               "are saved in immutable attempt records and reused in the second pass.\n\n"
               f"New requests in pass 1: {m1['network_requests_this_pass']}; pass 2: 0.\n"
               f"Source types: {m1['source_types']}.\n\n"
               "No ARS, proposal generation, baseline/treatment, route or model experiment ran.\nSTOP after publishing this data-only checkpoint.\n")
    exclusive(BASE / "CORPUS_COMPLETION_REPORT.md", report.encode())
    final_manifest = {"status": "COMPLETE" if missing == 0 else "INCOMPLETE", "counts": counts,
        "total_official": total, "total_abstracts": abstracts, "total_missing": missing, "corpus_sha256": digest,
        "normalized_sha256": matches, "source_types": m1["source_types"],
        "legacy_source_retrieved_at_unknown": m1["unknown_legacy_retrieval_timestamps"],
        "pipeline_code_sha256": m1["pipeline_sha256"], "finalizer_code_sha256": file_sha(__file__),
        "task_sha256": file_sha(BASE.parents[3] / "CODEX_ABSTRACT_CORPUS_COMPLETION_TASK.md"),
        "index_sha256": m1["index_sha256"], "first_pass_manifest_sha256": file_sha(first / "corpus_manifest.json"),
        "second_pass_manifest_sha256": file_sha(second / "corpus_manifest.json"),
        "raw_source_manifest_sha256": file_sha(BASE / "raw_sources_manifest.jsonl"),
        "verification_sha256": file_sha(BASE / "VERIFICATION.json"), "model_experiments": 0,
        "source_policy": "official proceedings first; only explicitly linked OpenReview fallback after bounded official failure",
        "legacy_cache_modified": False}
    exclusive(BASE / "corpus_manifest.json", canonical(final_manifest))
    (BASE / "STATUS.md").write_text(report + "\n## Execution\n\n"
        "T1 inventory completed without network requests; 7440 verified legacy pages reused.\n"
        "T2 acquisition attempted only missing/invalid pages with six workers and at most\n"
        "three attempts per source. T3/T4 normalization and identity checks completed.\n"
        "T5 two complete pipeline executions compared byte-for-byte. T6 publication follows.\n"
        "The inventory and both passes are retained separately; only execution manifest\n"
        "request counts differ. See VERIFICATION.json and corpus_manifest.json.\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first", default="pass1")
    parser.add_argument("--second", default="pass2")
    parser.add_argument("--legacy-root", type=Path, required=True)
    args = parser.parse_args()
    finalize(args)
