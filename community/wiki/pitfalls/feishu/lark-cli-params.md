---
name: lark-cli-params
type: pitfall
module: feishu
status: verified
confidence: 0.95
created: 2026-04-13
last_validated: 2026-04-13
tags: [feishu, lark-cli, params, API]
---

# lark-cli 参数格式陷阱

## 问题描述
lark-cli 的很多命令不支持 `--token` 等直接传参方式，必须使用 `--params` JSON 格式传递参数。不查看 schema 就猜测参数格式会导致命令执行失败。

## 根因
lark-cli 的 API 封装与直觉不符：
- `wiki spaces get_node` 不支持 `--token` 参数
- 必须使用 `--params '{"token":"xxx"}'` 格式

## 修复方案
1. 使用任何 lark-cli 命令前，先查看 schema：`lark-cli schema {resource}.{method}`
2. 按 schema 中的参数定义构造 `--params` JSON
3. 常见正确用法：
   ```bash
   # ❌ 错误：直接传 --token
   lark-cli wiki spaces get_node --token xxx

   # ✅ 正确：用 --params JSON 格式
   lark-cli wiki spaces get_node --params '{"token":"xxx"}' --as user
   ```

## 相关条目
- [[patterns/feishu/wiki-doc-read|飞书Wiki文档读取三步流程]]
