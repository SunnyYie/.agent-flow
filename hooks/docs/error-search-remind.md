# error-search-remind.py

| 属性 | 值 |
|------|-----|
| 事件 | PostToolUse |
| 匹配器 | Bash |
| 作用 | 命令失败时提醒搜索知识库 |

## 功能

1. 检测 Bash 命令输出中的错误指示词（Error:, Failed, exit code: 1 等）
2. 有错误 → 增加错误计数（`.error-count`）
3. 第1次失败 → 搜索提醒（要求 Grep Skills/Wiki/Pitfalls）
4. 第2次失败 → 强制暂停，请求人工决策
5. 成功执行 → 重置错误计数

### 错误指示词
`Error:`, `Failed`, `exit code: 1`, `404`, `500`, `Permission denied`, `fatal:`, `Exception`, `Traceback` 等。

## 两轮循环上限

连续失败 2 次后，**必须暂停**并请求人工决策。禁止自行推测、盲目重试、忽略错误。

## 输出

- 第1次：搜索提醒（`exit 0`）
- 第2次：强制升级（`exit 0`），但消息强烈要求暂停

## 关联

- 对应 Pitfall: `skip-search-before-execute.md`, `skill-first-before-action.md`
- 错误计数器：`.agent-flow/state/.error-count`
