---
title: "LLM 输出质量退化与上下文污染"
category: concept
module: workflow
agents: [main, verifier, researcher]
scope: global
tags: [llm, degradation, context-pollution, quality, compact]
confidence: 0.85
sources: [shanraisshan/claude-code-best-practice, Anthropic infrastructure reports]
status: verified
created: 2026-04-14
updated: 2026-04-14
---

# LLM 输出质量退化与上下文污染

> LLM 输出质量在会话内退化，90% 是上下文污染，不是模型变笨。

## 问题描述

LLM 输出质量在长会话中明显退化，开发者常误以为是"模型变差了"，实际原因多为上下文窗口被无关信息污染。

## 退化的9层因素（从模型权重向上）

```
权重层（最低层，很少是原因）
  ↑ 1. 模型权重更新（罕见）
  ↑ 2. 后训练对齐（罕见）
  ↑ 3. 采样参数变化（罕见）
  ↑ 4. 推测解码路径差异（偶发）
  ↑ 5. MoE 路由方差（±8-14% 日间波动）
  ↑ 6. 硬件路由（TPU 分配不同）
  ↑ 7. 量化差异（API 端少见）
  ↑ 8. 编译器/运行时行为（已确认 3 个 Anthropic 基础设施 bug）
  ↑ 9. 系统提示 + 上下文窗口（最常见原因）← 90% 在这里
```

## 已确认的 Anthropic 基础设施 Bug

| Bug | 影响范围 | 状态 |
|-----|---------|------|
| 上下文窗口路由错误 | 最多 16% 请求 | 已修复 |
| TPU 输出损坏 | 随机 | 已修复 |
| XLA:TPU 编译器误编译 | 特定请求模式 | 已修复 |

## 上下文污染（最常见原因）

### 症状

- 回答越来越模糊、不够精确
- 开始"忘记"之前的指令
- 输出偏向对话中偶然出现的错误方向
- 同样的问题，会话初期回答很好，后期变差

### 原因

- 错误信息进入上下文后，后续生成被带偏
- 大量无关代码/日志占据上下文，有效指令被"稀释"
- 长对话中的中途方向变化导致信号冲突

### 修复方法

```
发现质量退化时：
1. /compact — 精简上下文（首选，保留会话）
2. 新开会话 — 完全重置（退化为严重时）
3. CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50 — 降低自动压缩阈值
4. 将长任务拆分为独立 Agent — 每个 Agent 有独立上下文窗口
```

## MoE 路由方差

Scale AI 研究发现：同一 prompt 在不同时间执行，质量波动 ±8-14%。这是 MoE（混合专家）架构的固有特性，非 bug。

**应对**：关键任务执行 2-3 次取最优结果，不要因一次结果差就放弃。

## 实践建议

1. **定期 compact**: 上下文超过 60% 时主动 `/compact`
2. **任务隔离**: 复杂任务用独立 Agent，避免上下文交叉污染
3. **不假设模型退步**: 先检查上下文污染，再怀疑模型质量
4. **降低 auto-compact 阈值**: 设置 `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50`
5. **批量任务用 /batch**: 避免单个长会话处理大量独立任务

## 相关页面

- [[context-pollution|上下文污染踩坑]]
- [[fatal-transient-errors|FATAL/TRANSIENT错误分类]]
