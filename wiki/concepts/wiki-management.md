---
name: wiki-management
type: concept
module: workflow
status: verified
confidence: 0.9
created: 2026-04-13
tags: [wiki, knowledge-base, obsidian, lifecycle, lint]
---

# Wiki 知识库管理规范

> 三层 Wiki 架构的统一规范：目录结构、页面格式、生命周期、Lint 规则

## 目录结构

```
wiki/
├── purpose.md          # 项目方向与核心问题
├── INDEX.md            # 动态导航索引（学习路径）
├── GLOSSARY.md         # 术语枢纽（交叉链接中心）
├── patterns/           # 成功模式
├── pitfalls/           # 踩坑记录
├── concepts/           # 核心概念
├── decisions/          # 架构决策记录（ADR）
└── queries/            # 高价值Q&A存档
```

## 页面创建规范

每个 Wiki 页面必须遵循以下格式（兼容 Obsidian）：

```markdown
---
title: "页面标题"
category: pattern | pitfall | concept | decision | query
module: workflow | security | environment | implementation | testing | architecture | gitlab | react-native | feishu
agents: [main, executor, verifier]
scope: global | project
confidence: 0.0-1.0
sources: [S6.1, S14.2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | verified | deprecated
---

# 页面标题

> 一句话摘要

## 问题描述 / 模式描述

{详细内容}

## 解决方案 / 应用方式

{具体做法}

## 相关页面

- [[another-page|显示文本]]
```

## 知识生命周期

| 状态 | 含义 | 转换条件 |
|------|------|----------|
| draft | 新创建，未经多阶段验证 | 默认初始状态 |
| verified | 经多个阶段验证有效 | confidence >= 0.9 且被 >= 2 个阶段引用 |
| deprecated | 已过时，被新模式替代 | 有更新的 wiki 页面替代，添加 `superseded_by` 字段 |

## 三层知识流动管道

```
.dev-workflow/wiki/ (项目Wiki，最详细)
    ↓ agent-flow reflect（手动触发，confidence >= 0.7, sources >= 2）
.agent-flow/wiki/ (项目级共享Wiki)
    ↓ agent-flow wiki sync（手动触发，abstraction: universal/framework）
~/.agent-flow/wiki/ (全局Wiki，跨项目通用)
```

**规则**：
- 晋升时只提取通用部分，不搬移项目特有内容
- 必须手动触发，避免项目特有知识污染全局

## Wiki Lint 规则

每 2-3 个阶段执行一次健康检查：

1. **断链检测**: wikilinks 指向的页面必须存在
2. **孤立检测**: 每个页面至少有一个入链或出链
3. **矛盾检测**: 同一主题不应有两个 status=verified 且结论冲突的页面
4. **过期检测**: status=deprecated 的页面仍被引用时发出警告

## 相关条目

- [[agent-roles|多角色协作体系]]
- [[dual-acceptance|双验收机制]]
