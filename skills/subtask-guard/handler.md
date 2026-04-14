---
name: subtask-guard
version: 1.0.0
trigger: 执行子任务, 子任务开始, subtask, 执行前搜索, 子任务执行
confidence: 1.0
abstraction: universal
created: 2026-04-13
---

# Skill: Subtask Guard

> **子任务执行守卫**。每个子任务执行前必须调用，确保"先查后执行"。这是对 pre-flight-check Step 2 的逐子任务细化。

## Trigger

每个子任务执行前必须触发。在 EXECUTE 阶段，Agent 准备动手执行某个子任务时，先执行本技能。

## Procedure

### Step 1: 提取子任务关键词

从 `.agent-flow/state/current_phase.md` 中读取当前子任务描述，提取2-3个核心关键词。

### Step 2: 快速搜索（4步，每步必执行）

```text
1. Grep "{关键词}" .agent-flow/skills/         → 项目技能（匹配 trigger 字段）
2. Grep "{关键词}" ~/.agent-flow/skills/        → 全局技能
3. Grep "{关键词}" .agent-flow/memory/main/Soul.md  → 项目经验
4. Grep "{关键词}" .agent-flow/wiki/ + ~/.agent-flow/wiki/ → 知识库
```

**注意**：这4步是 AND 关系，全部执行，不是找到就停。

### Step 3: 代码定位（涉及代码修改的子任务必须执行）

如果子任务涉及代码修改，**必须先精准定位代码位置**：

```text
1. 从子任务描述中提取领域关键词（业务实体词、技术特征词、交互动作词）
2. 按分层搜索定位代码（由窄到宽，不要直接全项目扫描）：
   - Layer 1: Grep "{业务实体词}" src/ -t {对应语言}  → 精确匹配
   - Layer 2: Grep "{词根}" src/                      → 模糊匹配
   - Layer 3: Grep "{关键词}" src/routes/ src/config/  → 路由/配置匹配
   - Layer 4: Grep "{关键词}" .                         → 全局（最后手段）
3. 整理为代码影响地图，写入 .agent-flow/state/code-impact-map.md
4. 详细步骤参考 requirement-code-mapping 技能
```

**绝对禁止**：跳过精准搜索，直接全项目扫描。

### Step 4: 选择执行方式（调度优先级）

根据子任务特征，按 **Skill → Agent → Command** 优先级选择执行方式：

```text
子任务评估：
├── 能在主对话内联完成？（简单查询/格式转换/知识注入）→ Skill 内联执行
├── 需要独立上下文？（复杂推理/代码审查/安全分析）→ Agent 独立执行
│   ├── 调试/探索类 → Explore Agent (haiku, 只读)
│   ├── 代码实现类 → Coder Agent (sonnet)
│   └── 深度分析类 → Researcher/Architect Agent (opus)
└── 需要编排多步骤？（用户入口/多Agent协作）→ Command 编排
    └── Command 内部可调度 Agent + Skill
```

**关键判断**：
- 预计产生大量中间输出（日志/调试信息/长代码） → **必须用 Agent**，避免污染主对话
- 简单知识查询（1-2步完成） → **用 Skill 内联**，零上下文开销
- 不确定 → 优先 Skill，如果执行中发现上下文膨胀则切换为 Agent

### Step 5: 根据搜索结果+执行方式执行

```text
知识搜索 + 代码定位 + 执行方式决策 → 有匹配 Skill？
├─ 有 → Read 该 Skill，严格按 Procedure 执行
│        执行方式: {Skill内联 / Agent独立}
│        在 Memory.md 中记录: "技能: {skill_name} | 方式: {inline|agent}"
└─ 无 → WebSearch "{关键词} best practice"
         在 Memory.md 中记录: "技能: 无-WebSearch搜索方案 | 方式: {inline|agent}"
```

### Step 6: 记录到 Memory.md

```markdown
[EXECUTE] {日期时间} T{n}: {子任务描述}
技能: {使用的技能名称，或"无-WebSearch搜索方案"}
执行方式: {Skill内联 / Agent独立 / Command编排}
代码定位: {关键词}→{文件路径}，或"不涉及代码修改"
操作: {具体操作}
结果: {成功/失败/部分完成}
```

## Rules

- **不搜索就执行 = 违规**：这是铁律，不可跳过
- **搜索全做**：4步搜索全部执行，不能只搜1-2步就停
- **有 Skill 必用**：找到匹配的 Skill 必须按其 Procedure 执行，不能自己发明方案
- **无 Skill 必搜**：没找到 Skill 时必须 WebSearch，不能凭空臆断
- **调度优先级**：Skill 内联 → Agent 独立 → Command 编排，优先选轻量方式
- **隔离大输出**：预计产生大量中间输出的子任务必须用 Agent，避免污染主对话
- **记录必写**：每次执行都必须写入 Memory.md，格式固定
