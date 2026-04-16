---
title: "主题：AgentFlow CLI"
category: topic-hub
module: agent-flow
agents: [main, planner, coder, verifier]
scope: global
tags: [agent-flow, cli, topic-hub]
confidence: 1.0
status: verified
created: 2026-04-15
updated: 2026-04-15
---

# 主题：AgentFlow CLI

> AgentFlow CLI 工具的踩坑记录、配置规范和架构决策。覆盖分支管理、Hook 路径、状态文件等常见问题。

## Patterns（成功模式）

_(暂无 AgentFlow CLI 专属模式)_

## Pitfalls（踩坑记录）

- [[agent-flow-ship-rebase|pitfalls/agent-flow/agent-flow-ship-rebase]] — ship自动rebase导致历史分叉
- [[add-feature-branch-conflict|pitfalls/agent-flow/add-feature-branch-conflict]] — add-feature与已有分支冲突
- [[hook-path-inconsistency|pitfalls/agent-flow/hook-path-inconsistency]] — Hook路径不一致：current_phase.md双路径问题
- [[git-stash-agent-flow-conflict|pitfalls/agent-flow/git-stash-agent-flow-conflict]] — git stash与agent-flow状态文件冲突

## Concepts（相关概念）

- [[wiki-management|concepts/wiki-management]] — Wiki知识库管理规范（目录结构/页面格式/生命周期/Lint规则）
- [[permission-gradation|concepts/permission-gradation]] — 权限梯度管理

## Decisions（架构决策）

- [[enforcement-structure|decisions/enforcement-structure]] — 规则执行保障架构：短规则 + 详细技能 + 守卫技能三层

## Related Topics（关联主题）

- [[workflow|topics/workflow]] — AgentFlow CLI 是工作流执行的载体
- [[security|topics/security]] — AgentFlow 权限管理与安全相关
