# 李亭皑的个人科研主页

这是一个中文优先的“个人学术主页 + 项目展示 + 研究知识库”，计划部署到：

**<https://Xia-zi2.github.io/>**

首页用于快速了解个人背景、研究兴趣、代表项目和最近研究动态；详细内容按项目、论文阅读、论文复现、技术笔记和 Blog 分开维护。它是静态站点，不需要服务器、数据库、登录系统、CMS 或付费服务。

## 技术方案

本站基于 [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) 9.7.7（MIT License）构建，并使用少量本地 CSS、SVG 和 Python 构建 hook 完成学术首页与内容自动聚合。

选择它的主要原因是：

- 中文界面、全文搜索、左侧知识库导航和页面目录成熟；
- Markdown、LaTeX、Mermaid、表格和代码高亮由稳定组件支持；
- Blog、Notes 和 Projects 可以保持不同的信息结构；
- 新增内容只需添加 Markdown，首页最近更新会在构建时自动生成；
- GitHub Actions 可以直接生成静态文件并部署到 GitHub Pages。

候选模板和完整取舍记录见[设计说明](docs/superpowers/specs/2026-09-11-academic-homepage-design.md)。上游 attribution 见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## Repository 结构

```text
.
├── data/profile.yml              # 姓名、单位、简介和链接的唯一配置入口
├── docs/
│   ├── index.md                  # 首页内容槽位
│   ├── projects/                 # 项目页
│   ├── papers/                   # 论文阅读
│   ├── reproductions/            # 论文复现
│   ├── learning/                 # 技术笔记
│   ├── blog/posts/               # Blog 文章
│   └── assets/                   # 图片、脚本、样式和下载文件
├── content-templates/            # 新内容模板
├── hooks/homepage.py             # 首页自动聚合与页面元数据
├── overrides/                    # 最小主题覆盖
├── scripts/check_site.py         # 内容与资源检查
├── tests/                        # 构建 hook 和仓库结构测试
├── .github/workflows/deploy.yml  # GitHub Pages 自动部署
├── mkdocs.yml                    # 站点、导航和 Markdown 配置
└── requirements.txt              # 固定版本依赖
```

## 首次配置个人信息

优先修改以下位置，不要在多个页面复制同一份资料：

1. `data/profile.yml`：姓名、学校、方向、简介、头像、GitHub、Email、CV、Scholar 和 ORCID。
2. `mkdocs.yml`：`site_name`、`site_description`、`site_url`、`repo_name`、`repo_url` 和页脚版权。
3. `docs/about.md` 与 `docs/cv.md`：只填写已经确认的详细经历。
4. `docs/assets/images/avatar-placeholder.svg`：替换为真实头像或个人标识，并同步修改 `data/profile.yml` 的 `avatar`。
5. `docs/assets/files/cv.pdf`：放入正式 PDF 后启用 `docs/cv.md` 中的下载链接。

仓库当前没有虚构邮箱、教育阶段、导师、论文、奖项、工作经历或实验结果。所有未知信息都明确标为 `TODO`。

## 本地运行

建议使用 Python 3.12 或 3.13。

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
mkdocs serve
```

macOS / Linux：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

然后打开 <http://127.0.0.1:8000/>。开发服务器会监听 Markdown、配置和样式的修改并自动刷新。

## 新增 Paper Note

复制 `content-templates/paper-note.md` 到 `docs/papers/<slug>.md`。按需填写：

```yaml
title:
authors:
venue:
year:
paper:
code:
project:
tags:
date:
updated:
status:
```

值为 `TODO` 的链接和元数据不会显示为可点击的真实信息。写完后，如需在顶部导航固定展示，再把页面加入 `mkdocs.yml`；即使不加入导航，页面仍会参与搜索、标签和首页最近更新。

如果不想使用本地命令，可以在仓库页面按 `.` 打开 github.dev 在线编辑器。站内的 `docs/writing.md` 提供了从复制模板到 Commit & Push 的完整图文式步骤。

## 新增 Reproduction Note

复制 `content-templates/reproduction-note.md` 到 `docs/reproductions/<slug>.md`。重点记录 Repository 的 commit SHA、系统/GPU/CUDA/PyTorch 版本、数据校验、运行命令、Bug / Fix 和最终状态。

## 新增 Technical Note

复制 `content-templates/technical-note.md` 到 `docs/learning/<topic>/<slug>.md`。建议按主题组织目录，并在 `mkdocs.yml` 的“笔记”导航中增加入口。

## 新增 Project

复制 `content-templates/project.md` 到 `docs/projects/<slug>.md`：

- `featured: true`：允许首页展示；
- `weight`：首页排序，数字越小越靠前；
- `image`：从站点根目录 `docs/` 开始的图片路径；
- `github`、`project`、`notes`：可选链接，`TODO` 不会渲染为按钮。

## 新增 Blog

复制 `content-templates/blog-post.md` 到 `docs/blog/posts/<slug>.md`。Blog 必须有 `date`，可以添加 `categories` 和 `tags`。Blog 适合完整文章；零散过程和实验日志应优先写入 Notes。

## 数学、图和代码

行间公式使用：

```text
\[
\mathcal{L} = \mathcal{L}_{recon} + \lambda \mathcal{L}_{reg}
\]
```

Mermaid 使用 `mermaid` fenced code block；代码块使用 `python`、`cpp`、`bash` 或其他 Pygments 语言名。示例见 `docs/papers/lightrag.md`、`docs/reproductions/arthoi.md` 和 `docs/learning/multi-head-attention.md`。

## 检查与构建

提交前运行：

```bash
python -m unittest discover -s tests -v
python scripts/check_site.py
mkdocs build --strict
```

静态输出位于 `site/`。严格构建会阻止带配置警告或构建错误的版本进入部署流程。

## GitHub Pages 部署

1. 在 GitHub 创建公开仓库 **`Xia-zi2.github.io`**。
2. 将本仓库推送到它的 `main` 分支。
3. 进入仓库 **Settings → Pages**。
4. 在 **Build and deployment → Source** 选择 **GitHub Actions**。
5. push 到 `main` 后，`.github/workflows/deploy.yml` 会执行测试、内容检查、严格构建并部署。
6. 在 Actions 页面确认“构建并部署 GitHub Pages”成功，随后访问 <https://Xia-zi2.github.io/>。

流程如下：

```text
git push → GitHub Actions → mkdocs build --strict → GitHub Pages
```

GitHub Pages 会自动提供 HTTPS。因为这是用户主页仓库且 `site_url` 使用根路径，CSS、JavaScript 和图片都会从正确的相对路径加载。

## License

本仓库的自定义代码与示例内容采用 [MIT License](LICENSE)。Material for MkDocs 保留其原始 MIT License 与版权；详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。发布真实个人内容前，如果你希望文章采用不同许可，请明确添加内容许可说明。
