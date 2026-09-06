import unittest

from experiments.idea_collapse.corpus.index_proceedings import IndexParser


class IndexTests(unittest.TestCase):
    def test_title_entities_and_nested_markup(self):
        parser = IndexParser(2024)
        parser.feed('<a title="paper title" href="/paper_files/paper/2024/hash/test-Abstract-Conference.html">A &amp; <em>B</em></a>')
        self.assertEqual(parser.rows[0]["title"], "A & B")

    def test_navigation_is_not_a_paper(self):
        parser = IndexParser(2024)
        parser.feed('<a href="/">Home</a>')
        self.assertEqual(parser.rows, [])

    def test_wrong_year_and_external_host_rejected(self):
        for href in ("/paper_files/paper/2025/hash/x-Abstract-Conference.html", "https://example.invalid/2024"):
            with self.subTest(href=href), self.assertRaises(ValueError):
                IndexParser(2024).feed(f'<a title="paper title" href="{href}">X</a>')


if __name__ == "__main__":
    unittest.main()
