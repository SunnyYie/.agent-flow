---
title: "跳过Verifier验收的严重后果"
category: pitfall
module: workflow
agents: [main, verifier]
tags: [dual-acceptance, verifier, quality-gate]
confidence: 0.95
sources: [S1.3, S1.5]
created: 2026-04-11
updated: 2026-04-12
status: verified
---

# 跳过Verifier验收的严重后果

> 跳过Verifier Agent验收，违反双验收铁律，导致遗漏问题未被发现

## 问题描述

因性能问题而跳过Verifier Agent验收而非优化启停策略，结果：
- `.gitignore` 文件丢失未被及时发现
- 缓存目录未加入 gitignore
- 文件存在性验证被Main Agent自检遗漏

同时，Verifier Agent在补充验收时确实发现了这些遗漏，证明了双验收机制的必要性。

## 解决方案

1. **按需启停Agent**：执行时开Executor关Verifier，验证时开Verifier关Executor，而非跳过验证
2. **绝不能因性能问题跳过验收**：性能问题应通过优化启停策略解决，而非牺牲质量
3. **Verifier的价值在于独立视角**：Main Agent自检容易遗漏自身盲点

## 相关页面

- [[dual-acceptance|双验收机制]]
- [[three-agent-model|三Agent协作模型]]
- [[security-module-verification|安全模块对抗性验证]]
