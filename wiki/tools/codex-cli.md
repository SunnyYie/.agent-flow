---
name: codex-cli
type: tool
module: tools
status: verified
confidence: 0.8
created: 2026-04-13
last_validated: 2026-04-13
tags: [codex, cli, openai, coding-agent]
---

# Codex CLI 配置参考

## 基本信息

- **安装位置**: `/opt/homebrew/bin/codex`
- **当前版本**: codex-cli 0.116.0
- **配置目录**: `~/.codex/`
- **配置文件**: `~/.codex/config.toml`
- **认证文件**: `~/.codex/auth.json`

## 关键配置文件

### auth.json（认证）

| 字段 | 说明 |
|------|------|
| `auth_mode` | `"apikey"` 或 `"chatgpt"` |
| `OPENAI_API_KEY` | API key 模式下的密钥 |
| `tokens` | ChatGPT 模式下的 OAuth tokens |

### config.toml（运行配置）

| 字段 | 说明 | 示例 |
|------|------|------|
| `model` | 默认模型 | `"gpt-5.3-codex"`, `"o3"` |
| `model_provider` | 模型提供商 | `"openai"`, `"azure"` |
| `preferred_auth_method` | 认证方式 | `"chatgpt"`, `"apikey"` |
| `model_reasoning_effort` | 推理力度 | `"low"`, `"medium"`, `"high"` |

## 内置 Provider

`openai` 是内置 provider，**不能**在 `[model_providers]` 中覆盖。自定义 provider 需用其他名称（如 `openai-custom`、`azure`）。

## 常用命令

```bash
codex login              # 交互式登录
codex login --with-api-key  # 管道传入 API key
codex login status       # 查看登录状态
codex logout             # 登出
codex -c model="o3"      # 临时覆盖配置
codex -m o3              # 临时切换模型
```

## 注意事项

- `codex login` 只更新 auth.json，不修改 config.toml
- 切换账号后必须手动同步 config.toml 中的 provider 和 auth_method
- Azure 代理需要自定义 `[model_providers.azure]` 段和 `base_url`

## 相关条目

- [[codex-provider-auth-mismatch|登录后配置不匹配踩坑]]
