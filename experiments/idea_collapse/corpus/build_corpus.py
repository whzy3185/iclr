"""Validate normalized source records and freeze an immutable candidate table.

This tool does not claim source verification or turn mock fixtures into a corpus.
Acquisition and scientific inclusion rules must be approved separately.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from ..generation.provenance import canonical_bytes, file_hash, object_hash, write_exclusive
from ..generation.schema import strict_json


DOMAINS = {"model_editing", "agents_tool_use", "post_training_optimization"}


def validate_records(records):
    seen = set()
    if not records:
        raise ValueError("empty corpus")
    for record in records:
        required = {"paper_id", "year", "title", "abstract", "keywords", "openreview_url",
                    "domain_tags", "provenance"}
        if not required <= set(record):
            raise ValueError("missing corpus field")
        if record["paper_id"] in seen or record["year"] not in (2024, 2025, 2026):
            raise ValueError("duplicate ID or out-of-scope year")
        if any(not isinstance(record[k], str) or not record[k].strip()
               for k in ("paper_id", "title", "abstract")):
            raise ValueError("missing paper text")
        if not isinstance(record["keywords"], list) or any(not isinstance(k, str) for k in record["keywords"]):
            raise ValueError("invalid keywords")
        tags = record["domain_tags"]
        if not isinstance(tags, list) or not tags or len(set(tags)) != len(tags) or not set(tags) <= DOMAINS:
            raise ValueError("invalid domain tags")
        url = urlparse(record["openreview_url"])
        if url.scheme != "https" or url.hostname != "openreview.net" or url.path != "/forum":
            raise ValueError("expected OpenReview forum URL")
        provenance = record["provenance"]
        if not isinstance(provenance, dict) or not {"source_url", "retrieved_at", "topic_rule"} <= set(provenance):
            raise ValueError("missing acquisition/topic provenance")
        seen.add(record["paper_id"])


def build(source, output, manifest):
    source, output, manifest = map(Path, (source, output, manifest))
    if output.exists() or manifest.exists() or output.resolve() == manifest.resolve():
        raise ValueError("outputs must be new and distinct")
    records = [strict_json(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    validate_records(records)
    records.sort(key=lambda row: (row["year"], row["paper_id"]))
    counts = Counter(tag for record in records for tag in record["domain_tags"])
    table = b"".join(canonical_bytes(row) for row in records)
    report = {"kind": "corpus_candidate_NOT_pilot_authorization",
              "created_at": datetime.now(timezone.utc).isoformat(),
              "input_sha256": file_hash(source), "records": len(records),
              "domain_counts": dict(counts), "taxonomy_sha256": object_hash([
                  (r["paper_id"], r["domain_tags"], r["provenance"]["topic_rule"]) for r in records]),
              "short_domains": sorted(d for d in DOMAINS if counts[d] < 150),
              "source_verification": "not_performed_by_this_validator"}
    write_exclusive(output, table)
    report["corpus_sha256"] = file_hash(output)
    write_exclusive(manifest, canonical_bytes(report))
    return report


def main():
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.input, args.output, args.manifest), indent=2))


if __name__ == "__main__":
    main()
