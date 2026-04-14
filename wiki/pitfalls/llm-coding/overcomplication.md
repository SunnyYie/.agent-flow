---
name: overcomplication
type: pitfall
module: llm-coding
status: verified
confidence: 0.9
created: 2026-04-13
source: https://github.com/forrestchang/andrej-karpathy-skills
tags: [over-engineering, strategy-pattern, abstraction, karpathy]
---

# LLM 代码过度复杂化陷阱

## 问题描述

LLM 倾向于为简单需求创建过度复杂的实现。这不是明显的错误——过度设计的代码往往遵循设计模式和最佳实践——问题在于**时机**：在需要之前添加复杂性。

## 典型表现

1. **为单次使用创建抽象**：Strategy 模式、Factory 模式、Config dataclass——只为一个折扣计算
2. **添加未请求的功能**：缓存系统、验证器、合并逻辑、通知系统——没人要求
3. **处理不可能的场景**：内部函数加了永远不会触发的错误处理
4. **投机性灵活性**：可配置的、可插拔的、可扩展的——但没有实际需求

## 为什么危险

- 更难理解（认知负荷增加）
- 引入更多 bug（代码越多 bug 越多）
- 耗时更长（实现+测试+审查）
- 更难测试（需要为不需要的功能写测试）
- **死代码的真正成本不在写它的时候，而在读它、维护它、重构它的时候**

## 检测方法

- **行数对比**：如果 50 行能搞定但你写了 200 行，需要简化
- **类数对比**：如果 1 个函数能搞定但你创建了 5 个类，需要简化
- **自检**："一个资深工程师会觉得这段代码过度设计了吗？"

## 正确做法

1. 先用最简单的实现解决问题
2. 当**真正的需求出现**时再增加复杂度
3. 复杂度应该是被需求拉动的，不是被预测推动的
4. "好代码是简单解决今天问题的代码，而非过早解决明天问题的代码"

## 相关条目
- [[karpathy-principles|concepts/karpathy-principles]]
- [[simplicity-first|patterns/llm-coding/simplicity-first]]
