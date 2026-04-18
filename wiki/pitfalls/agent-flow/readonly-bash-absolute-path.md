---
title: "thinking-chain-enforce 绝对路径不匹配 READONLY_BASH_PREFIXES"
category: pitfall
module: agent-flow
agents: [main, planner, coder, verifier]
scope: global
tags: [hook, thinking-chain, bash, readonly, absolute-path]
confidence: 0.9
status: verified
created: 2026-04-18
---

# thinking-chain-enforce 绝对路径不匹配 READONLY_BASH_PREFIXES

## 问题描述

`thinking-chain-enforce.py` 用 `cmd.startswith(prefix)` 判断 Bash 命令是否为只读。`READONLY_BASH_PREFIXES` 列表包含 `.venv/bin/pytest`、`pytest` 等前缀，但当 Claude Code 使用**绝对路径**执行命令时（如 `/Users/sunyi/ai/agent-flow/.venv/bin/pytest`），`startswith` 匹配失败，导致测试运行等只读命令被误判为"需要搜索标记的执行命令"。

### 匹配失败示例

```python
cmd = "/Users/sunyi/ai/agent-flow/.venv/bin/pytest tests/ -q"

# 期望匹配的前缀
".venv/bin/pytest"  → startswith → False  # 绝对路径不以相对路径开头
"pytest"            → startswith → False  # 绝对路径不以 pytest 开头
```

## 影响

- 所有通过绝对路径调用的只读命令（pytest、python -m 等）被误阻断
- Agent 被迫搜索 Skills/Wiki 后才能运行测试，即使搜索标记仍有效
- 特别影响 `pytest` 命令：Claude Code 经常使用 venv 的绝对路径

## 解决方案

### 修复方案：改用 `in` 或 basename 匹配

```python
def is_readonly_bash(command: str) -> bool:
    cmd = command.strip()
    # 方案1: 检查命令的 basename 部分
    import shlex
    try:
        parts = shlex.split(cmd)
        if parts:
            basename = os.path.basename(parts[0])
            for prefix in READONLY_BASH_PREFIXES:
                if basename == prefix or parts[0].endswith('/' + prefix):
                    return True
    except ValueError:
        pass
    # 方案2: 保留原有的 startswith 作为 fallback
    for prefix in READONLY_BASH_PREFIXES:
        if cmd.startswith(prefix):
            return True
    return False
```

### 临时绕过

Agent 可以使用短命令名代替绝对路径：

```bash
# 会被误阻断
/Users/sunyi/ai/agent-flow/.venv/bin/pytest tests/ -q

# 可以通过（匹配 "pytest" 前缀）
pytest tests/ -q
```

但 Claude Code 有时会自动使用绝对路径，Agent 无法完全控制。

## 频率

每次在 agent-flow 项目中运行 pytest 时都可能触发（2026-04-18 遇到）。

## 相关条目

- [[hook-chain-failure|pitfalls/agent-flow/hook-chain-failure]] — Hook 脚本缺失导致全链式阻断
- [[hook-path-inconsistency|pitfalls/agent-flow/hook-path-inconsistency]] — Hook 路径不一致问题
