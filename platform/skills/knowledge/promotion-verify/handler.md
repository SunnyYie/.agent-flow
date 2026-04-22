---
name: promotion-verify
version: 1.0.0
trigger: 晋升验收, 全局写入验收, promotion verify, 验收晋升内容
confidence: 1.0
abstraction: universal
created: 2026-04-14
---

# Skill: Promotion Verify

> **全局知识库写入前的多Agent验收**。确保晋升内容通用、无重复、质量达标后，才允许写入 `~/.agent-flow/`。

## Trigger

- `experience-promotion` Skill 写入全局前自动触发
- 被 `promotion-guard.py` Hook 拦截后手动触发
- 用户手动触发（`promotion-verify`）

## Procedure

### Step 1: 收集待验收内容

从以下来源收集待晋升内容：

1. 项目 `.agent-flow/memory/main/Soul.md` 中 `abstraction: universal/framework` 的条目
2. 项目 `.agent-flow/wiki/` 中适合全局复用的条目
3. 项目 `.agent-flow/skills/` 中 `abstraction: universal` 的技能

将内容列表写入 `.agent-flow/state/promotion-candidates.md`，格式：

```markdown
# 待晋升验收内容

## 候选 1: [标题/名称]
- 来源: Soul.md / Wiki / Skill
- 类型: pattern / pitfall / skill / concept
- confidence: X.X
- 内容摘要: [50字以内]
- 目标路径: ~/.agent-flow/xxx/yyy.md
```

### Step 2: 启动 Verifier Agent 独立验收

启动 Verifier Agent（subagent_type: general-purpose），输入以下验收任务：

```
你是 AgentFlow 验收 Agent。请独立审查以下待晋升到全局知识库的内容。

对每条候选内容，逐一检查并输出验收报告：

### 验收检查项（每项 pass/fail + 说明）

1. **通用性检查**
   - 内容是否包含项目特有信息（文件路径、项目名、特定技术栈细节）？
   - 去除项目上下文后，内容是否仍然有意义？
   - pass 条件：无项目特有信息，或已标注需去除的部分

2. **相似性检查**
   - Grep 搜索 `~/.agent-flow/wiki/` 和 `~/.agent-flow/skills/`，查找与候选内容主题相似的已有文档
   - 搜索关键词：从标题和内容中提取 3-5 个核心词
   - 如果找到相似文档，输出文件路径和相似点
   - pass 条件：无相似内容，或相似内容已有但需要合并（标注合并方式）

3. **质量检查**
   - confidence >= 0.7？
   - 内容结构完整（有标题、描述、解决方案/应用方式）？
   - 有 Why 和 How to apply 说明？
   - pass 条件：confidence 达标 + 结构完整

4. **合并建议**（如有相似内容）
   - 应更新已有文档的具体章节
   - 应追加到已有文档的新章节
   - 应替换已有文档的过时内容
   - 无相似内容 → 标记为"新建"

### 输出格式

对每条候选：
- 候选编号 + 标题
- 各检查项结果（pass/fail + 说明）
- 最终结论：approve / reject / merge
- merge 时给出目标文件路径和合并方式
```

### Step 3: Main Agent 复核验收报告

Main Agent 审查 Verifier Agent 的验收报告：

1. **全部 approve** → 进入 Step 4
2. **有 reject** → 分析原因：
   - 项目特有内容未清理 → 清理后重新提交验收
   - confidence 不够 → 不晋升，保留在项目级
   - 结构不完整 → 补充后重新提交验收
3. **有 merge** → 确认合并方式和目标文件
4. **Main 与 Verifier 结论不一致** → 提交用户裁决

### Step 4: 创建验收标记

验收通过后，在 `.agent-flow/state/.promotion-verified` 中写入已验收的文件路径：

```
~/.agent-flow/wiki/patterns/workflow/new-pattern.md
~/.agent-flow/skills/new-skill/handler.md
```

每个路径一行。这个文件会被 `promotion-guard.py` Hook 读取。

**重要**：
- 验收标记是一次性的——写入成功后 Hook 会自动清除对应行
- 如果验收后超过 30 分钟未写入，标记失效，需重新验收
- 每条路径必须精确匹配即将写入的文件路径

### Step 5: 执行晋升写入

验收标记创建后，按 `experience-promotion` Skill 的流程执行写入：

- **approve（新建）**: 写入新文件
- **merge（合并）**: Edit 已有文件，合并新内容，更新 `updated` 字段
- 写入时 Hook 检测到验收标记，自动放行

## Rules

- **必须双Agent验收**：Main + Verifier 两个 Agent 独立审查，不能只由 Main 单方面确认
- **相似内容必须合并**：如果全局已有相似主题文档，必须更新已有文档，禁止新建重复文档
- **验收标记一次性**：写入后自动失效，不可复用
- **30分钟有效期**：验收后超过 30 分钟未写入需重新验收
- **Reject 不覆盖**：验收未通过的内容不晋升，保留在项目级
