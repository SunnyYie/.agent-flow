# promotion-guard.py

| 属性 | 值 |
|------|-----|
| 事件 | PreToolUse |
| 匹配器 | Write\|Edit |
| 作用 | 拦截写入全局 agent-flow 知识库，强制执行验收流程 |

## 功能

### 全局知识库保护（~/.agent-flow/wiki/ 和 ~/.agent-flow/skills/）

1. **验收标记检查**：`.promotion-verified` 标记存在 → 放行并清除标记
2. **新建文件 → 相似内容检查**：
   - 在目标目录中搜索相似文档（Jaccard 相似度 ≥ 0.4 或标题包含）
   - 有相似文档 → 阻断，提示更新已有文档或执行 promotion-verify
   - 无相似文档 → 阻断，要求先通过多 Agent 验收
3. **更新已有文件** → 软提醒

### 项目级文档保护

- 保护 `project-structure.md` 和 `Agent.md`
- 更新时检查标签重复
- 未验证时软提醒

## 阻断行为

- 新建全局知识库文件：`exit 2`
- 更新已有文件：`exit 0`（软提醒）
- 标签重复：`exit 2`

## 关联

- 执行 promotion-verify Skill 后创建 `.promotion-verified` 标记
