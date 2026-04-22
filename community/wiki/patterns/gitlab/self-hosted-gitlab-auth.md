---
name: self-hosted-gitlab-auth
type: pattern
module: gitlab
status: verified
confidence: 0.8
created: 2026-04-13
tags: [gitlab, glab, self-hosted, auth, MR]
---

# 自托管 GitLab 实例的 glab CLI 认证与 MR 创建

> glab CLI 对自托管 GitLab 实例需要单独认证，认证后可用 API 直接操作

## 问题描述

标准 `glab mr create` 在自托管 GitLab 上常因路径解析失败（404）。需要：
1. 正确认证自托管实例
2. 绕过 glab 子命令的路径解析问题

## 解决方案

### 1. 认证

```bash
echo $TOKEN | glab auth login --hostname <host> --stdin
```

- Token 需要 `api` 权限
- 验证：`glab auth status`

### 2. 通过 API 创建 MR（推荐）

```bash
# 查找项目 ID
glab api "projects?search=<project_name>" --hostname <host> | \
  python3 -c "import sys,json; [print(f'ID: {p[\"id\"]}, Path: {p[\"path_with_namespace\"]}') for p in json.load(sys.stdin)]"

# 检查是否已有 MR
glab api "projects/<id>/merge_requests?state=opened&source_branch=<branch>" --hostname <host>

# 创建 MR
glab api --hostname <host> --method POST "projects/<id>/merge_requests" \
  -f source_branch=<src> -f target_branch=<target> \
  -f title="<title>" -f description="<desc>"
```

### 3. 关键规则

- `glab mr create` 优先用 API 而非子命令，避免路径解析 404
- 已有 MR 时不要重复创建，直接获取现有 MR 信息
- Token 需要 `api` 权限（`read_api` 不够）

## 相关条目

- [[gitlab-mr-creation|GitLab MR 创建技能]]
