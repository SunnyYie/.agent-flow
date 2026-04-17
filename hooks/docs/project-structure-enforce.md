# project-structure-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | PreToolUse |
| 匹配器 | Grep |
| 作用 | 搜索源码前强制读项目结构索引 |

## 功能

1. 检查 `.dev-workflow/wiki/project-structure.md` 是否存在（不存在则不强制）
2. 检查 `.project-structure-read` 标记是否已创建
3. 已读标记 → 放行
4. 未读标记 + 搜索路径针对源码目录 → 阻断，要求先读 project-structure.md

### 源码目录判定
搜索路径包含 `src/`、`rn/`、`lib/`、`app/`、`components/` 等，或非隐藏目录的子目录。

### 排除路径
搜索 `.agent-flow/skills/`、`.agent-flow/wiki/`、`.claude/` 等知识库路径时不触发。

## 阻断行为

- 阻断：`exit 2`，要求先 `Read .dev-workflow/wiki/project-structure.md`

## 标记文件

- `.agent-flow/state/.project-structure-read`（由 context-guard.py 在读取时自动创建）

## 关联

- 与 `context-guard.py` 配合：enforce 阻断搜索，guard 在读取 project-structure.md 时创建标记
