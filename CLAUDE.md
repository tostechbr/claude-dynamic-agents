# CLAUDE.md

Project instructions for Claude Code when working in this repository.

## What This Project Is

`claude-dynamic-agents` is an open source reference implementation of **Dynamic Agent Orchestration** using Claude Code. It demonstrates how an orchestrator agent can use LLM reasoning to decide at runtime which sub-agents to spawn, how many, and with what context — including skills, MCPs, and models tailored per task.

This is distinct from static orchestration (like everything-claude-code) where agents and their roles are pre-defined.

## Core Flow

```
/tos [user input]
    ↓
orchestrator.md
  1. classifica a tarefa (tipo, complexidade)
  2. checa registry: agente adequado já existe?
  3. se não → monta config do catalog → salva no registry
  4. gera ExecutionPlan JSON
    ↓
N agentes em paralelo/sequential (baseado em depends_on)
    ↓
synthesizer.md  ← agrega outputs via context.json
```

## Architecture Decisions

### Catalog vs Registry
- `catalog/` — paleta estática de ingredientes (skills, MCPs, models). Curado manualmente.
- `registry/` — agentes já montados e salvos de runs anteriores. Cresce com o uso.

The orchestrator checks the registry first before building from the catalog.

### Why separate commands/ and agents/?
- `commands/` are entry points (slash commands the user types)
- `agents/` are permanent agents (orchestrator, synthesizer)
- Task agents are ephemeral — spawned from catalog/registry, not stored as files

### Context propagation
Agents communicate via two files in `workspace/{run-id}/`:
- `context.json` — single source of truth: plan, outputs, status per agent
- `activity.jsonl` — append-only event log: one JSON object per line (started, tool_call, done, failed, blocked, rejected)

No agent reads another agent's output files directly — only via `context.json`.

### Failure handling
- Agent fails twice → escalate to user
- PR reviewer rejects → fix-loop (max 2 rounds) → escalate if unresolved
- Task ambiguous → /tos runs brainstorm first, or use /plan for explicit dry-run
- See `rules/failure-handling.md`

### Monorepo mode
When `/tos` is run inside this repo (detected by the presence of `.claude/agents/orchestrator.md`), generated projects go into `projects/{project-name}/` instead of the current working directory. Project name is inferred from the task in kebab-case. Git worktrees branch as `feat/{project-name}-{feature}` off this repo.

### Skills vs MCPs
- **Skills** = contextual knowledge injected into agent reasoning (how to think)
- **MCPs** = external tools the agent can call (what it can do)

### Execution plan format
The orchestrator always produces a JSON plan before spawning agents. `depends_on` controls parallel vs sequential execution. See `skills/execution-plan/` for schema.

## Implementation Order

Build in this order (each depends on the previous):

1. `CLAUDE.md` ← this file (done)
2. `README.md` ← project overview (done)
3. `docs/` ← architecture documentation (done)
4. `.claude/catalog/skills.md` ← available skills + when to use
5. `.claude/catalog/mcps.md` ← available MCPs + what they enable
6. `.claude/catalog/models.md` ← model selection rules
7. `.claude/registry/index.md` ← initially empty, grows with use
8. `.claude/settings.json` ← permissions config
9. `.claude/rules/orchestration.md` ← orchestration rules
10. `.claude/rules/agent-contracts.md` ← agent communication schema
11. `.claude/rules/failure-handling.md` ← failure + escalation rules
12. `.claude/skills/execution-plan/SKILL.md` ← plan JSON schema
13. `.claude/skills/fastapi-patterns/SKILL.md`
14. `.claude/skills/react-patterns/SKILL.md`
15. `.claude/skills/postgres-patterns/SKILL.md`
16. `.claude/agents/brainstorm.md` ← pre-analysis agent
17. `.claude/agents/orchestrator.md` ← THE core agent
18. `.claude/agents/synthesizer.md`
19. `.claude/commands/tos.md` ← /tos [task] — main entry point
20. `.claude/commands/plan.md` ← /plan [task] — dry-run mode

## Key Principles

- The orchestrator must always produce a structured ExecutionPlan before spawning agents
- Check the registry before building from the catalog — reuse when possible
- Agents are independent and ephemeral — they receive all context they need via context.json
- Skills = how to think, MCPs = what to do
- Fail loud, not silent — every failure is visible and escalated if unrecoverable
- Examples in `examples/` are actual generated outputs, not templates
