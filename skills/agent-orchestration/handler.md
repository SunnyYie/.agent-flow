---
name: agent-orchestration
version: 1.0.0
trigger: 多Agent协作, 编排Agent, agent编排, 子Agent, orchestrator, 流水线, pipeline
confidence: 0.8
abstraction: framework
created: 2026-04-13
---

# Skill: agent-orchestration

> 灵感来源: agency-agents Agents Orchestrator — 自主流水线管理，Dev-QA循环，质量门控

## Trigger
当需要编排多个子Agent协作完成一个复杂任务时触发

## Procedure

1. **分析任务**：将任务分解为可分配给子Agent的独立阶段
2. **选择Agent角色**：根据子任务类型分配对应角色

### 可用角色与分配策略

| 任务类型 | 角色 | 说明 |
|---------|------|------|
| 信息搜索/调研 | Researcher | 查资料、找方案、交叉验证 |
| 代码实现 | Coder | 按设计文档编码、TDD |
| 文档撰写/转换 | Writer | 按模板组织、精确保留数据 |
| 质量验收 | Verifier | 证据驱动、标准先行 |
| 架构设计 | Architect | 权衡分析、ADR记录 |
| 任务规划 | Planner | 分解任务、标注依赖 |

3. **编排流程**：

```
Planner(分解任务) → Main(确认计划)
    ↓
[T1,T2,...] → 按依赖分配Executor
    ↓
每个子任务完成 → Verifier双验收
    ↓ 验收通过
下一子任务
    ↓ 全部通过
Main(阶段总结)
```

4. **质量门控**：
   - 每个子任务必须通过双验收才能进入下一个
   - 验收失败 → 带反馈返回执行者，最多重试3次
   - 3次失败 → 标记为阻塞，继续后续任务

5. **上下文传递**：每个Agent启动时传入：
   - 任务描述和完成标准
   - 相关上下文（前置阶段输出）
   - 可用的Skill和Wiki条目路径

## Rules
- 严格执行质量门控，不跳过验收
- 子Agent用完即关，不保持空闲
- 每个Agent只做分配给它的任务，不越界
- 阶段完成后必须写阶段总结到 `.agent-flow/logs/dev_log.md`
