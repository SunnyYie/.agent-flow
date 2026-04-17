# phase-reminder.py

| 属性 | 值 |
|------|-----|
| 事件 | PostToolUse |
| 匹配器 | Write\|Edit |
| 作用 | 代码修改后提醒执行 pre-flight-check |

## 功能

1. 检查 `.agent-flow/state/current_phase.md` 是否存在
2. 不存在 → 提醒"Did you run pre-flight-check?"

## 输出

软提醒，不阻断（`exit 0`）。

## 历史

v2.0 从 settings.json 中的内联 bash 脚本提取为独立 Python 文件。

## 关联

- 与 `preflight-guard.py` / `preflight-enforce.py` 配合：reminder 是轻量级提示
