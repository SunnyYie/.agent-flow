---
title: "git stash 与 agent-flow 状态文件冲突"
category: pitfall
module: agent-flow
agents: [main]
scope: global
tags: [git, stash, conflict, agent-flow]
confidence: 0.85
status: open
created: 2026-04-14
---

# git stash 与 agent-flow 状态文件冲突

## 问题描述

创建 feature 分支时需要 `git stash` 保存当前修改，但 `.agent-flow/` 下的状态文件（Memory.md、Soul.md 等）也会被 stash，导致切换分支后冲突。

**典型错误**：
```
CONFLICT (modify/delete): .agent-flow/memory/main/Memory.md deleted in Updated upstream
and modified in Stashed changes.
```

## 影响

- 需要手动解决冲突
- 创建分支流程变慢
- 可能丢失 agent-flow 状态

## 根因

`.agent-flow/` 目录在 git 仓库内但不应被版本控制，stash 时仍会处理这些文件。

## 解决方案

**方案A（推荐）**：确保 `.agent-flow/` 和 `.dev-workflow/` 在 `.gitignore` 中，使用 `git stash -- . ':!.agent-flow' ':!.dev-workflow'` 排除。

**方案B**：创建分支前先 stash，但排除 agent-flow 文件。

**方案C**：将 agent-flow 状态文件移到仓库外（如 `/tmp/` 或 `~/.agent-flow/state/{project}/`）。

## 频率

每次在已有 agent-flow 修改的分支上创建新分支时遇到。
