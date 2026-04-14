---
title: ".venv路径解析错误"
category: pitfall
module: environment
agents: [main, executor]
tags: [environment, venv, path-resolution]
confidence: 0.95
sources: [S1.4, S2.2]
created: 2026-04-11
updated: 2026-04-12
status: verified
---

# .venv路径解析错误

> .venv在项目根目录而非子目录下，Executor Agent因路径错误导致命令找不到

## 问题描述

`.venv`虚拟环境在项目根目录`{project_root}/.venv/`，不在子目录下。Executor Agent因路径错误导致`pytest`/`ruff`命令找不到。

**错误模式**：
```bash
# 在子目录下执行会报 command not found
.venv/bin/pytest
```

**正确做法**：
```bash
# 必须使用完整路径
{project_root}/.venv/bin/pytest

# 或在项目根目录下执行
cd {project_root} && .venv/bin/pytest
```

## 解决方案

1. Agent.md项目环境段落必须使用绝对路径
2. 所有Skills文件中的命令路径需要同步
3. 在Executor/Verifier prompt模板中明确标注`.venv`位置

## 相关页面

- [[three-agent-model|三Agent协作模型]]
