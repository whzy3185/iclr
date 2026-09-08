"""R0: inventory and preserve observed local source artifacts, without a full rerun."""

import argparse
from collections import Counter
import json
from pathlib import Path
import zipfile

from recovery_common import BASE, ROOT, SPECS, digest, git, parse_source, source_links, write_json, write_jsonl


def preserve(source, destination):
    source, destination = Path(source), Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    cache_rows, corpus_counts = [], {}
    for year in (2025, 2026):
        links = source_links(source / f"iclr{year}_index.html", year)
        records = []
        for url in links:
            key = f"_source_cache/iclr{year}_abstract_pages/" + url.rsplit("/", 1)[-1]
            record = parse_source(source / key, url, year)
            records.append(record)
            cache_rows.append({"url": url, "cache_key": key, "year": year,
                               "sha256": record["source_page_sha256"], "bytes": record["source_bytes"],
                               "retrieval_status": "CACHED" if record["source_page_sha256"] else "MISSING",
                               "parse_status": record["parse_status"], "hard_errors": record["hard_errors"]})
        corpus_counts[str(year)] = {"official": len(links), "cached": sum(r["source_page_sha256"] is not None for r in records),
                                    "parsed": sum(r["parse_status"] == "MEASURED" for r in records)}
        write_jsonl(destination / f"iclr{year}_papers.jsonl.gz", records)
    write_jsonl(destination / "raw_sources_manifest.jsonl.gz", cache_rows)
    archive_files = [p for p in sorted(source.rglob("*")) if p.is_file()
                     and p.suffix in {".md", ".json", ".jsonl", ".csv", ".txt", ".py"}
                     and "_source_cache" not in p.parts and "source_archives" not in p.parts]
    files = []
    with zipfile.ZipFile(destination / "first_failed_run.zip", "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in archive_files:
            relative = str(path.relative_to(source))
            archive.writestr(zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0)), path.read_bytes(),
                             compress_type=zipfile.ZIP_DEFLATED)
            files.append({"path": relative, "sha256": digest(path), "bytes": path.stat().st_size})
    with (source / "seed_candidates.jsonl").open() as handle:
        old_gate = Counter(json.loads(line)["seed_status_provisional"] for line in handle)
    historical = {"status": "INCOMPLETE_GATE_SHORT_CIRCUIT", "reported_seed_states": dict(old_gate),
                  "matching_executed": False, "matching_count": None,
                  "interpretation": "empty first-run tables are not measured zero or scientific infeasibility",
                  "source_output_version_alignment": "UNKNOWN: committed script includes a later correction",
                  "files": files}
    write_json(destination / "first_run_manifest.json", historical)
    audit = []
    for year in (2025, 2026):
        from recovery_common import read_jsonl
        records = list(read_jsonl(destination / f"iclr{year}_papers.jsonl.gz"))
        audit.extend(sorted(records, key=lambda r: r["paper_id"])[:10])
    write_jsonl(destination / "pre_matching_audit_excerpt.jsonl", audit)
    manifest = {"baseline_main_sha": "b9cbbfdf0bafcf30adc7b8e261fdad6f08eb0ff8",
                "implementation_parent_sha": "049a313ed2900f1acd9c2d6673abd2124280b85f",
                "source_snapshot_sha": "e3eb75948dcd6745eb77f1def0ad0898cb1c839b",
                "branch": git("branch", "--show-current"), "git_commit": git("rev-parse", "HEAD"),
                "spec_hashes": {path: digest(ROOT / path) for path in SPECS},
                "corpus_counts": corpus_counts, "network_requests": 0,
                "tests": "legacy tests not found; recovery tests not yet implemented at R0",
                "audit_selection": "first 10 official IDs per year, before matching",
                "legacy_script_sha256": digest(BASE / "legacy/f0_source_only_audit.py"),
                "artifacts": {p.name: {"sha256": digest(p), "bytes": p.stat().st_size} for p in sorted(destination.iterdir()) if p.is_file()}}
    write_json(destination / "R0_MANIFEST.json", manifest)
    print(json.dumps(manifest["corpus_counts"], indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    preserve(args.source_root, args.output)
