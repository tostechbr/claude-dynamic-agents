# claude-dynamic-agents

> Dynamic Agent Orchestration using Claude Code — an open source reference implementation.

## The Idea

Most Claude Code setups use **static orchestration**: you pre-define which agents run and in what order. This project demonstrates **dynamic orchestration**: the orchestrator uses LLM reasoning to decide at runtime which agents to spawn, how many, what skills/MCPs/model each one gets — and saves agents for reuse.

```
/tos "add JWT auth to the FastAPI backend"
        ↓
[Orchestrator reasons...]
  → classifica: backend, complexidade média
  → checa registry: "backend-developer" já existe? não → cria do catalog
  → plano: backend-developer → pr-creator → pr-reviewer
        ↓
[backend-developer]              skills: fastapi-patterns, security-patterns
  implements JWT auth            mcps: filesystem
        ↓
[pr-creator]                     mcps: filesystem, github
  git commit + gh pr create
        ↓
[pr-reviewer]                    skills: security-patterns
  gh pr diff → review comments   mcps: github
        ↓
[synthesizer] → PR #42 created, 2 review comments added
```

## Static vs Dynamic

| | Static | Dynamic |
|---|---|---|
| Agents | Pre-defined | Decided at runtime |
| Count | Fixed | Variable (1 to N) |
| Skills per agent | Fixed | Chosen from catalog |
| MCPs per agent | Fixed | Only what's needed |
| Model | Fixed | Chosen by complexity |
| Reuse | None | Registry of saved agents |
| Example | everything-claude-code | This repo |

## How It Works

### 1. Catalog — the palette

Before running, the orchestrator reads a curated catalog:

```
.claude/catalog/
├── skills.md    ← contextual knowledge (how to think about domains)
├── mcps.md      ← external tools (what agents can do)
└── models.md    ← when to use haiku / sonnet / opus
```

### 2. Registry — saved agents

Agents built from the catalog get saved for reuse:

```
.claude/registry/
├── index.md
└── react-developer.json   ← saved config from a previous run
```

Next time a similar task arrives, the orchestrator adapts the existing config instead of building from scratch.

### 3. ExecutionPlan

The orchestrator always produces a JSON plan before spawning:

```json
{
  "task": "add JWT auth",
  "agents": [
    {
      "role": "backend-developer",
      "model": "sonnet",
      "skills": ["fastapi-patterns", "security-patterns"],
      "mcps": ["filesystem"],
      "depends_on": null
    },
    {
      "role": "pr-creator",
      "model": "haiku",
      "skills": [],
      "mcps": ["filesystem", "github"],
      "depends_on": "backend-developer"
    },
    {
      "role": "pr-reviewer",
      "model": "sonnet",
      "skills": ["security-patterns"],
      "mcps": ["github"],
      "depends_on": "pr-creator"
    }
  ]
}
```

`depends_on: null` = runs immediately. Multiple `depends_on` = barrier (waits for all). Independent agents run in parallel.

### 4. Context propagation

Agents share state via two files in `workspace/{run-id}/`:
- `context.json` — single source of truth: plan, outputs, status per agent
- `activity.jsonl` — append-only event log for full run observability

No agent reads another agent's output files directly — only via `context.json`.

### 5. Failure handling

- Agent fails twice → escalates to user
- PR reviewer rejects → fix-loop (max 2 rounds) → escalates if unresolved
- Task ambiguous → `/plan` dry-run, waits for confirmation

## Project Structure

```
claude-dynamic-agents/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── settings.json
│   ├── catalog/              ← palette (static, curated)
│   │   ├── skills.md
│   │   ├── mcps.md
│   │   └── models.md
│   ├── registry/             ← saved agent configs (grows with use)
│   │   └── index.md
│   ├── agents/
│   │   ├── orchestrator.md   ← THE BRAIN
│   │   └── synthesizer.md
│   ├── skills/               ← skill implementations (15 installed)
│   │   ├── execution-plan/
│   │   ├── fastapi-patterns/
│   │   ├── react-patterns/
│   │   ├── postgres-patterns/
│   │   ├── security-patterns/
│   │   ├── frontend-design/
│   │   ├── search-first/
│   │   ├── agentic-engineering/
│   │   ├── api-design/
│   │   ├── deployment-patterns/
│   │   ├── verification-loop/
│   │   ├── using-git-worktrees/
│   │   ├── dispatching-parallel-agents/
│   │   ├── subagent-driven-development/
│   │   └── workflow-orchestration-patterns/
│   ├── rules/
│   │   ├── orchestration.md
│   │   ├── agent-contracts.md
│   │   └── failure-handling.md
│   └── commands/
│       ├── tos.md            ← /tos [what to build]
│       └── plan.md           ← /plan (dry-run, shows plan without executing)
├── projects/                 ← generated projects (monorepo mode)
│   └── {project-name}/       ← e.g. todo-app/, blog-platform/
├── workspace/
│   └── {run-id}/             ← ephemeral run outputs + context.json
├── examples/
│   ├── todo-app/
│   └── blog-platform/
└── docs/
    ├── architecture.md
    ├── catalog.md
    ├── agent-lifecycle.md
    ├── context-propagation.md
    ├── failure-handling.md
    └── pr-review-flow.md
```

## Status

Work in progress. Architecture and documentation defined, implementation pending.

Start with `docs/architecture.md` for the full picture.

## Contributing

Open source. Contributions welcome. See `docs/` for architecture decisions.
