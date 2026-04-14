---
title: "高级工具用法：PTC / Dynamic Filtering / Tool Search"
category: concept
module: workflow
agents: [main, architect, coder]
scope: global
tags: [ptc, dynamic-filtering, tool-search, optimization, token-reduction]
confidence: 0.8
sources: [shanraisshan/claude-code-best-practice]
status: draft
created: 2026-04-14
updated: 2026-04-14
---

# 高级工具用法：PTC / Dynamic Filtering / Tool Search

> 三种减少 token 消耗、提升工具调用精度的 API 级特性。

## 问题描述

标准工具调用模式有两个问题：
1. 每次工具调用的完整输出都进入上下文，消耗大量 token
2. 大量工具定义占据系统提示，降低有效指令的信号比
3. Web Search/Fetch 返回大量无关结果，需要手动过滤

## 1. Programmatic Tool Calling (PTC)

### 原理

Claude 编写 Python 代码在沙箱中编排工具调用。只有最终的 stdout 进入上下文，中间过程不消耗 token。

### 效果

- **~37% token 减少**（相比标准工具调用链）
- 适合需要多步工具调用的复杂操作

### 使用方式

在工具定义中添加：
```json
{
  "allowed_callers": ["code_execution_20250825"]
}
```

### 示例场景

```python
# Claude 写的 PTC 代码（沙箱中执行）
results = []
for file in target_files:
    content = read_file(file)        # 工具调用，输出不进上下文
    analysis = analyze(content)      # 内部处理
    results.append(analysis)
print(json.dumps(results))           # 只有这行输出进入上下文
```

## 2. Dynamic Filtering for Web Search/Fetch

### 原理

Claude 在 Web Search/Fetch 结果进入上下文前，先写过滤代码，只保留相关信息。

### 效果

- **~24% 输入 token 减少**
- **+13-16pp 改善**（BrowseComp 基准测试）

### 工作流

```
Web Search/Fetch 返回原始结果
    ↓
Claude 写过滤代码（在沙箱中执行）
    ↓
过滤后的精简结果进入上下文
```

### 适用场景

- 搜索结果只需其中几条
- 网页内容只需特定段落
- API 返回大量 JSON 只需部分字段

## 3. Tool Search (defer_loading)

### 原理

对不常用的工具设置 `defer_loading: true`，工具定义不预先加载。当需要时，Claude 通过 Tool Search 工具按需查找和加载。

### 效果

- **~85% 工具定义 token 减少**
- Claude Code v2.1.7+ 自动启用为 `MCPSearch` auto 模式

### 配置

```bash
# 设置工具搜索阈值（上下文使用百分比）
export ENABLE_TOOL_SEARCH=auto:30
```

### 适用场景

- MCP 服务器有大量工具（如飞书几十个 API）
- 工具使用频率差异大
- 上下文窗口紧张

## 4. Tool Use Examples (input_examples)

### 原理

在工具 schema 中添加 `input_examples` 字段，提供正确使用的示例。

### 效果

- 复杂参数工具的准确率从 **72% → 90%**

### 使用方式

```json
{
  "input_schema": {
    "type": "object",
    "properties": { ... }
  },
  "input_examples": [
    {
      "query": "搜索最近一周的会议记录",
      "time_range": "last_7_days",
      "filters": {"organizer": "user_123"}
    }
  ]
}
```

## 实践建议

1. **MCP 工具多时必用 Tool Search** — 飞书/Atlassian 等 MCP 工具多，defer_loading 效果显著
2. **多步工具调用用 PTC** — 减少中间输出的 token 消耗
3. **Web 搜索用 Dynamic Filtering** — 过滤噪音，保留有用信息
4. **新 MCP 工具加 input_examples** — 提高首次调用准确率

## 相关页面

- [[claude-code-settings|关键设置与环境变量]]
- [[context-pollution|上下文污染]]
