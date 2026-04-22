---
name: jira-workflow
version: 1.0.0
trigger: jira, 需求流转, 创建子任务, 状态变更, transition, subtask, 开发中, 提测, 排期
confidence: 0.9
abstraction: universal
created: 2026-04-15
---

# Skill: jira-workflow

> Jira 需求完整生命周期操作 — 子任务创建、状态流转（含字段）、工作流推进。

## Trigger

当用户需要以下操作时触发：

- 创建 Jira 子任务
- 流转 Issue 状态（如：评审通过、开始开发、提测）
- 查看可用流转及字段要求
- 推进需求从评审到完成的完整流程
- 处理流转失败（缺少字段、缺少子任务等）

## Required Reading

- 项目 Agent.md 中的自定义字段参考和常见流转 ID 参考章节（字段 ID 因项目而异）

## Procedure

### P1: 创建子任务

前提：父 Issue 已存在，需要创建 RD 子任务才能继续流转。

```bash
# 交互模式（用户手动填写字段）
jira issue subtask PARENT-KEY -s "研发子任务-XXX"

# Agent 模式（全部参数预填，避免交互 prompt）
jira issue subtask PARENT-KEY \
  -s "研发子任务-XXX" \
  --rd-owner USERNAME \
  --platform Server \
  --pd-owner USERNAME \
  --assignee USERNAME
```

验证：运行 jira issue view PARENT-KEY，检查 Subtasks 区域是否出现新建子任务。

### P2: 查看可用流转

流转前必须先查询可用流转 ID 和字段要求：

```bash
jira issue transition KEY
```

输出表格中 Fields 列含义：
- `N required` → 该流转需要 N 个必填字段，必须用 `--field` 提供
- `N required, M may require` → 有 N 个必填 + M 个可能被工作流验证器要求的字段
- `N fields (may require)` → Jira 标记为可选但实际可能必需的字段，建议预填
- `-` → 无额外字段，直接流转即可

### P3: 执行简单流转（无字段要求）

```bash
jira issue transition KEY --id TRANSITION_ID
```

### P4: 执行带字段的流转

当流转有 required 字段时，Agent 必须用 --field KEY=VALUE 预填：

```bash
jira issue transition KEY --id TRANSITION_ID \
  --field customfield_XXXXX=VALUE \
  --field customfield_YYYYY=VALUE
```

字段值类型规则：
- date → YYYY-MM-DD 格式字符串
- number / float → 纯数字（如 3，不需要引号）
- string / textarea → 用引号包裹文本
- option → 选项的 value 字符串

### P5: 处理流转错误

| 错误信息 | 原因 | 处理 |
|---|---|---|
| 需要创建研发子任务后才可以继续 | 父 Issue 没有子任务 | P1 创建子任务，再重试流转 |
| 需要所有子任务都完成才可以继续 | 子任务未全部 Done | 流转子任务到完成状态 |
| XXX is required in this transition | 缺少必填字段 | P2 查询字段要求，P4 补充 --field |
| Transition ID X not found | ID 不属于当前状态 | P2 重新查询可用流转 |
| 字段校验未通过（字段值被拒） | --field 提供的值不合法 | CLI 自动提示重新输入，无需手动重跑 |

### P6: 添加外链（MR 链接等）

开发完成或提交 MR 后，常需在 Issue 上关联外部链接。详细操作见 [[jira-remotelink|skills/integration/jira-remotelink/handler]]。

```bash
# 快速添加 MR 链接
jira issue remotelink KEY --url https://gitlab.com/merge/42 --title "MR !42"
```

## Rules

1. 流转前必查询：每次 transition --id 前，必须先不带 --id 查询可用流转，确认 ID 有效
2. Agent 模式不交互：Agent 必须预填所有参数，避免触发 Typer prompt 或 EDITOR
3. 先子后父：父 Issue 的流转可能依赖子任务状态，先处理子任务再流转父 Issue
4. 错误不重试：遇到验证错误，先分析原因（缺字段/缺子任务），修正后再执行，不盲目重试同一命令
