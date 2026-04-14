---
name: execute-without-search
type: pitfall
module: workflow
status: verified
confidence: 0.95
created: 2026-04-13
last_validated: 2026-04-14
tags: [workflow, execute, pitfall, quality, search-first, skill-first]
---

# 不查就执行陷阱

> 不搜索 Skill/Wiki/Soul 就直接执行，导致输出质量差、已知问题重复踩坑。

## 三种典型表现

### 表现 1: 完全不搜索就执行
EXECUTE 阶段跳过搜索现有方案就自行执行，导致输出质量差：
- 内容过滤：没搜索过滤规范 → 保留了冗余内容
- 格式转换：没搜索标准模板 → 自行臆断格式
- 双验收：没搜索验收标准 → 验收项不专业

### 表现 2: 跳过搜索导致已知问题重复
执行子任务时，没有先搜索 skill/soul/wiki 中的已有知识，直接凭经验执行，导致已知问题再次发生。例如：全局已有 `gitlab-mr-creation` skill 明确记录了"glab mr create 可能 404，优先用 API"，但跳过搜索步骤直接用了 `glab mr create`。

### 表现 3: 先试错再查 Skill
先用自己的方式尝试（如 glab mr create），失败后才去搜索和读取相关 Skill。根因是对已知操作过于自信，认为不需要查 Skill，试错成本心理预期过低。

## 根因

1. 认知循环中"查找技能"只停留在工具层面，没有扩展到知识层面（过滤规范、格式模板、验收标准）
2. 对已知操作过于自信，认为不需要查 Skill
3. 忘记了"搜索先行"铁律适用于所有任务，包括看似熟悉的操作

## 修复方案

**每个子任务执行前必须执行搜索检查**：
1. `Grep` 搜索 `~/.agent-flow/skills/` 查找匹配技能
2. `Grep` 搜索 `.agent-flow/skills/` 查找项目技能
3. `Grep` 搜索 Soul.md 查找相关经验
4. `Grep` 搜索 Wiki 查找相关知识
5. 找到匹配 → 按 Procedure 执行
6. 未找到 → WebSearch 后再执行

**绝对禁止**：不搜索就直接执行，即使"觉得自己知道怎么做"。agent-flow 高频违规场景表是必须检查的清单，不是参考。

## 相关条目
- [[search-before-execute|patterns/workflow/search-before-execute]]
- [[git-archaeology-oversearch|Git考古过度搜索陷阱]]（反面：搜索过度）
