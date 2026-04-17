# agent-dispatch-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt（Medium/Complex 任务，EXECUTE 阶段时） |
| 作用 | 检查是否需要派发子Agent |

## 功能

1. 读取复杂度级别
2. 判断当前 RPI 阶段是否为 EXECUTE/Implement
3. 读取 `flow-context.yaml` 的上下文预算
4. 根据预算状态输出不同强度的提醒：
   - 预算 > 70%：强制派发（CRITICAL）
   - Medium/Complex 任务在 EXECUTE 阶段：建议派发

## 输出示例

```
[AgentFlow DISPATCH CRITICAL] Context budget > 70% during EXECUTE phase!
```

## 关联

- 依赖 `flow-context.yaml`（由 `context-budget-tracker.py` 维护）
- 参考 `~/.agent-flow/skills/agent-orchestration/main-agent-dispatch/handler.md`
