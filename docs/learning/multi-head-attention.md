---
title: Multi-head Attention
description: Multi-head Attention 的符号、张量形状与实现检查清单。
summary: 从公式、张量形状和最小代码理解 Multi-head Attention。
type: technical
date: 2026-09-09
updated: 2026-09-09
status: 草稿
tags:
  - Transformer
  - Attention
  - Deep Learning
---

# Multi-head Attention

<!-- AUTO:DOCUMENT_META -->

!!! note "笔记状态"
    这是技术排版示例，后续可继续补充推导、引用与实现验证。

## 定义

给定查询、键和值矩阵，单头缩放点积注意力为：

\[
\operatorname{Attention}(Q,K,V)
= \operatorname{softmax}\!\left(\frac{QK^{\mathsf T}}{\sqrt{d_k}}\right)V.
\]

多头注意力将不同线性投影的结果拼接：

\[
\operatorname{MHA}(Q,K,V)
= \operatorname{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)W^O.
\]

## 张量形状

| 张量 | 形状示例 | 说明 |
| --- | --- | --- |
| 输入 | `(B, L, D)` | batch、序列长度、模型维度 |
| 分头后 | `(B, H, L, D/H)` | `D` 需可被 `H` 整除 |
| 注意力矩阵 | `(B, H, L, L)` | 需要注意显存复杂度 |

## Python 示例

```python
import torch

batch, heads, length, head_dim = 2, 8, 128, 64
query = torch.randn(batch, heads, length, head_dim)
key = torch.randn_like(query)
scores = query @ key.transpose(-2, -1) / head_dim**0.5
assert scores.shape == (batch, heads, length, length)
```

## C++ 形状检查示意

```cpp
#include <cassert>

void validate_attention_shape(int model_dim, int heads) {
    assert(heads > 0);
    assert(model_dim % heads == 0);
}
```

## 常见问题

1. mask 的广播维度是否正确？
2. softmax 是否沿最后一个键序列维度计算？
3. 混合精度下 logits 是否出现溢出？
4. KV cache 是否与位置编码策略一致？
