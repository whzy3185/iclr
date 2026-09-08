"""Data-only official ICLR abstract acquisition and deterministic normalization."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import gzip
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import ProxyHandler, Request, build_opener

BASE = Path(__file__).resolve().parents[1]
EXPECTED = {2024: 2260, 2025: 3703, 2026: 5351}
HOST = "https://proceedings.iclr.cc"
SCHEMA = ("paper_id", "year", "title", "abstract", "authors", "proceedings_abstract_url",
          "openreview_url", "pdf_url", "source_type", "source_retrieved_at", "source_sha256",
          "abstract_sha256", "parse_status")


def canonical(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def file_sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def exclusive(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def write_rows(path, rows):
    raw = b"".join(canonical(row) for row in rows)
    if Path(path).exists():
        if Path(path).read_bytes() != raw:
            raise ValueError(f"refusing to overwrite differing output: {path}")
    else:
        exclusive(path, raw)
    return sha(raw)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.papers = {}, [], []
        self.abstract_parts, self.abstract_depth = [], 0
        self.title_href, self.title_parts = None, []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name"):
            self.meta.setdefault(attrs["name"], []).append(attrs.get("content", ""))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
            if attrs.get("title") == "paper title":
                self.title_href, self.title_parts = attrs["href"], []
        if tag == "p":
            if "paper-abstract" in attrs.get("class", "").split():
                self.abstract_depth = 1
            elif self.abstract_depth:
                self.abstract_depth += 1

    def handle_data(self, text):
        if self.abstract_depth:
            self.abstract_parts.append(text)
        if self.title_href is not None:
            self.title_parts.append(text)

    def handle_endtag(self, tag):
        if tag == "p" and self.abstract_depth:
            self.abstract_depth -= 1
        if tag == "a" and self.title_href is not None:
            self.papers.append((self.title_href, " ".join("".join(self.title_parts).split())))
            self.title_href = None


def read_index(path, year, expected=None):
    parsed = Page()
    parsed.feed(Path(path).read_text(encoding="utf-8"))
    rows, seen = [], set()
    for href, title in parsed.papers:
        url = urljoin(HOST, href)
        prefix = f"{HOST}/paper_files/paper/{year}/hash/"
        if not url.startswith(prefix) or not url.endswith("-Abstract-Conference.html"):
            raise ValueError("non-Conference or wrong-year paper link")
        digest_id = url.rsplit("/", 1)[-1].split("-Abstract", 1)[0]
        pid = f"ICLR{year}_{digest_id}"
        if pid in seen or not title:
            raise ValueError("duplicate ID or empty indexed title")
        seen.add(pid)
        rows.append({"paper_id": pid, "year": year, "title": title, "proceedings_abstract_url": url})
    if expected is not None and len(rows) != expected:
        raise ValueError(f"official denominator mismatch: {year}: {len(rows)} != {expected}")
    return sorted(rows, key=lambda row: row["paper_id"])


def valid_abstract(text, title):
    if not isinstance(text, str) or not text.strip() or text.strip() == title.strip():
        return False
    if text.strip().lower() in {"access denied", "forbidden", "not found", "404 not found", "internal server error", "just a moment..."}:
        return False
    return not bool(re.search(r"<!doctype\s+html|<html(?:\s|>)", text, re.I))


def parse_official(raw, paper):
    parsed = Page()
    try:
        parsed.feed(raw.decode("utf-8"))
    except UnicodeError:
        return None, "INVALID_UTF8", []
    title = parsed.meta.get("citation_title", [""])[0].strip()
    abstract = " ".join(" ".join(parsed.abstract_parts).split())
    linked = [urljoin(paper["proceedings_abstract_url"], url) for url in parsed.links]
    linked = [url for url in linked if urlparse(url).hostname == "openreview.net" and urlparse(url).path == "/forum"]
    pdf = parsed.meta.get("citation_pdf_url", [None])[0]
    if pdf:
        pdf = urljoin(paper["proceedings_abstract_url"], pdf)
        if paper["paper_id"].split("_", 1)[1] not in pdf:
            return None, "PDF_IDENTITY_MISMATCH", linked
    normalize_title = lambda s: " ".join(s.split()).casefold()
    if not title or normalize_title(title) != normalize_title(paper["title"]):
        return None, "TITLE_IDENTITY_MISMATCH", linked
    if not valid_abstract(abstract, title):
        return None, "EMPTY_OR_ERROR_ABSTRACT", linked
    return {"title": title, "abstract": abstract, "authors": parsed.meta.get("citation_author", []),
            "pdf_url": pdf, "openreview_url": linked[0] if linked else None}, None, linked


def parse_openreview(raw, paper, linked):
    def value(obj):
        return obj.get("value") if isinstance(obj, dict) else obj
    try:
        note_id = parse_qs(urlparse(linked).query)["id"][0]
        notes = json.loads(raw)["notes"]
        note = next(n for n in notes if n.get("id") == note_id)
        content = note["content"]
        title, abstract = value(content["title"]), value(content["abstract"])
        if " ".join(title.split()).casefold() != " ".join(paper["title"].split()).casefold():
            raise ValueError("linked-note title mismatch")
        if not valid_abstract(abstract, title):
            raise ValueError("missing real abstract")
        authors = value(content.get("authors", []))
        pdf = value(content.get("pdf"))
        return {"title": title, "abstract": abstract, "authors": authors if isinstance(authors, list) else [],
                "pdf_url": urljoin("https://openreview.net", pdf) if pdf else None, "openreview_url": linked}, None
    except (ValueError, KeyError, StopIteration, TypeError, AttributeError):
        return None, "INVALID_LINKED_OPENREVIEW_RECORD"


def normalized(paper, parsed=None, source_type="missing", retrieved=None, raw_hash=None, error=None):
    row = dict.fromkeys(SCHEMA)
    row.update(paper)
    row.update(authors=[], source_type=source_type, source_retrieved_at=retrieved, source_sha256=raw_hash,
               parse_status=error or "MISSING_ABSTRACT")
    if parsed:
        row.update(parsed, parse_status="VERIFIED_ABSTRACT", abstract_sha256=sha(parsed["abstract"].encode()))
    return row


class Pipeline:
    def __init__(self, base, legacy_root, verified_manifest, proxy=None, max_attempts=3):
        self.base, self.legacy_root = Path(base), Path(legacy_root)
        self.cache = self.base / "_cache"
        self.max_attempts = max_attempts
        self.expected = {}
        with gzip.open(verified_manifest, "rt", encoding="utf-8") as handle:
            for row in map(json.loads, handle):
                if row.get("sha256") and row.get("parse_status") == "MEASURED":
                    self.expected[row["url"]] = row["sha256"]
        self.proxy = proxy

    def cached(self, paper):
        url = paper["proceedings_abstract_url"]
        path = self.legacy_root / f"_source_cache/iclr{paper['year']}_abstract_pages" / url.rsplit("/", 1)[-1]
        errors = []
        linked = []
        if path.exists():
            raw = path.read_bytes()
            actual = sha(raw)
            parsed, error, linked = parse_official(raw, paper)
            expected = self.expected.get(url)
            if expected == actual and parsed:
                return normalized(paper, parsed, "official_proceedings_legacy_cache", None, actual), errors, linked
            errors.append({"paper_id": paper["paper_id"], "stage": "legacy_cache_validation", "error": error or "LEGACY_HASH_UNVERIFIED_OR_CHANGED",
                           "source_sha256": actual, "expected_sha256": expected, "url": url})
        directory = self.cache / paper["paper_id"]
        for meta_path in sorted(directory.glob("*.json")):
            meta = json.loads(meta_path.read_text())
            if meta.get("http_status") != 200:
                continue
            body = directory / meta["body_file"]
            if not body.exists() or file_sha(body) != meta["source_sha256"]:
                errors.append({"paper_id": paper["paper_id"], "stage": "new_cache_validation", "error": "CACHE_HASH_MISMATCH", "cache_key": str(meta_path.relative_to(self.base))})
                continue
            if meta["source_type"] == "official_proceedings":
                parsed, error, more = parse_official(body.read_bytes(), paper)
                linked.extend(more)
            else:
                parsed, error = parse_openreview(body.read_bytes(), paper, meta["linked_forum"])
            if parsed:
                return normalized(paper, parsed, meta["source_type"], meta["source_retrieved_at"], meta["source_sha256"]), errors, linked
        return None, errors, linked

    def request(self, url):
        opener = build_opener(ProxyHandler({"http": self.proxy, "https": self.proxy})) if self.proxy else build_opener()
        request = Request(url, headers={"User-Agent": "ICLR-Abstract-Corpus/1.0 (public scholarly metadata)", "Accept": "text/html,application/json"})
        try:
            with opener.open(request, timeout=25) as response:
                raw = response.read(2_000_001)
                return response.status, raw, None, response.headers.get("Retry-After")
        except HTTPError as error:
            return error.code, error.read(2_000_001), "HTTP_ERROR", error.headers.get("Retry-After")
        except (URLError, TimeoutError, OSError) as error:
            return None, b"", type(error).__name__, None

    def acquire(self, paper, network):
        cached, errors, linked = self.cached(paper)
        if cached:
            return cached, errors, 0
        if not network:
            return normalized(paper, error="NOT_ACQUIRED"), errors, 0
        calls = 0
        directory = self.cache / paper["paper_id"]
        directory.mkdir(parents=True, exist_ok=True)
        sources = [("official_proceedings", paper["proceedings_abstract_url"], None)]
        for kind, url, forum in sources:
            for attempt in range(1, self.max_attempts + 1):
                name = ("official" if forum is None else "openreview") + f"-{attempt:02d}"
                meta_path, body_path = directory / (name + ".json"), directory / (name + ".body")
                if meta_path.exists():
                    meta = json.loads(meta_path.read_text())
                    linked.extend(meta.get("linked_openreview", []))
                    continue
                if body_path.exists():
                    errors.append({"paper_id": paper["paper_id"], "stage": name, "error": "INTERRUPTED_ATTEMPT_BODY_RETAINED"})
                    continue
                status, raw, error, retry_after = self.request(url)
                calls += 1
                if len(raw) > 2_000_000:
                    error = "RESPONSE_TOO_LARGE"
                parsed, parse_error = None, error
                if status == 200 and error is None:
                    if forum is None:
                        parsed, parse_error, more = parse_official(raw, paper)
                        linked.extend(more)
                    else:
                        parsed, parse_error = parse_openreview(raw, paper, forum)
                elif raw and forum is None:
                    _, _, more = parse_official(raw, paper)
                    linked.extend(more)
                stamp = datetime.now(timezone.utc).isoformat()
                meta = {"paper_id": paper["paper_id"], "url": url, "source_type": kind, "attempt": attempt,
                        "source_retrieved_at": stamp, "source_sha256": sha(raw), "body_file": body_path.name,
                        "http_status": status, "parse_status": "VERIFIED_ABSTRACT" if parsed else "FAILED",
                        "error": parse_error or (None if parsed else "UNAVAILABLE"), "linked_openreview": sorted(set(linked)),
                        "linked_forum": forum}
                exclusive(body_path, raw)
                exclusive(meta_path, canonical(meta))
                if parsed:
                    return normalized(paper, parsed, kind, stamp, meta["source_sha256"]), errors, calls
                delay = min(60, int(retry_after)) if retry_after and retry_after.isdigit() else 2 ** attempt
                if attempt < self.max_attempts:
                    time.sleep(delay)
            if forum is None and linked:
                chosen = sorted(set(linked))[0]
                note = parse_qs(urlparse(chosen).query).get("id", [])
                if note:
                    sources.append(("linked_openreview_metadata", "https://api2.openreview.net/notes?" + urlencode({"id": note[0]}), chosen))
        if not linked:
            errors.append({"paper_id": paper["paper_id"], "stage": "fallback", "error": "NO_LINKED_OPENREVIEW_AVAILABLE"})
        return normalized(paper, error="UNAVAILABLE_AFTER_BOUNDED_ATTEMPTS"), errors, calls


def all_papers(base):
    return [row for year, n in EXPECTED.items() for row in read_index(base / f"indexes/iclr{year}.html", year, n)]


def execute(args):
    papers = all_papers(BASE)
    pipeline = Pipeline(BASE, args.legacy_root, args.verified_manifest, args.proxy)
    rows, validation_events = [], []
    calls = done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(pipeline.acquire, paper, not args.inventory): paper for paper in papers}
        for future in as_completed(futures):
            row, errors, count = future.result()
            rows.append(row)
            validation_events.extend(errors)
            calls += count
            done += 1
            if done % 250 == 0 or done == len(papers):
                print(f"{done}/{len(papers)} checked; requests this pass={calls}; verified={sum(r['abstract'] is not None for r in rows)}", flush=True)
    rows.sort(key=lambda row: (row["year"], row["paper_id"]))
    if len({r["paper_id"] for r in rows}) != sum(EXPECTED.values()):
        raise ValueError("duplicate or dropped official ID")
    counts = {str(y): {"official": n, "abstracts": sum(r["abstract"] is not None for r in rows if r["year"] == y),
                       "missing": sum(r["abstract"] is None for r in rows if r["year"] == y)} for y, n in EXPECTED.items()}
    destination = BASE / ("inventory" if args.inventory else args.output)
    destination.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for year in EXPECTED:
        subset = [row for row in rows if row["year"] == year]
        if len(subset) != EXPECTED[year]:
            raise ValueError("per-year denominator drift")
        hashes[f"iclr{year}_abstracts.jsonl"] = write_rows(destination / f"iclr{year}_abstracts.jsonl", subset)
        hashes[f"iclr{year}_missing.jsonl"] = write_rows(destination / f"iclr{year}_missing.jsonl", [r for r in subset if r["abstract"] is None])
    hashes["corpus_2024_2026.jsonl"] = write_rows(destination / "corpus_2024_2026.jsonl", rows)
    failures = list(validation_events)
    for meta in sorted(pipeline.cache.glob("*/*.json")):
        record = json.loads(meta.read_text())
        if record.get("parse_status") != "VERIFIED_ABSTRACT":
            failures.append(record)
    failures.sort(key=lambda r: (r["paper_id"], r.get("stage", ""), r.get("source_type", ""), r.get("attempt", 0)))
    hashes["acquisition_failures.jsonl"] = write_rows(destination / "acquisition_failures.jsonl", failures)
    write_rows(destination / "source_cache_catalog.jsonl", [{"paper_id": r["paper_id"], "source_type": r["source_type"],
        "source_retrieved_at": r["source_retrieved_at"], "source_sha256": r["source_sha256"], "parse_status": r["parse_status"],
        "proceedings_abstract_url": r["proceedings_abstract_url"]} for r in rows])
    manifest = {"counts": counts, "normalized_sha256": hashes, "pipeline_sha256": file_sha(__file__),
                "index_sha256": {str(y): file_sha(BASE / f"indexes/iclr{y}.html") for y in EXPECTED},
                "source_types": dict(Counter(r["source_type"] for r in rows)),
                "unknown_legacy_retrieval_timestamps": sum(r["source_type"] == "official_proceedings_legacy_cache" for r in rows),
                "timestamp_policy": "preserved network timestamp, or null for legacy cache without historical acquisition timestamps",
                "network_requests_this_pass": calls, "inventory_only": args.inventory,
                "official_identity_validation": "Conference index membership, citation-title match and PDF identity when present",
                "synthetic_abstracts": 0, "model_calls": 0}
    exclusive(destination / "corpus_manifest.json", canonical(manifest))
    exclusive(destination / "corpus_sha256.txt", (hashes["corpus_2024_2026.jsonl"] + "\n").encode())
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-root", type=Path, required=True)
    parser.add_argument("--verified-manifest", type=Path, required=True)
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--output", default="pass1")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--proxy")
    args = parser.parse_args()
    if not 1 <= args.workers <= 8 or Path(args.output).name != args.output:
        parser.error("workers must be 1-8 and output must be a directory name")
    execute(args)
