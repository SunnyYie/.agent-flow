---
name: wiki-doc-read
type: pattern
module: feishu
status: verified
confidence: 0.85
created: 2026-04-13
last_validated: 2026-04-13
tags: [feishu, lark-cli, wiki, document]
---

# 飞书Wiki文档读取三步流程

## 问题描述
飞书 Wiki 链接（/wiki/TOKEN）的 token 是节点 token，不能直接当 file_token 使用。

## 解决方案
1. 从 URL 提取 wiki_token
2. `lark-cli wiki spaces get_node --params '{"token":"{wiki_token}"}' --as user` 获取节点信息
3. 提取 `obj_token` 和 `obj_type`
4. 根据 obj_type选择对应 API：
   - docx → `lark-cli docs +fetch --doc {obj_token} --as user --format pretty`
   - sheet → lark-sheets skill
   - bitable → lark-base skill

## 相关条目
- [[pitfalls/feishu/lark-cli-params|lark-cli参数格式陷阱]]
