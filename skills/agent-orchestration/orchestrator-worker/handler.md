# Skill: 编排者-工作者模式

> 来源: [claude-cookbooks/orchestrator_workers.ipynb](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/orchestrator_workers.ipynb)
>
> **v2.0 更新**: 现已集成主 Agent + 子 Agent 上下文隔离架构。Medium/Complex 任务的 EXECUTE 阶段，工作者通过 Claude Code Agent tool 派发为独立子 Agent，避免上下文溢出。

## Trigger — 何时使用

- 复杂任务需要多个不同视角或方法来处理时
- 子任务类型和数量无法预先确定，需要根据具体输入动态决定时
- 需要比较不同策略或风格的输出时
- 单一 LLM 调用无法覆盖任务的多个维度时

## Required Reading — 前置阅读

- `~/.agent-flow/skills/agent-orchestration/main-agent-dispatch/handler.md` — 主 Agent 派发协议（上下文隔离核心）
- `~/.agent-flow/skills/ai-optimization/prompt-caching-optimization/handler.md` — 提示词缓存优化（编排者可预热缓存）
- `.agent-flow/wiki/patterns/orchestrator-workers.md` — 模式详解

## Procedure — 执行步骤

### Step 1: 判断是否适用

```
任务是否需要多种方法/视角？
├── 是 → 适合编排者-工作者模式
│   └── 子任务是否可预先确定？
│       ├── 否 → 必须使用编排者-工作者（动态分解是核心价值）
│       └── 是 → 考虑简单并行化（更简单高效）
└── 否 → 不适合，使用单一 LLM 调用
```

**适用**：内容生成（多风格）、分析任务（多角度）、问题解决（多策略）
**不适用**：简单单输出任务、延迟敏感场景、子任务永远相同

### Step 2: 定义编排者提示词

编排者提示词模板必须包含：

1. **任务分析指令**：要求理解任务并决定分解策略
2. **XML 输出格式要求**：`<analysis>` + `<tasks>` 结构
3. **子任务数量指导**：通常 2-3 个，可根据任务复杂度调整

```python
ORCHESTRATOR_PROMPT = """
Analyze this task and break it down into 2-3 distinct approaches:

Task: {task}

Return your response in this format:

<analysis>
Explain your understanding of the task and which variations would be valuable.
</analysis>

<tasks>
    <task>
    <type>approach_name</type>
    <description>What this approach should focus on</description>
    </task>
</tasks>
"""
```

### Step 3: 定义工作者提示词

工作者提示词模板必须传递三个变量：

1. **{original_task}**：原始完整任务描述（保持上下文）
2. **{task_type}**：工作者应采用的风格/方法
3. **{task_description}**：具体的执行指令

```python
WORKER_PROMPT = """
Generate content based on:
Task: {original_task}
Style: {task_type}
Guidelines: {task_description}

Return your response in this format:

<response>
Your content here.
</response>
"""
```

### Step 4: 执行与聚合

**方式一：Claude Code Agent tool 派发（推荐，上下文隔离）**

当任务复杂度 ≥ Medium 时，使用 Claude Code Agent tool 派发独立子 Agent：

```python
# 主 Agent 上下文中只保留流程状态
# 1. 更新 flow-context.yaml
# 2. 创建任务包
# 3. 派发子 Agent

# 并行派发多个无依赖的工作者
Agent({
    description: "executor-1: {task_type_1}",
    prompt: "你是执行者 Agent。\n任务: {task_description}\n验收标准: {criteria}\n任务包: .agent-flow/artifacts/task-{id}-packet.md\n摘要: .agent-flow/artifacts/task-{id}-summary.md",
    subagent_type: "general-purpose"
})

Agent({
    description: "executor-2: {task_type_2}",
    prompt: "你是执行者 Agent。\n任务: {task_description}\n验收标准: {criteria}\n任务包: .agent-flow/artifacts/task-{id}-packet.md\n摘要: .agent-flow/artifacts/task-{id}-summary.md",
    subagent_type: "general-purpose"
})
```

详见 `~/.agent-flow/skills/agent-orchestration/main-agent-dispatch/handler.md`。

**方式二：Python FlexibleOrchestrator（简单任务，无需上下文隔离）**

```python
from agent_flow.core.orchestrator import FlexibleOrchestrator, ORCHESTRATOR_PROMPT, WORKER_PROMPT

orchestrator = FlexibleOrchestrator(
    orchestrator_prompt=ORCHESTRATOR_PROMPT,
    worker_prompt=WORKER_PROMPT,
    llm_call=my_llm_call_fn,
    max_workers=3,
)

result = orchestrator.process(
    task="Write a product description for X",
    context={"target_audience": "developers", "key_features": ["fast", "secure"]},
)

# result.analysis — 编排者分析
# result.worker_results — 工作者结果列表
# result.metadata — 执行统计（成功/失败数）
```

### Step 5: 投机缓存优化

编排者分解任务后，工作者将共享相同的大上下文。可以在工作者执行前预热缓存：

```python
# 编排者完成后，工作者执行前
# 对共享上下文发送 1-token 预热请求
# 确保所有工作者命中缓存
```

## Rules — 规则约束

1. **工作者必须收到完整上下文**：禁止仅传递子任务 ID 而不传递原始任务描述
2. **输出必须验证**：工作者可能返回空值或格式错误，必须兜底处理
3. **成本考量**：编排者-工作者需要 N+1 次 LLM 调用（1 编排 + N 工作者），仅在任务确实需要多视角时使用
4. **延迟考量**：工作者并行执行可降低延迟，串行执行会增加总时间
5. **XML 解析健壮性**：LLM 可能不严格遵循 XML 格式，解析代码需容错
6. **工作者失败兜底**：子Agent可能因429速率限制失败，主Agent必须用Glob检查产出文件是否存在，不存在则自行完成。详见 `wiki/pitfalls/workflow/multi-agent-rate-limit-recovery.md`

## 相关

- [提示词缓存优化](prompt-caching-optimization/handler.md)
- [AI 上下文管理](ai-context-management/handler.md)
- [编排者-工作者 Wiki](.agent-flow/wiki/patterns/orchestrator-workers.md)
