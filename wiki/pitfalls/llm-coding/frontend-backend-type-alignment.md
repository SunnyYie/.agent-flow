---
name: frontend-backend-type-alignment
description: 前后端共享的类型枚举必须完全对齐，前端不允许简化版本
type: pitfall
category: llm-coding
confidence: 0.95
created: 2026-04-14
tags: [type-alignment, frontend, backend, enum, contract]
---

# 跨模块类型枚举不对齐

> 当两个模块共享同一类型（如状态枚举、模式枚举），消费者端不允许简化版本。简化会导致运行时类型不匹配。

## 问题描述

当服务端（或API提供方）定义了 N 种枚举值的类型时，消费者端（前端、SDK、微服务客户端）有时会"简化"为只使用 M 种（M < N），认为不需要的值前端用不到。这会导致：

1. 提供方返回消费者不支持的状态时，类型不匹配
2. 验收时被发现需要补修
3. 状态流转逻辑不一致（消费者无法表达某些流转路径）

## Why: 为什么会犯这个错

- 编码时倾向"够用就行"，未充分考虑提供方可能返回的所有状态
- 缺乏"消费者类型必须与提供方完全对齐"的强制检查点
- 类型定义分散在不同文件/仓库中，不容易直接对比
- 认为某些状态"前端不需要关心"是合理简化

## 典型表现

### 案例 1: 状态枚举不对齐
- 服务端定义 6 种附件状态：`temporary | bound | superseded | released | expired | failed`
- 前端只写了 4 种：`temporary | bound | expired | released`（缺 `superseded` 和 `failed`）
- 当服务端返回 `superseded` 状态时，前端类型系统无法处理

### 案例 2: 会话阶段不对齐
- 服务端定义细粒度阶段：`component_generating_preview | component_awaiting_apply | ...`
- 前端使用简化阶段：`submitting | result_ready`
- 前端简化阶段可正常工作但与服务端不对齐，增加后续对齐成本

## How to apply: 避免方法

1. **新增枚举类型时**：先写提供方完整版，消费者必须 1:1 复制所有值，不可简化
2. **代码审查时**：对比两端同名/同义类型的枚举值数量和内容
3. **验收时**：将"跨模块类型对齐"列为必检项
4. **考虑共享类型文件**：如果项目支持，将共享类型放在公共包中
5. **自动化检查**：编写 contract test 对比两端枚举值数量

## 严重度

HIGH — 踩坑≥2次，类型不对齐会导致运行时异常

## 相关条目
- [[execute-without-search|pitfalls/workflow/execute-without-search]]（表现4：跳过子任务搜索导致类型不对齐未提前发现）
