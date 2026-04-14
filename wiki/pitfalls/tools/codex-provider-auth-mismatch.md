---
name: codex-provider-auth-mismatch
type: pitfall
module: tools
status: verified
confidence: 0.9
created: 2026-04-13
last_validated: 2026-04-13
tags: [codex, auth, config, provider]
---

# Codex CLI: 登录后 config.toml 与 auth.json 不匹配导致请求失败

## 问题描述

使用 `codex login` 切换到新账号后，`auth.json` 更新了认证信息，但 `config.toml` 仍指向旧 provider，导致请求失败。

**典型场景**：从 Azure 代理账号（apikey 认证）切换到 ChatGPT Team 账号（OAuth 认证）。

**根因**：`codex login` 只更新 `~/.codex/auth.json`，不会自动修改 `~/.codex/config.toml` 中的 `model_provider`、`preferred_auth_method` 和 `[model_providers.xxx]` 段。

## 错误表现

- 请求发往旧 provider 的 base_url，token 格式不匹配，返回 401/403
- 无明显报错但无响应（请求被旧代理丢弃）

## 解决方案

手动同步 `config.toml` 的三个关键字段：

```toml
# 切换到 OpenAI 官方
model_provider = "openai"
preferred_auth_method = "chatgpt"

# 删除 [model_providers.azure] 整段
# ⚠️ 不要添加 [model_providers.openai] 段 —— openai 是内置 provider，不能在 model_providers 中覆盖
```

**关键注意**：`openai` 是 Codex CLI 内置 provider ID，在 `[model_providers]` 中重复定义会报错：
```
Error loading config.toml: model_providers contains reserved built-in provider IDs: `openai`
```

## 切换账号的完整步骤

1. `codex logout` — 清除旧认证
2. `codex login` — 用新账号登录
3. 编辑 `~/.codex/config.toml` — 同步 provider 和 auth_method
4. 如果从自定义 provider 切回 openai，**删除** `[model_providers.xxx]` 段

## 相关条目

- [[codex-cli-config|Codex CLI 配置参考]]
