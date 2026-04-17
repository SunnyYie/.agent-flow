# dev-workflow-enforce.py

| 属性 | 值 |
|------|-----|
| 事件 | PreToolUse |
| 匹配器 | Write\|Edit\|Bash |
| 作用 | 强制5条开发铁律 |

## 功能

### 检查1: Git 分支保护（Write/Edit 代码文件时）
- 当前分支为 main/master/develop → 阻断
- 提示创建 feature 分支

### 检查2: 实施计划文档（Write/Edit 代码文件时）
- 没有 `requirement-decomposition.md` 或 `## 实施计划` 章节 → 阻断
- legacy 格式计划 → 软提醒

### 检查3: Skill 搜索提醒（Bash 时）
- 检测 `glab mr` 或 `git push origin` 命令 → 提醒先搜索 Skill

### 检查4: 需求澄清标记（Write/Edit 代码文件时，v3.0 新增）
- `.requirement-clarified` 不存在 → 软提醒

### 检查5: 设计决策确认标记（Write/Edit 代码文件时，v3.0 新增）
- `.design-confirmed` 不存在 → 软提醒

### 检查6: 连续 Edit/Write 搜索守卫
- 追踪连续代码修改次数（状态保存在 `.subtask-guard-state.json`）
- 超过阈值（4次）且无搜索 → 首次软提醒，再次硬阻断
- 有搜索标记证据（`.search-done` / `.subtask-guard-done`）→ 重置计数
- 30分钟无活动自动重置状态

## 阻断行为

- 检查1,2,6(再次): `exit 2`（硬阻断）
- 检查3,4,5,6(首次): `exit 0`（软提醒）

## 关联

- 与 `git-branch-guard.py` 互补：guard 拦截 Bash 中的 git 命令，enforce 拦截 Write/Edit
- 与 `thinking-chain-enforce.py` 配合：enforce 检查搜索守卫，chain 检查搜索标记
- 与 `search-tracker.py` 配合：tracker 创建搜索标记，enforce 读取标记
