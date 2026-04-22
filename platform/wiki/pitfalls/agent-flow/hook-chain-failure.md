---
title: "Hook 脚本缺失导致 PreToolUse 全链式阻断"
category: pitfall
module: agent-flow
agents: [main, planner, coder, verifier]
scope: global
tags: [hook, PreToolUse, chain-failure, agent-flow, init]
confidence: 0.95
status: verified
created: 2026-04-18
---

# Hook 脚本缺失导致 PreToolUse 全链式阻断

## 问题描述

Claude Code 的 PreToolUse hook 是**全量执行**的：每次工具调用时，settings.json 中所有匹配 `matcher` 的 hook 都会被执行。如果某个 hook 脚本文件不存在（如被意外删除或 `agent-flow init --force` 重置后未重装），该 hook 执行失败会导致**整个 PreToolUse 链中断**，进而阻断所有匹配的工具调用。

### 具体场景

1. `agent-flow init --dev-workflow --force` 重新初始化项目后，`~/.agent-flow/hooks/` 中的部分 hook 脚本可能被清除
2. `agent-flow adapt --platform claude-code` 未重新执行，导致 hook 脚本文件不完整
3. 手动删除或移动了某个 hook 脚本

### 连锁效应

```
pre-compress-guard.py 缺失
  → 所有 PreToolUse hook 执行失败
  → Read/Write/Edit/Bash/Glob/Grep 全部被阻断
  → Agent 完全无法操作任何文件
  → 无法通过 Write 工具修复缺失的 hook（因为 Write 也被阻断）
  → 形成鸡生蛋问题：需要修复的文件就是导致阻断的文件
```

## 影响

- **严重性：Critical** — Agent 完全丧失文件操作能力，无法自我修复
- **覆盖范围**：所有 PreToolUse matcher 匹配的工具（Write|Edit|Bash|NotebookEdit 等）
- **触发频率**：每次 `agent-flow init --force` 后如果忘记重新 `adapt` 就会触发

## 解决方案

### 紧急修复

用户在终端手动执行：

```bash
cp agent_flow/templates/hooks/pre-compress-guard.py ~/.agent-flow/hooks/
cp agent_flow/templates/hooks/session-end-recorder.py ~/.agent-flow/hooks/
# 或者一次性重装所有 hooks
agent-flow adapt --platform claude-code
```

### 预防措施（代码层面）

1. **`init --force` 后自动 adapt**：在 `init_dev_workflow(force=True)` 末尾自动调用 hook 安装
2. **`doctor` 命令检测**：`agent-flow doctor` 已能检测 hook 脚本缺失，但应在 `init --force` 后主动提示

### 建议改进

在 `init_project_config()` 和 `init_dev_workflow()` 的 `force=True` 路径中，增加 hook 重装逻辑：

```python
if force:
    install_claude_md_bootstrap_hook()
    install_claude_startup_context_hook()
    install_claude_precompress_hook()
    install_claude_session_end_hook()
    install_claude_project_init_guard_hook()
    ensure_claude_settings_bootstrap_hook()
```

## 频率

踩坑 1 次（2026-04-18），导致整个会话无法执行文件操作直到用户手动修复。

## 相关条目

- [[hook-path-inconsistency|pitfalls/agent-flow/hook-path-inconsistency]] — Hook 路径不一致问题
- [[enforcement-structure|decisions/enforcement-structure]] — 规则执行保障架构
