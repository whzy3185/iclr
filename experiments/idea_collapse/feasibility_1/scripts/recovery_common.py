"""Deterministic source-only recovery helpers; no acquisition or model clients."""

import csv
import gzip
import hashlib
from html.parser import HTMLParser
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urljoin

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
SPECS = ["CODEX_F0_RECOVERY_TASK.md", "CODEX_F0_EXECUTION_PROMPT.md", "CODEX_F0_MASTER.md",
         "research/iclr_fit_validation/round52_identification_measurement_and_f0_recovery.md"]
spec = importlib.util.spec_from_file_location("f0_legacy", BASE / "legacy/f0_source_only_audit.py")
legacy = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = legacy
spec.loader.exec_module(legacy)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False,
                       separators=(",", ":")) + "\n").encode("utf-8")


def digest(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def identity(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=15).strip()


def write_json(path, value):
    with Path(path).open("xb") as handle:
        handle.write(encoded(value))


def write_jsonl(path, rows):
    path = Path(path)
    with path.open("xb") as raw:
        if path.suffix == ".gz":
            with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="", compresslevel=6) as stream:
                for row in rows:
                    stream.write(encoded(row))
        else:
            for row in rows:
                raw.write(encoded(row))


def read_jsonl(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def write_csv(path, rows, fields):
    with Path(path).open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class SourceHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.links = []
        self.parts = []
        self.abstract_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and "name" in attrs:
            self.meta.setdefault(attrs["name"], []).append(attrs.get("content", ""))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "p":
            if "paper-abstract" in attrs.get("class", "").split():
                self.abstract_depth = 1
            elif self.abstract_depth:
                self.abstract_depth += 1

    def handle_endtag(self, tag):
        if tag == "p" and self.abstract_depth:
            self.abstract_depth -= 1

    def handle_data(self, value):
        if self.abstract_depth:
            self.parts.append(value)


def source_links(index, year):
    parser = SourceHTML()
    parser.feed(Path(index).read_text(encoding="utf-8"))
    urls = sorted({urljoin("https://proceedings.iclr.cc", link) for link in parser.links
                   if link.endswith("-Abstract-Conference.html")})
    prefix = f"https://proceedings.iclr.cc/paper_files/paper/{year}/hash/"
    if not urls or any(not url.startswith(prefix) for url in urls):
        raise ValueError("official index identity/year cannot be established")
    return urls


def parse_source(path, url, year):
    paper_hash = url.rsplit("/", 1)[-1].split("-Abstract", 1)[0]
    record = {"paper_id": f"ICLR{year}_{paper_hash}", "year": year,
              "proceedings_url": url, "title": None, "abstract": None,
              "openreview_url": None, "authors": [], "proceedings_publication_date": None,
              "first_public_date": None, "temporal_status": "UNKNOWN",
              "date_search_coverage": "cached_proceedings_only; preprint/original-public-note not resolved",
              "source_page_sha256": None, "abstract_sha256": None,
              "parse_status": "MISSING_SOURCE", "hard_errors": [], "source_bytes": None}
    if not path.exists():
        record["hard_errors"] = ["MISSING_SOURCE_PAGE"]
        return record
    raw = path.read_bytes()
    record.update(source_page_sha256=hashlib.sha256(raw).hexdigest(), source_bytes=len(raw))
    try:
        parser = SourceHTML()
        parser.feed(raw.decode("utf-8"))
        title = parser.meta.get("citation_title", [""])[0].strip()
        abstract = " ".join(" ".join(parser.parts).split())
        pdf = parser.meta.get("citation_pdf_url", [""])[0]
        if pdf and paper_hash not in pdf:
            record["hard_errors"].append("CORRUPTED_IDENTITY_PDF_MISMATCH")
        if not title or not abstract:
            record["hard_errors"].append("MISSING_TITLE_OR_ABSTRACT")
        record.update(title=title or None, abstract=abstract or None,
                      authors=parser.meta.get("citation_author", []),
                      proceedings_publication_date=parser.meta.get("citation_publication_date", [None])[0],
                      openreview_url=next((u for u in parser.links if u.startswith("https://openreview.net/forum?")), None),
                      abstract_sha256=hashlib.sha256(abstract.encode()).hexdigest() if abstract else None,
                      parse_status="MEASURED" if not record["hard_errors"] else "FAILED")
    except (UnicodeError, ValueError) as error:
        record.update(parse_status="FAILED", hard_errors=[type(error).__name__])
    return record
