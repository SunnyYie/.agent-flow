---
title: "Path.resolve vs PurePosixPath：路径遍历绕过漏洞"
category: pitfall
module: security
agents: [main, executor, verifier]
tags: [security, path-traversal, PurePosixPath, adversarial-input, adversarial-testing]
confidence: 0.95
sources: [S6.1]
created: 2026-04-11
updated: 2026-04-14
status: verified
---

# Path.resolve vs PurePosixPath：路径遍历绕过漏洞

> PurePosixPath 不解析 `..` 路径段，导致路径遍历攻击可绕过安全检查。仅验证正常功能路径不足以发现安全漏洞，安全模块验收必须包含对抗性输入测试。

## 漏洞描述

Worktree 边界检查使用 `PurePosixPath` 的 `startswith` 比较，导致 `/worktree/../etc/passwd` 可绕过检查。`PurePosixPath` 仅做字符串操作，不会规范化 `..` 路径段。

安全模块首次验收时，正常路径测试全通过，但 Verifier Agent 主动测试路径遍历（`/worktree/../etc/passwd`）才发现 `PurePosixPath` 不解析 `..` 的漏洞。

## 漏洞代码 vs 安全代码

```python
# 危险！PurePosixPath 不解析 ..
if PurePosixPath(user_path).is_relative_to(worktree_root):
    ...

# 正确！Path.resolve() 先规范化再比较
if Path(user_path).resolve().is_relative_to(worktree_root):
    ...
```

## 解决方案

### 路径安全三原则
1. **文件路径比较必须使用 `Path.resolve()` 规范化后再比较**
2. **安全相关代码必须考虑对抗性输入**（路径遍历、大小写绕过、空输入等）
3. **纯字符串路径操作在安全场景中不可信**

### 安全模块验收检查清单
1. 路径遍历：`../`, `..\\`, URL编码绕过
2. 大小写绕过：混合大小写路径
3. 空输入：None、空字符串
4. 超长输入：缓冲区溢出测试
5. 注入攻击：命令注入、SQL注入

### 验证策略
- 非安全模块：轻量验收（Verifier报告 + spot check）
- 安全模块：完整验收（逐条验证 + 对抗性输入）

**核心教训**：仅验证正常功能路径不足以发现安全漏洞。

## 相关页面
- [[three-agent-model|三Agent协作模型]]
- [[skipping-verifier|跳过Verifier验收的后果]]
