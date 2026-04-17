# preflight-guard.py

| 属性 | 值 |
|------|-----|
| 事件 | UserPromptSubmit |
| 触发条件 | 每次用户提交prompt |
| 作用 | 检查 pre-flight 状态，注入开发铁律 |

## 功能

### Pre-flight 未完成时
强制注入 `<system-reminder>` 协议指令，要求 Agent 按顺序执行 5 步 pre-flight：
1. 检查项目配置
2. 知识检索（5次搜索）
3. 分析写入 Memory.md
4. 计划写入 current_phase.md
5. 用户确认

### Pre-flight 已完成时
注入开发铁律提醒，并检查以下标记：
- `.self-questioning-done` — 自我质询是否完成
- `.complexity-level` — 复杂度评估是否完成
- `.requirement-clarified` — 需求澄清是否完成
- `.design-confirmed` — 设计决策是否确认
- `.user-acceptance-done` — 用户验收是否完成

### 其他检查
- 项目未初始化 agent-flow → 建议运行 `agent-flow init`
- 初始化不完整 → 列出缺失文件，建议 `agent-flow init --dev-workflow --force`
- 项目上下文为空 → 提醒重新 init
- 清除过时的验收标记（任务变更时）

## 输出

`<system-reminder>` 块，包含协议指令或铁律提醒。

## 关联

- 与 `preflight-enforce.py` 配合：guard 在 prompt 时提醒，enforce 在工具调用时阻断
- 与 `self-questioning-enforce.py` 配合：guard 提醒，enforce 阻断
