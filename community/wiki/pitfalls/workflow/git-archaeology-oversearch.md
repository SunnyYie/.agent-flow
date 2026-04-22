---
name: git-archaeology-oversearch
type: pitfall
module: workflow
status: verified
confidence: 0.95
created: 2026-04-14
tags: [git, oversearch, development-flow, react-native]
---

# Git考古过度搜索陷阱

## 问题描述
在搜索到相关代码后，不去切分支开发，而是反复执行 git log、git show、git diff 去"考古"其他分支或历史提交，浪费时间而不推进实际开发。

## 典型表现
1. 搜索到代码相关位置后，不去创建分支开始开发，而是用 git log/show/diff 翻历史
2. 搜索不到某个字段时，不去判定为新增字段并开发，而是去其他分支验证"是否已实现"
3. 读取了飞书需求文档和已有代码后，仍然不断用 git 命令确认而不是开始工作

## 根因
1. 对"搜索不到 = 新增"的判断缺乏信心，需要反复确认
2. 好奇心驱动：想了解"别人怎么做的"而非"我该做什么"
3. 忘记了 git workflow 规则：搜索完 → 更新主分支 → 创建新分支 → 开始开发

## 正确做法
1. 搜索到相关代码位置 → 立即 `git pull --rebase` → `git checkout -b feat/xxx` → 开始开发
2. 搜索不到字段 → 判定为新增字段 → 直接开发，不需要去其他分支验证
3. 有疑问时直接问用户，不要用 git 命令自行考古

## 相关条目
- [[skip-search-before-execute|跳过搜索直接执行陷阱]]（反面：这个是搜索过度）
- [[execute-without-search|不查就执行陷阱]]
