# Academic Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Chinese-first academic homepage and research knowledge base that deploys to `Xia-zi2.github.io` from Markdown.

**Architecture:** Material for MkDocs supplies navigation, search, blog, tags, code highlighting and responsive theming. A focused Python build hook scans YAML front matter to render profile, featured projects and recent content on the homepage without duplicating content. GitHub Actions builds and deploys the static output.

**Tech Stack:** Python 3.12, MkDocs, Material for MkDocs, PyMdown Extensions, MathJax, Mermaid, GitHub Pages Actions.

---

### Task 1: Repository and framework configuration

**Files:**
- Create: `mkdocs.yml`
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `THIRD_PARTY_NOTICES.md`

- [ ] Pin the small Python dependency set and configure Chinese navigation, light/dark palettes, search, tags, blog, MathJax, Mermaid, code highlighting, sitemap and strict builds.
- [ ] Add MIT license and Material for MkDocs attribution.
- [ ] Run `python -m pip install -r requirements.txt`; expect exit code 0.

### Task 2: Test homepage content aggregation first

**Files:**
- Create: `tests/test_homepage_hook.py`
- Create: `hooks/homepage.py`
- Create: `data/profile.yml`

- [ ] Write tests that define the required behavior: parse front matter, ignore drafts, sort by updated/date descending, choose featured projects by weight, render profile placeholders safely, and generate relative links.
- [ ] Run `python -m unittest discover -s tests -v`; expect failures because `hooks.homepage` does not exist.
- [ ] Implement the minimum pure functions and MkDocs `on_page_markdown` hook.
- [ ] Re-run the suite; expect all tests to pass.

### Task 3: Homepage and visual system

**Files:**
- Create: `docs/index.md`
- Create: `docs/assets/stylesheets/extra.css`
- Create: `docs/assets/javascripts/mathjax.js`
- Create: `docs/assets/images/favicon.svg`
- Create: `docs/assets/images/avatar-placeholder.svg`
- Create: `docs/assets/images/project-placeholder.svg`
- Create: `overrides/partials/extrahead.html`
- Create: `overrides/partials/footer.html`

- [ ] Add hook placeholders for Hero, interests, selected projects, recent Notes and recent Blog.
- [ ] Implement compact academic cards, restrained colors, focus styles and responsive single-column behavior.
- [ ] Add a simple site-specific favicon and neutral replaceable placeholders.
- [ ] Add canonical/Open Graph metadata without inventing a social image.

### Task 4: Information architecture and representative content

**Files:**
- Create: `docs/projects/index.md`
- Create: `docs/projects/arthoi-reconstruction.md`
- Create: `docs/research/index.md`
- Create: `docs/papers/index.md`
- Create: `docs/papers/lightrag.md`
- Create: `docs/reproductions/index.md`
- Create: `docs/reproductions/arthoi.md`
- Create: `docs/learning/index.md`
- Create: `docs/learning/multi-head-attention.md`
- Create: `docs/blog/index.md`
- Create: `docs/blog/posts/welcome.md`
- Create: `docs/about.md`
- Create: `docs/cv.md`
- Create: `docs/tags.md`
- Create: `docs/404.md`

- [ ] Add one honest placeholder example for each requested content type, explicitly marking unknown claims and results as TODO.
- [ ] Demonstrate paper metadata, a display equation, Mermaid pipeline, tables, Python/C++/Bash highlighting, images and external citations.
- [ ] Keep Notes and Blog distinct in both copy and route structure.

### Task 5: Maintenance documentation and automation

**Files:**
- Create: `README.md`
- Create: `docs/CONTRIBUTING.md`
- Create: `.github/workflows/deploy.yml`
- Create: `scripts/check_site.py`
- Create: `tests/test_site_structure.py`

- [ ] Test the required site structure, nav targets, asset references and front matter fields before implementing the checker.
- [ ] Add clear copy-paste templates for Paper Note, Reproduction, Project, Technical Note and Blog.
- [ ] Configure least-privilege GitHub Pages deployment with concurrency protection and strict build.

### Task 6: Verification

- [ ] Run `python -m unittest discover -s tests -v`; expect zero failures.
- [ ] Run `python scripts/check_site.py`; expect all required content and local assets to pass.
- [ ] Run `mkdocs build --strict`; expect exit code 0 and a generated `site/` tree.
- [ ] Serve the built site locally and verify the homepage plus representative routes at desktop and mobile widths.
- [ ] Check generated HTML for MathJax, Mermaid, search index, canonical/OG metadata, favicon, code markup, tags, sitemap, robots and 404.
- [ ] Review `git diff --check` and `git status` before handoff.
