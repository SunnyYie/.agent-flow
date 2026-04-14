# AgentFlow

> Universal AI Agent Workflow Protocol for Claude Code

AgentFlow is a structured development workflow system that transforms Claude Code into a rule-governed, multi-agent collaboration platform with quality controls and knowledge management.

## Architecture

```
Layer 1: ~/.agent-flow/          → Global (skills, wiki, souls, whitelist)
Layer 2: .agent-flow/            → Project (config, experience, state)
Layer 3: .dev-workflow/           → Dev (agent roles, skills by agent, wiki with schema)
```

**Principle: Don't duplicate, only supplement.** Layer 3 references Layer 1, doesn't repeat it.

## Core Cognitive Cycle

Every task follows a 6-phase cognitive cycle:

```
THINK → PLAN → EXECUTE → VERIFY → REFLECT → EVOLVE
```

- **THINK** — Analyze requirements, search Skills/Wiki/Soul before acting
- **PLAN** — Decompose requirements, document analysis and plan
- **EXECUTE** — Implement with TDD, parallel agents for independent tasks
- **VERIFY** — Multi-agent verification, self-questioning check
- **REFLECT** — Promote universal experiences to `~/.agent-flow/`
- **EVOLVE** — Update Wiki, Skills, Soul with new knowledge

## Agent Roles

| Role | File | When to Activate |
|------|------|-----------------|
| Main | `souls/main.md` | Always — supervises, verifies, accumulates |
| Planner | `souls/planner.md` | Task decomposition |
| Coder | `souls/coder.md` | Code implementation (TDD) |
| Writer | `souls/writer.md` | Document drafting |
| Researcher | `souls/researcher.md` | Information research |
| Verifier | `souls/verifier.md` | Quality verification at checkpoints |
| Architect | `souls/architect.md` | Architecture design and ADR |

## Skills (40+)

Skills are reusable, searchable knowledge units that guide agent behavior:

| Category | Skills |
|----------|--------|
| Workflow | `pre-flight-check`, `task-complexity`, `phase-review`, `self-questioning`, `requirement-decomposition` |
| Code | `code-implementation`, `code-review`, `tdd-workflow`, `testing-strategies`, `implementation-patterns` |
| Knowledge | `knowledge-search`, `experience-promotion`, `critical-knowledge`, `ai-context-management` |
| Design | `architecture-design`, `workflow-design`, `prompt-engineering`, `claude-code-design` |
| Tools | `tool-precheck`, `git-workflow`, `gitlab-mr-creation`, `feishu-doc-access`, `web-research` |
| Quality | `security-checks`, `error-recovery`, `acceptance-check`, `subtask-guard`, `content-filter` |
| Advanced | `orchestrator-worker`, `agent-orchestration`, `prompt-caching-optimization`, `pydantic-patterns` |

## Enforcement Hooks (12)

Python scripts that enforce workflow rules at runtime:

| Hook | Purpose |
|------|---------|
| `preflight-guard.py` | Enforce pre-flight check before any task |
| `preflight-enforce.py` | Validate pre-flight completion |
| `thinking-chain-enforce.py` | Enforce cognitive cycle phases |
| `search-tracker.py` | Track search-before-execute compliance |
| `promotion-guard.py` | Enforce experience promotion after REFLECT |
| `self-questioning-enforce.py` | Enforce self-questioning before REFLECT |
| `user-acceptance-guard.py` | Block push/MR without user acceptance |
| `tool-precheck-guard.py` | Enforce tool pre-check for critical tools |
| `dev-workflow-enforce.py` | Enforce dev workflow compliance |
| `project-structure-enforce.py` | Validate project structure |
| `context-guard.py` | Guard against context window overflow |
| `error-search-remind.py` | Remind to search before error recovery |

## Wiki Knowledge Base

```
wiki/
├── INDEX.md              # Global navigation
├── patterns/             # Success patterns
│   ├── feishu/           # Feishu/Lark patterns
│   ├── workflow/         # Workflow patterns (3-agent model, RPI, cross-model)
│   ├── architecture/     # Architecture patterns (ADR, error classification)
│   ├── document/         # Document conversion templates
│   ├── requirement/      # Requirement analysis patterns
│   └── gitlab/           # Self-hosted GitLab patterns
├── pitfalls/             # Lessons learned
│   ├── feishu/           # Lark CLI parameter traps
│   ├── workflow/         # Execute-without-search, over-search, skip-plan
│   ├── security/         # Path traversal, injection
│   ├── environment/      # venv path, tool config
│   ├── llm-coding/       # Overcomplication, drive-by refactoring, context pollution
│   └── react-native/     # Jest/Babel compatibility
├── concepts/             # Core concepts
│   ├── agent-roles.md    # Multi-role collaboration
│   ├── memory-systems.md # 4-layer memory architecture
│   ├── karpathy-principles.md # LLM coding principles
│   └── ...
├── tools/                # Tool documentation
└── decisions/            # Architecture Decision Records
```

## 12 Iron Laws

1. **Search First** — Always check Skills/Soul/Wiki before doing anything new
2. **Requirement Decomposition** — Break requirements into change points (CP1, CP2...), confirm each with user
3. **Precise Location** — Code search from narrow to wide (L1 exact → L2 fuzzy → L3 route → L4 global)
4. **Git Safety** — No commits on main; pull before branching; search Skill before MR
5. **Experience Promotion** — REFLECT must promote universal experiences to `~/.agent-flow/`
6. **Ask When Uncertain** — Must pause and ask when requirements are ambiguous
7. **Multi-Agent Parallelism** — Verification, coding, testing must use parallel agents
8. **Complexity Quantification** — Every task must run 5-dimensional complexity scoring
9. **Self-Questioning** — Must execute self-questioning after VERIFY, before REFLECT
10. **Critical Knowledge Priority** — Check Soul.md critical knowledge before using external tools
11. **Deep Clarification** — Exhaust assumptions,追问 boundary scenarios, confirm impact scope before coding
12. **User Acceptance Gate** — No push/MR without explicit user acceptance confirmation

## Tool Whitelist

```yaml
auto_install:         # No confirmation needed
  - git, docker, npm, pip, python3, node, gh, uv, curl, wget, jq, yq

need_confirmation:    # Requires user approval
  - lark-cli, cargo, brew, apt-get, yum, pipx, npx, markitdown

blacklist:            # Prohibited
  - rm -rf /, mkfs, dd if=, format
```

## Multi-Agent Parallel Scenarios

| Phase | Parallel Strategy | Reason |
|-------|-------------------|--------|
| Requirements review | Dual review: Verifier + Main Agent | Single perspective misses issues |
| Coding | Multiple independent Executor Agents | Serial = wasted time |
| Code review | Independent code-reviewer Agent | Developer blind spots |
| Test acceptance | Verifier + Main Agent dual acceptance | Single acceptance = low quality |

## Task Complexity Routing

| Level | Score | Workflow | Search Depth |
|-------|-------|----------|-------------|
| Simple | 1-2 | Fast path | 2 steps |
| Medium | 3-4 | Standard path with checkpoints | 5 steps |
| Complex | 5+ | Strict path with all gates | 5 steps + WebSearch |

## Configuration

`config.yaml`:
```yaml
default_platform: claude-code
log_level: INFO
critical_tools:
  - lark-cli
  - glab
  - gh
  - docker
```

## Quick Start

1. Initialize a project:
   ```bash
   agent-flow init --dev-workflow
   ```

2. Read `Agent.md` after initialization

3. Follow the pre-flight check protocol before each task

## License

Private — Internal use only.
