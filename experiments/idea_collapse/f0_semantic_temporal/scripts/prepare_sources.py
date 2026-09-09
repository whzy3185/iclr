"""Reconcile, preserve masking, inventory dated sources and remove outer metadata."""

import argparse
from collections import Counter
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.request import ProxyHandler, build_opener, Request

from common import BASE, ROOT, CORPUS, RECOVERY, git, hash_value, read_rows, render_evidence, save, sha, text

sys.path.insert(0, str(RECOVERY / "scripts"))
from recovery_algorithms import make_seed, PAIRS, legacy
sys.path.insert(0, str(CORPUS / "scripts"))
from complete_corpus import Page


def parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value.replace("/", "-")[:10]).isoformat()
    except (ValueError, AttributeError):
        return None


def source_path(row, legacy_root):
    if row["source_type"] == "official_proceedings_legacy_cache":
        return legacy_root / f"_source_cache/iclr{row['year']}_abstract_pages" / row["proceedings_abstract_url"].rsplit("/", 1)[-1]
    directory = CORPUS / "_cache" / row["paper_id"]
    for meta_path in sorted(directory.glob("*.json")):
        m = json.loads(meta_path.read_text())
        if m.get("source_sha256") == row["source_sha256"] and m.get("http_status") == 200:
            return directory / m["body_file"]
    raise FileNotFoundError(row["paper_id"])


def prepare(args):
    config = json.loads((BASE / "config.json").read_text())
    actual = sha(CORPUS / "corpus_2024_2026.jsonl")
    if actual != config["corpus_sha256"]:
        raise ValueError("CORPUS HASH MISMATCH; STOP")
    corpus = read_rows(CORPUS / "corpus_2024_2026.jsonl")
    counts = Counter(p["year"] for p in corpus)
    if counts != {2024: 2260, 2025: 3703, 2026: 5351} or len({p["paper_id"] for p in corpus}) != 11314 or any(not p["abstract"] for p in corpus):
        raise ValueError("corpus denominator/missingness mismatch")
    previous_path = RECOVERY / "runs/F0R-9f61bff4538465a7a96f/seed_candidates.jsonl.gz"
    previous = {p["seed_id"]: p for p in read_rows(previous_path)}
    seeds = []
    unchanged = rebuilt = 0
    for p in corpus:
        if p["year"] != 2026:
            continue
        sid = "SEED_" + p["paper_id"]
        if previous[sid]["extractable"]:
            s = previous[sid]
            unchanged += 1
        else:
            s = make_seed({**p, "parse_status": "MEASURED", "hard_errors": []})
            rebuilt += 1
        seeds.append(s)
    evidence = [p for p in corpus if p["year"] == 2025]
    save(BASE / "seeds.jsonl", seeds, rows=True)
    save(BASE / "evidence.jsonl", evidence, rows=True)
    save(BASE / "route_definitions.json", {"pairs": PAIRS, "definitions": legacy.ROUTE_DEFS,
        "source": "preserved recovery implementation", "provisional": True})
    reconciliation = {"base_commit": config["base_commit"], "task_commit": config["task_commit"],
        "task_sha256": sha(ROOT / "CODEX_F0_SEMANTIC_TEMPORAL_ANONYMIZATION_TASK.md"),
        "corpus_sha256": actual, "counts": dict(counts), "unique_ids": 11314, "missing_abstracts": 0,
        "evidence_year": 2025, "seed_year": 2026, "auxiliary_2024_used_in_evidence": False,
        "previous_seed_file_sha256": sha(previous_path), "unchanged_available_seeds": unchanged,
        "formerly_missing_seeds_rebuilt_by_same_masking": rebuilt,
        "source_matching_allowed": sum(s["source_matching_allowed"] for s in seeds),
        "masking_code_sha256": sha(RECOVERY / "legacy/f0_source_only_audit.py")}
    save(BASE / "T0_INPUT_RECONCILIATION.json", reconciliation)
    records, failures, arxiv_links = [], [], []
    for p in evidence + [p for p in corpus if p["year"] == 2026]:
        path = source_path(p, args.legacy_root)
        if sha(path) != p["source_sha256"]:
            raise ValueError("raw source changed")
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        events = []
        publication = parse_date(page.meta.get("citation_publication_date", [None])[0])
        if publication:
            events.append({"date": publication, "date_source_type": "OFFICIAL_PROCEEDINGS_PUBLICATION",
                "url": p["proceedings_abstract_url"], "source_field": "citation_publication_date",
                "source_retrieved_at": p["source_retrieved_at"], "source_sha256": p["source_sha256"]})
        links = sorted(set(re.findall(r"https?://arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", " ".join(page.links))))
        for identifier in links:
            arxiv_links.append({"paper_id": p["paper_id"], "title": p["title"], "arxiv_id": identifier})
        records.append({"paper_id": p["paper_id"], "year": p["year"], "earliest_public_date": min((e["date"] for e in events), default=None),
            "date_events": events, "status": "FALLBACK_ONLY" if events else "UNKNOWN",
            "history_exhaustive": False, "earlier_source_search": "linked arxiv scan; OpenReview bulk unavailable (403 challenge)",
            "raw_source_sha256": p["source_sha256"]})
    indexed = {r["paper_id"]: r for r in records}
    opener = build_opener(ProxyHandler({"https": args.proxy, "http": args.proxy}))
    for candidate in arxiv_links:
        identifier = candidate["arxiv_id"]
        url = "https://arxiv.org/abs/" + identifier
        cache = BASE / "temporal/raw" / (identifier + ".html")
        try:
            if not cache.exists():
                with opener.open(Request(url, headers={"User-Agent": "F0-source-date-audit/1.0"}), timeout=20) as response:
                    raw = response.read(2_000_000)
                cache.write_bytes(raw)
                save(cache.with_suffix(".receipt.json"), {"url": url, "retrieved_at": datetime.now(timezone.utc).isoformat(), "sha256": sha(cache)})
            raw_text = cache.read_text(encoding="utf-8")
            page = Page()
            page.feed(raw_text)
            title = page.meta.get("citation_title", [""])[0]
            if text(title).casefold() != text(candidate["title"]).casefold():
                raise ValueError("ARXIV_LINK_IDENTITY_MISMATCH")
            match = re.search(r"\[v1\]\s*([A-Za-z]+,\s*\d{1,2}\s+[A-Za-z]+\s+\d{4}\s+\d{2}:\d{2}:\d{2}\s+(?:UTC|GMT))", re.sub(r"<[^>]+>", " ", raw_text))
            if not match:
                raise ValueError("ARXIV_V1_PUBLIC_DATE_UNRESOLVED")
            value = parsedate_to_datetime(match.group(1)).date().isoformat()
            receipt = json.loads(cache.with_suffix(".receipt.json").read_text())
            row = indexed[candidate["paper_id"]]
            row["date_events"].append({"date": value, "date_source_type": "ARXIV_V1_PUBLIC_SUBMISSION", "url": url,
                "source_field": "Submission history [v1]", "source_retrieved_at": receipt["retrieved_at"], "source_sha256": sha(cache)})
            row["earliest_public_date"] = min(e["date"] for e in row["date_events"])
            row["status"] = "EARLIER_SOURCE_VERIFIED"
        except Exception as error:
            failures.append({**candidate, "url": url, "status": "UNRESOLVED", "reason": str(error)})
    failures.append({"source": "OpenReview public API bulk lookup", "status": "BLOCKED", "http_status": 403,
        "reason": "ChallengeRequiredError; not bypassed; no claim of per-paper successful search", "receipt": "temporal/raw/openreview_bulk_403.json",
        "sha256": sha(BASE / "temporal/raw/openreview_bulk_403.json")})
    save(BASE / "temporal/earliest_public_dates.jsonl", sorted(records, key=lambda r: r["paper_id"]), rows=True)
    save(BASE / "temporal/temporal_failures.jsonl", failures, rows=True)
    temporal_summary = {str(year): {"total": sum(r["year"] == year for r in records),
        "date_known": sum(r["year"] == year and r["earliest_public_date"] is not None for r in records),
        "status_counts": dict(Counter(r["status"] for r in records if r["year"] == year))} for year in (2025, 2026)}
    save(BASE / "temporal/temporal_summary.json", {"coverage": temporal_summary, "linked_arxiv_candidates": len(arxiv_links),
        "rule": "minimum verified date discovered; not a proof that no earlier version exists",
        "limitation": "proceedings fallback alone cannot certify actual historical evidence availability before the seed"})
    anonymous = [{"internal_key": hash_value(p["paper_id"])[:24], "abstract_text": text(p["abstract"]),
                  "abstract_sha256": hashlib.sha256(text(p["abstract"]).encode()).hexdigest()} for p in evidence]
    save(BASE / "anonymization/anonymous_evidence.jsonl", anonymous, rows=True)
    save(BASE / "anonymization/anonymization_manifest.json", {"transform": "NFC + whitespace only; no semantic rewriting",
        "render": "abstract_text only; internal key/hash never rendered", "evidence_count": len(anonymous),
        "source_to_internal": {p["paper_id"]: a["internal_key"] for p, a in zip(evidence, anonymous)},
        "input_corpus_sha256": actual})
    sentinel = {"abstract_text": "A scientific method from 2025 keeps https://example.org as content.", "title": "SECRET_TITLE",
                "authors": "SECRET_AUTHOR", "venue": "SECRET_VENUE", "year": "SECRET_YEAR", "url": "SECRET_URL",
                "paper_id": "SECRET_ID", "score": "SECRET_SCORE", "rank": "SECRET_RANK", "database": "SECRET_DATABASE"}
    rendered = render_evidence([sentinel])
    if rendered != sentinel["abstract_text"] or any(str(v) in rendered for k, v in sentinel.items() if k != "abstract_text"):
        raise ValueError("metadata leak in renderer")
    save(BASE / "anonymization/leak_audit.json", {"status": "PASS_METADATA_TEMPLATE_TEST", "metadata_fields_tested": 9,
        "abstracts_exactly_preserved_after_declared_normalization": len(anonymous),
        "abstracts_with_intrinsic_urls": sum(bool(re.search(r"https?://", a["abstract_text"])) for a in anonymous),
        "abstracts_with_intrinsic_years": sum(bool(re.search(r"\b20\d{2}\b", a["abstract_text"])) for a in anonymous),
        "intrinsic_content_identifiers": "RETAINED; metadata anonymity is not a guarantee of unidentifiability"})
    print(json.dumps({"T0": reconciliation, "T1": temporal_summary, "T4": len(anonymous)}, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--legacy-root", type=Path, required=True)
    p.add_argument("--proxy", default="http://127.0.0.1:10808")
    prepare(p.parse_args())
