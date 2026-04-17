# startup-context.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt |
| 作用 | 注入紧凑的启动上下文到会话 |

## 功能

在用户提交 prompt 时，调用 `agent_flow.core.startup_context` 模块：
1. 构建当前项目的启动上下文（技能命中、记忆命中、recall 命中）
2. 渲染为 `<system-reminder>` 块注入到 Agent 上下文

## 输入

从 stdin 读取 JSON：
- `prompt`: 用户输入的 prompt 文本
- `hook_event_name`: 事件名（支持 SessionStart 兼容）

## 输出

`<system-reminder>` 块，包含当前项目相关的技能、记忆和 recall 摘要。

## 依赖

- `agent_flow.core.startup_context` 模块
- `.agent-flow/` 目录存在

## 关联

- 与 `claude-md-bootstrap.py` 配合：bootstrap 确保文件存在，startup-context 注入内容
