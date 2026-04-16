---
title: "标签索引"
category: topic-hub
module: meta
agents: [main, planner, architect, researcher, coder, verifier, writer]
scope: global
tags: [index, meta, tags, topic-hub]
confidence: 1.0
status: verified
created: 2026-04-15
updated: 2026-04-15
---

# Tag Index（标签索引）

> tag → documents 映射。用法：`Grep "feishu" TAG-INDEX.md` → 找到所有飞书相关文档路径。
> 文档路径省略 `.md` 后缀，与 wikilink 惯例一致。

## Tags

| Tag | Documents |
|-----|-----------|
| ADR | patterns/architecture/adr-decision-record |
| API | pitfalls/feishu/lark-cli-params |
| CLAUDE.md | concepts/memory-systems |
| MR | patterns/gitlab/self-hosted-gitlab-auth |
| PurePosixPath | pitfalls/security/path-traversal-bypass |
| ReAct | concepts/thinking-chain-guidelines |
| SRS | patterns/document/requirements-spec-template |
| abstraction | pitfalls/llm-coding/overcomplication |
| add-feature | pitfalls/agent-flow/add-feature-branch-conflict |
| adversarial-input | pitfalls/security/path-traversal-bypass |
| adversarial-testing | pitfalls/security/path-traversal-bypass |
| agent | concepts/agent-roles, concepts/agent-resolution-order |
| agent-flow | pitfalls/agent-flow/agent-flow-ship-rebase, pitfalls/agent-flow/add-feature-branch-conflict, decisions/enforcement-structure |
| agent-model | patterns/workflow/three-agent-model |
| agent-orchestration | pitfalls/workflow/code-review-not-triggered, pitfalls/workflow/parallel-execution-not-enforced |
| agent-teams | patterns/workflow/agent-teams |
| architecture | patterns/workflow/three-agent-model, patterns/architecture/adr-decision-record |
| auth | patterns/gitlab/self-hosted-gitlab-auth, pitfalls/tools/codex-provider-auth-mismatch |
| authorization | concepts/permission-gradation |
| auto-memory | concepts/memory-systems |
| babel | pitfalls/react-native/jest-babel-compatibility |
| backend | pitfalls/llm-coding/frontend-backend-type-alignment |
| best-practices | concepts/karpathy-principles |
| branch | pitfalls/agent-flow/add-feature-branch-conflict |
| caching | patterns/architecture/prompt-caching, patterns/architecture/speculative-caching |
| circuit-breaker | pitfalls/llm-coding/circuit-breaker-halfopen-probe |
| claude-code | tools/claude-code-settings, concepts/memory-systems |
| claudemd | tools/monorepo-claudemd |
| cli | tools/codex-cli |
| codex | tools/codex-cli, pitfalls/tools/codex-provider-auth-mismatch |
| cognitive-loop | patterns/workflow/search-before-execute |
| code-review | pitfalls/workflow/code-review-not-triggered |
| coding-agent | tools/codex-cli |
| compact | concepts/llm-degradation, pitfalls/llm-coding/context-pollution |
| configuration | tools/claude-code-settings |
| conflict | pitfalls/agent-flow/git-stash-agent-flow-conflict, pitfalls/agent-flow/add-feature-branch-conflict |
| constraint | pitfalls/llm-coding/constraint-fix-pairing |
| context-pollution | concepts/llm-degradation, pitfalls/llm-coding/context-pollution |
| coordination | patterns/workflow/agent-teams |
| cost-optimization | patterns/architecture/prompt-caching |
| cross-model | patterns/workflow/cross-model-workflow |
| decision | patterns/architecture/adr-decision-record |
| degradation | concepts/llm-degradation, pitfalls/llm-coding/context-pollution |
| diff-noise | pitfalls/llm-coding/drive-by-refactoring |
| document | patterns/feishu/wiki-doc-read |
| document-conversion | tools/markitdown |
| document-driven | concepts/thinking-chain-guidelines, pitfalls/workflow/skip-implementation-plan |
| dual-acceptance | patterns/workflow/three-agent-model, pitfalls/workflow/skipping-verifier |
| e2e | patterns/workflow/e2e-script-three-part-structure |
| efficiency | pitfalls/workflow/parallel-execution-not-enforced |
| enforcement | decisions/enforcement-structure |
| enum | pitfalls/llm-coding/frontend-backend-type-alignment |
| environment | pitfalls/environment/venv-path-resolution |
| environment-variables | tools/claude-code-settings |
| error-handling | patterns/architecture/fatal-transient-errors |
| escalation | concepts/thinking-chain-guidelines |
| execute | patterns/workflow/search-before-execute, pitfalls/workflow/execute-without-search |
| fault-tolerance | patterns/architecture/fatal-transient-errors |
| feishu | patterns/feishu/wiki-doc-read, pitfalls/feishu/lark-cli-params, tools/mai-jira-cli |
| feishu-sso | tools/mai-jira-cli |
| force-push | pitfalls/agent-flow/agent-flow-ship-rebase |
| frontend | pitfalls/llm-coding/frontend-backend-type-alignment |
| gate | patterns/workflow/rpi-workflow |
| git | pitfalls/agent-flow/git-stash-agent-flow-conflict, pitfalls/workflow/git-archaeology-oversearch |
| glab | patterns/gitlab/self-hosted-gitlab-auth |
| goal-driven | concepts/karpathy-principles |
| hook | pitfalls/agent-flow/hook-path-inconsistency |
| implementation | pitfalls/workflow/skip-implementation-plan |
| integration-test | patterns/workflow/e2e-script-three-part-structure |
| internal-tool | tools/mai-jira-cli |
| jest | pitfalls/react-native/jest-babel-compatibility |
| jira | tools/mai-jira-cli |
| karpathy | concepts/karpathy-principles, pitfalls/llm-coding/drive-by-refactoring, pitfalls/llm-coding/overcomplication |
| knowledge-base | concepts/wiki-management |
| lark-cli | patterns/feishu/wiki-doc-read, pitfalls/feishu/lark-cli-params |
| latency | patterns/architecture/speculative-caching |
| lifecycle | concepts/wiki-management |
| lint | concepts/wiki-management |
| llm | concepts/llm-degradation |
| llm-coding | concepts/karpathy-principles, pitfalls/llm-coding/overcomplication, pitfalls/llm-coding/drive-by-refactoring, pitfalls/llm-coding/context-pollution, pitfalls/llm-coding/frontend-backend-type-alignment, pitfalls/llm-coding/constraint-fix-pairing, pitfalls/llm-coding/shared-constants-dedup, pitfalls/llm-coding/circuit-breaker-halfopen-probe, pitfalls/llm-coding/rollback-honest-marking |
| loading | tools/monorepo-claudemd |
| markdown | tools/markitdown |
| memory | concepts/memory-systems |
| microsoft | tools/markitdown |
| mocha | pitfalls/react-native/jest-babel-compatibility |
| monorepo | tools/monorepo-claudemd |
| multi-agent | concepts/agent-roles, patterns/workflow/orchestrator-workers, pitfalls/workflow/parallel-execution-not-enforced, patterns/workflow/three-agent-model, pitfalls/workflow/multi-agent-rate-limit-recovery |
| multi-llm | patterns/workflow/cross-model-workflow |
| multi-session | patterns/workflow/agent-teams |
| obsidian | concepts/wiki-management |
| openai | tools/codex-cli |
| optimization | tools/advanced-tool-use |
| orchestration | concepts/agent-roles, patterns/workflow/orchestrator-workers |
| over-engineering | pitfalls/llm-coding/overcomplication |
| oversearch | pitfalls/workflow/git-archaeology-oversearch |
| parallel | patterns/workflow/agent-teams, patterns/workflow/orchestrator-workers, pitfalls/workflow/parallel-execution-not-enforced |
| params | pitfalls/feishu/lark-cli-params |
| path | pitfalls/agent-flow/hook-path-inconsistency |
| path-resolution | pitfalls/environment/venv-path-resolution |
| path-traversal | pitfalls/security/path-traversal-bypass |
| performance | patterns/architecture/prompt-caching, patterns/architecture/speculative-caching |
| permissions | concepts/permission-gradation |
| pitfall | pitfalls/workflow/execute-without-search |
| plan | patterns/workflow/rpi-workflow |
| priority | concepts/agent-resolution-order |
| prompt-caching | tools/advanced-tool-use |
| ptc | tools/advanced-tool-use |
| quality | concepts/llm-degradation, patterns/workflow/search-before-execute, pitfalls/workflow/execute-without-search |
| quality-gate | pitfalls/workflow/skipping-verifier |
| rate-limit | pitfalls/workflow/multi-agent-rate-limit-recovery |
| react-native | pitfalls/react-native/jest-babel-compatibility |
| reasoning | concepts/thinking-chain-guidelines |
| rebase | pitfalls/agent-flow/agent-flow-ship-rebase |
| refactoring | pitfalls/llm-coding/drive-by-refactoring |
| research | patterns/workflow/rpi-workflow |
| resolution | concepts/agent-resolution-order |
| retry-strategy | patterns/architecture/fatal-transient-errors |
| rollback | pitfalls/llm-coding/rollback-honest-marking |
| rules | decisions/enforcement-structure |
| rpi | patterns/workflow/rpi-workflow |
| schema | wiki/.wiki-schema |
| search-first | pitfalls/workflow/execute-without-search |
| search-to-develop | patterns/workflow/search-before-execute |
| security | concepts/permission-gradation, pitfalls/security/path-traversal-bypass |
| self-hosted | patterns/gitlab/self-hosted-gitlab-auth |
| session-management | pitfalls/llm-coding/context-pollution |
| settings | tools/claude-code-settings |
| shared-constants | pitfalls/llm-coding/shared-constants-dedup |
| ship | pitfalls/agent-flow/agent-flow-ship-rebase |
| simplicity | concepts/karpathy-principles |
| skill | concepts/agent-resolution-order |
| skill-first | pitfalls/workflow/execute-without-search |
| speculative | patterns/architecture/speculative-caching |
| stash | pitfalls/agent-flow/git-stash-agent-flow-conflict |
| strategy-pattern | pitfalls/llm-coding/overcomplication |
| style-drift | pitfalls/llm-coding/drive-by-refactoring |
| supervision | patterns/workflow/three-agent-model |
| surgical-changes | concepts/karpathy-principles |
| task-decomposition | patterns/workflow/orchestrator-workers |
| test-matrix | patterns/workflow/test-matrix-5-dimension-check |
| testing | pitfalls/react-native/jest-babel-compatibility |
| think-before-coding | concepts/karpathy-principles |
| thinking | concepts/thinking-chain-guidelines |
| token-reduction | tools/advanced-tool-use |
| tool-search | tools/advanced-tool-use |
| trade-off | patterns/architecture/adr-decision-record |
| type-alignment | pitfalls/llm-coding/frontend-backend-type-alignment |
| venv | pitfalls/environment/venv-path-resolution |
| verification | patterns/workflow/cross-model-workflow |
| verifier | pitfalls/workflow/skipping-verifier |
| wiki | concepts/wiki-management, patterns/feishu/wiki-doc-read |
| workflow | patterns/workflow/search-before-execute, patterns/workflow/rpi-workflow, pitfalls/workflow/execute-without-search |
| 代码搜索 | pitfalls/workflow/broad-keyword-search |
| 关键词 | pitfalls/workflow/broad-keyword-search |
| 功能拆分 | patterns/requirement/frontend-backend-classification |
| 去重 | pitfalls/workflow/promotion-duplication |
| 模板 | patterns/document/requirements-spec-template |
| 文档转换 | patterns/document/requirements-spec-template |
| 晋升 | pitfalls/workflow/promotion-duplication |
| 精准定位 | pitfalls/workflow/broad-keyword-search |
| 经验沉淀 | pitfalls/workflow/promotion-duplication |
| 知识管理 | pitfalls/workflow/promotion-duplication |
| 前后端分类 | patterns/requirement/frontend-backend-classification |
| 需求规格说明书 | patterns/document/requirements-spec-template |
| 需求分析 | patterns/requirement/frontend-backend-classification, pitfalls/workflow/broad-keyword-search |
