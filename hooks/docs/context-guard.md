# context-guard.py

| 属性 | 值 |
|------|-----|
| 事件 | PostToolUse |
| 匹配器 | Read\|Bash |
| 作用 | 监控上下文膨胀和污染风险 |

## 功能

### Read 工具监控
1. 当读取 `project-structure.md` 时，自动创建 `.project-structure-read` 标记（供 project-structure-enforce.py 使用）
2. 大文件（>500行）未指定行范围 → 提醒指定 offset+limit
3. 连续读取 3+ 个大文件 → 强烈建议用 Explore Agent 或 /compact

### Bash 工具监控
1. 检测日志输出命令（tail -f, kubectl logs, docker logs 等）→ 提醒用 head/grep 限制输出

## 输出

软提醒，不阻断（`exit 0`）。

## 关联

- 创建 `.project-structure-read` 标记 → `project-structure-enforce.py` 消费
- 与 `context-budget-tracker.py` 互补：guard 做即时提醒，tracker 做预算追踪
