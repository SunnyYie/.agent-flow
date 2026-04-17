# parallel-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt（有 current_phase.md 时） |
| 作用 | 检测可并行子任务，提醒并行执行 |

## 功能

1. 读取 `current_phase.md` 中的子任务列表和依赖关系
2. 解析依赖图（支持 `T1→T2→T3` 和 `T1→[T2,T3]→T4` 两种格式）
3. 找出无依赖关系的子任务组
4. 输出并行执行提醒

## 条件

- 需要 `current_phase.md` 存在
- 复杂度不为 `simple`（简单任务不需要并行）
- 至少有 2 个待执行子任务

## 输出示例

```
[AgentFlow PARALLEL] 5 pending subtasks detected with parallelizable groups: T5, T6, T7

Independent subtasks should be executed in parallel to save time.
```

## 关联

- 依赖 `current_phase.md` 的实施计划格式
