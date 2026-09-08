import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from complete_corpus import Pipeline, canonical, normalized, parse_official, parse_openreview, read_index, sha, valid_abstract, write_rows


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.paper = {"paper_id": "ICLR2025_abc", "year": 2025, "title": "Actual paper",
                      "proceedings_abstract_url": "https://proceedings.iclr.cc/paper_files/paper/2025/hash/abc-Abstract-Conference.html"}
        self.raw = b'<meta name="citation_title" content="Actual paper"><meta name="citation_author" content="Author A"><meta name="citation_pdf_url" content="/paper_files/paper/2025/file/abc-Paper-Conference.pdf"><p class="paper-abstract"><p>Real source abstract &amp; evidence.</p></p>'

    def tearDown(self):
        self.tmp.cleanup()

    def test_index_counts_and_duplicates(self):
        path = self.root / "index.html"
        html = '<a title="paper title" href="/paper_files/paper/2025/hash/abc-Abstract-Conference.html">Actual paper</a>'
        path.write_text(html)
        self.assertEqual(len(read_index(path, 2025, 1)), 1)
        with self.assertRaises(ValueError):
            read_index(path, 2025, 2)
        path.write_text(html + html)
        with self.assertRaises(ValueError):
            read_index(path, 2025)

    def test_real_nested_abstract_and_provenance(self):
        parsed, error, links = parse_official(self.raw, self.paper)
        self.assertIsNone(error)
        self.assertEqual(parsed["abstract"], "Real source abstract & evidence.")
        self.assertEqual(parsed["authors"], ["Author A"])

    def test_empty_error_and_title_surrogate_rejected(self):
        for text in (None, "", "Access Denied", "<html>error</html>", "Actual paper"):
            self.assertFalse(valid_abstract(text, "Actual paper"))
        self.assertIsNone(parse_official(b"<html><h1>403 Forbidden</h1></html>", self.paper)[0])

    def test_pdf_identity_mismatch_rejected(self):
        altered = self.raw.replace(b"abc-Paper", b"different-Paper")
        self.assertEqual(parse_official(altered, self.paper)[1], "PDF_IDENTITY_MISMATCH")

    def test_normalization_and_hash_stability(self):
        parsed, _, _ = parse_official(self.raw, self.paper)
        first = normalized(self.paper, parsed, "official_proceedings", "2026-09-08T00:00:00Z", sha(self.raw))
        second = normalized(self.paper, parsed, "official_proceedings", "2026-09-08T00:00:00Z", sha(self.raw))
        self.assertEqual(canonical(first), canonical(second))
        self.assertEqual(first["abstract_sha256"], sha(parsed["abstract"].encode()))
        path = self.root / "output.jsonl"
        self.assertEqual(write_rows(path, [first]), write_rows(path, [second]))
        with self.assertRaises(ValueError):
            write_rows(path, [{**first, "abstract": "changed"}])

    def test_missing_preserves_id_and_null(self):
        row = normalized(self.paper)
        self.assertEqual(row["paper_id"], self.paper["paper_id"])
        self.assertIsNone(row["abstract"])
        self.assertIsNone(row["abstract_sha256"])

    def test_verified_legacy_cache_never_downloaded(self):
        manifest = self.root / "verified.jsonl.gz"
        with gzip.open(manifest, "wt") as f:
            f.write(json.dumps({"url": self.paper["proceedings_abstract_url"], "sha256": sha(self.raw), "parse_status": "MEASURED"}) + "\n")
        cache = self.root / "old/_source_cache/iclr2025_abstract_pages"
        cache.mkdir(parents=True)
        path = cache / "abc-Abstract-Conference.html"
        path.write_bytes(self.raw)
        pipeline = Pipeline(self.root / "new", self.root / "old", manifest)
        pipeline.request = lambda _: self.fail("verified cached page must not be redownloaded")
        one, errors, calls = pipeline.acquire(self.paper, network=True)
        two, _, calls2 = pipeline.acquire(self.paper, network=True)
        self.assertEqual(one, two)
        self.assertEqual(calls + calls2, 0)
        self.assertFalse(errors)
        self.assertIsNone(one["source_retrieved_at"])
        self.assertEqual(path.read_bytes(), self.raw)

    def test_new_acquisition_timestamp_is_cached_for_replay(self):
        manifest = self.root / "verified.jsonl.gz"
        with gzip.open(manifest, "wt") as f:
            f.write("")
        pipeline = Pipeline(self.root / "new", self.root / "old", manifest)
        pipeline.request = lambda _: (200, self.raw, None, None)
        first, _, calls = pipeline.acquire(self.paper, network=True)
        pipeline.request = lambda _: self.fail("newly verified cache must be reused")
        second, _, calls2 = pipeline.acquire(self.paper, network=True)
        self.assertEqual(first, second)
        self.assertEqual((calls, calls2), (1, 0))
        self.assertIsNotNone(first["source_retrieved_at"])

    def test_linked_openreview_identity_required(self):
        raw = json.dumps({"notes": [{"id": "NOTE", "content": {"title": {"value": "Actual paper"}, "abstract": {"value": "A real abstract."}, "authors": {"value": ["Author"]}}}]}).encode()
        parsed, error = parse_openreview(raw, self.paper, "https://openreview.net/forum?id=NOTE")
        self.assertIsNone(error)
        self.assertEqual(parsed["abstract"], "A real abstract.")
        self.assertIsNone(parse_openreview(raw, self.paper, "https://openreview.net/forum?id=OTHER")[0])


if __name__ == "__main__":
    unittest.main()
