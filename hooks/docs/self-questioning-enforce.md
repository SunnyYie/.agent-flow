# self-questioning-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt（当前阶段 ≥ REFLECT 时） |
| 作用 | 检查自我质询是否完成 |

## 功能

1. 读取 `current_phase.md` 判断当前 RPI 阶段
2. 如果已到 REFLECT 阶段但 `.self-questioning-done` 标记不存在
3. 输出警告，要求执行 self-questioning skill

## 标记文件

- `.agent-flow/state/.self-questioning-done`

## 输出示例

```
[AgentFlow WARNING] Self-questioning not completed before REFLECT phase!
```

## 关联

- 与 `preflight-guard.py` 配合：guard 提醒标记缺失，enforce 在 REFLECT 阶段强制
- 执行 self-questioning skill 后创建标记
