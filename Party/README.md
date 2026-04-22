# Party Team Flow

本目录是团队级 Agent-flow 配置根目录，初始化后可直接被项目通过 `team_id: Party` 绑定并复用。

## 如何使用

1. 在项目目录初始化并绑定团队：
   - `agent-flow init --project`
   - `agent-flow bind-team Party`
2. 在项目内查看资源解析结果：
   - `agent-flow asset resolve`
   - `agent-flow asset list --layer team`
3. 在团队目录维护共享资产，项目会按 `project > team > global` 顺序解析。

## 目录说明

- `hooks/`: 团队级 Hook（运行时与治理）
- `references/`: 团队共享参考资料
- `skills/`: 团队共享技能；`ANCHOR.md` 记录全局技能锚点
- `souls/`: 角色系统提示与职责定义
- `tools/`: 工具白名单与工具配置
- `wiki/`: 团队共享知识文档；`ANCHOR.md` 记录全局 wiki 锚点
- `team.yaml`: 团队元信息（team_id、名称、schema）

## 维护建议

- 新增团队技能：`agent-flow asset create --kind skills --name <scene>/<skill> --layer team --team-id Party`
- 新增团队 wiki：`agent-flow asset create --kind wiki --name <scene>/<doc> --layer team --team-id Party`
- 定期更新 `skills/ANCHOR.md` 与 `wiki/ANCHOR.md`（重新执行初始化或按需手动维护）。
