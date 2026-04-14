---
name: gitlab-mr-creation
version: 1.0.0
trigger: gitlab, MR, merge request, glab, 创建MR, 提交MR
applicable_agents: [main, executor]
confidence: 0.85
abstraction: universal
created: 2026-04-13
---

# Skill: GitLab MR 创建（自托管实例）

## Trigger
当需要在自托管 GitLab 实例上创建 MR 时触发

## Required Reading
- `~/.agent-flow/wiki/patterns/gitlab/self-hosted-gitlab-auth.md`（认证模式）

## Procedure
1. 检查 glab 安装：`which glab && glab --version`
2. 认证自托管实例：`echo $TOKEN | glab auth login --hostname <host> --stdin`
3. 验证认证：`glab auth status`
4. 查找项目 ID：`glab api "projects?search=<project_name>" --hostname <host> | python3 -c "import sys,json; [print(f'ID: {p[\"id\"]}, Path: {p[\"path_with_namespace\"]}') for p in json.load(sys.stdin)]"`
5. 检查是否已有 MR：`glab api "projects/<id>/merge_requests?state=opened&source_branch=<branch>" --hostname <host>`
6. 创建 MR：`glab api --hostname <host> --method POST "projects/<id>/merge_requests" -f source_branch=<src> -f target_branch=<target> -f title="<title>" -f description="<desc>"`
7. 获取 MR URL：从返回的 JSON 中提取 `web_url`

## Rules
- glab mr create 可能因路径解析失败（404），优先使用 API 直接创建
- 已有 MR 时不要重复创建，直接获取现有 MR 信息
- Token 需要 api 权限
