---
name: git-workflow
version: 1.1.0
trigger: git, 提交代码, 创建分支, commit, push, PR, MR, 合并, 分支管理, worktree
confidence: 0.9
abstraction: universal
created: 2026-04-13
---

# Skill: git-workflow

## Trigger
当需要执行 Git 操作（提交、分支、合并、PR、Worktree）时触发

## Required Reading

- 当前项目的命令路径配置（如 .venv 位置等）
- 项目设计文档中的 Git Flow 约定（如有）

## Git Flow Model

```
main (protected)
  └── develop (protected)
        ├── feature/agent-{task_id}-frontend
        ├── feature/agent-{task_id}-backend
        └── feature/agent-{task_id}-review
```

**规则**：
- 开发 Agent 只能在 feature 分支上开发
- 只有 Reviewer Agent 可以合并 MR 和删除分支
- main 和 develop 受保护，不可直接 push

## Procedure

1. **查看当前状态**：`git status` + `git diff`
2. **按场景执行**：

### Branch Management

```bash
# 创建 feature 分支（从 develop）
git checkout develop
git pull origin develop
git checkout -b feature/agent-{task_id}-{role}

# 提交变更
git add {specific_files}
git commit -m "{type}: {description}"

# 推送 feature 分支
git push -u origin feature/agent-{task_id}-{role}
```

### Commit Code

```bash
git add {specific_files}
git commit -m "{type}: {description}"
```
- type: feat/fix/refactor/docs/test/chore/perf/ci
- 只 add 相关文件，不用 `git add -A`
- 提交前检查无敏感文件（.env, credentials）

### Create Branch

```bash
git checkout -b {type}/{short-description}
# type: feature/ bugfix/ hotfix/ refactor/ docs
```

### Worktree Operations

```bash
# 创建 worktree（隔离开发）
git worktree add .worktrees/{task_id}-{role} feature/agent-{task_id}-{role}

# 移除 worktree
git worktree remove .worktrees/{task_id}-{role}

# 列出所有 worktree
git worktree list
```

### MR/PR Operations (GitHub)

```bash
# 创建 PR
gh pr create \
  --base develop \
  --head feature/agent-{task_id}-{role} \
  --title "{title}" \
  --body "$(cat <<'EOF'
## Summary
{bullet points}

## Test plan
{checklist}
EOF
)"

# 合并 PR
gh pr merge {pr_number} --merge

# 删除远程分支
git push origin --delete feature/agent-{task_id}-{role}
```

### MR Operations (GitLab)

```bash
# 创建 MR
glab mr create \
  --target-branch develop \
  --source-branch feature/agent-{task_id}-{role} \
  --title "{title}" \
  --description "{description}"

# 合并 MR
glab mr merge {mr_id}
```

### Merge Conflict Resolution

1. `git diff {base-branch}...HEAD` 查看变更
2. 逐文件解决冲突，不使用 `git reset --hard`
3. 解决后运行测试确认无破坏

## Branch Protection

| 分支 | 谁可以 push | 谁可以合并 |
|------|------------|-----------|
| main | 无人（仅通过 release） | 仅 Maintainer |
| develop | 无人（仅通过 MR） | 仅 Reviewer Agent |
| feature/* | 对应开发 Agent | 仅通过 MR |

## Commit Message Format

```
<type>: <description>

类型: feat, fix, refactor, docs, test, chore, perf, ci
```

## MR Description Template

```markdown
## 需求来源
{PRD 链接或任务 ID}

## PRD 摘要
{简要描述本次变更对应的需求}

## 改动文件
{文件列表及改动说明}

## 测试说明
{测试方法和结果}

## 审核报告
{Reviewer Agent 的审核结果}
```

## Git Error Recovery

| 错误 | 原因 | 修复 |
|------|------|------|
| `merge conflict` | 分支与 develop 冲突 | `git rebase origin/develop` 解决冲突 |
| `push rejected` | 远程有新提交 | `git pull --rebase origin feature-branch` |
| `detached HEAD` | 检出了 commit 而非分支 | `git checkout {branch-name}` |
| worktree 残留 | 进程中断 | `git worktree prune` |
| `.gitignore` 不生效 | 缓存了已追踪文件 | `git rm --cached {file}` |

## Rules
- **禁止在 main/master/develop 上直接提交代码**，必须创建 feature 分支
- **开始新任务前必须先拉最新代码再创建分支**：`git pull --rebase` → `git checkout -b feat/xxx`
- 如果在主分支上做了修改，先 `git stash` → `git pull --rebase` → `git checkout -b feat/xxx` → `git stash pop`
- 禁止 `git push --force` 到 main/develop
- 禁止 `git reset --hard` 在有未提交变更时
- 禁止 `git add -A`（可能包含 .env 等敏感文件）
- 提交前确认 `.gitignore` 覆盖所有应忽略的文件
- 每个 feature 分支只对应一个 Agent 的一个任务
- 不使用 `--no-verify` 跳过钩子
- 优先创建新 commit 而非 amend
- 提交前检查：无敏感文件、无大文件、lint通过
- 合并冲突逐文件解决，不用破坏性操作
