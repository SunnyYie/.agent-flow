---
name: enforcement-structure
type: decision
module: architecture
status: verified
confidence: 0.9
created: 2026-04-13
tags: [enforcement, rules, skills, agent-flow]
---

# 规则执行保障架构：短规则 + 详细技能 + 守卫技能

## 问题

AgentFlow 协议定义完善，但 Agent 在实际执行中经常不遵守：

1. 不按思维链生成任务执行文档
2. 不检查项目配置（.dev-workflow / .agent-flow）
3. 不搜索 skill/soul/wiki/memory 就直接执行

根因：规则靠文档传达，没有结构化的强制执行机制。Agent 必须"记得"去遵守，但实际执行中经常忘记。

**Why**: Soul.md 记录了 confidence 0.95 的教训："EXECUTE阶段最大的问题：没有先查找Skill/Wiki/Web就自行执行"，验证了2次仍未解决。说明仅靠文档记录教训不足以改变行为。

## 决策

采用三层执行保障架构：

### Layer 1: 短规则文件（~/.claude/rules/agent-flow-enforcement.md）

- 每次对话自动加载，无需主动读取
- 极简（3条铁律），不超过30行
- 作用：提醒 Agent 必须做什么

### Layer 2: 详细技能文件（~/.agent-flow/skills/pre-flight-check/）

- 按需加载，包含完整的5步Procedure
- 作用：指导 Agent 怎么做

### Layer 3: 守卫技能（~/.agent-flow/skills/subtask-guard/）

- 每个子任务执行前触发
- 4步搜索（Skill → Soul → Wiki → WebSearch）
- 作用：防止 Agent 跳过搜索步骤

**How to apply**:

- 新项目：`pre-flight-check` 技能会检查 `.dev-workflow/` 和 `.agent-flow/` 是否存在
- 每个任务：短规则文件提醒执行 pre-flight-check
- 每个子任务：subtask-guard 强制搜索知识库
- 关键词：在规则文件中用"违规"等强措辞增强约束力

## 相关条目

- [[search-before-execute|先查后执行模式]]
- [[execute-without-search|不查就执行陷阱]]
