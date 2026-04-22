---
title: "Claude Code 关键设置与环境变量"
category: concept
module: workflow
agents: [main, architect, researcher]
scope: global
tags: [claude-code, settings, environment-variables, configuration]
confidence: 0.85
sources: [shanraisshan/claude-code-best-practice]
status: verified
created: 2026-04-14
updated: 2026-04-14
---

# Claude Code 关键设置与环境变量

> 60+ 设置项和 170+ 环境变量的精选参考，只收录最实用的高频配置。

## 高频设置（settings.json）

### 性能与上下文

| 设置 | 默认值 | 说明 |
|------|--------|------|
| `effortLevel` | - | 持久化努力等级，跨会话保持 |
| `plansDirectory` | `.claude/plans/` | 计划输出目录，可自定义 |
| `autoMemoryDirectory` | - | 自动记忆存储目录（仅用户级设置） |
| `statusLine` + `refreshInterval` | - | 状态栏配置，支持 JSON 输入（model/cost/context/rate limits） |

### 沙箱与安全

| 设置 | 说明 |
|------|------|
| `sandbox.network.allowMachLookup` | macOS XPC 服务名（iOS Simulator/Playwright） |
| `sandbox.filesystem.allowWrite` | 允许写入的路径模式 |
| `sandbox.filesystem.denyWrite` | 禁止写入的路径模式 |
| `sandbox.filesystem.allowRead` | 允许读取的路径模式 |
| `sandbox.filesystem.denyRead` | 禁止读取的路径模式 |

### MCP 服务器

| 设置 | 说明 |
|------|------|
| `enableAllProjectMcpServers` | 自动批准所有 .mcp.json 服务器 |
| `allowedMcpServers` | 托管 MCP 服务器白名单 |
| `deniedMcpServers` | 托管 MCP 服务器黑名单 |

### 权限语法

```
路径模式:
  //  → 绝对路径 (//etc/hosts)
  ~/ → 用户主目录 (~/.*\.env)
  /  → 项目相对路径 (/src/**)
  ./ → 当前目录 (./test/**)

工具模式:
  Bash(ls *)       # Word boundary: matches "ls foo" not "lsabc"
  Bash(ls*)        # No boundary: matches "lsabc" too
  Agent(name)      # 子Agent生成权限
  Skill(skill-name) # Skill调用权限
  MCP(server:tool) # MCP工具权限，等同 mcp__server__tool
```

## 高频环境变量

### 上下文与压缩

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | ~95% | 自动压缩阈值（建议设为 50-70%） |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | - | 解耦压缩阈值与显示的上下文百分比 |

### 模型与子进程

| 变量 | 说明 |
|------|------|
| `CLAUDE_CODE_SUBAGENT_MODEL` | 覆盖所有子Agent的模型 |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | 从子进程环境中剥离凭证（防御纵深） |
| `ENABLE_TOOL_SEARCH` | MCP工具搜索阈值，如 `auto:30`（上下文30%时启用） |

### 会话控制

| 变量 | 说明 |
|------|------|
| `CLAUDE_CODE_PERFORCE_MODE` | Perforce VCS 写保护支持 |
| `CLAUDE_CODE_NO_FLICKER` | 无闪烁的 alt-screen 渲染 |
| `CLAUDE_CODE_SCRIPT_CAPS` | 限制每会话脚本调用次数 |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 启用多会话协作（需设为 1） |

### 企业级

| 变量 | 说明 |
|------|------|
| `forceLoginOrgUUID` | 限制登录到特定组织（接受 UUID 数组） |
| `apiKeyHelper` | 动态 auth token 生成脚本 |
| `companyAnnouncements` | 自定义启动公告（企业） |
| `autoMode` | 自定义 auto mode 分类器（environment/allow/soft_deny 文本） |

## Worktree 配置

| 设置 | 说明 |
|------|------|
| `worktree.symlinkDirectories` | symlink 到 worktree 的目录（如 node_modules），节省磁盘 |
| `worktree.sparsePaths` | git sparse-checkout 路径，用于大型 monorepo |

## 相关页面

- [[advanced-tool-use|高级工具用法（PTC/Dynamic Filtering）]]
- [[memory-systems|四层记忆系统]]
- [[monorepo-claudemd|Monorepo CLAUDE.md 加载]]
