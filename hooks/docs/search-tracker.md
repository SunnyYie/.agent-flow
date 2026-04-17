# search-tracker.py

| 属性 | 值 |
|------|-----|
| 事件 | PostToolUse |
| 匹配器 | Grep\|Read\|Glob\|WebSearch\|Agent\|Skill |
| 作用 | 搜索知识库时创建标记文件，供其他 hook 消费 |

## 功能

### 主标记：`.search-done`
当 Agent 搜索了 Skills/Wiki/Soul 等知识库路径时创建，供 thinking-chain-enforce.py 和 subtask-guard-enforce.py 检查。

格式：
```
tool=Grep
time=1713345600.123
```

### Skills 搜索标记：`.subtask-guard-done`
搜索 `agent-flow/skills/` 或 `dev-workflow/skills/` 时自动创建，供 subtask-guard-enforce.py 检查。

### Wiki 搜索标记：`.wiki-search-done`
搜索 `agent-flow/wiki/` 或 `dev-workflow/wiki/` 时创建。

### 工具 Wiki 标记：`.tool-wiki-read`
当搜索命中 `pitfalls/` 目录中涉及 critical tools（lark-cli, glab, gh, docker）的条目时创建，供 tool-precheck-guard.py 检查。

### 有效搜索判定
- WebSearch/Agent/Skill → 始终视为有效搜索
- Grep/Read/Glob → 搜索路径需包含知识库关键词（agent-flow/skills, agent-flow/wiki, Soul 等）

## 输出

静默创建标记文件（`exit 0`）。

## 关联

- 消费者：`thinking-chain-enforce.py`, `subtask-guard-enforce.py`, `dev-workflow-enforce.py`
- 读取 `~/.agent-flow/config.yaml` 的 `critical_tools` 列表
