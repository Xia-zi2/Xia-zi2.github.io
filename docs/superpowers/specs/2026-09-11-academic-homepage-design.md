# 个人学术主页设计说明

## 目标

为 `Xia-zi2.github.io` 建立一个中文优先、低维护成本的静态学术主页。网站同时承担个人介绍、项目展示、科研知识库和公开博客四个职责，首页不以时间流为中心。

## 模板调研与选型

| 方案 | GitHub / License | 页面结构与优势 | GitHub Pages 与维护 | 主要不足 |
| --- | --- | --- | --- | --- |
| al-folio | `alshedivat/al-folio`，MIT，约 15.7k Star | 学术主页、论文、项目和 Blog 完整；视觉成熟；数学和代码支持完善 | 官方 Actions；Markdown + Jekyll | Ruby/Jekyll 插件链较重；深层 Notes、中文搜索和知识库导航不是核心场景；定制后升级易冲突 |
| Academic Pages | `academicpages/academicpages.github.io`，MIT，约 17.1k Star | 经典学术主页；履历、论文、Talk、Portfolio 完整 | 原生 GitHub Pages 友好；Markdown | 界面与信息架构偏传统；本地 Ruby 环境较重；多层技术笔记、中文化与搜索扩展成本较高 |
| HugoBlox Academic CV | `HugoBlox/theme-academic-cv`，MIT，约 5.0k Star | 学术简历与项目组件丰富；Hugo 构建快；Markdown 内容 | 支持 GitHub Pages | Block 配置层较多；模板生态变化较快；免费/Pro 边界和升级迁移提高长期维护成本 |
| Material for MkDocs | `squidfunk/mkdocs-material`，MIT，约 27k Star | 强项是分层知识库、全文搜索、页面 TOC、标签、代码、数学、Mermaid、Blog 和移动端阅读 | 单一 Python 依赖集；Actions 构建；新增内容就是 Markdown | 默认是文档站，需要少量主题覆盖才能形成真正的学术首页 |

选择 **Material for MkDocs**。它不是最“学术模板化”的候选，但与本项目长期内容结构最吻合。个人主页所需的 Hero、研究方向和项目卡片只需少量 HTML/CSS；而 Notes、搜索、目录、标签、公式与代码等长期使用频率更高的能力由成熟框架直接提供。

## 架构

- `mkdocs.yml`：站点导航、中文界面、Markdown 扩展、主题与插件配置。
- `data/profile.yml`：姓名、单位、方向和外部链接的唯一资料源；未知字段保留 TODO。
- `docs/`：所有公开内容。项目、论文阅读、复现、技术笔记与 Blog 分目录维护。
- `hooks/homepage.py`：构建时读取 profile 与各内容目录的 YAML front matter，生成首页 Hero、研究方向、代表项目、最近 Notes 和最近 Blog。
- `overrides/`：只覆盖必要的首页布局和 head 元数据，不复制 Material 主题的大量模板。
- `docs/assets/stylesheets/extra.css`：站点视觉系统、首页卡片、元数据区块和响应式样式。
- `.github/workflows/deploy.yml`：push 到 `main` 后构建并上传 GitHub Pages artifact。

## 内容流

作者新增 Markdown 文件并填写 front matter。MkDocs 构建时，导航、全文搜索、标签和 Blog 归档由框架生成；自定义 hook 读取日期、类型、摘要和 featured 字段，自动更新首页列表。Git 历史承担版本记录，不引入数据库、CMS 或客户端状态。

## 页面与导航

一级导航保持六项：首页、项目、研究/论文、笔记、博客、关于/CV。论文阅读与复现分别建库；技术笔记按学科分组，并启用左侧导航、页内 TOC 和上一篇/下一篇。

## 视觉方向

整体使用高信息密度但留白克制的学术风格。色彩以深海军蓝和青绿色为强调色，浅色/暗色模式均保持高对比。首页头像使用可替换的中性占位，不出现巨型 Hero、动画、渐变或技能百分比。项目图片位置固定比例，便于以后替换真实结果图。

## 兼容性与可访问性

- 正文基础字号不低于 16px，移动端卡片改单列。
- 链接和按钮有清晰焦点样式；所有图片要求 alt 文本。
- 数学由 MathJax 渲染；Mermaid 使用 Material 官方集成方式；代码由 Pygments 高亮。
- 严格构建用于捕获断链；另加脚本检查首页自动聚合、必需文件和本地资源引用。

## 许可证

项目自定义代码采用 MIT License。Material for MkDocs 作为依赖使用并在 `THIRD_PARTY_NOTICES.md` 中保留来源和 MIT attribution；不复制上游 demo 或主题源代码。

## 部署

仓库名使用 `Xia-zi2.github.io`，`site_url` 指向 `https://Xia-zi2.github.io/`。GitHub Actions 使用官方 Pages artifact 流程：checkout → Python 环境 → 固定依赖安装 → 严格构建 → deploy-pages。无需服务器、数据库或付费服务。
