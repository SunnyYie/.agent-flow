---
name: search-before-execute
type: pattern
module: workflow
status: verified
confidence: 0.95
created: 2026-04-13
last_validated: 2026-04-14
tags: [workflow, execute, quality, cognitive-loop, search-to-develop]
---

# 先查后执行模式

> 每个子任务执行前必须查找已有方案，搜索完成后立即切分支开发。

## 问题描述
EXECUTE 阶段跳过搜索 Skill/Wiki/Web 就直接执行，导致输出质量差：冗余内容、格式臃肿、验收标准不专业。搜索完后不知道下一步做什么，在搜索和开发之间反复犹豫。

## 解决方案

### 步骤 1: 搜索已有方案（按顺序）
1. `.agent-flow/skills/` 和 `~/.agent-flow/skills/` — 查找相关技能
2. `.agent-flow/memory/main/Soul.md` — 查找相关经验
3. `.agent-flow/wiki/` 和 `~/.agent-flow/wiki/` — 查找相关知识
4. WebSearch — 搜索专业标准和最佳实践

### 步骤 2: 搜索完成后的标准流程（线性执行，无分支）

```
搜索相关代码 → 分析结果
  ├─ 找到相关代码 → 定位修改点 → git pull --rebase → git checkout -b feat/xxx → 开始开发
  └─ 搜索不到字段 → 判定为新增字段 → git pull --rebase → git checkout -b feat/xxx → 开始开发
```

### 关键判断规则
1. 搜索不到 = 新增 → 直接开发，不需要验证其他分支
2. 搜索到但不确定 = 问用户 → 不要自行 git 考古
3. 搜索到且确认 = 立即切分支开发 → 不要过度分析

### 禁止行为
- 搜索完后用 git log/show/diff 继续考古
- 搜索不到字段时去其他分支验证
- 读取需求文档后不立即切分支开发

## 验证案例
- 飞书文档转需求规格说明书：不搜索就直接写 → 保留了冗余引言和项目管理占位符；搜索后发现需求规格说明书只需功能需求/非功能需求/埋点 → 优化后质量大幅提升

## 相关条目
- [[execute-without-search|pitfalls/workflow/execute-without-search]]
- [[git-archaeology-oversearch|pitfalls/workflow/git-archaeology-oversearch]]
