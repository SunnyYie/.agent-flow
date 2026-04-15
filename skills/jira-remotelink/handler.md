---
name: jira-remotelink
version: 1.0.0
trigger: remotelink, 远程链接, 外链, MR链接, GitLab链接, 添加链接, 关联MR
confidence: 0.95
abstraction: universal
created: 2026-04-15
---

# Skill: jira-remotelink

> Jira 远程链接管理 — 添加/查看/删除 Issue 上的外部链接（MR、文档、监控等）。

## Trigger

当用户需要以下操作时触发：

- 给 Jira Issue 添加 MR/GitLab 链接
- 查看 Issue 上已有的外部链接
- 删除 Issue 上的某个外链
- 关联代码合并请求到需求单

## Procedure

### P1: 添加远程链接

```bash
jira issue remotelink KEY --url URL --title TITLE

# 示例：添加 MR 链接
jira issue remotelink MPR-30977 --url https://gitlab.com/group/project/-/merge_requests/42 --title "MR !42"

# 示例：添加监控链接
jira issue remotelink MPR-30977 --url https://grafana.internal/d/dashboard --title "监控面板"

# 指定 relationship 类型（默认 "Web Link"）
jira issue remotelink KEY --url URL --title TITLE --relationship "Git Pull Request"
```

参数说明：
- `--url`（必填）：外部链接 URL
- `--title`（必填）：链接显示标题
- `--relationship`（可选）：关系类型，默认 "Web Link"

### P2: 列出所有远程链接

```bash
jira issue remotelink KEY --list

# 不带任何参数也等同于 --list
jira issue remotelink KEY
```

输出表格包含：ID、Title、URL、Relationship。

### P3: 删除远程链接

```bash
# 先 --list 获取链接 ID，再删除
jira issue remotelink KEY --delete LINK_ID

# 示例
jira issue remotelink MPR-30977 --delete 10042
```

## Common Scenarios

| 场景 | 命令 |
| --- | --- |
| 开发完成，关联 MR | `jira issue remotelink KEY --url MR_URL --title "MR !N"` |
| 查看需求关联了哪些代码 | `jira issue remotelink KEY --list` |
| MR 关联错误需重加 | `jira issue remotelink KEY --delete ID` 然后 `--url` 重新添加 |

## Rules

1. **添加必须指定 url+title**：`--url` 和 `--title` 缺一不可，否则报错
2. **删除前先列出**：先用 `--list` 确认链接 ID，再 `--delete`
3. **URL 不转义**：直接传完整 URL，CLI 内部处理
4. **Agent 模式无需交互**：所有参数通过命令行提供，无 prompt
