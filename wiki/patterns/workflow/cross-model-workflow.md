---
title: "跨模型工作流：多 LLM 交叉验证"
category: pattern
module: workflow
agents: [main, verifier, architect]
scope: global
tags: [cross-model, qa, codex, verification, multi-llm]
confidence: 0.8
sources: [shanraisshan/claude-code-best-practice]
status: draft
created: 2026-04-14
updated: 2026-04-14
---

# 跨模型工作流：多 LLM 交叉验证

> 用不同 LLM 提供商做规划和验证，利用模型差异消除单一模型的盲区。

## 模式描述

不同 LLM 有不同的训练数据、对齐策略和推理偏好。利用这种差异，让一个模型规划、另一个模型验证，可以发现单一模型无法察觉的问题。

## 核心流程

```
Claude (Opus) → 规划和设计
    ↓
Codex (GPT)  → QA 审查，插入 "Phase 2.5" 发现
    ↓
Claude (Sonnet) → 实施
    ↓
Codex (GPT)  → 最终验证
```

## 关键原则

1. **规划用最强推理模型** (Opus/GPT-5) — 需要深度思考
2. **验证用不同提供商** — 消除训练偏差盲区
3. **实施用最强编码模型** (Sonnet) — 平衡速度和质量
4. **QA 发现只增不改** — Codex 插入中间阶段，不重写已有计划

## Codex 中间阶段模式

Codex 审查 Plan 后，不重写 Plan，而是插入 "Phase 2.5" 等中间阶段：

```markdown
## Phase 2.5: Codex Finding

### 发现 1: 竞态条件风险
- **位置**: Plan Phase 3, Step 2
- **问题**: 多线程写入无锁保护
- **建议**: 添加 mutex 或使用原子操作

### 发现 2: API 兼容性
- **位置**: Plan Phase 4, Step 1
- **问题**: 新 API 端点与 v2 客户端不兼容
- **建议**: 添加版本协商中间件
```

## 与 AgentFlow 的集成

```
AgentFlow 规划阶段
    ↓ planner agent 产出 PLAN.md
Codex 审查（人工触发或自动化）
    ↓ 插入 Codex Findings
AgentFlow 实施阶段
    ↓ coder agent 执行
AgentFlow 验证阶段
    ↓ verifier agent + Codex 双验证
```

## 实践建议

1. **关键架构决策**必用跨模型验证
2. **简单功能**无需跨模型，单一模型足够
3. Codex 发现 **只增不改**，避免打乱已有计划
4. 验证结果差异大时，说明方案可能有问题，需重新评审
5. 不同模型对同一问题的分歧本身就有价值 — 它暴露了不确定性

## 限制

- 需要多个 LLM API 访问权限
- 增加工作流复杂度和时间
- 不同模型的指令格式不同，需要适配
- 适合关键路径决策，不适合日常开发

## 相关页面

- [[rpi-workflow|RPI 工作流]]
- [[agent-teams|Agent Teams 多会话协作]]
- [[llm-degradation|LLM 质量退化因素]]
