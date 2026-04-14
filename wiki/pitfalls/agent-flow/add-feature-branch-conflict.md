---
name: add-feature-branch-conflict
type: pitfall
module: agent-flow
status: verified
confidence: 0.8
created: 2026-04-13
tags: [agent-flow, branch, add-feature, conflict]
---

# agent-flow add-feature 与已有分支冲突

> add-feature 会创建新分支，但项目中可能已有同名功能分支

## 问题描述

`agent-flow add-feature` 命令会自动创建新分支。但如果项目中已存在同名功能分支（如之前手动创建或遗留的分支），add-feature 会创建新分支覆盖或产生冲突，导致重复工作。

## 解决方案

1. 在执行 add-feature 前，先检查现有分支：`git branch -a | grep <feature_name>`
2. 如果已有同名分支，直接切换到该分支：`git checkout <existing_branch>`
3. 而非让 add-feature 创建新分支
4. 如需使用已有分支但 add-feature 不支持，可跳过 add-feature 步骤，手动设置分支状态

## 相关条目

- [[agent-flow-ship-rebase-pitfall|agent-flow ship rebase 坑]]
