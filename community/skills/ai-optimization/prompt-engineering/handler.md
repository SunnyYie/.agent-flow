# Shared Skill: Prompt Engineering for Agent Plugins

## Trigger

When designing Agent prompts, system rules, or skill prompts. Used in Phase 10 (Agent plugins) and whenever creating/modifying prompt.md files. Inspired by agency-agents personality-driven prompt architecture.

## Required Reading

- `documents/设计.md` — 第9节三层提示词架构
- `.dev-workflow/Agent.md` — 铁律

## Three-Layer Prompt Architecture

```
┌─────────────────────────────────────────────┐
│ Layer 1: System Prompt（系统规则层）         │
│ - 安全规则、Git 权限、Worktree 限制          │
│ - 所有 Agent 共享                            │
│ - 来源: aw/plugins/system_rules.md           │
├─────────────────────────────────────────────┤
│ Layer 2: Role Prompt（角色专业层）           │
│ - Agent 特定的专业知识和流程                  │
│ - 每个 Agent 独有                            │
│ - 来源: aw/plugins/{agent}/prompt.md         │
├─────────────────────────────────────────────┤
│ Layer 3: Skill Prompt（技能注入层）          │
│ - 动态注入的任务相关 SOP                      │
│ - ChromaDB 上下文                             │
│ - 来源: skills/ 目录 + ChromaDB 搜索         │
└─────────────────────────────────────────────┘
```

## Prompt Design Patterns

### Pattern 1: Role Definition with Personality

```markdown
# PRD Agent

## 你是谁
你是一位资深产品经理，擅长将模糊的需求转化为精确的技术规格。

## 你的核心能力
- 文档清洗：从冗余的飞书文档中提取核心业务目标
- Logic/UI 拆分：区分后端逻辑变更和前端界面变更
- ASSUMPTION 标注：在信息不足时明确标注假设

## 你的工作流程
1. 读取 → 2. 清洗 → 3. 拆分 → 4. 标注 → 5. 输出
```

### Pattern 2: Structured Output Specification

```markdown
## 输出格式

### PRD.md（人类可读）
- 功能需求章节
- Logic 变更清单
- UI 变更清单
- ASSUMPTION 列表
- 待确认问题

### PRD.json（机器可解析）
{
  "requirement_id": "R-001",
  "features": [
    {
      "id": "F-001",
      "type": {"primary": "logic", "impact": ["backend"]},
      "description": "...",
      "assumptions": ["..."],
      "affected_files": ["..."]
    }
  ]
}
```

### Pattern 3: Constraint-First Rules

```markdown
## 你必须遵守的规则
1. 不做超出 PRD 范围的设计决策
2. 不确定时标注 [ASSUMPTION]，不自行推断
3. Logic 和 UI 必须明确分类，不允许"两者皆是"
4. 所有功能点必须有 acceptance criteria
```

### Pattern 4: Few-Shot Example

```markdown
## 示例

输入: "用户需要一个登录页面"
输出:
  Logic: 后端认证 API（POST /auth/login）、JWT token 生成
  UI: 登录表单组件、错误提示组件
  ASSUMPTION: 使用 JWT 而非 session（假设前后端分离架构）
  受影响文件: src/api/auth.py, src/components/LoginForm.tsx
```

### Pattern 5: Variable Substitution for Multi-Step Context

多步骤 AI 流程中，通过变量替换在步骤间传递上下文：

```markdown
## 上下文注入
$ARGUMENTS          — 用户原始输入
$PREVIOUS_OUTPUT    — 上一步骤的输出
$ARTIFACTS_DIR/plan.md — 前序步骤的产物文件路径
$nodeId.output.field — 上游节点的结构化输出字段
```

**规则**：
- 变量在执行时替换为实际值，提示词中用 `$` 前缀标记
- 大段内容通过文件路径引用（`$ARTIFACTS_DIR/xxx.md`），不内联到提示词中
- 敏感变量（密钥、token）不得使用变量替换传递
- 参考 `ai_context_management.md` 了解完整的上下文管理策略

## System Rules Template (Layer 1)

```markdown
# 安全规则

## Git 权限
- 你只能在分配的 feature 分支上工作
- 禁止 push 到 main 或 develop
- 提交前确认 .gitignore 生效

## 命令限制
- 禁止执行: rm -rf, DROP TABLE, mkfs, dd
- 禁止访问: .env, *.key, *.pem, credentials*
- 禁止上传数据到: pastebin, gist 等外部服务

## Worktree 限制
- 只能在指定 Worktree 目录内创建/修改文件
- 不读取 Worktree 外的文件（除非是只读参考）
```

## Prompt Anti-Patterns

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| 模糊指令 | "分析文档" → 输出不可预测 | "提取业务目标和前置条件，输出为 JSON" |
| 无约束 | Agent 可能发散 | 设置明确的边界和禁止事项 |
| 过长提示词 | 关键信息被淹没 | 三层分离，按需注入 |
| 无输出格式 | 格式不一致 | 提供 JSON schema 或 markdown 模板 |
| 无示例 | Agent 理解偏差 | 提供输入→输出的 few-shot 示例 |

## Prompt Quality Checklist

- [ ] 角色定义清晰（你是谁、你做什么）
- [ ] 工作流程有序（Step 1, 2, 3...）
- [ ] 输出格式明确（JSON schema 或 markdown 模板）
- [ ] 约束条件列举（不能做什么）
- [ ] 有 few-shot 示例（至少一个输入→输出对）
- [ ] 与设计文档对齐（字段名、枚举值、流程一致）

## Rules

- 提示词三层分离，不在 Role Prompt 中重复安全规则
- 每个 Agent 的 prompt.md 必须包含：角色定义、工作流程、输出格式、约束
- 输出格式必须同时提供人类可读和机器可解析两种
- 提示词长度控制在合理范围（避免信息过载）
- 新增提示词必须与设计文档对齐
