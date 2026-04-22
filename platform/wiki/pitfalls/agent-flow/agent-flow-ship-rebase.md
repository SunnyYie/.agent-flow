---
name: agent-flow-ship-rebase-pitfall
type: pitfall
module: agent-flow
status: verified
confidence: 0.9
created: 2026-04-13
tags: [agent-flow, rebase, force-push, ship]
---

# agent-flow ship 自动 rebase 导致历史分叉

> 已推送到远端的分支执行 agent-flow ship sync 时，自动 rebase 会造成历史分叉

## 问题描述

`agent-flow ship` 在 sync 阶段会自动 rebase 分支到 base branch。如果代码已推送到远端，rebase 会改变本地历史，导致 push 时 non-fast-forward 错误。

## 解决方案

1. 对于已推送到远端的分支，跳过 ship 的 sync 步骤
2. 或在 ship 失败后，用 `git reset --hard origin/<branch>` 恢复原始状态
3. 然后直接通过 glab API 创建 MR

## 相关条目

- [[self-hosted-gitlab-auth|自托管 GitLab 认证模式]]
