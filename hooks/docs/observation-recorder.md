# observation-recorder.py

| 属性 | 值 |
|------|-----|
| 事件 | PostToolUse |
| 匹配器 | Read\|Write\|Edit\|Bash\|Grep\|Glob\|WebSearch |
| 作用 | 静默记录操作到 SQLite 数据库 |

## 功能

1. 从 `.current-session-id` 获取会话 ID
2. 提取工具调用的关键信息（tool_name, file_path, command 等）
3. 推断 observation 类型（read/write/search/install/execute）
4. 判断层级（global/project/dev）
5. 写入 `observations.db`

### 噪声过滤
- 跳过 `.git/`, `node_modules/`, `__pycache__/`, `.venv/` 等路径
- 跳过 ls, pwd, whoami 等简单命令

### FTS5 全文搜索
observations 表配有 FTS5 虚拟表，支持全文搜索。

## 数据库

- 路径：`.agent-flow/observations.db`
- 表：`sessions`, `observations`, `observations_fts`
- WAL 模式，5秒超时
- 性能目标：< 50ms

## 输出

静默执行（`exit 0`），出错也静默。

## 关联

- 与 `session-starter.py` 配合：starter 创建 session_id，recorder 读取并关联
- 数据可用于 `agent-flow recall` 回溯历史
