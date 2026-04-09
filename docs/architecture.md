# Architecture

## Overview

```
task arrives (/tos "build a submit button")
        ↓
[orchestrator]
  1. classify task (type, complexity)
  2. check agents/: does a matching agent already exist?
  3. if not → build config from catalog → save to .claude/agents/ after run
  4. generate ExecutionPlan JSON
        ↓
[brainstorm]  ← runs for medium/high complexity
  analyzes explicit/implicit requirements, ambiguities
        ↓
[agents in parallel or sequential]
  backend-developer → pr-creator → pr-reviewer
        ↓
[synthesizer]
  aggregates outputs via context.json → final report
```

---

## Two distinct layers

### Catalog (static, manually curated)
The palette of available ingredients. Does not change with usage.

```
.claude/catalog/
├── skills.md    ← domain knowledge (how to think about problems)
├── mcps.md      ← external tools (what agents can do)
└── models.md    ← model selection rules
```

### Registry (dynamic, grows with use)
Agent configs saved from previous runs. The orchestrator checks here before building from scratch.

Dynamic agents are saved as `.md` files directly inside `.claude/agents/` — the same folder where permanent agents live. Claude Code reads the `name:` frontmatter from these files and uses it to label subagents correctly in LangSmith traces.

```
.claude/agents/
├── orchestrator.md       ← permanent
├── brainstorm.md         ← permanent
├── synthesizer.md        ← permanent
├── backend-developer.md  ← saved after run 2026-04-08-001
├── test-developer.md     ← saved after run 2026-04-08-002
└── ...                   ← new roles added automatically after each successful /tos run
```

`registry/index.md` maintains the summary index and agent `.md` template only.

Each agent `.md` file contains frontmatter (name, model, tools), a standard contract section, a saved configuration table, and a Run History table the orchestrator uses to understand past usage patterns.

---

## Task classification

Before spawning, the orchestrator classifies:

| Field | Example |
|-------|---------|
| type | frontend / backend / fullstack / infra / fix / other |
| complexity | low / medium / high |
| needs_git | true / false |
| suggested agents | backend-developer, pr-creator, pr-reviewer |
| execution | sequential / parallel / mixed |

This prevents over-engineering: adding a button doesn't need 5 agents.

---

## Parallel vs sequential execution

```json
{
  "agents": [
    { "role": "db-architect",       "depends_on": null },
    { "role": "backend-developer",  "depends_on": "db-architect" },
    { "role": "frontend-developer", "depends_on": "db-architect" },
    { "role": "pr-creator",         "depends_on": ["backend-developer", "frontend-developer"] },
    { "role": "pr-reviewer",        "depends_on": "pr-creator" }
  ]
}
```

- `depends_on: null` → can run immediately
- `depends_on: ["A", "B"]` → waits for both to complete (barrier)
- Agents with no dependency between them run in parallel

---

## Monorepo mode

When `/tos` runs inside this repo, generated code goes to `projects/{name}/` instead of the current directory:

| Condition | Mode | Code goes to |
|-----------|------|--------------|
| `.claude/agents/orchestrator.md` exists in cwd | Monorepo | `projects/{project-name}/` |
| Otherwise | External | Current working directory |

---

## Full folder structure

```
claude-dynamic-agents/
├── CLAUDE.md
├── README.md
├── projects/                     ← generated projects (monorepo mode)
│   └── {project-name}/
├── .claude/
│   ├── settings.json
│   ├── catalog/
│   │   ├── skills.md
│   │   ├── mcps.md
│   │   └── models.md
│   ├── registry/
│   │   └── index.md              ← summary index + agent .md template
│   ├── agents/                   ← ALL agents live here (permanent + dynamic)
│   │   ├── orchestrator.md       ← THE BRAIN (permanent)
│   │   ├── brainstorm.md         ← pre-analysis for medium/high complexity (permanent)
│   │   ├── synthesizer.md        ← permanent
│   │   └── ...                   ← dynamic agents saved here after each successful run
│   ├── skills/                   ← 15 skills installed
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
│       ├── tos.md                ← /tos [task] — main entry point
│       └── plan.md               ← /plan (dry-run)
├── workspace/
│   └── {run-id}/                 ← ephemeral run outputs
│       ├── context.json          ← shared state between agents
│       └── activity.jsonl        ← append-only event log (observability)
├── examples/
│   ├── todo-app/
│   └── blog-platform/
└── docs/
    ├── architecture.md           ← this file
    ├── catalog.md
    ├── agent-lifecycle.md
    ├── context-propagation.md
    ├── failure-handling.md
    ├── observability.md
    └── pr-review-flow.md
```
