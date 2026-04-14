# AgentFlow

> Claude Code 通用 AI Agent 工作流协议

AgentFlow 是一套结构化开发工作流系统，将 Claude Code 转化为规则驱动、多Agent协作的开发平台，具备质量管控和知识管理能力。

## 架构

```
Layer 1: ~/.agent-flow/          → 全局层（skills, wiki, souls, whitelist）
Layer 2: .agent-flow/            → 项目层（config, experience, state）
Layer 3: .dev-workflow/           → 开发层（agent 角色, 按 agent 分配的 skills, 带 schema 的 wiki）
```

**原则：不重复，只补充。** L3 引用 L1，不复述。

## 核心认知循环

每个任务遵循 6 阶段认知循环：

```
THINK → PLAN → EXECUTE → VERIFY → REFLECT → EVOLVE
```

- **THINK** — 分析需求，执行前先搜索 Skills/Wiki/Soul
- **PLAN** — 拆解需求，文档化分析和计划
- **EXECUTE** — TDD 方式实现，独立子任务并行 Agent 执行
- **VERIFY** — 多 Agent 验证，自我质询检查
- **REFLECT** — 将通用经验晋升到 `~/.agent-flow/`
- **EVOLVE** — 用新知识更新 Wiki、Skills、Soul

## Agent 角色

| 角色 | 文件 | 激活时机 |
|------|------|---------|
| Main | `souls/main.md` | 始终激活 — 监督、验证、积累 |
| Planner | `souls/planner.md` | 任务分解 |
| Coder | `souls/coder.md` | 代码实现（TDD） |
| Writer | `souls/writer.md` | 文档撰写 |
| Researcher | `souls/researcher.md` | 信息调研 |
| Verifier | `souls/verifier.md` | 检查点质量验证 |
| Architect | `souls/architect.md` | 架构设计与 ADR |

## 技能库（40+）

技能是可复用、可搜索的知识单元，指导 Agent 行为：

| 分类 | 技能 |
|------|------|
| 工作流 | `pre-flight-check`, `task-complexity`, `phase-review`, `self-questioning`, `requirement-decomposition` |
| 代码 | `code-implementation`, `code-review`, `tdd-workflow`, `testing-strategies`, `implementation-patterns` |
| 知识 | `knowledge-search`, `experience-promotion`, `critical-knowledge`, `ai-context-management` |
| 设计 | `architecture-design`, `workflow-design`, `prompt-engineering`, `claude-code-design` |
| 工具 | `tool-precheck`, `git-workflow`, `gitlab-mr-creation`, `feishu-doc-access`, `web-research` |
| 质量 | `security-checks`, `error-recovery`, `acceptance-check`, `subtask-guard`, `content-filter` |
| 高级 | `orchestrator-worker`, `agent-orchestration`, `prompt-caching-optimization`, `pydantic-patterns` |

## 执行守卫 Hooks（12 个）

运行时强制执行工作流规则的 Python 脚本：

| Hook | 用途 |
|------|------|
| `preflight-guard.py` | 任务前强制执行预检 |
| `preflight-enforce.py` | 验证预检完成 |
| `thinking-chain-enforce.py` | 强制执行认知循环阶段 |
| `search-tracker.py` | 跟踪"先搜索再执行"合规性 |
| `promotion-guard.py` | REFLECT 后强制执行经验晋升 |
| `self-questioning-enforce.py` | REFLECT 前强制执行自我质询 |
| `user-acceptance-guard.py` | 无用户验收则阻止 push/MR |
| `tool-precheck-guard.py` | 关键工具使用前强制预检 |
| `dev-workflow-enforce.py` | 强制开发工作流合规 |
| `project-structure-enforce.py` | 验证项目结构 |
| `context-guard.py` | 防止上下文窗口溢出 |
| `error-search-remind.py` | 错误恢复前提醒搜索 |

## Wiki 知识库

```
wiki/
├── INDEX.md              # 全局导航
├── patterns/             # 成功模式
│   ├── feishu/           # 飞书相关模式
│   ├── workflow/         # 工作流模式（三Agent模型、RPI、跨模型验证）
│   ├── architecture/     # 架构模式（ADR、错误分类）
│   ├── document/         # 文档转换模板
│   ├── requirement/      # 需求分析模式
│   └── gitlab/           # 自托管 GitLab 模式
├── pitfalls/             # 踩坑记录
│   ├── feishu/           # Lark CLI 参数陷阱
│   ├── workflow/         # 不查就执行、过度搜索、跳过计划
│   ├── security/         # 路径遍历、注入攻击
│   ├── environment/      # venv 路径、工具配置
│   ├── llm-coding/       # 过度复杂化、顺手重构、上下文污染
│   └── react-native/     # Jest/Babel 兼容性
├── concepts/             # 核心概念
│   ├── agent-roles.md    # 多角色协作
│   ├── memory-systems.md # 四层记忆架构
│   ├── karpathy-principles.md # LLM 编程原则
│   └── ...
├── tools/                # 工具文档
└── decisions/            # 架构决策记录
```

## 核心铁律（12 条）

1. **搜索先行** — 每个子任务执行前必须先搜索 Skill/Soul/Wiki。不搜索就执行 = 臆断 = 质量差
2. **需求拆解** — 需求文档必须先拆解为变更点（CP1, CP2, ...），逐项向用户确认，再定位代码
3. **精准定位** — 代码搜索由窄到宽（L1 精确 → L2 模糊 → L3 路由 → L4 全局），禁止直接全项目扫描
4. **Git 安全** — 禁止在 main 上提交；每次开发前先拉代码再创建分支；创建 MR 前搜索 Skill
5. **经验晋升** — REFLECT 后必须将 abstraction:universal 的经验晋升到 `~/.agent-flow/`
6. **不确定就问** — 需求模糊、多种方案、范围不清时必须暂停询问，禁止假设
7. **多Agent并行** — 验收、写代码、测试时必须开启多Agent并行，提高效率和视角多样性
8. **复杂度量化** — 每个任务必须调用 task-complexity skill 执行 5 维量化评分
9. **自我质询** — VERIFY 后、REFLECT 前必须执行 self-questioning skill
10. **临界知识优先** — 使用 lark-cli、glab、gh 等外部工具前，必须先检查 Soul.md 临界知识区
11. **深度澄清** — 需求拆解后必须执行深度澄清，穷举假设、追问边界场景、确认影响范围。禁止带着未澄清的假设进入代码编写
12. **用户验收闸** — 推送代码或创建 MR 前，必须获得用户明确验收确认。用户验收标记（.user-acceptance-done）是 push/MR 的硬性前置条件

## 工具白名单

```yaml
auto_install:         # 无需确认
  - git, docker, npm, pip, python3, node, gh, uv, curl, wget, jq, yq

need_confirmation:    # 需要用户确认
  - lark-cli, cargo, brew, apt-get, yum, pipx, npx, markitdown

blacklist:            # 禁止使用
  - rm -rf /, mkfs, dd if=, format
```

## 多Agent并行场景

| 阶段 | 并行策略 | 原因 |
|------|---------|------|
| 需求规格说明书验收 | 双验收：Verifier Agent + Main Agent 独立审查 | 单视角验收容易遗漏 |
| 写代码 | 多个独立子任务并行 Executor Agent | 无依赖的子任务串行 = 浪费时间 |
| 代码审查 | code-reviewer Agent 独立审查 | 开发者自己审查有盲区 |
| 测试验收 | Verifier + Main Agent 双验收 | 单一验收 = 低质量 |

## 任务复杂度分级路由

| 级别 | 评分 | 工作流 | 搜索深度 |
|------|------|--------|---------|
| Simple（简单） | 1-2 | 快速路径 | 2 步 |
| Medium（中等） | 3-4 | 标准路径 + 检查点 | 5 步 |
| Complex（复杂） | 5+ | 严格路径 + 全部门控 | 5 步 + WebSearch |

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

2. 初始化完成后阅读 `Agent.md`

3. 每个任务前遵循 pre-flight check 协议

## 许可证

私有 — 仅供内部使用。
