# 内容维护约定

## 最短发布流程

1. 从 `content-templates/` 复制对应模板到 `docs/` 下的内容目录。
2. 修改文件名、front matter 和正文；日期使用 `YYYY-MM-DD`。
3. 本地运行测试、内容检查和严格构建。
4. 提交并推送到 `main`，GitHub Actions 自动部署。

```bash
python -m unittest discover -s tests -v
python scripts/check_site.py
mkdocs build --strict
git add .
git commit -m "docs: add note about ..."
git push
```

## 内容边界

- `projects/`：围绕一个项目组织目标、实现和结果。
- `papers/`：理解论文，强调问题、方法、公式和评价。
- `reproductions/`：重新运行论文代码，强调环境、命令、问题和真实结果。
- `learning/`：按主题长期修订的技术知识。
- `blog/posts/`：已经整理为完整叙事的公开文章。

## Front matter

- `description` 用于页面 metadata 和搜索摘要。
- `summary` 用于首页卡片或最近更新列表。
- `date` 是首次记录时间；`updated` 是最近实质更新日期。
- `draft: true` 的内容不会出现在首页自动列表中；发布前改为 `false`。
- 项目设置 `featured: true` 才会进入首页，`weight` 越小越靠前。
- 不确定的信息保留 `TODO`，不要用看似合理的内容代替核验。

## 图片与大文件

- 通用图片放在 `docs/assets/images/`；CV 等下载文件放在 `docs/assets/files/`。
- 图片必须提供有意义的 alt 文本。
- 不要提交密钥、Token、私有数据集路径或包含个人信息的终端日志。
- 视频优先使用稳定外链；确需仓库存储时先评估文件大小和 Git LFS。
