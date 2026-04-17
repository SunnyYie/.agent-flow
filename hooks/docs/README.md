# AgentFlow Hooks 使用文档

> 本目录包含 Claude Code hooks 的使用文档。每个 hook 对应一个 `.md` 文件。

## Hook 架构概览

```
hooks/
├── docs/                          ← 使用文档（本目录）
├── contract_utils.py              ← 共享工具函数库
│
├── ─── UserPromptSubmit ──────────── 用户提交prompt时触发
│   ├── startup-context.py         ← 注入启动上下文（技能/记忆/recall命中）
│   ├── claude-md-bootstrap.py     ← 确保项目 CLAUDE.md 和 MCP 配置存在
│   ├── preflight-guard.py         ← 检查 pre-flight 状态，注入开发铁律
│   ├── parallel-enforce.py        ← 检测可并行子任务，提醒并行执行
│   ├── session-starter.py         ← 创建会话ID，写入SQLite
│   ├── self-questioning-enforce.py← 检查自我质询是否完成
│   ├── user-acceptance-guard.py   ← 检查用户验收是否完成
│   └── agent-dispatch-enforce.py  ← 检查是否需要派发子Agent
│
├── ─── PreToolUse ──────────────── 工具执行前触发
│   ├── git-branch-guard.py        ← 阻止在保护分支上 git commit/push
│   ├── preflight-enforce.py       ← pre-flight 未完成时阻断代码修改
│   ├── dev-workflow-enforce.py    ← 强制5条开发铁律（分支/计划/搜索/守卫）
│   ├── thinking-chain-enforce.py  ← 强制思维链（搜索先行才能执行）
│   ├── promotion-guard.py         ← 拦截写入全局知识库（需验收）
│   ├── project-structure-enforce.py← 搜索源码前强制读项目结构索引
│   └── subtask-guard-enforce.py   ← 代码修改前强制搜索知识库
│
├── ─── PostToolUse ─────────────── 工具执行后触发
│   ├── context-guard.py           ← 监控上下文膨胀（大文件/日志输出）
│   ├── phase-reminder.py          ← 代码修改后提醒 pre-flight
│   ├── error-search-remind.py     ← 命令失败时提醒搜索知识库
│   ├── search-tracker.py          ← 搜索知识库时创建标记文件
│   ├── code-review-remind.py      ← 代码修改后提醒启动 code-reviewer
│   ├── context-budget-tracker.py  ← 追踪上下文 token 使用量
│   └── observation-recorder.py    ← 静默记录操作到 SQLite
│
└── ─── 已废弃 ─────────────────────
    └── tool-precheck-guard.py     ← 已合并到 thinking-chain-enforce.py
```

## 标记文件依赖关系

```
search-tracker.py ──创建──→ .search-done
                          .subtask-guard-done
                          .wiki-search-done
                          .tool-wiki-read

thinking-chain-enforce.py ──读取──→ .search-done
subtask-guard-enforce.py ──读取──→ .search-done, .subtask-guard-done
dev-workflow-enforce.py ──读取──→ .search-done, .subtask-guard-done
context-guard.py ──创建──→ .project-structure-read
project-structure-enforce.py ──读取──→ .project-structure-read

session-starter.py ──创建──→ .current-session-id
observation-recorder.py ──读取──→ .current-session-id

preflight-guard.py ──检查──→ current_phase.md, .self-questioning-done, .complexity-level
preflight-enforce.py ──检查──→ current_phase.md, .complexity-level
self-questioning-enforce.py ──检查──→ .self-questioning-done
user-acceptance-guard.py ──检查──→ .user-acceptance-done
```

## 优化历史

### v2.0 (2026-04-17)

**Bug 修复：**
- `agent-dispatch-enforce.py`: 从 PreToolUse(Write|Edit) 移到 UserPromptSubmit（它不处理 tool_input）
- `self-questioning-enforce.py`: 从 PreToolUse(Write|Edit) 移到 UserPromptSubmit（它不处理 tool_input）
- `user-acceptance-guard.py`: 从 PreToolUse(Bash) 移到 UserPromptSubmit（它不处理 tool_input）
- `tool-precheck-guard.py`: 匹配器 Bash 不匹配代码中的 Write|Edit 逻辑，该 hook 从不生效，已合并删除

**去重：**
- `startup-context.py`: 从 SessionStart 删除重复注册（UserPromptSubmit 已覆盖）
- `tool-precheck-guard.py`: 功能与 thinking-chain-enforce.py 重叠，已合并

**内联脚本提取：**
- PreToolUse 的 git 分支保护 bash → `git-branch-guard.py`
- PostToolUse 的 current_phase.md 检查 bash → `phase-reminder.py`
