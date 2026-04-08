# Models Catalog

Model selection directly impacts cost, speed, and quality. The orchestrator assigns a model to each agent based on task complexity and role.

## Available Models

| Model | ID | Strengths | Cost |
|-------|----|-----------|------|
| Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast, cheap, good for simple tasks | Low |
| Sonnet 4.6 | `claude-sonnet-4-6` | Best coding model, balanced | Medium |
| Opus 4.6 | `claude-opus-4-6` | Deepest reasoning, complex decisions | High |

---

## Selection Rules

### Use Haiku when:
- Task is simple and well-defined (no ambiguity)
- Agent produces boilerplate or templated output
- Agent role is mechanical, not creative (e.g. `pr-creator`)
- High volume, low stakes (formatting, simple transforms)

### Use Sonnet when:
- Writing or reviewing multi-file code changes
- Agent needs to reason about correctness and quality
- Most coding agents: `backend-developer`, `frontend-developer`, `db-architect`, `pr-reviewer`
- Default choice when unsure

### Use Opus when:
- The **orchestrator** itself — needs deep reasoning to decompose complex tasks
- The **brainstorm** agent — needs to infer implicit requirements and ambiguities
- Architectural decisions with long-term consequences
- Tasks where getting it wrong means expensive rework

---

## Quick Assignment Guide

| Agent Role | Model | Reason |
|------------|-------|--------|
| `orchestrator` | `opus` | Complex decomposition, catalog reasoning |
| `brainstorm` | `opus` | Inferring implicit requirements, flagging ambiguities |
| `db-architect` | `sonnet` | Schema design requires quality reasoning |
| `backend-developer` | `sonnet` | Multi-file code, correctness matters |
| `frontend-developer` | `sonnet` | Component architecture, TypeScript |
| `devops-agent` | `sonnet` | Docker, CI/CD, deployment config — precision required |
| `pr-creator` | `haiku` | Mechanical: git commit + gh pr create |
| `pr-reviewer` | `sonnet` | Needs to reason about code quality and security |
| `synthesizer` | `sonnet` | Integrates all outputs, writes final summary |

---

## Cost Awareness

For a typical full-stack feature run with 5 agents:
- `opus` (orchestrator + brainstorm) → ~2 calls
- `sonnet` (3–4 coding agents) → ~4 calls
- `haiku` (pr-creator) → ~1 call

Avoid using `opus` for agents that don't need deep reasoning — the cost difference is significant at scale.
