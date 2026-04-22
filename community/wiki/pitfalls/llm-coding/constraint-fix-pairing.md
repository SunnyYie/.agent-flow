# constraint-fix-pairing

## 问题

每定义一个 block 级禁止性约束，如果异常兜底修复函数中没有对应修复路径，系统能检测到问题却无法自动修复，走 warn_only 分支直接放行不合规输出。

## 踩坑记录

步骤16中 `checkProhibitiveConstraints()` 定义了10种约束，但 `applyStyleFallback()` 的 prohibitive_violation 分支只处理了4种，遗漏了 ZERO_SIZE_COMPONENT 和 CONTRAST_INSUFFICIENT。双Agent验收（Verifier）发现此问题。

## 规则

**每新增一个 block 级禁止性约束，必须在异常兜底修复函数中添加对应的修复分支。两者必须成对存在。**

验证方式：
1. Code Review 时对照约束枚举和修复分支是否 1:1
2. 为每种 block 级约束编写 check → fallback → verify 三段式测试用例

## 适用范围

所有实现"检测+修复"模式的代码：样式校验、数据校验、安全检查等。

## 来源

步骤16双Agent验收（2026-04-15），confidence: 0.95
