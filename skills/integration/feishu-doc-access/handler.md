---
name: feishu-doc-access
version: 1.0.0
trigger: 飞书文档, lark doc, feishu document, 访问飞书, 读取飞书, 飞书wiki
confidence: 0.9
abstraction: framework
created: 2026-04-13
---

# Skill: feishu-doc-access

## Trigger
当需要访问、读取飞书云文档或Wiki时触发

## Required Reading
- Soul.md 中关于飞书授权的经验
- Wiki 中关于 lark-cli 的知识

## Procedure
1. **从URL提取token**：
   - Wiki链接 `/wiki/{token}` → wiki_token
   - 文档链接 `/docx/{token}` → file_token（可直接使用）
   - 表格链接 `/sheets/{token}` → file_token（可直接使用）
2. **判断是否需要查询节点**：
   - Wiki链接 → 必须先查节点获取 obj_token
   - 非 Wiki 链接 → token 即 file_token，跳到步骤4
3. **查询Wiki节点**：
   ```bash
   lark-cli wiki spaces get_node --params '{"token":"{wiki_token}"}' --as user
   ```
   提取 `obj_token` 和 `obj_type`（docx/doc/sheet/bitable/slides/file/mindnote）
4. **根据类型读取内容**：
   - docx/doc → `lark-cli docs +fetch --doc {obj_token} --as user --format pretty`
   - sheet → 使用 lark-sheets skill
   - bitable → 使用 lark-base skill
5. **权限不足时授权**：
   ```bash
   lark-cli auth login --scope "{所需scope}" --as user
   ```
   常见 scope：`wiki:node:read`, `docx:document:readonly`, `drive:drive:readonly`

## 权限速查

| API | 所需 scope |
|-----|-----------|
| wiki spaces get_node | `wiki:node:read` |
| docs +fetch | `docx:document:readonly` 或 `drive:drive:readonly` |
| sheets | `sheets:spreadsheet:readonly` |
| bitable | `bitable:bitable:readonly` |

## Rules
- Wiki链接的token不能直接当file_token，必须先查节点
- lark-cli参数用 `--params` JSON格式，不支持 `--token` 直接传参
- 使用前先查schema：`lark-cli schema {resource}.{method}`
- 授权需指定scope（`--scope "xxx"`），不使用 `--domain` 全量授权
