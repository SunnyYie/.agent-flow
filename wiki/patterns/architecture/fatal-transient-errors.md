---
title: "FATAL/TRANSIENT错误分类与容错模式"
category: pattern
module: architecture
agents: [main, executor]
tags: [error-handling, fault-tolerance, retry-strategy]
confidence: 0.95
sources: [S3.3]
created: 2026-04-12
updated: 2026-04-12
status: verified
---

# FATAL/TRANSIENT错误分类与容错模式

> 错误分类驱动重试策略：FATAL永不重试，TRANSIENT指数退避重试

## 模式描述

### 错误分类

| 类型 | 特征 | 处理方式 | 示例 |
|------|------|----------|------|
| **FATAL** | 认证/权限/余额耗尽 | 永不重试，直接升级 | 401, 403, API key无效 |
| **TRANSIENT** | 超时/限流/临时故障 | 指数退避重试 | 429, 503, 超时, 网络抖动 |

### 现有问题

现有重试策略往往未区分错误类型——如果遇到API限流(429)立即重试会加重问题。

### 增强方案

```
错误分类 → FATAL直接升级 → TRANSIENT指数退避重试
```

指数退避参数：
- 初始延迟：1秒
- 最大延迟：60秒
- 最大重试：3次
- 抖动：±20%避免惊群

## 应用方式

1. 所有错误处理先分类为FATAL/TRANSIENT
2. FATAL错误：记录日志 + 通知用户 + 停止当前操作
3. TRANSIENT错误：指数退避重试 + 超过阈值后升级
4. 在Executor Agent中实现为通用retry装饰器

## 相关页面

- [[three-agent-model|三Agent协作模型]]
