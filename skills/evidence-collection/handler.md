# Skill: Evidence Collection & Verification Report

## Trigger

When generating any [VERIFY-REPORT]. Inspired by the Evidence Collector pattern — claims without evidence are worthless.

## Required Reading

- `.dev-workflow/Agent.md` — 验收报告格式定义
- `.dev-workflow/verifier/skills/acceptance_check.md` — 验收流程

## Evidence Types (Ranked by Reliability)

| 等级 | 证据类型 | 示例 | 可靠度 |
|------|----------|------|--------|
| L1 | 命令输出 | pytest stdout, ruff check 输出 | 最高 |
| L2 | 文件内容 | 源码、配置文件 | 高 |
| L3 | 结构验证 | import 成功、类/函数存在 | 中 |
| L4 | 逻辑推断 | "代码看起来正确" | 低（需 L1-L3 支持） |

**规则**：每个验收标准至少需要 L1 或 L2 证据。仅靠 L4 证据不能判定 PASS。

## Evidence Collection Procedure

### Step 1: Gather Raw Evidence

```bash
# 1. 运行测试，捕获完整输出
/Users/sunyi/ai/sunyi-llm/.venv/bin/pytest agent-workflow/tests/test_{module}.py -v

# 2. 运行 lint，捕获结果
/Users/sunyi/ai/sunyi-llm/.venv/bin/ruff check agent-workflow/aw/{module}.py

# 3. 验证 import 链
/Users/sunyi/ai/sunyi-llm/.venv/bin/python -c "from aw.{module} import {Class}"

# 4. 读取实现文件关键部分
# 用 Read 工具查看源码
```

### Step 2: Map Evidence to Acceptance Criteria

对于实施计划中的每个"完成标志"：

```
完成标志: "所有 Agent 和工作流节点可依赖的中央状态契约"
  ↓
证据1 (L1): pytest 输出 24 passed
证据2 (L2): state.py 包含 WorkflowState TypedDict 含 18 个字段
证据3 (L3): `from aw.core.state import WorkflowState` 成功
  ↓
结论: ✅ PASS
```

### Step 3: Check for Evidence Gaps

- 有没有验收标准只有 L4 证据？
- 有没有文件存在性只看报告未验证？
- 有没有测试覆盖但未实际运行的？

### Step 4: Generate Report

```
[VERIFY-REPORT] S{x.y}: {任务标题}
- 完成标志1: ✅ PASS - pytest 输出 {N} passed（L1证据）
- 完成标志2: ✅ PASS - state.py 第{行}包含{具体内容}（L2证据）
- 完成标志3: ❌ FAIL - {具体原因}（L1证据: pytest 输出第{行}）
- 测试: PASS ({N}/{M} passed)
- Lint: PASS/FAIL
- 总体: PASS / FAIL
```

## Anti-Patterns to Avoid

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| "代码已实现" | 没有证据证明可运行 | 提供 pytest 输出 |
| "看起来正确" | 主观判断 | 提供客观证据 |
| "测试应该通过" | 没有实际运行 | 提供运行结果 |
| "与计划一致" | 没有逐条对比 | 逐条列出对应关系 |
| 只报告 PASS 的项 | 隐瞒 FAIL | 所有标准都报告 |

## Cross-Reference Verification

当验收标准引用设计文档时，需要交叉验证：

```
实施计划说: "定义 WorkflowState TypedDict 包含设计文档 5.2 节所有字段"
  ↓
1. 读取 documents/设计.md 第 5.2 节
2. 提取所有字段列表
3. 与实际 state.py 中的字段逐一对比
4. 报告：哪些匹配、哪些缺失、哪些多余
```

## Rules

- 每个验收标准必须有 L1 或 L2 级别证据
- FAIL 的条目必须包含具体原因和修复建议
- 交叉验证时不假设实施计划描述100%正确——以设计文档为准
- 不遗漏任何验收标准，即使看起来"明显通过"
