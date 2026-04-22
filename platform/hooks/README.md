# Platform Hooks

Platform 团队的 hooks 负责框架运行时、会话生命周期、上下文预算与治理保护。

## 使用前提

- 在 Claude Code hooks 配置中注册对应脚本路径。
- 运行目录需要存在 `.agent-flow/` 或 `.dev-workflow/`（多数 hook 才会生效）。
- Python hook 建议使用 `python3` 执行。

## 文件说明

### `runtime/agent-dispatch-enforce.py`
- 功能：在中高复杂度任务中提醒主 Agent 做子 Agent 分发，避免主线程串行执行。
- 如何使用：注册到 `UserPromptSubmit`。
- 触发时机：读取 `current_phase.md` 后，当复杂度为 `medium/complex` 且处于执行相关阶段时输出提醒。

### `runtime/context-budget-tracker.py`
- 功能：跟踪 `Read/Grep/Glob` 导致的上下文 token 消耗，写入 `flow-context.yaml`，并在 50%/70% 阈值预警。
- 如何使用：注册到 `PostToolUse`，匹配 `Read|Grep|Glob`。
- 触发时机：每次读取或搜索后累计预算并判断是否告警。

### `runtime/context-guard.py`
- 功能：检测上下文膨胀风险（连续大文件读取、日志流输出等），给出降噪建议。
- 如何使用：注册到 `PostToolUse`。
- 触发时机：`Read` 大文件未分页、连续大文件读取、`Bash` 日志类命令输出时触发提醒。

### `runtime/contract_utils.py`
- 功能：共享工具函数库（状态路径、复杂度、计划格式、标记文件读取）。
- 如何使用：供其它 hook `import`，无需单独注册。
- 触发时机：不直接触发。

### `runtime/observation-recorder.py`
- 功能：记录工具调用观测到 SQLite（`observations.db`），用于回放、检索与分析。
- 如何使用：注册到 `PostToolUse`。
- 触发时机：每次工具调用后静默记录（含过滤噪声逻辑）。

### `runtime/pre-compress-guard.py`
- 功能：在上下文压缩前注入高置信记忆，减少压缩后关键信息丢失。
- 如何使用：注册到 `PreToolUse`。
- 触发时机：会话达到最小时长/遥测阈值后，在压缩相关场景输出 `<system-reminder>`。

### `runtime/session-end-recorder.py`
- 功能：在会话结束时写入生命周期事件，清理会话级状态。
- 如何使用：注册到 `SessionEnd`。
- 触发时机：Claude Code 会话结束。

### `runtime/session-starter.py`
- 功能：新用户消息进入时创建会话记录，写入 `.current-session-id`。
- 如何使用：注册到 `UserPromptSubmit`。
- 触发时机：每次用户提交消息时启动/切换会话。

### `runtime/startup-context.py`
- 功能：注入启动上下文（SessionStart 全量、UserPromptSubmit 增量 diff）。
- 如何使用：注册到 `SessionStart` 与 `UserPromptSubmit`。
- 触发时机：会话启动或用户新一轮输入时。

### `governance/promotion-guard.py`
- 功能：守卫知识晋升，拦截未验收的全局知识写入，并做相似内容检查。
- 如何使用：注册到 `PreToolUse`（建议匹配 `Write|Edit`）。
- 触发时机：写入 `~/.agent-flow/wiki/`、`~/.agent-flow/skills/` 或受保护项目文档时。

## 推荐注册顺序

1. `startup-context.py` / `session-starter.py`
2. `context-*` 与 `observation-recorder.py`
3. `agent-dispatch-enforce.py`
4. `promotion-guard.py`
5. `session-end-recorder.py`

