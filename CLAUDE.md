## Team-Aware Wiki Query Guide

> Knowledge lookup must follow team-first paths.

### Lookup Order (Required)

1. **Project Wiki** (highest priority)
   - `.agent-flow/wiki/`
   - `.dev-workflow/wiki/`

2. **Team Wiki**
   - `~/.agent-flow/platform/wiki/`
   - `~/.agent-flow/community/wiki/`

3. **Global Wiki** (index/legacy only)
   - `~/.agent-flow/wiki/`

### Practical Steps

1. Read team indexes first:
   - `Read ~/.agent-flow/platform/wiki/INDEX.md`
   - `Read ~/.agent-flow/community/wiki/INDEX.md`
2. If needed, grep by keyword in team wikis:
   - `Grep "{keyword}" ~/.agent-flow/platform/wiki/`
   - `Grep "{keyword}" ~/.agent-flow/community/wiki/`
3. Use global wiki only as fallback for topics/index artifacts.

## Team-Aware Skills Query Guide

> Skill lookup must use team directories first.

### Lookup Order (Required)

1. **Project Skills**
   - `.agent-flow/skills/`
   - `.dev-workflow/skills/`

2. **Team Skills**
   - `~/.agent-flow/platform/skills/`
   - `~/.agent-flow/community/skills/`

3. **Global Skills** (index/legacy only)
   - `~/.agent-flow/skills/`

### Practical Steps

1. Read team skill indexes first:
   - `Read ~/.agent-flow/platform/skills/INDEX.md`
   - `Read ~/.agent-flow/community/skills/INDEX.md`
2. Then grep by keyword if needed:
   - `Grep "{keyword}" ~/.agent-flow/platform/skills/`
   - `Grep "{keyword}" ~/.agent-flow/community/skills/`
3. Use global skills only as fallback for index/topic references.

## Team Routing Rule

- Framework/runtime/orchestration/governance issues -> prioritize **platform** assets.
- Business/integration/implementation/tooling scenarios -> prioritize **community** assets.

## Souls Path

Primary soul definitions are under:

- `~/.agent-flow/platform/souls/`
