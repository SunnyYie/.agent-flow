# claude-md-bootstrap.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt |
| 作用 | 确保项目 CLAUDE.md 和 MCP 配置文件存在 |

## 功能

调用 `agent_flow.core.config` 模块：
1. `ensure_project_claude_md()` — 确保项目根目录有 CLAUDE.md
2. `ensure_project_mcp_config()` — 确保项目有 .mcp.json 配置

如果文件不存在，自动生成默认内容。

## 条件

- 需要项目有 `.agent-flow/` 或 `.dev-workflow/` 目录
- 需要 `agent_flow` 包已安装

## 关联

- 在 `startup-context.py` 之前运行，确保文件结构就绪
