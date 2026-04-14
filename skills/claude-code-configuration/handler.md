# Claude Code 配置体系技能

> 来源：shanraisshan/claude-code-best-practice 项目研究

## 概述

Claude Code 提供了一套完整的配置体系，包括 CLAUDE.md、settings.json、commands、agents、skills、hooks、rules 七大配置面。掌握这些配置面是高效使用 Claude Code 的基础。

## 七大配置面

### 1. CLAUDE.md — 项目指令文件

CLAUDE.md 是项目级别的指令文件，Claude Code 在每次对话开始时自动加载。

**加载优先级**（从高到低）：
- `~/.claude/CLAUDE.md` — 全局用户指令
- `项目根目录/CLAUDE.md` — 项目级指令
- `项目根目录/.claude/CLAUDE.md` — 项目 Claude 配置指令
- 子目录中的 `CLAUDE.md` — 上下文相关指令（进入该目录时加载）

**最佳实践**：
- 项目级 CLAUDE.md 定义触发规则、铁律、开发流程
- 全局 CLAUDE.md 定义跨项目通用偏好（如 commit message 格式）
- 子目录 CLAUDE.md 用于领域特定规则（如 `frontend/CLAUDE.md` 定义前端规范）
- 保持简洁，避免冗长描述，用结构化格式

### 2. settings.json — 权限与行为配置

**三层配置合并**（优先级从高到低）：
- `~/.claude/settings.local.json` — 个人本地配置（不入 Git）
- `项目/.claude/settings.json` — 团队共享配置（入 Git）
- `项目/.claude/settings.local.json` — 项目本地配置（不入 Git）

**核心配置项**：
```json
{
  "permissions": {
    "allow": ["Bash(git:*)", "Bash(pytest:*)", "Read", "Glob", "Grep"],
    "deny": ["Bash(rm -rf:*)"],
    "ask": ["Bash(python:*)"]
  },
  "env": {
    "PYTHONPATH": "./agent-workflow"
  },
  "mcpServers": {
    "autoApprove": ["pencil", "supabase"]
  }
}
```

### 3. Commands — 用户自定义斜杠命令

存放路径：`.claude/commands/`

**核心用法**：
- 用户通过 `/command-name` 触发
- 支持 `.md` 格式，frontmatter 定义元数据
- 可嵌套目录组织复杂工作流
- 命令是最外层的编排入口

### 4. Agents — 自定义智能体

存放路径：`.claude/agents/`

**核心用法**：
- 定义专用角色的 Agent，自动或手动触发
- 通过 `description` 中的 "PROACTIVELY" 关键词实现主动触发
- 支持 model/permissionMode/maxTurns/skills/hooks 等精细控制
- Agent 是中间层的自主执行单元

### 5. Skills — 可复用技能包

存放路径：`.claude/skills/`

**两种使用模式**：
- **预加载模式**：Agent 的 `skills` 字段指定，启动时注入完整内容
- **调用模式**：用户通过 `/skill-name` 触发，独立执行

### 6. Hooks — 事件钩子

存放路径：在 `settings.json` 中配置

**4 种钩子类型**：
- `command`：执行 shell 命令
- `prompt`：注入提示文本
- `agent`：启动子 Agent
- `http`：发送 HTTP 请求

**27 个事件**：
- PreToolUse / PostToolUse / PostToolUseFailure
- Notification / Stop / SubagentStop
- PermissionRequest / PermissionResponse
- 等

### 7. Rules — 上下文规则

存放路径：`.claude/rules/`

**核心用法**：
- 通过 `glob` 模式匹配文件，自动激活规则
- 支持全局规则和项目规则
- 适合定义编码标准、文档规范等

## 架构模式：Command → Agent → Skill

这是 Claude Code 最核心的架构模式：

```
用户输入 /command
    ↓
Command 编排入口
    ├── 解析用户意图
    ├── 协调多步流程
    ├── 管理用户交互
    └── 启动 Agent 执行
            ↓
        Agent 自主执行
            ├── 预加载 Skills（知识注入）
            ├── 受限工具集（安全边界）
            ├── 独立上下文（context: fork）
            └── 完成后返回结果
```

**设计原则**：
1. **Command 是编排者**：不直接执行，而是调度 Agent
2. **Agent 是执行者**：在受限环境中自主工作
3. **Skill 是知识**：注入 Agent 上下文，而非独立执行

## 与本项目三Agent模型的映射

| claude-code-best-practice | 本项目 .dev-workflow |
|---------------------------|---------------------|
| Command | Main Agent（编排入口） |
| Agent | Executor Agent（执行者） |
| Skill (preloaded) | executor/skills/（执行技能） |
| Skill (invoked) | main/skills/（管理技能） |
| Hooks | 阶段门控 + 双验收机制 |
| Rules | code_standards.md + 铁律 |

## 应用指南

- **新建项目时**：先规划 Command → Agent → Skill 三层架构
- **复杂工作流**：用 Command 编排多 Agent 协作
- **安全敏感操作**：用 Agent 的 `disallowedTools` + `permissionMode` 限制
- **团队共享**：settings.json 入 Git，settings.local.json 不入
- **持续改进**：Agent 完成后更新自身 Skills（自进化模式）
