# Skills Catalog

Skills inject contextual knowledge into an agent's reasoning. They teach the agent *how to think* about a domain — not what tools to use.

## How the orchestrator uses this

For each agent in the ExecutionPlan, pick skills that match:
1. The agent's role (backend? frontend? database?)
2. The specific task requirements (auth? schema design? UI component?)

Never assign skills the agent doesn't need — it bloats context.

---

## Local Skills

Installed at `.claude/skills/`. Available to all agents in this project.

| Skill | Path | When to assign |
|-------|------|----------------|
| `execution-plan` | `skills/execution-plan/` | Orchestrator only — defines the JSON plan schema |
| `fastapi-patterns` | `skills/fastapi-patterns/` | Any agent writing or reviewing FastAPI code |
| `react-patterns` | `skills/react-patterns/` | Any agent writing or reviewing React/TypeScript code |
| `postgres-patterns` | `skills/postgres-patterns/` | Any agent designing schemas, writing migrations, or optimizing queries |
| `security-patterns` | `skills/security-patterns/` | Any agent writing or reviewing code with auth, input validation, or sensitive data |

---

## Installed Community Skills

Installed at `.claude/skills/`. Sourced from community (Antigravity registry / Anthropic).

| Skill | Path | When to assign |
|-------|------|----------------|
| `using-git-worktrees` | `skills/using-git-worktrees/` | Any agent that writes code and needs branch isolation |
| `dispatching-parallel-agents` | `skills/dispatching-parallel-agents/` | Orchestrator — when task has independent sub-tasks |
| `subagent-driven-development` | `skills/subagent-driven-development/` | Orchestrator — when executing a multi-step implementation plan |
| `workflow-orchestration-patterns` | `skills/workflow-orchestration-patterns/` | Orchestrator — for durable, sequential workflow design |
| `frontend-design` | `skills/frontend-design/` | Frontend agent — produces distinctive UIs, avoids generic AI aesthetics |
| `search-first` | `skills/search-first/` | Brainstorm + any coding agent — research existing libs before writing code |
| `agentic-engineering` | `skills/agentic-engineering/` | Orchestrator — eval-first cycles, cost-aware model routing, task decomposition |
| `deployment-patterns` | `skills/deployment-patterns/` | Devops agent — Docker, CI/CD, production-ready deployment workflows |
| `verification-loop` | `skills/verification-loop/` | PR reviewer + synthesizer — multi-stage quality assurance |
| `api-design` | `skills/api-design/` | Backend agent — REST naming, status codes, versioning, response envelopes |

---

## Quick Assignment Guide

| Agent Role | Recommended Skills |
|------------|-------------------|
| `orchestrator` | `execution-plan`, `agentic-engineering`, `dispatching-parallel-agents`, `subagent-driven-development`, `workflow-orchestration-patterns` |
| `brainstorm` | `search-first` |
| `db-architect` | `postgres-patterns` |
| `backend-developer` | `fastapi-patterns`, `api-design`, `security-patterns`, `using-git-worktrees` |
| `frontend-developer` | `react-patterns`, `frontend-design`, `using-git-worktrees` |
| `devops-agent` | `deployment-patterns`, `using-git-worktrees` |
| `pr-creator` | `using-git-worktrees` |
| `pr-reviewer` | domain skill + `security-patterns` + `verification-loop` (e.g. `fastapi-patterns`, `security-patterns` for backend PRs) |
| `synthesizer` | _(none — reads context.json directly)_ |

---

## Adding New Skills

To add a local skill:
```
mkdir .claude/skills/<name>
# create .claude/skills/<name>/SKILL.md
```

To install from community:
```bash
npx skillfish add <owner>/<repo> --project
# or copy from ~/.gemini/antigravity/skills/<name>/SKILL.md
```
