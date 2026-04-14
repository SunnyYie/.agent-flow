# Global Wiki 知识导航

## Patterns（成功模式）

- [feishu](patterns/feishu/) — 飞书相关模式
  - [wiki-doc-read](patterns/feishu/wiki-doc-read.md) — Wiki文档读取三步流程
- [workflow](patterns/workflow/) — 工作流模式
  - [search-before-execute](patterns/workflow/search-before-execute.md) — 先查后执行 + 搜索到开发一步到位
  - [three-agent-model](patterns/workflow/three-agent-model.md) — 三Agent协作模型（双验收 + 生命周期 + 并行执行）
  - [rpi-workflow](patterns/workflow/rpi-workflow.md) — RPI 工作流：Research→Plan→Implement + GO/NO-GO 门控
  - [cross-model-workflow](patterns/workflow/cross-model-workflow.md) — 跨模型交叉验证（Claude 规划 + Codex QA）
  - [agent-teams](patterns/workflow/agent-teams.md) — 多会话并行协作（tmux + worktree + 共享任务列表）
- [architecture](patterns/architecture/) — 架构模式
  - [adr-decision-record](patterns/architecture/adr-decision-record.md) — 架构决策记录(ADR)
  - [fatal-transient-errors](patterns/architecture/fatal-transient-errors.md) — FATAL/TRANSIENT错误分类与容错
- [document](patterns/document/) — 文档转换模式
  - [requirements-spec-template](patterns/document/requirements-spec-template.md) — 需求规格说明书四段式模板
- [requirement](patterns/requirement/) — 需求分析模式
  - [frontend-backend-classification](patterns/requirement/frontend-backend-classification.md) — 需求文档前后端功能分类
- [gitlab](patterns/gitlab/) — 自托管GitLab模式
  - [self-hosted-gitlab-auth](patterns/gitlab/self-hosted-gitlab-auth.md) — glab CLI认证与API操作

## Pitfalls（踩坑记录）

- [feishu](pitfalls/feishu/) — 飞书相关踩坑
  - [lark-cli-params](pitfalls/feishu/lark-cli-params.md) — lark-cli参数格式陷阱
- [workflow](pitfalls/workflow/) — 工作流踩坑
  - [execute-without-search](pitfalls/workflow/execute-without-search.md) — 不查就执行（含跳过搜索、先试错再查Skill）
  - [git-archaeology-oversearch](pitfalls/workflow/git-archaeology-oversearch.md) — Git考古过度搜索
  - [skip-implementation-plan](pitfalls/workflow/skip-implementation-plan.md) — 跳过实施计划文档直接开发
  - [broad-keyword-search](pitfalls/workflow/broad-keyword-search.md) — 泛化关键词搜索导致范围扩大
  - [skipping-verifier](pitfalls/workflow/skipping-verifier.md) — 跳过验证者的后果
  - [promotion-duplication](pitfalls/workflow/promotion-duplication.md) — 晋升时创建重复内容而非更新已有文档
- [security](pitfalls/security/) — 安全踩坑
  - [path-traversal-bypass](pitfalls/security/path-traversal-bypass.md) — 路径遍历绕过漏洞 + 安全模块对抗性测试
- [environment](pitfalls/environment/) — 环境踩坑
  - [venv-path-resolution](pitfalls/environment/venv-path-resolution.md) — .venv路径解析错误
- [tools](pitfalls/tools/) — 工具踩坑
  - [codex-provider-auth-mismatch](pitfalls/tools/codex-provider-auth-mismatch.md) — Codex登录后config.toml与auth.json不匹配
- [agent-flow](pitfalls/agent-flow/) — agent-flow CLI踩坑
  - [agent-flow-ship-rebase](pitfalls/agent-flow/agent-flow-ship-rebase.md) — ship自动rebase导致历史分叉
  - [add-feature-branch-conflict](pitfalls/agent-flow/add-feature-branch-conflict.md) — add-feature与已有分支冲突
- [react-native](pitfalls/react-native/) — React Native踩坑
  - [jest-babel-compatibility](pitfalls/react-native/jest-babel-compatibility.md) — 旧版RN项目Jest/Babel不兼容
- [llm-coding](pitfalls/llm-coding/) — LLM编程踩坑（源自Karpathy原则）
  - [overcomplication](pitfalls/llm-coding/overcomplication.md) — 代码过度复杂化陷阱
  - [drive-by-refactoring](pitfalls/llm-coding/drive-by-refactoring.md) — 顺带重构陷阱
  - [context-pollution](pitfalls/llm-coding/context-pollution.md) — 上下文污染：长会话质量退化

## Tools（工具）

- [markitdown](tools/markitdown.md) — Microsoft 文件转 Markdown 工具（PDF/DOCX/PPTX/XLSX 等）
- [codex-cli](tools/codex-cli.md) — Codex CLI 配置参考（认证/Provider/常见坑）
- [claude-code-settings](tools/claude-code-settings.md) — Claude Code 关键设置与环境变量精选参考
- [advanced-tool-use](tools/advanced-tool-use.md) — 高级工具用法（PTC/Dynamic Filtering/Tool Search）
- [monorepo-claudemd](tools/monorepo-claudemd.md) — Monorepo CLAUDE.md 加载机制（祖先/后代/兄弟）

## Concepts（核心概念）

- [agent-roles](concepts/agent-roles.md) — 多角色协作体系（索引 → 详见 souls/）
- [agent-resolution-order](concepts/agent-resolution-order.md) — Agent 调度优先级：Skill → Agent → Command
- [memory-systems](concepts/memory-systems.md) — Claude Code 四层记忆系统（CLAUDE.md/Auto-memory//memory/Agent memory）
- [permission-gradation](concepts/permission-gradation.md) — 权限梯度管理
- [thinking-chain-guidelines](concepts/thinking-chain-guidelines.md) — 思维链准则（文档驱动 + ReAct/Plan-and-Resolve/Reflection/自主学习/升级规则）
- [wiki-management](concepts/wiki-management.md) — Wiki知识库管理规范（目录结构/页面格式/生命周期/Lint规则）
- [karpathy-principles](concepts/karpathy-principles.md) — Karpathy LLM编程四原则（Think/Simplicity/Surgical/Goal-Driven + 场景示例 + 反模式速查）
- [llm-degradation](concepts/llm-degradation.md) — LLM 输出质量退化9层因素与上下文污染修复

## Decisions（架构决策）

- [enforcement-structure](decisions/enforcement-structure.md) — 规则执行保障架构：短规则 + 详细技能 + 守卫技能三层
