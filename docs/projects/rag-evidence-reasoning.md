---
title: RAG / Evidence Reasoning Research
description: 可追溯检索与证据推理项目页面结构示例；内容待补充。
summary: 面向可靠问答的检索、证据组织与推理流程探索。
type: project
date: 2026-09-09
updated: 2026-09-09
period: "TODO：填写项目时间"
status: 文献调研中
featured: true
weight: 30
tags:
  - RAG
  - Evidence Reasoning
  - Agent
image: assets/images/project-placeholder.svg
github: "TODO：填写仓库链接"
project: "TODO：填写项目主页"
---

# RAG / Evidence Reasoning Research

<!-- AUTO:DOCUMENT_META -->

!!! warning "占位说明"
    本页用于组织研究计划与过程，不声明尚未完成的模型、数据集或结果。

## 目标

TODO：描述任务边界、证据可追溯要求和目标评价指标。

## 初步框架

```mermaid
flowchart LR
    Q[问题] --> R[检索]
    R --> E[证据选择]
    E --> G[基于证据生成]
    G --> V[引用与一致性检查]
```

## 待验证问题

- 如何衡量检索覆盖率与证据充分性？
- 如何区分模型记忆与可引用证据？
- 如何记录失败查询和修正过程？
