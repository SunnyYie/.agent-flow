# thinking-chain-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | PreToolUse |
| 匹配器 | Write\|Edit\|Bash |
| 作用 | 强制思维链执行模式（搜索先行才能执行） |

## 功能

核心机制：Agent 搜索了 Skills/Wiki → search-tracker.py 创建 `.search-done` 标记 → 本 hook 检查标记 → 无标记 = 没搜索 = 阻断

### 按复杂度分级
| 复杂度 | 搜索标记有效期 | 首次违规行为 |
|--------|---------------|-------------|
| Simple | 30 分钟 | 软提醒（不阻断） |
| Medium | 15 分钟 | 硬阻断 |
| Complex | 10 分钟 | 硬阻断 |

### 代码文件判断
- 只拦截代码文件修改（.ts, .py, .go 等）
- `.agent-flow/`、`.dev-workflow/`、`.claude/` 路径不受限
- `.md`、`.txt` 等文档不受限

### Bash 只读命令豁免
只读命令（ls, cat, git status, pytest, mkdir 等）不需要搜索标记。

## 阻断行为

- Simple 首次违规：`exit 0`（软提醒），记录违规次数
- Medium/Complex 或 Simple 再次违规：`exit 2`（硬阻断）

## 标记文件

- `.agent-flow/state/.search-done`（由 search-tracker.py 创建）
- `.agent-flow/state/.chain-violation-count`（违规计数）

## 关联

- 与 `search-tracker.py` 配合：tracker 创建标记，enforce 检查标记
- 已合并 `tool-precheck-guard.py` 的功能（v2.0）
