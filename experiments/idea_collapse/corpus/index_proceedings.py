"""Parse an acquired official annual index; output is NOT an abstract corpus."""

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse

from ..generation.provenance import canonical_bytes, file_hash, write_exclusive


class IndexParser(HTMLParser):
    def __init__(self, year):
        super().__init__(convert_charrefs=True)
        self.year = year
        self.rows = []
        self.href = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("title") == "paper title":
            self.href = attrs.get("href")
            self.parts = []

    def handle_data(self, text):
        if self.href is not None:
            self.parts.append(text)

    def handle_endtag(self, tag):
        if tag == "a" and self.href is not None:
            url = urljoin("https://proceedings.iclr.cc/", self.href)
            parsed = urlparse(url)
            prefix = f"/paper_files/paper/{self.year}/hash/"
            if parsed.hostname != "proceedings.iclr.cc" or not parsed.path.startswith(prefix):
                raise ValueError("unexpected paper-title link host/year")
            title = " ".join("".join(self.parts).split())
            if not title or not parsed.path.endswith("-Abstract-Conference.html"):
                raise ValueError("unexpected annual-index link schema")
            self.rows.append({"year": self.year, "title": title, "abstract_page_url": url})
            self.href = None
            self.parts = []


def build_index(source, year, output, manifest):
    if year not in (2024, 2025, 2026):
        raise ValueError("out-of-scope year")
    source, output, manifest = map(Path, (source, output, manifest))
    if output.exists() or manifest.exists() or output.resolve() == manifest.resolve():
        raise ValueError("outputs must be new and distinct")
    parser = IndexParser(year)
    parser.feed(source.read_text(encoding="utf-8"))
    parser.close()
    rows = sorted(parser.rows, key=lambda row: row["abstract_page_url"])
    if not rows or len({row["abstract_page_url"] for row in rows}) != len(rows):
        raise ValueError("empty index or duplicate paper link")
    write_exclusive(output, b"".join(canonical_bytes(row) for row in rows))
    result = {"kind": "official_title_index_NOT_frozen_pilot_corpus", "year": year,
              "source_url": f"https://proceedings.iclr.cc/paper_files/paper/{year}",
              "indexed_at": datetime.now(timezone.utc).isoformat(),
              "raw_html_sha256": file_hash(source), "index_sha256": file_hash(output),
              "records": len(rows), "abstracts_acquired": 0,
              "domain_filtering": "not_performed", "pilot_eligible": False}
    write_exclusive(manifest, canonical_bytes(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build_index(args.input, args.year, args.output, args.manifest), indent=2))


if __name__ == "__main__":
    main()
