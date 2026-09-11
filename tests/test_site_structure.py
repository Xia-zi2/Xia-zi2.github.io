import tempfile
import unittest
from pathlib import Path

from scripts.check_site import (
    check_front_matter,
    find_missing_built_links,
    find_missing_local_assets,
)


class SiteStructureTests(unittest.TestCase):
    def test_reports_missing_required_front_matter(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "paper.md"
            page.write_text("---\ntitle: Example\n---\n# Example", encoding="utf-8")

            errors = check_front_matter(page, {"title", "date", "status"})

        self.assertEqual(errors, ["paper.md: missing front matter field 'date'", "paper.md: missing front matter field 'status'"])

    def test_finds_missing_markdown_and_front_matter_images(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp)
            (docs / "assets").mkdir()
            (docs / "assets" / "exists.svg").write_text("<svg/>", encoding="utf-8")
            page = docs / "page.md"
            page.write_text(
                "---\nimage: assets/missing.svg\n---\n"
                "![Exists](assets/exists.svg)\n![Missing](assets/also-missing.png)\n",
                encoding="utf-8",
            )

            errors = find_missing_local_assets(docs)

        self.assertEqual(
            errors,
            [
                "page.md: missing local asset 'assets/also-missing.png'",
                "page.md: missing local asset 'assets/missing.svg'",
            ],
        )

    def test_finds_missing_links_in_built_html(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp)
            (site / "assets").mkdir()
            (site / "assets" / "ok.css").write_text("", encoding="utf-8")
            (site / "notes").mkdir()
            (site / "notes" / "index.html").write_text("<h1>Notes</h1>", encoding="utf-8")
            (site / "index.html").write_text(
                '<link href="assets/ok.css">'
                '<a href="notes/">Notes</a>'
                '<a href="missing/">Missing</a>'
                '<a href="https://example.org/">External</a>',
                encoding="utf-8",
            )

            errors = find_missing_built_links(site)

        self.assertEqual(errors, ["index.html: broken built link 'missing/'"])


if __name__ == "__main__":
    unittest.main()
