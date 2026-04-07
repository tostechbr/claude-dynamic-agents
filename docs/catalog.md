# The Catalog

The catalog is the orchestrator's palette. Instead of pre-assigning skills/MCPs/models to fixed agents, the orchestrator picks from the catalog at runtime based on the task.

## Key distinction: Skills vs MCPs

| | Skills | MCPs |
|---|---|---|
| What | Teaches the agent **how to think** | Lets the agent **act** on external systems |
| Execution | LLM-driven (non-deterministic) | API/schema-driven (deterministic) |
| Format | Markdown (SKILL.md) | JSON-RPC tool schema via server |
| When | Consistent reasoning or workflows | Real-world actions or data access |

## Structure

```
.claude/catalog/
├── skills.md    ← contextual knowledge injected into agent reasoning
├── mcps.md      ← external tools the agent can call
└── models.md    ← when to use haiku / sonnet / opus
```

## Two types of skills

Skills can be local (in this repo) or from the marketplace (installed via skillfish):

```
local:
  fastapi-patterns   → .claude/skills/fastapi-patterns/SKILL.md
  react-patterns     → .claude/skills/react-patterns/SKILL.md
  postgres-patterns  → .claude/skills/postgres-patterns/SKILL.md
  security-patterns  → .claude/skills/security-patterns/SKILL.md

marketplace:
  gh-issues          → openclaw/gh-issues (automates GitHub issue lifecycle)
  agentic-engineering → affaan-m/agentic-engineering (eval-first execution loop)
  coding-orchestrator → openclaw/coding-agent (background agents + worktrees)
```

The orchestrator selects from both. Marketplace skills must be installed first.

## mcps.md (example entries)

```
filesystem   → read/write files on disk (almost always needed)
github       → gh CLI: create PRs, branches, review comments
database     → direct DB access for schema inspection
```

## models.md (selection rules)

```
haiku    → simple, repetitive tasks (boilerplate, formatting, pr-creator)
sonnet   → most coding tasks, multi-file changes, review
opus     → orchestrator itself, complex architectural decisions
```

## How the orchestrator uses it

The orchestrator reads the catalog as part of its context, then assigns each agent exactly what it needs:

```json
{
  "role": "backend-developer",
  "model": "sonnet",
  "skills": ["fastapi-patterns", "security-patterns"],
  "mcps": ["filesystem", "github"]
}
```

- `skills` → injected as context so the agent knows *how to think*
- `mcps` → tools available so the agent knows *what it can do*

No agent gets skills or MCPs it doesn't need — minimizes context bloat.
