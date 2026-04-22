# AgentFlow

> Universal AI Agent Workflow Protocol for Claude Code

AgentFlow is a structured development workflow system that transforms Claude Code into a rule-governed, multi-agent collaboration platform with quality controls and knowledge management.

## Architecture

```text
Layer 1: ~/.agent-flow/          -> Global control plane (config, runtime state, legacy indexes)
Layer 2: ~/.agent-flow/platform/ -> Platform team assets (core framework)
Layer 3: ~/.agent-flow/community/-> Community team assets (business/integration)
Layer 4: .agent-flow/            -> Project-local assets (project memory/state)
Layer 5: .dev-workflow/          -> Dev-local supplements
```

### Team Asset Layout

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

## Team Responsibilities

- **Platform Team**: framework runtime, orchestration, governance, core cognition loop enablement.
- **Community Team**: business workflows, external integrations, implementation patterns, domain/tool practices.

## Core Cognitive Cycle

Every task follows a 6-phase cycle:

```text
THINK -> PLAN -> EXECUTE -> VERIFY -> REFLECT -> EVOLVE
```

## Resource Lookup (Team-First)

1. Project layer: `.agent-flow/` and `.dev-workflow/`
2. Team layer: `~/.agent-flow/platform/` and `~/.agent-flow/community/`
3. Global layer: only for shared control/index artifacts

## Agent Roles

Primary role definitions are stored in:

- `~/.agent-flow/platform/souls/main.md`
- `~/.agent-flow/platform/souls/planner.md`
- `~/.agent-flow/platform/souls/coder.md`
- `~/.agent-flow/platform/souls/researcher.md`
- `~/.agent-flow/platform/souls/verifier.md`
- `~/.agent-flow/platform/souls/architect.md`
- `~/.agent-flow/platform/souls/writer.md`

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

1. Initialize project:

```bash
agent-flow init --dev-workflow
```

2. Read `CLAUDE.md` for team-aware resource lookup rules.
3. Run tasks with team-first search and verification gates.

## License

Private - Internal use only.
