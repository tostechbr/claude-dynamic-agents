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

## Installed skills (15 total)

All skills live in `.claude/skills/`. The orchestrator assigns them per agent role.

**Local skills (custom for this project):**

| Skill | When to use |
|-------|-------------|
| `execution-plan` | Orchestrator only — defines the JSON plan schema |
| `fastapi-patterns` | Backend agents writing or reviewing FastAPI code |
| `react-patterns` | Frontend agents writing or reviewing React/TypeScript |
| `postgres-patterns` | DB agents designing schemas, migrations, or queries |
| `security-patterns` | Any agent handling auth, input validation, sensitive data |

**Community skills (installed via skillfish / Anthropic):**

| Skill | Source | When to use |
|-------|--------|-------------|
| `frontend-design` | Anthropic | Frontend agent — distinctive UIs, avoids AI slop aesthetics |
| `search-first` | affaan-m/everything-claude-code | Brainstorm + coding agents — research before implementing |
| `agentic-engineering` | affaan-m/everything-claude-code | Orchestrator — eval-first cycles, cost-aware model routing |
| `api-design` | affaan-m/everything-claude-code | Backend agent — REST naming, status codes, versioning |
| `deployment-patterns` | affaan-m/everything-claude-code | Devops agent — Docker, CI/CD, production deployments |
| `verification-loop` | affaan-m/everything-claude-code | PR reviewer + synthesizer — multi-stage quality assurance |
| `using-git-worktrees` | Antigravity | Any code-writing agent needing branch isolation |
| `dispatching-parallel-agents` | Antigravity | Orchestrator — spawning independent sub-tasks in parallel |
| `subagent-driven-development` | Antigravity | Orchestrator — multi-step implementation plans |
| `workflow-orchestration-patterns` | Antigravity | Orchestrator — durable, sequential workflow design |

## Available MCPs

| MCP | Tools | When to use |
|-----|-------|-------------|
| `filesystem` | read, write, edit, list files | Any agent that reads or writes files |
| `github` | create PR, review, list commits | `pr-creator`, `pr-reviewer` |
| `context7` | fetch live library docs | Any agent working with specific lib versions |
| `memory` | read/write agent registry | `orchestrator` only |

## Model selection

```
haiku    → simple, mechanical tasks (pr-creator: git commit + gh pr create)
sonnet   → most coding tasks, multi-file changes, review, synthesis
opus     → orchestrator + brainstorm (deep reasoning, task decomposition)
```

## How the orchestrator uses it

The orchestrator reads the catalog as part of its context, then assigns each agent exactly what it needs:

```json
{
  "role": "backend-developer",
  "model": "sonnet",
  "skills": ["fastapi-patterns", "api-design", "security-patterns", "using-git-worktrees"],
  "mcps": ["filesystem", "context7"]
}
```

- `skills` → injected as context so the agent knows *how to think*
- `mcps` → tools available so the agent knows *what it can do*

No agent gets skills or MCPs it doesn't need — minimizes context bloat.
