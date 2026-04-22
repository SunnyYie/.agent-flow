---
title: "Hook 路径不一致：current_phase.md 双路径问题"
category: pitfall
module: agent-flow
agents: [main, planner, coder, verifier]
scope: global
tags: [hook, path, preflight, thinking-chain, current_phase]
confidence: 0.95
status: verified
created: 2026-04-14
---

# Hook 路径不一致：current_phase.md 双路径问题

## 问题描述

三层架构中 `current_phase.md` 的读写路径不一致：

| 消费方 | 检查/读取路径 |
|--------|-------------|
| `preflight-enforce.py` | `.agent-flow/state/current_phase.md` |
| `thinking-chain-enforce.py` | `.agent-flow/state/current_phase.md` |
| `dev-workflow-enforce.py` | `.agent-flow/state/current_phase.md` |
| `subtask-guard-enforce.py` | `.agent-flow/state/current_phase.md` |
| Boot Protocol (Agent.md) | `.dev-workflow/state/current_phase.md` |
| pre-flight-check skill | `.agent-flow/state/current_phase.md` |

Hook 脚本和 Skill 指向 `.agent-flow/state/`，但 Boot Protocol 指向 `.dev-workflow/state/`。

## 影响

- 写入 `.dev-workflow/state/current_phase.md` → Hook 检查不到 → 阻断所有执行命令（git checkout、代码编辑等）
- 需要手动复制文件到 `.agent-flow/state/`，浪费时间
- 混淆开发者应该写入哪个位置
- 踩坑频率高：每个新任务首次启动时都可能遇到

## 解决方案

**已实施**：修改所有 Hook 脚本同时检查两个路径：

```python
phase_files = [
    ".agent-flow/state/current_phase.md",
    ".dev-workflow/state/current_phase.md",
]
phase_found = any(
    os.path.isfile(pf) and os.path.getsize(pf) > 10
    for pf in phase_files
)
```

**长期方案**：统一为 `.agent-flow/state/current_phase.md`，修改 Agent.md Boot Protocol。

## 频率

踩坑 2 次（2026-04-14），已通过 Hook 双路径检查修复。
