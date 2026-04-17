# preflight-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | PreToolUse |
| 匹配器 | Write\|Edit\|Bash\|NotebookEdit |
| 作用 | pre-flight 未完成时阻断代码修改和命令执行 |

## 功能

### 检查逻辑
1. 检查 `current_phase.md` 是否存在且非空 → pre-flight 已完成
2. 检查 `.complexity-level` 是否存在 → 复杂度已评估
3. Simple 任务：检查 `.simple-preflight-done` 标记

### 放行规则
- **始终放行的工具**：Read, Glob, Grep, Agent, AskUserQuestion, TodoWrite, WebSearch 等
- **Write/Edit**：只允许写入 `.agent-flow/`、`.dev-workflow/`、`.claude/` 目录
- **Bash**：只允许只读命令（ls, cat, git status 等）和 mkdir 创建 agent-flow 目录
- **NotebookEdit**：阻断

### 阻断原因分类
1. `current_phase.md` 不存在 → pre-flight 未完成
2. `.complexity-level` 不存在 → 复杂度未评估

## 阻断行为

- 阻断：`exit 2`
- 提示中明确说明阻断原因和解决步骤

## 关联

- 与 `preflight-guard.py` 配合：guard 在 prompt 时提醒，enforce 在工具调用时阻断
