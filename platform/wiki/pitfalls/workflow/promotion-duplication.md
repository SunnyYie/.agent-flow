---
name: promotion-duplication
type: pitfall
module: workflow
status: verified
confidence: 0.95
created: 2026-04-14
tags: [晋升, 去重, 经验沉淀, 知识管理]
---

# 晋升时创建重复内容而非更新已有文档

## 问题描述

REFLECT 阶段将项目经验晋升到全局知识库（`~/.agent-flow/wiki/` 和 `~/.agent-flow/skills/`）时，如果已有相似主题的文档，旧流程只会跳过或创建新文档，导致：

1. **重复文档**：同一主题出现多个文档，内容重叠但各有侧重
2. **信息碎片化**：相似经验散落在不同文档中，查找时需翻多篇
3. **维护负担**：更新时需要同步修改多个文档，容易遗漏

## 根因

`experience-promotion` v1 的去重逻辑过于简单：

- Soul.md：只检查"是否存在"，已存在则跳过或比较 confidence，不做内容合并
- Wiki：只检查"同名文件"，不同名但主题相似的文档被忽略
- Skills：只检查"同名技能"，功能相似但命名不同的技能被忽略

## 解决方案

**v2.0 三重保障**：

1. **相似性检测**（promotion-guard.py Hook）

   - 写入全局 wiki/skills 时自动拦截
   - 用关键词 Jaccard 相似度 + 标题子串匹配检测相似内容
   - 发现相似文档 → 阻断新建，提示更新已有文档

2. **多Agent验收**（promotion-verify Skill）

   - Verifier Agent 独立审查：通用性、相似性、质量
   - 验收通过才创建 `.promotion-verified` 标记
   - Hook 检测到标记才放行写入

3. **合并更新策略**（experience-promotion v2.0）

   - Soul.md：相似条目 → 合并 confidence 和内容
   - Wiki：相似文档 → Edit 合并新内容到已有文档
   - Skills：相似技能 → 合并 Procedure 步骤

## 相关条目

- [[wiki-management|Wiki知识库管理规范]]
- [[dual-acceptance|双验收机制]]
