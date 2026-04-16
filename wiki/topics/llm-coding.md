---
title: "主题：LLM Coding LLM编程"
category: topic-hub
module: llm-coding
agents: [main, coder, verifier]
scope: global
tags: [llm-coding, topic-hub]
confidence: 1.0
status: verified
created: 2026-04-15
updated: 2026-04-15
---

# 主题：LLM Coding LLM编程

> LLM编程原则、踩坑、质量退化相关的全部知识。源自 Karpathy 四原则，覆盖从上下文管理到代码质量的完整链路。

## Patterns（成功模式）

_(无 LLM 编程专属模式，相关模式见 workflow 主题)_

## Pitfalls（踩坑记录）

- [[overcomplication|pitfalls/llm-coding/overcomplication]] — 代码过度复杂化陷阱（策略模式滥用、过度抽象）
- [[drive-by-refactoring|pitfalls/llm-coding/drive-by-refactoring]] — 顺带重构陷阱（风格漂移、diff噪音）
- [[context-pollution|pitfalls/llm-coding/context-pollution]] — 上下文污染：长会话质量退化
- [[frontend-backend-type-alignment|pitfalls/llm-coding/frontend-backend-type-alignment]] — 跨模块类型枚举不对齐（前端简化导致运行时异常）
- [[constraint-fix-pairing|pitfalls/llm-coding/constraint-fix-pairing]] — 约束-修复配对缺失（定义禁止性约束但缺兜底修复）
- [[shared-constants-dedup|pitfalls/llm-coding/shared-constants-dedup]] — 共享常量去重（相同字面量多处定义导致不一致）
- [[circuit-breaker-halfopen-probe|pitfalls/llm-coding/circuit-breaker-halfopen-probe]] — 熔断器半开探测缺失（halfOpenProbeCount 未消费）
- [[rollback-honest-marking|pitfalls/llm-coding/rollback-honest-marking]] — 回滚诚实标记（自动执行标记completed，需外部执行标pending）

## Concepts（相关概念）

- [[karpathy-principles|concepts/karpathy-principles]] — Karpathy LLM编程四原则（Think/Simplicity/Surgical/Goal-Driven + 反模式速查）
- [[llm-degradation|concepts/llm-degradation]] — LLM 输出质量退化9层因素与上下文污染修复

## Related Topics（关联主题）

- [[workflow|topics/workflow]] — 工作流质量直接影响 LLM 编码质量
- [[react-native|topics/react-native]] — React Native 中的类型对齐问题是跨模块协作的典型场景
