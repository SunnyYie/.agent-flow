# user-acceptance-guard.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt（Medium/Complex 任务，IMPLEMENT 之后） |
| 作用 | 检查用户验收是否完成 |

## 功能

1. 读取复杂度级别（`.complexity-level`）
2. Simple 任务跳过
3. 判断是否已过 IMPLEMENT 阶段
4. 检查 `.user-acceptance-done` 标记
5. Complex 任务：输出强制验收提醒（含完整格式说明）
6. Medium 任务：输出建议验收提醒

## 标记文件

- `.agent-flow/state/.user-acceptance-done`
- 格式：`phase=research|plan|implement` + `status=accepted` + `timestamp=` + `task=` + `confirmed_by=` + `summary=`

## 关联

- 与 `preflight-guard.py` 配合：guard 也检查验收标记
