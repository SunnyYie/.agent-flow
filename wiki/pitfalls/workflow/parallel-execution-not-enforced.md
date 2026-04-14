---
title: "多Agent并行未强制执行"
category: pitfall
module: workflow
agents: [main, planner, coder, verifier]
scope: global
tags: [parallel, multi-agent, efficiency, agent-orchestration]
confidence: 0.85
status: open
created: 2026-04-14
---

# 多Agent并行未强制执行

## 问题描述

agent-flow 铁律要求"多Agent并行"（验收、写代码、测试时），但实际执行中各阶段倾向串行处理，没有强制并行机制。

**典型表现**：
- Research 阶段：飞书文档读取和代码搜索串行执行，可并行
- Plan 阶段：Explore Agent 搜索数据流和 Main Agent 读取代码串行执行
- Implement 阶段：独立子任务串行执行
- 验收阶段：Verifier + Main 双验收未并行

## 影响

- 总耗时增加 30-50%
- 单视角验收容易遗漏问题

## 根因

1. 无 hook 强制检查并行执行
2. agent-orchestration skill 只描述流程，不强制并行
3. Agent 调度倾向串行（更简单、更可控）

## 解决方案

**短期**：在 agent-orchestration skill 中增加并行检查点，标注哪些步骤必须并行。

**长期**：创建 parallel-enforce.py hook，在特定阶段转换时检查是否有并行 Agent 在运行。

## 频率

每次 Complex 任务都会遇到。
