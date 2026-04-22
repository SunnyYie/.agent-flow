---
title: "RPI 工作流：Research → Plan → Implement"
category: pattern
module: workflow
agents: [main, planner, coder, verifier, researcher, architect]
scope: global
tags: [workflow, rpi, research, plan, implement, gate]
confidence: 0.85
sources: [shanraisshan/claude-code-best-practice]
status: verified
created: 2026-04-14
updated: 2026-04-14
---

# RPI 工作流：Research → Plan → Implement

> 结构化三阶段工作流，每阶段有明确的输入/输出和 GO/NO-GO 门控。

## 模式描述

RPI (Research → Plan → Implement) 是一种结构化开发工作流，每个阶段结束时进行 GO/NO-GO 评审，确保方向正确后才进入下一阶段。

## 三阶段详解

### Phase 1: Research（调研）

**输入**: 用户需求（原始描述）

**执行**: 并行启动多个调研 Agent
- 需求解析 Agent — 理解和拆解需求
- 产品经理 Agent — 评估业务价值
- 代码探索 Agent — 了解现有实现
- 技术顾问 Agent — 评估技术可行性
- 文档分析 Agent — 收集相关文档

**输出**: `RESEARCH.md`
- 需求理解（澄清模糊点）
- 现有代码分析
- 技术方案选项
- 风险评估

**门控**: GO（进入 Plan）/ NO-GO（回退补充调研）

### Phase 2: Plan（规划）

**输入**: `RESEARCH.md`（GO 通过后）

**执行**: 并行启动规划 Agent
- 高级工程师 Agent — 技术方案设计
- 产品经理 Agent — 优先级排序
- UX 设计师 Agent — 交互设计（如适用）
- 文档撰写 Agent — 文档规划

**输出**:
- `PLAN.md` — 总体计划
- `pm.md` — 产品经理视角
- `ux.md` — UX 设计视角
- `eng.md` — 工程实施视角

**门控**: GO（进入 Implement）/ NO-GO（回退修改计划）

### Phase 3: Implement（实施）

**输入**: `PLAN.md` + 各视角文档（GO 通过后）

**执行**: 编排实施 Agent
- 代码探索 Agent — 定位变更点
- 高级工程师 Agent — 编写代码
- 代码审查 Agent — 审查质量

**输出**: `IMPLEMENT.md` + 代码变更

## 与 AgentFlow 的映射

| RPI 阶段 | AgentFlow 对应 | 产出文件 |
|----------|---------------|---------|
| Research | pre-flight-check + knowledge-search | `.agent-flow/state/current_phase.md` |
| Plan | planner agent + requirement-decomposition | `requirement-decomposition.md` |
| Implement | code-implementation + tdd-workflow | 代码 + 测试 |

## GO/NO-GO 评审标准

### GO 条件
- [ ] 需求理解无歧义
- [ ] 技术方案可行且风险可控
- [ ] 依赖项已识别
- [ ] 有明确的验收标准

### NO-GO 条件
- 需求存在歧义且无法自行澄清
- 技术方案有重大风险未解决
- 缺少关键依赖信息
- 验收标准不明确

## 应用方式

1. **简单任务**: 跳过 Research，直接 Plan → Implement
2. **中等任务**: 完整三阶段，单人执行
3. **复杂任务**: 完整三阶段，多 Agent 并行（参考 Agent 编排模式）
4. **跨模型**: Research + Plan 用 Opus，Implement 用 Sonnet，QA 用 Codex

## 相关页面

- [[agent-resolution-order|Agent调度优先级]]
- [[three-agent-model|三Agent协作模型]]
- [[search-before-execute|先查后执行]]
