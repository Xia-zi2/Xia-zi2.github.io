"""Fast repository checks that complement `mkdocs build --strict`."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_FILES = (
    "mkdocs.yml",
    "requirements.txt",
    "data/profile.yml",
    "docs/index.md",
    "docs/projects/index.md",
    "docs/papers/index.md",
    "docs/reproductions/index.md",
    "docs/learning/index.md",
    "docs/blog/index.md",
    "docs/writing.md",
    ".github/workflows/deploy.yml",
)

CONTENT_RULES = {
    "docs/projects/*.md": {"title", "description"},
    "docs/papers/*.md": {"title", "description"},
    "docs/reproductions/*.md": {"title", "description"},
    "docs/learning/*.md": {"title", "description"},
    "docs/blog/posts/*.md": {"title", "description", "date"},
}


def _front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        return {}
    parts = text.replace("\r\n", "\n").split("---", 2)
    if len(parts) < 3:
        return {}
    result = yaml.safe_load(parts[1]) or {}
    return result if isinstance(result, dict) else {}


def check_front_matter(path: Path, required: Iterable[str]) -> list[str]:
    """Return deterministic messages for absent or empty metadata fields."""
    meta = _front_matter(path)
    errors = []
    for field in sorted(required):
        if field not in meta or meta[field] in (None, ""):
            errors.append(f"{path.name}: missing front matter field '{field}'")
    return errors


def _is_local_asset(value: str) -> bool:
    lowered = value.lower()
    return bool(value) and not lowered.startswith(("http://", "https://", "data:", "#", "mailto:"))


def find_missing_local_assets(docs_dir: Path = DOCS) -> list[str]:
    """Check Markdown image references and root-relative front matter images."""
    errors: list[str] = []
    markdown_image = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
    html_image = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)

    for page in docs_dir.rglob("*.md"):
        text = page.read_text(encoding="utf-8-sig")
        references = set(markdown_image.findall(text)) | set(html_image.findall(text))
        meta = _front_matter(page)
        if isinstance(meta.get("image"), str):
            image = meta["image"]
            if _is_local_asset(image) and not (docs_dir / image.lstrip("/")).exists():
                references.add("/" + image.lstrip("/"))

        for reference in references:
            if not _is_local_asset(reference):
                continue
            clean = reference.split("#", 1)[0].split("?", 1)[0]
            target = docs_dir / clean.lstrip("/") if clean.startswith("/") else page.parent / clean
            if not target.exists():
                display = clean.lstrip("/") if clean.startswith("/") else clean
                relative_page = page.relative_to(docs_dir).as_posix()
                errors.append(f"{relative_page}: missing local asset '{display}'")
    return sorted(errors)


class _LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        wanted = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script", "source", "video"} else None
        if not wanted:
            return
        for name, value in attrs:
            if name == wanted and value:
                self.links.append(value)


def find_missing_built_links(site_dir: Path) -> list[str]:
    """Validate local href/src targets in generated HTML."""
    errors: list[str] = []
    for html_path in site_dir.rglob("*.html"):
        parser = _LinkCollector()
        parser.feed(html_path.read_text(encoding="utf-8-sig"))
        for raw_link in parser.links:
            parsed = urlsplit(raw_link)
            if parsed.scheme or parsed.netloc or raw_link.startswith("//") or not parsed.path:
                continue
            clean = unquote(parsed.path)
            target = site_dir / clean.lstrip("/") if clean.startswith("/") else html_path.parent / clean
            if target.is_dir():
                target = target / "index.html"
            elif clean.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                relative_html = html_path.relative_to(site_dir).as_posix()
                errors.append(f"{relative_html}: broken built link '{raw_link}'")
    return sorted(set(errors))


def validate_built_site(site_dir: Path) -> list[str]:
    errors: list[str] = []
    required = (
        "index.html",
        "404.html",
        "search/search_index.json",
        "sitemap.xml",
        "robots.txt",
        "tags/index.html",
        "blog/welcome/index.html",
        "projects/arthoi-reconstruction/index.html",
        "papers/lightrag/index.html",
        "reproductions/arthoi/index.html",
        "learning/multi-head-attention/index.html",
    )
    for relative in required:
        if not (site_dir / relative).exists():
            errors.append(f"built site missing: {relative}")

    homepage = site_dir / "index.html"
    if homepage.exists():
        html = homepage.read_text(encoding="utf-8-sig")
        for token in ("academic-hero", "project-card", "recent-list", 'property="og:title"', "favicon.svg"):
            if token not in html:
                errors.append(f"built homepage missing rendered token: {token}")
        if "<title>李亭皑｜个人科研主页 - 李亭皑｜个人科研主页</title>" in html:
            errors.append("built homepage title redundantly repeats the site name")
        if "<!-- AUTO:" in html:
            errors.append("built homepage still contains unresolved AUTO markers")

    paper = site_dir / "papers" / "lightrag" / "index.html"
    if paper.exists():
        html = paper.read_text(encoding="utf-8-sig")
        for token in ("arithmatex", "mathjax@3.2.2", 'class="mermaid"'):
            if token not in html:
                errors.append(f"paper example missing rendered token: {token}")

    technical = site_dir / "learning" / "multi-head-attention" / "index.html"
    if technical.exists() and "language-python highlight" not in technical.read_text(encoding="utf-8-sig"):
        errors.append("technical note missing syntax-highlighted code")

    errors.extend(find_missing_built_links(site_dir))
    return sorted(errors)


def validate_repository(root: Path = ROOT) -> list[str]:
    errors = []
    for relative in REQUIRED_FILES:
        if not (root / relative).exists():
            errors.append(f"missing required file: {relative}")

    for pattern, required in CONTENT_RULES.items():
        for path in root.glob(pattern):
            if path.name == "index.md":
                continue
            for message in check_front_matter(path, required):
                errors.append(f"{path.relative_to(root).as_posix()}: {message.split(': ', 1)[1]}")

    profile_path = root / "data" / "profile.yml"
    if profile_path.exists():
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8-sig")) or {}
        for key in ("name", "institution", "fields", "intro", "links", "interests"):
            if not profile.get(key):
                errors.append(f"data/profile.yml: missing profile field '{key}'")

    errors.extend(find_missing_local_assets(root / "docs"))
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--built", action="store_true", help="also validate generated site/ output")
    args = parser.parse_args()
    errors = validate_repository()
    if args.built:
        site_dir = ROOT / "site"
        if not site_dir.exists():
            errors.append("built site directory does not exist: run 'mkdocs build --strict' first")
        else:
            errors.extend(validate_built_site(site_dir))
    if errors:
        print("Site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    scope = "source and built output" if args.built else "source"
    print(f"Site checks passed ({scope}): structure, metadata, profile data, assets and links are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
