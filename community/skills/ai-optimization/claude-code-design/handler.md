---
name: claude-code-design
version: 1.0.0
trigger: Agent设计, Skill设计, 自进化, 漂移检测, Agent frontmatter, SKILL.md, agent design, skill design
confidence: 0.9
abstraction: universal
created: 2026-04-14
---

# Skill: Claude Code Design Patterns (Agent + Skill + Self-Evolution)

> 来源：shanraisshan/claude-code-best-practice 项目研究。Agent/Skill 设计模式 + 自进化 + 漂移检测。

## Trigger

- 设计或优化 Agent、Skill 时
- 实现 Agent 自进化机制时
- 需要监控知识漂移时

## Agent Frontmatter Schema（16 字段）

```yaml
---
name: string                    # 小写 + 连字符
description: string             # 用 "PROACTIVELY" 实现主动触发
tools: string/list              # 允许的工具白名单
disallowedTools: string/list    # 禁止的工具黑名单
model: string                   # haiku/sonnet/opus/inherit
permissionMode: string          # default/acceptEdits/auto/dontAsk/bypassPermissions/plan
maxTurns: integer               # 最大 Agent 轮次
skills: list                    # 预加载的 Skill 名称
hooks: object                   # 生命周期钩子
memory: string                  # user/project/local
background: bool                # 后台运行
effort: string                  # low/medium/high/max
isolation: string               # "worktree" = 临时 git worktree
---
```

## 五种 Agent 设计模式

| 模式 | 适用场景 | 关键配置 |
|------|---------|---------|
| 角色专用 | 需要领域知识的专门任务 | 预加载 skills，受限 tools |
| 自进化 | 需要持续学习的复杂任务 | prompt 内嵌自进化指令 + Stop Hook |
| 研究代理 | 信息收集和外部资源研究 | bypassPermissions，结构化报告 |
| 轻量代理 | 简单任务 | model: haiku, maxTurns: 3 |
| 漂移检测 | 监控外部文档变化 | 定时获取外部文档，与本地比较 |

## Skill Frontmatter Schema（13 字段）

```yaml
---
name: string                    # 显示名称 + /slash-command
description: string             # 何时调用
argument-hint: string           # 自动补全提示
user-invocable: bool            # false = 背景知识
allowed-tools: string           # 允许的工具
model: string                   # haiku/sonnet/opus
effort: string                  # low/medium/high/max
context: string                 # "fork" = 隔离子 Agent 上下文
---
```

## Skill 两种使用模式

1. **预加载模式**：Agent 的 `skills` 字段指定，启动时注入完整内容。适用于稳定领域知识。
2. **调用模式**：用户 `/skill-name` 触发，独立执行。适用于用户主动触发的操作。

## Command → Agent → Skill 架构

```
用户输入 /command
    ↓
Command 编排入口（不直接执行，调度 Agent）
    ↓
Agent 自主执行（预加载 Skills，受限工具集，独立上下文）
    ↓
Skill 知识注入（定义"查什么"和"怎么做"）
```

**设计原则**：Command 是编排者，Agent 是执行者，Skill 是知识。

## 自进化模式

Agent 在每次执行后主动更新自身 Skills，形成闭环学习：

```
Agent 执行任务 → 发现新边界情况 → 更新 Skill → 记录 Learnings → 同步跨 Skill 一致性
```

**实现方式**：
- **Agent Prompt 内嵌**：prompt 中加入自进化要求
- **Stop Hook 触发**：`Stop` 事件注入回顾提示

**与本项目经验沉淀的映射**：
| 自进化模式 | AgentFlow 经验沉淀 |
|-----------|-------------------|
| 更新 Skill 边界情况 | 更新 skills/ 实现模式 |
| 记录 Learnings | 更新 Soul.md 动态经验 |
| 跨 Skill 同步 | shared/skills/ 知识一致性 |

差异：自进化是实时的，本项目是阶段性的。两者互补。

## 漂移检测模式

监控外部知识源变化，检测与本地知识的不一致：

```
漂移检测触发 → 获取外部最新文档 → 与本地比较 → 标记状态(NEW/RECURRING/RESOLVED) → 用户审批后应用
```

**五个检测维度**：Commands, Settings, Skills, Subagents, Concepts

## 安全设计

- **最小权限原则**：Agent 只授权需要的工具
- **工具限制**：用 `disallowedTools` 明确禁止危险操作
- **权限模式选择**：按场景选 default/acceptEdits/bypassPermissions

## 反模式

1. Agent 做太多事 → 拆分为专用 Agent
2. 过度权限 → 按最小权限原则
3. 无 maxTurns 限制 → 设置合理上限
4. Skill 过于泛化 → 拆分为专用 Skill
5. 缺少 description → 写明何时调用
6. 自进化无审核 → 关键修改需用户确认
7. Learnings 堆积不清理 → 定期归档精简
