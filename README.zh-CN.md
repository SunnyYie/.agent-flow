# AgentFlow

> Claude Code 通用 AI Agent 工作流协议

AgentFlow 是一套结构化开发工作流系统，将 Claude Code 转化为规则驱动、多 Agent 协作的开发平台，并提供质量管控与知识管理能力。

## 架构

```text
Layer 1: ~/.agent-flow/           -> 全局控制层（配置、运行状态、遗留索引）
Layer 2: ~/.agent-flow/platform/  -> Platform 团队资产（框架内核）
Layer 3: ~/.agent-flow/community/ -> Community 团队资产（业务与集成）
Layer 4: .agent-flow/             -> 项目层资产（项目记忆/状态）
Layer 5: .dev-workflow/           -> 开发层补充资产
```

### 团队资产目录

```text
~/.agent-flow/
  platform/
    team.yaml
    hooks/{runtime,governance}/
    wiki/
    skills/
    souls/
    references/
    tools/

  community/
    team.yaml
    hooks/runtime/
    wiki/
    skills/
    references/
    tools/
```

## 团队职责

- **Platform 团队**：框架运行时、Agent 编排、治理规则、核心认知循环保障。
- **Community 团队**：业务工作流、外部系统集成、实现模式、领域工具实践。

## 核心认知循环

每个任务遵循 6 阶段循环：

```text
THINK -> PLAN -> EXECUTE -> VERIFY -> REFLECT -> EVOLVE
```

## 资源查找顺序（团队优先）

1. 项目层：`.agent-flow/`、`.dev-workflow/`
2. 团队层：`~/.agent-flow/platform/`、`~/.agent-flow/community/`
3. 全局层：仅用于共享控制与索引类资产

## Agent 角色

角色定义存放在：

- `~/.agent-flow/platform/souls/main.md`
- `~/.agent-flow/platform/souls/planner.md`
- `~/.agent-flow/platform/souls/coder.md`
- `~/.agent-flow/platform/souls/researcher.md`
- `~/.agent-flow/platform/souls/verifier.md`
- `~/.agent-flow/platform/souls/architect.md`
- `~/.agent-flow/platform/souls/writer.md`

## 配置

`config.yaml`：

```yaml
default_platform: claude-code
log_level: INFO
critical_tools:
  - lark-cli
  - glab
  - gh
  - docker
```

## 快速开始

1. 初始化项目：

```bash
agent-flow init --dev-workflow
```

2. 阅读 `CLAUDE.md` 了解团队化资源检索规则。
3. 按团队优先检索与质量门控执行任务。

## 许可证

私有 - 仅内部使用。
