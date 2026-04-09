# Models Catalog

Model selection directly impacts cost, speed, and quality. The orchestrator assigns a model to each agent based on task complexity and role.

## Available Models

| Model | ID | Strengths | Cost |
|-------|----|-----------|------|
| Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast, cheap, good for simple tasks | Low |
| Sonnet 4.6 | `claude-sonnet-4-6` | Best coding model, balanced | Medium |
| Opus 4.6 | `claude-opus-4-6` | Deepest reasoning, complex decisions | High |

---

## Assignment Rules — follow this table exactly

**Do not default everything to sonnet.** Each role has a specific model for a reason.

| Agent Role | Model | Full Model ID | Reason |
|------------|-------|---------------|--------|
| `orchestrator` | **opus** | `claude-opus-4-6` | Complex decomposition, needs deep reasoning to build the right plan |
| `brainstorm` | **opus** | `claude-opus-4-6` | Inferring implicit requirements, flagging ambiguities |
| `backend-developer` | **sonnet** | `claude-sonnet-4-6` | Multi-file code, correctness matters |
| `frontend-developer` | **sonnet** | `claude-sonnet-4-6` | Component architecture, TypeScript, styling |
| `test-developer` | **sonnet** | `claude-sonnet-4-6` | Writing correct async tests requires reasoning |
| `db-architect` | **sonnet** | `claude-sonnet-4-6` | Schema design requires quality reasoning |
| `devops-agent` | **sonnet** | `claude-sonnet-4-6` | Docker, CI/CD — precision required |
| `pr-reviewer` | **sonnet** | `claude-sonnet-4-6` | Needs to reason about code quality and security |
| `pr-creator` | **haiku** | `claude-haiku-4-5-20251001` | Mechanical: git commit + gh pr create, no reasoning needed |
| `synthesizer` | **haiku** | `claude-haiku-4-5-20251001` | Simple aggregation of outputs, no creativity needed |

---

## When to deviate

Override the table only in these cases:

| Situation | Override |
|-----------|----------|
| Task `complexity: high` for a coding agent | upgrade to `opus` |
| Agent is doing pure file operations or templating | downgrade to `haiku` |
| Budget constraint explicitly mentioned by user | downgrade all by one tier |

---

## Why model diversity matters

When the LangSmith trace shows every agent using `claude-sonnet-4-6`, it means the orchestrator is not reasoning about model selection — it's defaulting. The whole point of dynamic orchestration is that **different agents get different models based on what they actually need**.

A correct run should show:
```
orchestrator      → claude-opus-4-6          (planning)
backend-developer → claude-sonnet-4-6        (coding)
test-developer    → claude-sonnet-4-6        (testing)
pr-creator        → claude-haiku-4-5-20251001 (mechanical)
pr-reviewer       → claude-sonnet-4-6        (analysis)
synthesizer       → claude-haiku-4-5-20251001 (aggregation)
```

---

## Cost reference

For a typical backend feature run (6 agents):
- `opus` × 1 (orchestrator) → most expensive, but called once
- `sonnet` × 3–4 (coding agents) → medium cost, most of the work
- `haiku` × 2 (pr-creator + synthesizer) → cheap, fast

Avoid using `opus` for agents that don't need deep reasoning — the cost difference is significant at scale.
