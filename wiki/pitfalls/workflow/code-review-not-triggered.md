---
title: "代码审查未自动触发"
category: pitfall
module: workflow
agents: [main, coder, verifier]
scope: global
tags: [code-review, quality, agent-orchestration]
confidence: 0.9
status: open
created: 2026-04-14
---

# 代码审查未自动触发

## 问题描述

agents.md 规定"代码刚写完/修改后 - 使用 code-reviewer agent"，但实际执行中代码修改后从未启动 code-reviewer Agent。

## 影响

- 代码质量无独立审查
- 可能遗漏安全问题、性能问题、风格问题
- CLAUDE.md 中 AI Governance 要求遵循 rn-ai-rules.yaml，但无自动检查

## 根因

1. 无 hook 在代码修改后强制触发 code-review
2. Agent 完成代码修改后直接进入验证，跳过审查
3. development-workflow.md 规定了 Code Review 步骤但非强制

## 解决方案

**方案A（推荐）**：创建 PostToolUse hook，在代码文件 Write/Edit 后提醒执行 code-review。

**方案B**：在 subtask-guard Step 4 中增加"代码修改后必须启动 code-reviewer"检查项。

**方案C**：在 Implement 阶段结束时，current_phase.md 检查代码修改记录，强制启动 code-review。

## 频率

每次代码修改都会遇到。
