# session-starter.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt |
| 作用 | 创建新会话ID，写入SQLite数据库 |

## 功能

1. 生成会话 ID（格式：`YYYY-MM-DD-HHMMSS`）
2. 关闭之前未结束的会话（SQLite sessions 表）
3. 创建新会话记录
4. 写入标记文件 `.agent-flow/state/.current-session-id`

## 数据库

- 路径：`.agent-flow/observations.db`
- 表：`sessions`（session_id, started_at, ended_at, user_prompt, project_dir, observation_count）
- WAL 模式，5秒超时

## 关联

- 与 `observation-recorder.py` 配合：starter 创建 session_id，recorder 读取并关联观测记录
