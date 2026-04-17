---
title: "三Agent协作模型"
category: pattern
module: workflow
agents: [main, executor, verifier]
tags: [architecture, agent-model, supervision, dual-acceptance, parallel-execution, lifecycle]
confidence: 0.95
sources: [S1.1, S1.3, S1.5, S6.1]
created: 2026-04-11
updated: 2026-04-14
status: verified
---

# 三Agent协作模型

> Main Agent（监督验收）+ Executor Agent（代码实现）+ Verifier Agent（质量验证）

## 角色定义

| 角色 | 职责 | SOUL.md路径 |
|------|------|-------------|
| **Main Agent** | 全局控制、验收、阶段总结、Agent启停、状态追踪 | `.dev-workflow/main/SOUL.md` |
| **Executor Agent** | 按规范写代码、写测试、创建文件 | `.dev-workflow/executor/SOUL.md` |
| **Verifier Agent** | 运行测试、检查代码质量、对照验收标准逐条验证 | `.dev-workflow/verifier/SOUL.md` |

**运行时架构**：Main Agent就是当前上下文的Claude自身。Executor和Verifier是通过Agent工具创建的子Agent，按需启停。

## 双验收机制

每个子任务必须由 Verifier Agent + Main Agent 同时验收，两者都 PASS 才能继续：

| Verifier | Main | 动作 |
|----------|------|------|
| PASS | PASS | 标记 COMPLETED，进入下一子任务 |
| FAIL | any | 修复后重新双验收 |
| PASS | FAIL | 记录 Main 发现的问题，修复后重新双验收 |

**验证分级**：
- 非安全模块：轻量验收（Verifier报告 + spot check）
- 安全模块：完整验收（逐条验证 + 对抗性输入）

**绝对禁止跳过 Verifier Agent**。

## Agent 生命周期管理（按需启停）

Executor 和 Verifier 互斥运行，绝不同时存在：

| 阶段 | 启动的Agent | 关闭的Agent |
|------|------------|-------------|
| 子任务执行 | Executor Agent | Verifier Agent |
| 子任务验收 | Verifier Agent | Executor Agent |
| 阶段总结 | Main Agent only | 两个子Agent都关闭 |

### 运行规则
1. **用完即关**：Agent完成工作后立即关闭，不保持空闲
2. **互斥运行**：Executor 和 Verifier 绝不同时运行
3. **阶段结束必清理**：每个阶段完成后检查并删除所有残留子Agent

### 阶段清理检查
```
[PHASE-CLEANUP] Phase {n}
- Executor Agent: CLOSED / STILL RUNNING → (如运行中则删除)
- Verifier Agent: CLOSED / STILL RUNNING → (如运行中则删除)
- 所有子Agent已清理: YES / NO
```

## 并行执行模式

多个 Executor Agent 同时启动，互不依赖互不冲突，有效提升效率。

**成功条件**：
1. 每个Agent的文件互不冲突（各自在不同目录下）
2. 每个Agent独立运行测试确认自己的测试通过
3. 全量测试在所有Agent完成后运行一次确认无冲突

**注意事项**：
1. 并行Agent产出文件可能有lint问题（行过长/未用import），需在所有Agent完成后由Main Agent统一修复
2. 并行Executor修改同一文件时需特别注意

**应用方式**：
1. 阶段规划时分析依赖图：同一组内无依赖的子任务可并行执行
2. 一条消息启动多个Agent：使用多个Agent工具调用，每个任务一个Executor
3. 合并小任务：预估<100行的子任务合并到同组任务一起执行

## 常见违规：跳过 Verifier

因性能问题跳过 Verifier Agent 验收，违反双验收铁律，导致遗漏问题未被发现：

- `.gitignore` 文件丢失未被及时发现
- 缓存目录未加入 gitignore
- 文件存在性验证被 Main Agent 自检遗漏

**正确做法**：按需启停 Agent — 执行时开 Executor 关 Verifier，验证时开 Verifier 关 Executor。绝不能因性能问题跳过验收，性能问题应通过优化启停策略解决，而非牺牲质量。Verifier 的价值在于独立视角，Main Agent 自检容易遗漏自身盲点。

## 相关页面

- [[execute-without-search|不查就执行陷阱]]
