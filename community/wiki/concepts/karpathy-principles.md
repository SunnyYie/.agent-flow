---
name: karpathy-principles
type: concept
module: llm-coding
status: verified
confidence: 0.9
created: 2026-04-13
source: https://github.com/forrestchang/andrej-karpathy-skills
tags: [karpathy, llm-coding, best-practices, simplicity, surgical-changes, goal-driven, think-before-coding]
---

# Karpathy LLM Coding Principles

> Andrej Karpathy 识别的 LLM 编程三大核心问题，以及对应四条原则。

## 三大核心问题

1. **隐式假设问题**：模型自行做出错误假设并顺水推舟，不管理困惑、不寻求澄清、不暴露不一致、不展示权衡。
2. **过度工程问题**：模型喜欢过度复杂化代码和 API，膨胀抽象，不清理死代码……用 1000 行实现本该 100 行完成的功能。
3. **副作用修改问题**：模型有时会修改/删除它不充分理解的注释和代码，即使这些内容与任务正交。

## 原则 1: Think Before Coding（先想后写）

**座右铭**：不假设、不隐藏困惑、展示权衡。

### 具体做法
1. **明确陈述假设** — 不确定就问
2. **多种理解全部呈现** — 不静默选择一种理解
3. **有更简单方案就说出来** — 该反驳就反驳
4. **不清楚就停下** — 命名困惑，请求澄清

### 场景示例
- 需求："添加用户数据导出功能"
  - 错误：静默假设导出全部用户、CSV 格式、同步下载，直接写 15 行代码
  - 正确：列出假设 — 范围（全部 vs 筛选）？格式（下载 vs API）？哪些字段（有敏感字段）？体量（需后台任务吗）？然后提议最简方案
- 需求："让搜索更快"
  - 错误：直接加缓存、数据库索引、异步处理
  - 正确：呈现三种理解 — (1) 响应时间更快 (2) 并发量更大 (3) 感知速度更快 UX，附各方案工作量估算

### 自检
> "Am I making assumptions the user didn't state?" If yes, surface them.

## 原则 2: Simplicity First（简洁优先）

**座右铭**：用解决问题的最少代码，不做投机性设计。

### 具体做法
1. **只实现被要求的功能** — 不加额外特性
2. **单次使用不建抽象** — 一个函数足够，不需要 Strategy/Factory/Config 体系
3. **不加未请求的灵活性** — 没人要求可配置，就硬编码
4. **不处理不可能的场景** — 内部代码信任框架保证，只在系统边界验证
5. **200 行能 50 行搞定就重写** — 复杂度是负债，不是资产

### 代码对比
- 过度设计：为折扣计算创建 Strategy 模式（30+ 行 ABC + Config + Calculator）
- 简洁优先：`def calculate_discount(amount, percent): return amount * percent / 100`

### 自检
> "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 何时可以增加复杂度
当复杂度是**真正需要**的时候：需求明确要求多种策略、性能测试证明需要缓存、用户实际报告了边界情况。

## 原则 3: Surgical Changes（精准修改）

**座右铭**：只改必须改的，只清理自己的残留。

### 修改现有代码时
1. **不"顺便改善"相邻代码** — 除非被要求
2. **不重构没坏的东西** — 即使觉得能写更好
3. **匹配现有风格** — 即使你会用不同方式
4. **注意到无关死代码时提及但不删除** — 报告，不行动

### 自己的修改产生残留时
1. **删除自己的修改使未用的 import/变量/函数** — 清理自己的残留
2. **不删除之前就存在的死代码** — 除非被要求

### 自检
> 每一行变更都应该能追溯到用户的请求。

### 场景示例
- 需求："修复空邮箱导致验证器崩溃的 bug"
  - 错误：同时"改善"邮箱验证、加用户名验证、改注释、加 docstring，diff 涉及 10+ 行
  - 正确：只改修复空邮箱处理的那 2-3 行

## 原则 4: Goal-Driven Execution（目标驱动执行）

**座右铭**：定义可验证的成功标准，循环直到验证通过。

### 将模糊任务转化为可验证目标

| 模糊目标 | 可验证目标 |
|---------|-----------|
| "添加验证" | "为无效输入写测试，然后让它们通过" |
| "修复 bug" | "写一个复现 bug 的测试，然后让它通过" |
| "重构 X" | "确保重构前后测试都通过" |

### 多步骤任务的验证计划
```
1. [步骤] -> verify: [检查]
2. [步骤] -> verify: [检查]
3. [步骤] -> verify: [检查]
```

### 增量实现策略
以 API 限流为例：
1. 基本内存限流（单端点）→ verify: 测试通过 + 手动 curl
2. 提取为中间件（所有端点）→ verify: 现有测试仍通过
3. Redis 后端（多服务器）→ verify: 重启后限流保持
4. 按端点配置 → verify: 各端点限流独立工作

### 关键原则
- **强标准可独立循环** — "写测试 X，让它通过"可以独立完成
- **弱标准需反复澄清** — "让它工作"无法判断完成

## 核心洞察

过度复杂的代码并非明显错误——它们遵循设计模式和最佳实践。问题在于**时机**：在需要之前添加复杂性，使代码更难理解、引入更多 bug、耗时更长、更难测试。**好代码是简单解决今天问题的代码，而非过早解决明天问题的代码。**

## 与 AgentFlow 协议的关系

| Karpathy 原则 | AgentFlow 对应 |
|--------------|---------------|
| Think Before Coding | THINK 阶段 + 铁律3（边界澄清） |
| Simplicity First | EXECUTE 阶段核心原则 |
| Surgical Changes | EXECUTE 阶段"不扩范围"原则 |
| Goal-Driven Execution | PLAN 阶段验收检查点 + VERIFY 阶段 |

## 反模式速查

| 原则 | 反模式 | 正确做法 |
|------|--------|---------|
| Think Before Coding | 静默假设文件格式、字段、范围 | 列出假设，请求澄清 |
| Simplicity First | 单一折扣计算用 Strategy 模式 | 一个函数直到复杂度真正需要 |
| Surgical Changes | 修 bug 时顺手改引号、加类型标注 | 只改修复问题相关的行 |
| Goal-Driven | "我来审查和改善代码" | "写测试复现 bug → 让它通过 → 验证无回归" |

## 相关条目
- [[overcomplication|pitfalls/llm-coding/overcomplication]]
- [[drive-by-refactoring|pitfalls/llm-coding/drive-by-refactoring]]
