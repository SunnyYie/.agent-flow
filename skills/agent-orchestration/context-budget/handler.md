---
name: context-budget
version: 1.0.0
trigger: 上下文预算, context budget, 预算追踪, context overflow
confidence: 1.0
abstraction: universal
created: 2026-04-15
---

# Skill: 上下文预算追踪

> **量化上下文消耗**：通过启发式方法追踪主 Agent 的上下文使用量，在预算不足时触发派发或压缩。

## Trigger

- 每次读取文件后（PostToolUse Read/Bash/Grep/Glob）
- 每次 flow-context.yaml 更新时
- 主 Agent 需要决策是否派发子 Agent 时

## 估算方法

Claude Code 不暴露 token 计数，使用启发式方法：

### 方法 1: 文件大小追踪（PostToolUse Hook 自动执行）

```python
# 每次读取文件时，累加文件大小到预算追踪器
# 估算公式: tokens ≈ file_size_bytes / 4 (英文) / 2 (中文)
def estimate_tokens(file_path: str) -> int:
    size = os.path.getsize(file_path)
    # 保守估算：假设混合内容，1 byte ≈ 0.3 token
    return int(size * 0.3)
```

### 方法 2: 对话轮次估算

```
估算 tokens ≈ 对话轮次数 × 2000 (平均每轮)
```

### 方法 3: 流程状态文件追踪

在 `.agent-flow/state/flow-context.yaml` 中维护预算：

```yaml
context_budget:
  used: 45000      # 估算已用 tokens
  max: 200000      # 上下文窗口上限
  status: "healthy" # healthy|warning|critical
  files_read: 12   # 已读取文件数
  last_update: "2026-04-15T10:00:00"
```

## 预算阈值与行为

| 状态 | 使用率 | 行为 |
|------|--------|------|
| **healthy** | <50% | 正常工作，Simple 任务可直接执行 |
| **warning** | 50-70% | 优先派发子 Agent；避免读取大文件；主动压缩已有摘要 |
| **critical** | >70% | 强制派发所有剩余工作；主 Agent 只做状态管理；禁止读取 L3 结果 |

## Procedure

### Step 1: 初始化预算追踪

任务开始时，在 flow-context.yaml 中设置初始预算：

```yaml
context_budget:
  used: 0
  max: 200000
  status: "healthy"
  files_read: 0
  last_update: "{ISO8601}"
```

### Step 2: 自动更新（PostToolUse Hook）

context-budget-tracker.py hook 在每次文件读取后自动：
1. 估算读取文件的 token 数
2. 累加到 `context_budget.used`
3. 根据 used/max 比例更新 status
4. 写回 flow-context.yaml

### Step 3: 手动更新（主 Agent 决策时）

主 Agent 在以下场景主动更新预算：
- 派发子 Agent 前后
- 读取 L2 摘要后
- 完成任务阶段后

```python
# 更新预算的伪代码
def update_budget(estimated_new_tokens: int):
    context = read_flow_context()
    budget = context["context_budget"]
    budget["used"] += estimated_new_tokens

    ratio = budget["used"] / budget["max"]
    if ratio < 0.5:
        budget["status"] = "healthy"
    elif ratio < 0.7:
        budget["status"] = "warning"
    else:
        budget["status"] = "critical"

    write_flow_context(context)
```

### Step 4: 预算不足时的压缩策略

当 status = warning 或 critical 时：

1. **摘要淘汰**: flow-context.yaml 中的 L1 摘要只保留最近 5 条，更早的只保留 artifact 路径
2. **避免读取大文件**: 优先读取 summary 文件而非 result 文件
3. **强制派发**: 将剩余任务全部派发给子 Agent
4. **状态最小化**: 只保留当前阶段和待处理任务列表

### Step 5: 预算重置

每个新阶段（PLAN→EXECUTE→VERIFY→REFLECT）开始时：
- 保留阶段标识和任务状态
- 重置 `used` 为当前 flow-context.yaml 大小的估算值
- 这是因为 Claude Code 的上下文压缩会自动清理旧内容

## Rules

1. **保守估算**: 低估比高估更危险，宁可多算 30%
2. **不依赖精确值**: 这是启发式方法，目的是防止溢出而非精确计量
3. **hook 自动执行**: 预算追踪由 PostToolUse hook 自动完成，主 Agent 无需手动操作
4. **warning 时主动行动**: 不要等到 critical 才压缩，warning 时就应开始淘汰
5. **新阶段重置**: 每个阶段开始时重置预算，因为上下文压缩会释放空间

## 变更历史

- v1.0.0 (2026-04-15): 初始版本，启发式上下文预算追踪
