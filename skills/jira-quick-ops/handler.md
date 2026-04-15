---
name: jira-quick-ops
version: 1.0.0
trigger: 查看, 搜索, 评论, view, search, comment, JQL, Jira详情
confidence: 0.95
abstraction: universal
created: 2026-04-15
---

# Skill: jira-quick-ops

> Jira 只读查询和轻量写入操作 — 查看详情、JQL 搜索、添加评论。

## Trigger

当用户需要以下操作时触发：

- 查看 Issue 详情（状态、子任务、评论）
- 搜索 Issue（JQL 查询）
- 添加评论
- 快速了解某个需求的当前状态
- 查看我的待办、某个项目的 Issue 列表

## Procedure

### P1: 查看 Issue 详情

```bash
jira issue view KEY
```

输出包含：基础信息（状态/优先级/类型/负责人/报告人）、Labels、Parent Issue、Subtasks 表格、Description、Comments 列表。

### P2: JQL 搜索

```bash
# 基本搜索
jira issue search "assignee = sunyi AND status = 开发中"

# 限制结果数
jira issue search "project = MPR AND sprint in openSprints()" -n 10

# 常用 JQL 模板
jira issue search "assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC"
jira issue search "project = MPR AND status in (开发中, 测试) ORDER BY updated DESC"
jira issue search "parent = MPR-30956"
```

JQL 语法要点：
- 字段名区分大小写（status 不是 Status）
- 中文状态值需要精确匹配（如 开发中 不是 In Progress）
- 用 AND / OR / NOT 组合条件
- ORDER BY 排序

### P3: 添加评论

```bash
# Agent 模式（必须用 -m）
jira issue comment KEY -m "评论内容"
```

### P4: 常用查询场景

**查看我的待办**：
```bash
jira issue search "assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC" -n 20
```

**查看某个需求的子任务状态**：
```bash
jira issue view PARENT-KEY
```

**查看最近更新的 Issue**：
```bash
jira issue search "project = MPR AND updated >= -7d ORDER BY updated DESC" -n 15
```

## Rules

1. 搜索优先：不确定 Issue Key 时，先 search 再 view
2. 评论用 -m：Agent 必须用 -m 参数，不依赖 EDITOR
3. 结果数控制：默认 -n 50，精确查询时减小到 -n 10 减少输出
