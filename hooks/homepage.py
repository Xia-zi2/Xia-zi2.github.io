"""Generate the homepage's dynamic sections from Markdown front matter."""

from __future__ import annotations

from datetime import date, datetime
from html import escape
from pathlib import Path
from typing import Any, Iterable

import yaml


MARKERS = {
    "profile": "<!-- AUTO:PROFILE -->",
    "interests": "<!-- AUTO:INTERESTS -->",
    "projects": "<!-- AUTO:PROJECTS -->",
    "notes": "<!-- AUTO:RECENT_NOTES -->",
    "blog": "<!-- AUTO:RECENT_BLOG -->",
    "document_meta": "<!-- AUTO:DOCUMENT_META -->",
}


def parse_front_matter(text: str) -> dict[str, Any]:
    """Return YAML front matter from a Markdown document."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}
    normalized = text.replace("\r\n", "\n", 1)
    try:
        _, raw, _ = normalized.split("---", 2)
    except ValueError:
        return {}
    data = yaml.safe_load(raw) or {}
    return data if isinstance(data, dict) else {}


def _as_text(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return "" if value is None else str(value)


def _sort_date(entry: dict[str, Any]) -> str:
    return _as_text(entry.get("updated") or entry.get("date") or "0000-00-00")


def _route_for(path: Path, docs_dir: Path) -> str:
    relative = path.relative_to(docs_dir).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "index":
        parts.pop()
    return "/".join(parts) + "/"


def collect_documents(docs_dir: Path | str, folders: Iterable[str]) -> list[dict[str, Any]]:
    """Collect published Markdown entries and sort them by newest update."""
    root = Path(docs_dir)
    entries: list[dict[str, Any]] = []
    for folder in folders:
        section = root / folder
        if not section.exists():
            continue
        for path in section.rglob("*.md"):
            if path.name == "index.md":
                continue
            meta = parse_front_matter(path.read_text(encoding="utf-8-sig"))
            if not meta or bool(meta.get("draft", False)):
                continue
            entry = dict(meta)
            entry.setdefault("title", path.stem.replace("-", " ").title())
            entry.setdefault("summary", entry.get("description", ""))
            if folder.replace("\\", "/").rstrip("/") == "blog/posts":
                entry["url"] = f"blog/{_as_text(meta.get('slug') or path.stem)}/"
            else:
                entry["url"] = _route_for(path, root)
            entry["source"] = path.relative_to(root).as_posix()
            entry["section"] = folder.split("/", 1)[0]
            entries.append(entry)
    return sorted(entries, key=_sort_date, reverse=True)


def _safe_link(value: Any) -> str | None:
    link = _as_text(value).strip()
    if not link or link.upper().startswith("TODO"):
        return None
    return link


def render_profile(profile: dict[str, Any]) -> str:
    """Render the compact academic identity block."""
    links = profile.get("links", {}) or {}
    fields = " · ".join(escape(_as_text(item)) for item in profile.get("fields", []))
    buttons: list[str] = []
    labels = (("github", "GitHub"), ("email", "Email"), ("cv", "CV"), ("scholar", "Google Scholar"), ("orcid", "ORCID"))
    for key, label in labels:
        url = _safe_link(links.get(key))
        if url:
            external = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
            buttons.append(
                f'<a class="profile-link" href="{escape(url, quote=True)}"{external}>{escape(label)}</a>'
            )
        elif key == "email":
            buttons.append('<span class="profile-link profile-link--muted">Email（待补充）</span>')

    avatar = escape(_as_text(profile.get("avatar", "assets/images/avatar-placeholder.svg")), quote=True)
    return (
        '<section class="academic-hero" aria-labelledby="profile-name">'
        '<div class="academic-hero__content">'
        f'<p class="eyebrow">{escape(_as_text(profile.get("eyebrow", "个人学术主页 · Research Notes")))}</p>'
        f'<h1 id="profile-name">{escape(_as_text(profile.get("name", "TODO：姓名")))}</h1>'
        f'<p class="academic-hero__institution">{escape(_as_text(profile.get("institution", "TODO：学校 / 单位")))}</p>'
        f'<p class="academic-hero__fields">{fields}</p>'
        f'<p class="academic-hero__intro">{escape(_as_text(profile.get("intro", "TODO：个人简介")))}</p>'
        f'<div class="profile-links">{"".join(buttons)}</div>'
        '</div>'
        '<div class="academic-hero__visual">'
        f'<img src="{avatar}" alt="个人头像占位图，可在 data/profile.yml 中替换" width="240" height="240">'
        '<p>头像 / 标识待替换</p>'
        '</div>'
        '</section>'
    )


def render_interests(profile: dict[str, Any]) -> str:
    cards = []
    for item in profile.get("interests", []):
        name = escape(_as_text(item.get("name")))
        description = escape(_as_text(item.get("description")))
        cards.append(
            '<article class="interest-card">'
            f'<h3>{name}</h3><p>{description}</p>'
            '</article>'
        )
    return '<div class="interest-grid">' + "".join(cards) + "</div>"


def _tag_list(tags: Any) -> str:
    if isinstance(tags, str):
        tags = [tags]
    return "".join(f'<span class="tag-chip">{escape(_as_text(tag))}</span>' for tag in (tags or []))


def render_projects(projects: Iterable[dict[str, Any]], limit: int = 6) -> str:
    """Render featured projects ordered by explicit editorial weight."""
    featured = [project for project in projects if project.get("featured", False)]
    featured.sort(key=lambda item: (int(item.get("weight", 999)), _sort_date(item)))
    cards = []
    for project in featured[:limit]:
        url = escape(_as_text(project.get("url")), quote=True)
        image = escape(_as_text(project.get("image", "assets/images/project-placeholder.svg")), quote=True)
        title = escape(_as_text(project.get("title")))
        summary = escape(_as_text(project.get("summary") or project.get("description")))
        date_text = escape(_as_text(project.get("period") or project.get("date")))
        actions = [f'<a href="{url}">项目详情</a>']
        for key, label in (("github", "GitHub"), ("project", "Project Page"), ("notes", "Notes")):
            link = _safe_link(project.get(key))
            if link:
                actions.append(f'<a href="{escape(link, quote=True)}">{label}</a>')
        cards.append(
            '<article class="project-card">'
            f'<a class="project-card__image" href="{url}"><img src="{image}" alt="{title} 项目图片占位" loading="lazy"></a>'
            '<div class="project-card__body">'
            f'<p class="project-card__date">{date_text}</p>'
            f'<h3><a href="{url}">{title}</a></h3>'
            f'<p>{summary}</p><div class="tag-row">{_tag_list(project.get("tags"))}</div>'
            f'<div class="project-card__links">{"".join(actions)}</div>'
            '</div></article>'
        )
    return '<div class="project-grid">' + "".join(cards) + "</div>"


def render_recent(entries: Iterable[dict[str, Any]], limit: int = 5) -> str:
    labels = {
        "papers": "论文阅读",
        "reproductions": "论文复现",
        "learning": "技术笔记",
        "blog": "博客",
    }
    rows = []
    for entry in list(entries)[:limit]:
        title = escape(_as_text(entry.get("title")))
        summary = escape(_as_text(entry.get("summary") or entry.get("description")))
        url = escape(_as_text(entry.get("url")), quote=True)
        date_text = escape(_sort_date(entry))
        kind = escape(labels.get(_as_text(entry.get("section")), _as_text(entry.get("type", "笔记"))))
        rows.append(
            '<li class="recent-item">'
            f'<div><span class="recent-item__type">{kind}</span><a href="{url}">{title}</a>'
            f'<p>{summary}</p></div><time>{date_text}</time>'
            '</li>'
        )
    return '<ul class="recent-list">' + "".join(rows) + "</ul>"


def render_document_meta(meta: dict[str, Any]) -> str:
    """Render optional structured metadata for research and project pages."""
    rows: list[str] = []
    labels = {
        "authors": "作者",
        "venue": "会议 / 期刊",
        "year": "年份",
        "status": "状态",
        "period": "时间",
        "cuda": "CUDA",
        "pytorch": "PyTorch",
    }
    for key, label in labels.items():
        value = meta.get(key)
        if isinstance(value, list):
            value = "、".join(_as_text(item) for item in value)
        text = _as_text(value).strip()
        if not text or text.upper().startswith("TODO"):
            continue
        rows.append(
            f'<div><dt>{escape(label)}</dt><dd>{escape(text)}</dd></div>'
        )

    links: list[str] = []
    link_labels = {
        "paper": "论文",
        "code": "代码",
        "project": "项目主页",
        "repository": "Repository",
    }
    for key, label in link_labels.items():
        url = _safe_link(meta.get(key))
        if url:
            links.append(
                f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener">{escape(label)}</a>'
            )
    if links:
        rows.append(f'<div><dt>链接</dt><dd class="document-meta__links">{"".join(links)}</dd></div>')
    if not rows:
        return ""
    return '<dl class="document-meta" aria-label="页面元数据">' + "".join(rows) + "</dl>"


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str | None:
    """Replace homepage markers during a MkDocs build."""
    document_marker = MARKERS["document_meta"]
    if document_marker in markdown:
        markdown = markdown.replace(document_marker, render_document_meta(dict(getattr(page, "meta", {}) or {})))

    if getattr(page.file, "src_uri", "") != "index.md":
        return markdown

    docs_dir = Path(config["docs_dir"])
    project_root = Path(config.config_file_path).parent
    profile = yaml.safe_load((project_root / "data" / "profile.yml").read_text(encoding="utf-8-sig")) or {}
    projects = collect_documents(docs_dir, ["projects"])
    notes = collect_documents(docs_dir, ["papers", "reproductions", "learning"])
    blog = collect_documents(docs_dir, ["blog/posts"])

    replacements = {
        MARKERS["profile"]: render_profile(profile),
        MARKERS["interests"]: render_interests(profile),
        MARKERS["projects"]: render_projects(projects),
        MARKERS["notes"]: render_recent(notes),
        MARKERS["blog"]: render_recent(blog, limit=3),
    }
    for marker, generated in replacements.items():
        markdown = markdown.replace(marker, generated)
    return markdown
