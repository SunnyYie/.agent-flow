---
title: "主题：Workflow 工作流"
category: topic-hub
module: workflow
agents: [main, planner, coder, verifier, researcher, architect]
scope: global
tags: [workflow, topic-hub]
confidence: 1.0
status: verified
created: 2026-04-15
updated: 2026-04-15
---

# 主题：Workflow 工作流

> 工作流执行、多Agent协作、质量门控相关的全部知识。涵盖从搜索先行到验收完成的全流程。

## Patterns（成功模式）

- [[search-before-execute|patterns/workflow/search-before-execute]] — 先查后执行 + 搜索到开发一步到位
- [[three-agent-model|patterns/workflow/three-agent-model]] — 三Agent协作模型（双验收 + 生命周期 + 并行执行）
- [[rpi-workflow|patterns/workflow/rpi-workflow]] — RPI 工作流：Research→Plan→Implement + GO/NO-GO 门控
- [[cross-model-workflow|patterns/workflow/cross-model-workflow]] — 跨模型交叉验证（Claude 规划 + Codex QA）
- [[agent-teams|patterns/workflow/agent-teams]] — 多会话并行协作（tmux + worktree + 共享任务列表）
- [[test-matrix-5-dimension-check|patterns/workflow/test-matrix-5-dimension-check]] — 测试矩阵5维检查（覆盖度/可追溯/自动化映射/边界场景/双验收）
- [[e2e-script-three-part-structure|patterns/workflow/e2e-script-three-part-structure]] — 联调脚本三段式结构（输入模板+预期输出+验证要点）
- [[orchestrator-workers|patterns/workflow/orchestrator-workers]] — 编排器-工作者模式（任务分解+并行执行）

## Pitfalls（踩坑记录）

- [[execute-without-search|pitfalls/workflow/execute-without-search]] — 不查就执行（4种表现：跳过搜索/已知问题重复/先试错再查/研究阶段搜过以为实施阶段不用搜）
- [[git-archaeology-oversearch|pitfalls/workflow/git-archaeology-oversearch]] — Git考古过度搜索
- [[skip-implementation-plan|pitfalls/workflow/skip-implementation-plan]] — 跳过实施计划文档直接开发
- [[broad-keyword-search|pitfalls/workflow/broad-keyword-search]] — 泛化关键词搜索导致范围扩大
- [[skipping-verifier|pitfalls/workflow/skipping-verifier]] — 跳过验证者的后果
- [[promotion-duplication|pitfalls/workflow/promotion-duplication]] — 晋升时创建重复内容而非更新已有文档
- [[parallel-execution-not-enforced|pitfalls/workflow/parallel-execution-not-enforced]] — 多Agent并行未强制执行
- [[code-review-not-triggered|pitfalls/workflow/code-review-not-triggered]] — 代码审查未自动触发
- [[multi-agent-rate-limit-recovery|pitfalls/workflow/multi-agent-rate-limit-recovery]] — 多Agent并行429失败：主Agent必须Glob检查+兜底

## Concepts（相关概念）

- [[thinking-chain-guidelines|concepts/thinking-chain-guidelines]] — 思维链准则（文档驱动 + ReAct/Plan-and-Resolve/Reflection/自主学习/升级规则）
- [[agent-resolution-order|concepts/agent-resolution-order]] — Agent 调度优先级：Command → Agent → Skill
- [[memory-systems|concepts/memory-systems]] — Claude Code 四层记忆系统
- [[wiki-management|concepts/wiki-management]] — Wiki知识库管理规范

## Decisions（架构决策）

- [[enforcement-structure|decisions/enforcement-structure]] — 规则执行保障架构：短规则 + 详细技能 + 守卫技能三层

## Related Topics（关联主题）

- [[multi-agent|topics/multi-agent]] — 多Agent协作是工作流执行的核心机制
- [[llm-coding|topics/llm-coding]] — LLM编程踩坑与工作流质量直接相关
- [[agent-flow-cli|topics/agent-flow-cli]] — AgentFlow CLI 是工作流执行的载体
