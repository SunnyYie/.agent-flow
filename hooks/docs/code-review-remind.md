# code-review-remind.py

| 属性 | 值 |
|------|-----|
| 事件 | PostToolUse |
| 匹配器 | Write\|Edit |
| 作用 | 代码修改后提醒启动 code-reviewer Agent |

## 功能

1. 记录代码修改次数（`.code-change-count`）
2. 按改动量和复杂度分级提醒：
   - 首次修改 → 轻提醒
   - 3+ 次修改（大改动）→ 标准提醒
   - Complex + 大改动 → 强烈提醒（附 code-review skill 步骤）
3. 如果 `.code-review-done` 标记已存在 → 跳过

## 输出

软提醒，不阻断（`exit 0`）。

## 标记文件

- `.agent-flow/state/.code-change-count` — 修改计数
- `.agent-flow/state/.code-review-done` — code-review 已执行

## 关联

- 与 agents.md 中的 code-reviewer agent 配合
