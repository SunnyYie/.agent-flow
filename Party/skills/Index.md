# Team Skills Index

This index summarizes reusable Agent-flow skills for fast lookup.
Global skills root: `/Users/sunyi/ai/agent-flow-team/agent_flow/resources/skills`
Source mode: bundled fallback (local global skills not found).

## Quick Routing

- 任务入口与规划: `workflow/pre-flight-check`
- 并行子 Agent 编排: `agent-orchestration/orchestrator-worker`
- 知识先行检索: `knowledge/knowledge-search`
- 代码实现与测试: `development/code-implementation`
- 交付前质量与验收: `workflow/acceptance-check`

## Implemented Skill Domains
- `agent-orchestration` (3): 多 Agent 编排、上下文预算与派发协议
- `development` (6): 实现模式、TDD、审查与安全校验
- `documentation` (3): 文档转换、过滤与需求拆解
- `knowledge` (2): 知识检索、经验晋升与关键知识固化
- `research` (3): 源码/网络调研与工具前置检查
- `workflow` (5): 任务流程控制、复杂度评估、阶段门控与验收

## Scene Examples
- `agent-orchestration`: `agent-orchestration/agent-orchestration`, `agent-orchestration/main-agent-dispatch`, `agent-orchestration/orchestrator-worker`
- `development`: `development/architecture-design`, `development/code-implementation`, `development/code-review`
- `documentation`: `documentation/content-filter`, `documentation/doc-conversion`, `documentation/requirement-decomposition`
- `knowledge`: `knowledge/critical-knowledge`, `knowledge/knowledge-search`
- `research`: `research/source-code-research`, `research/tool-precheck`, `research/web-research`
- `workflow`: `workflow/acceptance-check`, `workflow/phase-review`, `workflow/pre-flight-check`

## Notes For Agents

- 先按 domain 路由，再定位具体 skill。
- 若多个 skill 同时适用，优先执行 workflow 相关 skill。
- 新增团队技能后，建议更新本索引。
