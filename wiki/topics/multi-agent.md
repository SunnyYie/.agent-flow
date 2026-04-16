---
title: "主题：Multi-Agent 多Agent协作"
category: topic-hub
module: multi-agent
agents: [main, planner, coder, verifier, architect]
scope: global
tags: [multi-agent, topic-hub]
confidence: 1.0
status: verified
created: 2026-04-15
updated: 2026-04-15
---

# 主题：Multi-Agent 多Agent协作

> 多Agent协作模式、编排策略、并行执行、角色定义。从架构到执行的全链路知识。

## Patterns（成功模式）

- [[three-agent-model|patterns/workflow/three-agent-model]] — 三Agent协作模型（双验收 + 生命周期 + 并行执行）
- [[agent-teams|patterns/workflow/agent-teams]] — 多会话并行协作（tmux + worktree + 共享任务列表）
- [[orchestrator-workers|patterns/workflow/orchestrator-workers]] — 编排器-工作者模式（任务分解+并行执行）

## Pitfalls（踩坑记录）

- [[parallel-execution-not-enforced|pitfalls/workflow/parallel-execution-not-enforced]] — 多Agent并行未强制执行
- [[skipping-verifier|pitfalls/workflow/skipping-verifier]] — 跳过验证者的后果
- [[code-review-not-triggered|pitfalls/workflow/code-review-not-triggered]] — 代码审查未自动触发
- [[multi-agent-rate-limit-recovery|pitfalls/workflow/multi-agent-rate-limit-recovery]] — 多Agent并行429失败：主Agent必须Glob检查+兜底

## Concepts（相关概念）

- [[agent-roles|concepts/agent-roles]] — 多角色协作体系（Main/Planner/Coder/Writer/Researcher/Verifier/Architect）
- [[agent-resolution-order|concepts/agent-resolution-order]] — Agent 调度优先级：Command → Agent → Skill

## Related Topics（关联主题）

- [[workflow|topics/workflow]] — 多Agent是工作流执行的核心机制
- [[architecture|topics/architecture]] — 多Agent架构设计决策
