---
name: drive-by-refactoring
type: pitfall
module: llm-coding
status: verified
confidence: 0.9
created: 2026-04-13
source: https://github.com/forrestchang/andrej-karpathy-skills
tags: [refactoring, style-drift, diff-noise, karpathy]
---

# 顺带重构陷阱

## 问题描述

LLM 在修改代码时，常常"顺便"做与任务无关的修改：改引用风格、加类型标注、加 docstring、重格式化、重构相邻代码。这些修改增加 diff 噪音，可能引入意外破坏，且让 code review 更困难。

## 典型表现

1. **修 bug 时顺便改善验证**：用户只要求修空邮箱崩溃，结果同时改善了用户名验证
2. **加功能时顺便改风格**：用户要求加日志，结果同时把单引号改双引号、加类型标注
3. **重构时顺便删死代码**：用户要求重构 A 模块，结果同时删除了 B 模块的"死代码"（实际在用）
4. **修复时顺便加 docstring**：用户要求修一个 bug，结果同时给整个文件加了文档

## 为什么危险

- **diff 噪音**：reviewer 需要检查更多行，容易遗漏真正的变更
- **意外破坏**：风格修改可能改变行为（如布尔表达式重写）
- **责任模糊**：如果"顺便"的修改引入 bug，是谁的责任？
- **版本控制噪音**：git blame 追踪到不相关的提交
- **冲突放大**：无关修改增加了合并冲突的可能性

## 正确做法

1. **每一行变更都追溯到用户请求**
2. **匹配现有风格** — 即使你会用不同方式
3. **注意到问题时提及但不行动** — "我注意到这里有些死代码，是否需要清理？"
4. **只清理自己创建的残留** — 自己的修改使某些 import 未用，才删除
5. **不删除之前就存在的死代码** — 除非用户明确要求

## 相关条目
- [[karpathy-principles|concepts/karpathy-principles]]
- [[surgical-changes|patterns/llm-coding/surgical-changes]]
