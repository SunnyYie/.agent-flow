# subtask-guard-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | PreToolUse |
| 匹配器 | Write\|Edit |
| 作用 | 代码修改前强制搜索知识库 |

## 功能

1. 检查 `.subtask-guard-done` 或 `.search-done` 标记是否有效
2. 标记有效（未过期）→ 放行
3. 标记无效或不存在 → 阻断

### 按复杂度分级
| 复杂度 | 标记有效期 |
|--------|-----------|
| Simple | 60 分钟 |
| Medium | 30 分钟 |
| Complex | 20 分钟 |

### 代码文件判断
同 thinking-chain-enforce.py：只拦截代码文件，`.agent-flow/` 等路径不受限。

## 阻断行为

- 阻断：`exit 2`，提示执行 Grep 搜索知识库

## 标记文件

- `.agent-flow/state/.subtask-guard-done`（由 search-tracker.py 创建）
- `.agent-flow/state/.search-done`（由 search-tracker.py 创建）

## 关联

- 与 `search-tracker.py` 配合：tracker 创建标记，enforce 检查标记
- 与 `thinking-chain-enforce.py` 类似但更严格：chain 对 Simple 任务软提醒，guard 硬阻断
