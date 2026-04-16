---
name: experience-promotion
version: 2.1.0
trigger: 经验晋升, 知识晋升, reflect, EVOLVE, 经验推广, promote, 知识同步
confidence: 1.0
abstraction: universal
created: 2026-04-13
updated: 2026-04-14
---

# Skill: Experience Promotion

> **项目经验晋升到全局**。REFLECT 阶段的最后一步，将项目中的通用经验同步到 `~/.agent-flow/`，确保跨项目复用。v2.1 新增记忆类型选择指导。

## Trigger

每个任务 REFLECT 阶段完成后触发。也可由用户手动触发（`agent-flow reflect`）。

## 记忆类型选择指导

晋升时选择正确的持久化机制：

```text
经验需要持久化：
├── 是项目规则/禁止项？ → 写入项目 CLAUDE.md（≤200行）
├── 是跨项目通用规则？ → 写入全局 CLAUDE.md 或 ~/.agent-flow/ 规则
├── 是用户偏好/工作习惯？ → Auto-memory（.claude/memory/）
├── 是 Agent 领域经验？ → Agent Memory（.claude/agent-memory/）
├── 是可复用的成功模式？ → Wiki patterns/
├── 是踩坑教训？ → Wiki pitfalls/
└── 是可执行的步骤？ → Skills/
```

**关键原则**：
- CLAUDE.md 只放规则和禁止项（始终加载，影响所有行为）
- Auto-memory 放用户偏好和上下文（仅主 Claude 可读）
- Wiki 放知识和经验（搜索后可读，按需加载）
- Skills 放可执行步骤（触发时加载，按需执行）

## Procedure

### Step 1: 扫描项目 Soul.md 中的通用经验

读取 `.agent-flow/memory/main/Soul.md`，筛选 `abstraction: universal` 或 `abstraction: framework` 的条目。

**晋升条件**（同时满足）：
- `abstraction` 为 `universal` 或 `framework`
- `confidence` >= 0.7
- 该经验在全局 Soul.md 中**不存在**（避免重复）

### Step 2: 逐条晋升到全局 Soul.md

对每条满足条件的经验：

1. 读取全局 `~/.agent-flow/memory/main/Soul.md`
2. Grep 检查全局 Soul.md 中是否已有**相似**经验（不只是同名，而是主题相近）
3. **不存在** → 追加到全局 Soul.md 动态区末尾
4. **已存在相似** → **合并更新**（不是跳过！）：
   - 比较 confidence：如果项目经验更高，用项目经验替换全局条目
   - 比较 validations：合并两边的验证次数
   - 合并内容：将项目经验中的新洞察补充到全局条目，保留全局条目的已有上下文
   - 更新日期为当天

**晋升时注意**：
- 去除项目特有的上下文（如具体文件路径、项目名），只保留通用部分
- 保留 confidence 和 validations 字段
- 保留 module 和 type 标签

### Step 3: 扫描项目 Wiki 中的通用知识

读取 `.agent-flow/wiki/INDEX.md`，找出适合跨项目复用的 Wiki 条目：

**晋升条件**：
- Wiki 条目的 `abstraction` 为 `universal`（如有标注）
- 内容描述的是通用模式/踩坑，不绑定特定项目

对每条满足条件的 Wiki 条目：

1. 读取项目 Wiki 条目内容
2. **执行 promotion-verify Skill** — 多Agent验收（详见该 Skill）
3. 验收通过后获得 `.promotion-verified` 标记
4. 检查全局 `~/.agent-flow/wiki/` 中是否已有**相似**条目：
   - Grep 搜索全局 wiki 目录，用条目标题的关键词搜索
   - 检查 wiki/INDEX.md 中是否有同类主题的条目
5. **不存在相似** → 复制到全局 Wiki 对应目录，更新全局 `~/.agent-flow/wiki/INDEX.md`
6. **已存在相似** → **合并更新已有文档**：
   - 读取已有文档内容
   - 将新内容中有价值的部分合并到已有文档
   - 更新 `updated` 字段为当天
   - 如果新内容是已有内容的补充视角，添加新章节而非替换
   - 如果新内容修正了已有内容的错误，替换对应部分并添加修正说明
   - 更新全局 INDEX.md 中该条目的描述（如有变化）

### Step 4: 扫描项目 Skills 中的通用技能

读取 `.agent-flow/skills/` 目录，找出 `abstraction: universal` 的技能：

**晋升条件**：
- `abstraction` 为 `universal`
- `confidence` >= 0.7

对每条满足条件的技能：

1. 读取项目技能文件
2. **执行 promotion-verify Skill** — 多Agent验收
3. 验收通过后获得 `.promotion-verified` 标记
4. 检查全局技能中是否已存在：
   - 同名技能 → 比较版本号和 confidence
   - **同名，项目版本更高** → 更新全局技能内容
   - **同名，全局版本更高** → 跳过（全局已是最新）
   - **不同名但功能相似** → 检查 Procedure 是否重叠
     - 重叠 > 50% → 合并到已有技能，扩展 Procedure 步骤
     - 重叠 <= 50% → 作为独立技能新建（需验收标记）

### Step 5: 记录晋升日志

在 `.agent-flow/memory/main/Memory.md` 中记录晋升结果：

```markdown
[PROMOTE] {日期时间}
晋升到全局 Soul.md: {条目摘要列表}
晋升到全局 Wiki: {条目列表}
  - 新建: {条目列表}
  - 合并更新: {已有文档} ← {新内容摘要}
晋升到全局 Skills: {技能列表}
  - 新建: {技能列表}
  - 合并更新: {已有技能} ← {新内容摘要}
  - 版本更新: {技能} v{旧} → v{新}
跳过（全局已是最新）: {条目列表}
验收未通过: {条目列表 + 原因}
```

## Rules

- **REFLECT 必触发**：每次 REFLECT 阶段结束后必须执行本技能
- **只晋升通用经验**：`abstraction: project` 的条目不晋升
- **去重用合并，不用跳过**：发现相似内容时，合并更新已有文档，而不是创建新文档或直接跳过
- **写入全局前必须验收**：Wiki 和 Skills 的晋升必须先通过 `promotion-verify` 多Agent验收
- **去项目上下文**：晋升时去除项目特有的文件路径、项目名等
- **confidence 阈值**：只晋升 confidence >= 0.7 的经验
- **不删除项目级**：晋升是复制，不是移动。项目级经验保留不动

## 变更历史

- v2.1.0 (2026-04-14): 新增记忆类型选择指导（CLAUDE.md/Auto-memory/Agent Memory/Wiki/Skills 分流）
- v2.0.0 (2026-04-14): 新增多Agent验收机制；相似内容合并更新而非跳过；与 promotion-guard.py Hook 联动
- v1.0.0 (2026-04-13): 初始版本
