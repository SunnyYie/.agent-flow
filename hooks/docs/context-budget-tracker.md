# context-budget-tracker.py

| 属性 | 值 |
|------|-----|
| 事件 | PostToolUse |
| 匹配器 | Read\|Grep\|Glob |
| 作用 | 追踪上下文 token 使用量 |

## 功能

1. 每次 Read/Grep/Glob 调用后估算 token 消耗
   - Read：按文件大小估算（bytes / 3.3）
   - Grep/Glob：按输出长度估算（len × 0.25）
2. 累加到 `flow-context.yaml` 的 `context_budget.used`
3. 超过 50% → 警告提醒
4. 超过 70% → 严重警告（建议子 Agent 派发）
5. 大文件（>50KB）→ 单独警告
6. 陈旧数据检测（used > 3× max）→ 自动重置为 30%

## flow-context.yaml 格式

```yaml
context_budget:
  used: 50000
  max: 200000
  status: healthy|warning|critical
  files_read: 42
  last_updated: 2026-04-17T10:30:00
```

## 输出

- 状态变化时输出 `<system-reminder>` 块
- 大文件读取时输出警告

## 关联

- 消费者：`agent-dispatch-enforce.py` 读取 budget status
- 与 `context-guard.py` 互补：guard 做即时提醒，tracker 做预算追踪
