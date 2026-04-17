# git-branch-guard.py

| 属性 | 值 |
|------|-----|
| 事件 | PreToolUse |
| 匹配器 | Bash |
| 作用 | 阻止在保护分支上执行 git commit/push |

## 功能

1. 检测 Bash 命令是否为 `git commit` 或 `git push`
2. 获取当前 git 分支名
3. 如果在 `main`/`master`/`develop` 分支上，阻断并提示创建 feature 分支

## 阻断行为

- 阻断：`exit 2`，Agent 必须先创建 feature 分支

## 输出示例

```
[BLOCKED] Git commit/push on protected branch: main. Create a feature branch first.
```

## 历史

v2.0 从 settings.json 中的内联 bash 脚本（~15行）提取为独立 Python 文件，提高可读性和可维护性。

## 关联

- 与 `dev-workflow-enforce.py` 的检查1互补：guard 拦截 Bash 中的 git commit/push，enforce 拦截 Write/Edit 代码文件
