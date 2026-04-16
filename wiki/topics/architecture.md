---
title: "主题：Architecture 架构"
category: topic-hub
module: architecture
agents: [main, architect, planner]
scope: global
tags: [architecture, topic-hub]
confidence: 1.0
status: verified
created: 2026-04-15
updated: 2026-04-15
---

# 主题：Architecture 架构

> 系统架构模式、决策记录和设计原则。覆盖ADR、容错、缓存等关键架构知识。

## Patterns（成功模式）

- [[adr-decision-record|patterns/architecture/adr-decision-record]] — 架构决策记录(ADR)格式与使用
- [[fatal-transient-errors|patterns/architecture/fatal-transient-errors]] — FATAL/TRANSIENT错误分类与容错模式
- [[prompt-caching|patterns/architecture/prompt-caching]] — 提示缓存模式（性能优化+成本控制）
- [[speculative-caching|patterns/architecture/speculative-caching]] — 投机性缓存（延迟优化）

## Pitfalls（踩坑记录）

_(暂无架构专属踩坑记录)_

## Concepts（相关概念）

- [[memory-systems|concepts/memory-systems]] — Claude Code 四层记忆系统（架构层面的存储设计）
- [[permission-gradation|concepts/permission-gradation]] — 权限梯度管理（架构层面的访问控制）

## Decisions（架构决策）

- [[enforcement-structure|decisions/enforcement-structure]] — 规则执行保障架构：短规则 + 详细技能 + 守卫技能三层

## Related Topics（关联主题）

- [[multi-agent|topics/multi-agent]] — 多Agent架构是架构设计的核心模式
- [[workflow|topics/workflow]] — 工作流架构与系统架构紧密关联
