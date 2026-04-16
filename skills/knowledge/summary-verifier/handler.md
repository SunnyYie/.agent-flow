---
name: summary-verifier
version: 1.0.0
trigger: 摘要验证, summary verify, 验证摘要, 抽检
confidence: 1.0
abstraction: universal
created: 2026-04-15
---

# Skill: 摘要验证（Verifier 抽检）

> **确保摘要准确性**：Verifier Agent 独立抽检子 Agent 生成的摘要，验证是否准确反映实际变更。

## Trigger

- Medium/Complex 任务子 Agent 完成后
- 主 Agent 收集 L2 摘要时
- flow-context.yaml 中任务状态从 in_progress 转为 completed 前

## 抽检策略

不是全量验证，而是按策略抽检：

| 复杂度 | 抽检比例 | 触发条件 |
|--------|---------|---------|
| Simple | 0% | 不抽检 |
| Medium | 50% | 变更文件 ≥3 个时必须抽检 |
| Complex | 100% | 始终抽检 |

## Procedure

### Step 1: 判断是否需要抽检

```
complexity = Simple → 跳过
complexity = Medium AND 修改文件 <3 → 可选抽检
complexity = Medium AND 修改文件 ≥3 → 必须抽检
complexity = Complex → 必须抽检
```

### Step 2: 派发 Verifier 子 Agent

```
Agent({
    description: "verifier-{n}: 抽检任务{id}摘要",
    prompt: "你是摘要验证者 Agent。\n\n## 验证目标\n验证 Task {id} 的摘要是否准确反映实际变更。\n\n## 验证材料\n1. 摘要: .agent-flow/artifacts/task-{id}-summary.md\n2. 文件列表: .agent-flow/artifacts/task-{id}-files.txt\n3. 任务包: .agent-flow/artifacts/task-{id}-packet.md\n\n## 验证检查项\n1. 【文件一致性】摘要中的 Files Modified 列表是否与 files.txt 一致\n2. 【变更准确性】摘要中的 Changes 是否与实际代码变更匹配\n3. 【测试结果】摘要中的 Test Results 是否与实际测试输出匹配\n4. 【遗漏检测】是否有重要变更未被摘要覆盖\n5. 【格式合规】摘要是否遵守了摘要模板格式\n\n## 验证方法\n- 读取 files.txt 中列出的每个文件，检查关键变更\n- 对比摘要声称的变更与实际文件内容\n- 检查测试命令的实际输出（如有）\n\n## 输出格式\n写验证结果到: .agent-flow/artifacts/task-{id}-verification.md\n\n验证结果格式:\n# Task {id} Verification\n## Verdict: {PASS|FAIL|PARTIAL}\n## Checks\n- 文件一致性: {PASS|FAIL} — {说明}\n- 变更准确性: {PASS|FAIL} — {说明}\n- 测试结果: {PASS|FAIL|N/A} — {说明}\n- 遗漏检测: {PASS|FAIL} — {说明}\n- 格式合规: {PASS|FAIL} — {说明}\n## Issues\n- {问题描述，如有}\n## Recommended Actions\n- {修复建议，如有}",
    subagent_type: "general-purpose"
})
```

### Step 3: 处理验证结果

主 Agent 读取 `.agent-flow/artifacts/task-{id}-verification.md`：

| Verdict | 动作 |
|---------|------|
| **PASS** | 确认任务完成，更新 flow-context.yaml |
| **PARTIAL** | 补充摘要缺失项，重新更新 summary 文件 |
| **FAIL** | 重新派发 executor 子 Agent 修复问题，或由主 Agent 直接修复摘要 |

### Step 4: 更新流程状态

验证完成后更新 flow-context.yaml：
- 添加 `verified: true/false` 到对应任务
- 如果 FAIL，将任务状态改为 `needs_fix` 而非 `completed`

## 验证结果文件格式

```markdown
# Task {id} Verification

## Verdict: {PASS|FAIL|PARTIAL}

## Checks
- 文件一致性: {PASS|FAIL} — {说明}
- 变更准确性: {PASS|FAIL} — {说明}
- 测试结果: {PASS|FAIL|N/A} — {说明}
- 遗漏检测: {PASS|FAIL} — {说明}
- 格式合规: {PASS|FAIL} — {说明}

## Issues
- {问题描述，如有}

## Recommended Actions
- {修复建议，如有}
```

## 与主 Agent 派发协议的集成

在 main-agent-dispatch Skill 的 Step 6（验证摘要准确性）中，本 Skill 定义了具体的验证流程和 Verifier prompt 模板。

## Rules

1. **Verifier 独立性**: Verifier Agent 必须独立于 executor Agent，不能共享 Memory
2. **不修改代码**: Verifier 只验证摘要，不修改任何代码文件
3. **FAIL 必须处理**: 验证 FAIL 的摘要不能直接忽略，必须修复或重新生成
4. **验证结果持久化**: verification.md 文件必须写入 artifacts 目录，供后续审计
5. **抽检比例遵守**: 不因赶时间而跳过必要抽检

## 变更历史

- v1.0.0 (2026-04-15): 初始版本，Verifier 抽检验证摘要准确性
