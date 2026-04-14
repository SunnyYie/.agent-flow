---
title: "Monorepo CLAUDE.md 加载机制"
category: concept
module: workflow
agents: [main, architect, planner]
scope: global
tags: [monorepo, claudemd, loading, ancestor, descendant, skills]
confidence: 0.85
sources: [shanraisshan/claude-code-best-practice]
status: verified
created: 2026-04-14
updated: 2026-04-14
---

# Monorepo CLAUDE.md 加载机制

> 理解 CLAUDE.md 在 monorepo 中的加载顺序和作用域，避免指令冲突。

## 问题描述

在 monorepo 中，多个 CLAUDE.md 文件可能存在不同目录层级。不了解加载机制会导致：
- 子目录的 CLAUDE.md 覆盖根目录的规则
- 不必要的 CLAUDE.md 被加载，浪费上下文
- 同一规则在多处重复定义，维护困难

## 加载方向

### 向上加载（Ancestor — 立即加载）

从当前目录向根目录遍历，所有路径上的 CLAUDE.md **立即加载**。

```
~/project/                    ← CLAUDE.md (加载)
~/project/packages/           ← CLAUDE.md (加载)
~/project/packages/frontend/  ← CLAUDE.md (加载) ← 当前工作目录
```

**特点**: 启动时全部加载，适合全局规则（技术栈、编码规范、禁止项）

### 向下加载（Descendant — 延迟加载）

当前目录的子目录中的 CLAUDE.md **延迟加载**，仅在读取该子目录中的文件时触发。

```
~/project/                    ← 当前工作目录
~/project/packages/frontend/  ← CLAUDE.md (仅在读取 frontend/ 文件时加载)
~/project/packages/backend/   ← CLAUDE.md (仅在读取 backend/ 文件时加载)
```

**特点**: 按需加载，适合子项目特有规则（框架配置、测试策略）

### 兄弟目录（Sibling — 不加载）

同一层级的其他目录中的 CLAUDE.md **永远不会加载**。

```
~/project/packages/frontend/  ← 当前工作目录
~/project/packages/backend/   ← CLAUDE.md (不加载，即使有文件也不读取)
```

## Skill 发现机制

Skill 的发现与 CLAUDE.md 不同：

- 嵌套的 `.claude/skills/` 在操作该子目录的文件时**自动发现**
- 优先级: Enterprise > Personal (`~/.claude/skills/`) > Project (`.claude/skills/`)
- 插件 Skill 使用 `plugin-name:skill-name` 命名空间
- Skill 描述始终加载（在字符预算内），完整内容仅在调用时加载
- 字符预算默认 15,000 chars，可通过 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 配置

## 最佳实践

### 1. 分层定义规则

```text
根目录 CLAUDE.md:
  - 全局编码规范
  - 技术栈声明
  - 禁止项

packages/frontend/CLAUDE.md:
  - React 特有规则
  - 组件命名规范

packages/backend/CLAUDE.md:
  - Go/Python 特有规则
  - API 设计规范
```

### 2. 不重复定义

- 子目录 CLAUDE.md 只补充，不重复根目录的规则
- 使用 `> See root CLAUDE.md for shared rules` 引用

### 3. 控制 CLAUDE.md 大小

- 每个 CLAUDE.md 不超过 200 行
- 超出部分移入 Skill 文件
- Skill 的描述始终加载，但完整内容按需加载

## 相关页面

- [[memory-systems|四层记忆系统]]
- [[claude-code-settings|关键设置与环境变量]]
