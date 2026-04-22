# Community Hooks

Community 团队 hooks 负责业务工作流约束、开发行为守卫、流程提醒与质量门控。

## 使用前提

- 在 Claude Code hooks 配置中注册脚本（`UserPromptSubmit` / `PreToolUse` / `PostToolUse`）。
- 项目目录应已初始化 `.agent-flow/` 或 `.dev-workflow/`。
- 多数守卫依赖 `.agent-flow/state/` 下的标记文件。

## 文件说明

### `runtime/project-init-guard.py`
- 功能：检测项目是否初始化，必要时自动执行 `agent-flow init --dev-workflow`。
- 如何使用：注册到 `UserPromptSubmit`。
- 触发时机：新会话/新任务开始，且未发现 `.agent-flow/` 与 `.dev-workflow/`。

### `runtime/claude-md-bootstrap.py`
- 功能：确保项目级 `CLAUDE.md` 与 MCP 基础配置存在。
- 如何使用：注册到 `UserPromptSubmit`（建议前置执行）。
- 触发时机：检测到 workflow 目录后自动补齐基础文件。

### `runtime/preflight-guard.py`
- 功能：任务开始时注入 pre-flight 与开发铁律提醒。
- 如何使用：注册到 `UserPromptSubmit`。
- 触发时机：每次用户提交 prompt 时检查 pre-flight 状态并提醒。

### `runtime/preflight-enforce.py`
- 功能：pre-flight 未完成时阻断执行型操作，仅放行读/搜类工具。
- 如何使用：注册到 `PreToolUse`（匹配 `Write|Edit|Bash`）。
- 触发时机：进入执行操作前，且缺失 pre-flight 必要标记。

### `runtime/thinking-chain-enforce.py`
- 功能：强制“先搜索再执行”思维链，缺失搜索标记则阻断代码修改/执行。
- 如何使用：注册到 `PreToolUse`（匹配 `Write|Edit|Bash`）。
- 触发时机：代码改动或执行命令前检查 `.search-done` 标记有效期。

### `runtime/subtask-guard-enforce.py`
- 功能：强制子任务搜索守卫，防止直接改代码。
- 如何使用：注册到 `PreToolUse`（匹配 `Write|Edit`）。
- 触发时机：代码文件写入前检查 `.subtask-guard-done/.search-done`。

### `runtime/dev-workflow-enforce.py`
- 功能：执行开发铁律（受保护分支、计划文档、连续编辑无搜索等）。
- 如何使用：注册到 `PreToolUse`。
- 触发时机：pre-flight 完成后，对代码修改和关键 Bash 操作进行强校验。

### `runtime/project-structure-enforce.py`
- 功能：要求先读项目结构索引再搜源码，减少盲目检索。
- 如何使用：注册到 `PreToolUse`（重点匹配 `Grep`）。
- 触发时机：搜索源码目录前若无 `.project-structure-read` 标记则阻断。

### `runtime/implementation-clarification-guard.py`
- 功能：存在实现澄清未决项时，阻断代码变更操作。
- 如何使用：注册到 `PreToolUse`。
- 触发时机：检测 `.implementation-question-raised` 未清理时。

### `runtime/mcp-tool-factory-guard.py`
- 功能：MCP 工具/服务扩展请求未审批前，阻断相关配置变更。
- 如何使用：注册到 `PreToolUse`。
- 触发时机：检测 `.mcp-tool-factory-requested` 未处理，且动作命中 MCP 变更信号时。

### `runtime/git-branch-guard.py`
- 功能：阻止在 `main/master/develop` 直接 `git commit/push`。
- 如何使用：注册到 `PreToolUse`（匹配 `Bash`）。
- 触发时机：执行 `git commit` 或 `git push` 时检查当前分支。

### `runtime/search-tracker.py`
- 功能：记录有效知识搜索，写入 `.search-done/.subtask-guard-done` 等标记。
- 如何使用：注册到 `PostToolUse`。
- 触发时机：`Read/Grep/Glob/WebSearch/Agent/Skill` 命中知识路径时。

### `runtime/error-search-remind.py`
- 功能：命令失败后提醒先搜索，不允许盲目重试；连续失败触发升级暂停。
- 如何使用：注册到 `PostToolUse`（匹配 `Bash`）。
- 触发时机：Bash 输出命中错误特征词。

### `runtime/code-review-remind.py`
- 功能：代码修改后按改动规模提醒执行 code review。
- 如何使用：注册到 `PostToolUse`（匹配 `Write|Edit`）。
- 触发时机：代码文件被修改且未发现 `.code-review-done`。

### `runtime/phase-reminder.py`
- 功能：缺失 `current_phase.md` 时提醒先做 pre-flight。
- 如何使用：注册到 `PostToolUse`（匹配 `Write|Edit`）。
- 触发时机：发生代码修改后检查阶段文件。

### `runtime/parallel-enforce.py`
- 功能：发现可并行子任务时提醒并行执行。
- 如何使用：注册到 `UserPromptSubmit`。
- 触发时机：读取 `current_phase.md` 判断存在多个独立待办项。

### `runtime/agent-team-init.py`
- 功能：按复杂度自动初始化 Agent Team 配置并注入协作协议提醒。
- 如何使用：注册到 `UserPromptSubmit`。
- 触发时机：读取 `.complexity-level` 后为 `medium/complex` 时生成 team 配置。

### `runtime/user-acceptance-guard.py`
- 功能：中高复杂度任务在推送前提醒必须用户验收。
- 如何使用：注册到 `UserPromptSubmit`。
- 触发时机：复杂度 `medium/complex` 且无 `.user-acceptance-done` 标记。

## 推荐执行链路

1. `project-init-guard.py` -> `claude-md-bootstrap.py` -> `preflight-guard.py`
2. `preflight-enforce.py` -> `thinking-chain-enforce.py` -> `subtask-guard-enforce.py` -> `dev-workflow-enforce.py`
3. `search-tracker.py` + `error-search-remind.py` + `code-review-remind.py`
4. `parallel-enforce.py` + `agent-team-init.py` + `user-acceptance-guard.py`

