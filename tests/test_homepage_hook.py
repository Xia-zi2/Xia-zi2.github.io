import tempfile
import unittest
from pathlib import Path

from hooks.homepage import (
    collect_documents,
    parse_front_matter,
    render_document_meta,
    render_profile,
    render_projects,
)


class FrontMatterTests(unittest.TestCase):
    def test_parses_yaml_front_matter_without_body(self):
        meta = parse_front_matter(
            "---\ntitle: LightRAG\ntags: [RAG, Retrieval]\nstatus: reading\n---\n# Body"
        )

        self.assertEqual(meta["title"], "LightRAG")
        self.assertEqual(meta["tags"], ["RAG", "Retrieval"])
        self.assertNotIn("Body", meta)

    def test_plain_markdown_has_no_metadata(self):
        self.assertEqual(parse_front_matter("# No metadata"), {})


class CollectionTests(unittest.TestCase):
    def test_ignores_drafts_and_sorts_by_updated_then_date(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp)
            papers = docs / "papers"
            papers.mkdir()
            (papers / "older.md").write_text(
                "---\ntitle: Older\ndate: 2026-01-01\nupdated: 2026-02-01\n---\n",
                encoding="utf-8",
            )
            (papers / "newer.md").write_text(
                "---\ntitle: Newer\ndate: 2026-01-02\nupdated: 2026-03-01\n---\n",
                encoding="utf-8",
            )
            (papers / "draft.md").write_text(
                "---\ntitle: Hidden\ndate: 2027-01-01\ndraft: true\n---\n",
                encoding="utf-8",
            )
            (papers / "index.md").write_text("# Index", encoding="utf-8")

            entries = collect_documents(docs, ["papers"])

        self.assertEqual([entry["title"] for entry in entries], ["Newer", "Older"])
        self.assertEqual(entries[0]["url"], "papers/newer/")

    def test_blog_route_uses_configured_slug_outside_posts_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp)
            posts = docs / "blog" / "posts"
            posts.mkdir(parents=True)
            (posts / "source-name.md").write_text(
                "---\ntitle: 中文标题\nslug: stable-slug\ndate: 2026-01-01\n---\n",
                encoding="utf-8",
            )

            entries = collect_documents(docs, ["blog/posts"])

        self.assertEqual(entries[0]["url"], "blog/stable-slug/")

    def test_project_cards_use_weight_and_escape_untrusted_text(self):
        projects = [
            {
                "title": "Later",
                "summary": "Second",
                "weight": 20,
                "featured": True,
                "url": "projects/later/",
                "tags": ["3D"],
                "image": "assets/images/project-placeholder.svg",
                "date": "2026",
                "github": "https://github.com/example/later",
            },
            {
                "title": "<First>",
                "summary": "Safe & short",
                "weight": 10,
                "featured": True,
                "url": "projects/first/",
                "tags": ["RAG"],
                "image": "assets/images/project-placeholder.svg",
                "date": "2025",
            },
        ]

        html = render_projects(projects)

        self.assertLess(html.index("&lt;First&gt;"), html.index("Later"))
        self.assertIn("Safe &amp; short", html)
        self.assertIn('href="projects/first/"', html)


class ProfileTests(unittest.TestCase):
    def test_profile_is_escaped_and_todo_links_are_not_clickable(self):
        html = render_profile(
            {
                "name": "李<亭皑",
                "institution": "中国科学技术大学",
                "fields": ["数学", "计算机科学"],
                "intro": "研究与工程记录",
                "avatar": "assets/images/avatar-placeholder.svg",
                "links": {
                    "github": "https://github.com/Xia-zi2",
                    "email": "TODO",
                    "cv": "cv/",
                },
            }
        )

        self.assertIn("李&lt;亭皑", html)
        self.assertIn("https://github.com/Xia-zi2", html)
        self.assertNotIn('href="TODO"', html)
        self.assertIn("Email（待补充）", html)


class DocumentMetaTests(unittest.TestCase):
    def test_paper_metadata_renders_only_supplied_fields(self):
        html = render_document_meta(
            {
                "type": "paper",
                "authors": ["A. Author", "B. Author"],
                "venue": "TODO",
                "year": 2026,
                "paper": "https://example.org/paper.pdf",
                "code": "TODO",
                "status": "阅读中",
            }
        )

        self.assertIn("A. Author、B. Author", html)
        self.assertIn("2026", html)
        self.assertIn('href="https://example.org/paper.pdf"', html)
        self.assertIn("阅读中", html)
        self.assertNotIn("TODO", html)


if __name__ == "__main__":
    unittest.main()
