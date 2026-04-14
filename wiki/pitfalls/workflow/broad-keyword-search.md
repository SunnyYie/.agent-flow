---
name: broad-keyword-search
type: pitfall
module: requirements
status: verified
confidence: 0.9
created: 2026-04-13
tags: [需求分析, 代码搜索, 关键词, 精准定位]
---

# 需求分析时用泛化关键词搜索导致范围扩大

## 问题描述

分析需求文档时，用泛化关键词（如"AI评论"）搜索代码，匹配到多个不相关功能，导致分析范围扩大、修改位置不精准。

## 根因

需求文档通常包含业务领域关键词（如"实习圈"），而非技术实现关键词。按技术实现关键词搜索会匹配到所有相关但不属于当前业务的功能。

## 解决方案

1. 从需求文档提取**业务领域关键词**（如"实习圈"、"简历诊断"）
2. 用业务关键词精确搜索代码位置
3. 定位到具体目录/文件后再用技术关键词补充了解

**示例**：
- 错误：搜索"AI评论" → 匹配到 AICommentTag、AiCommentGuide、AICommentRelatedFeedList 等多个不相关功能
- 正确：搜索"实习圈" → 精确定位到 `gossip_detail_new/` 目录

## 相关条目
- [[search-before-execute|先查后执行模式]]
