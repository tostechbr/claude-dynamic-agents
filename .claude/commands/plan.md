---
description: Dry-run mode — shows the ExecutionPlan the orchestrator would generate for a task, without spawning any agents or writing any files.
---

# /plan

Preview what `/tos` would do before committing to execution.

## Usage

```
/plan <task description>
```

## Examples

```
/plan add JWT auth to the FastAPI backend
/plan build a checkout flow with Stripe
```

## What happens

1. Runs the full orchestrator reasoning pipeline (classify → brainstorm → registry check)
2. Generates the ExecutionPlan JSON
3. **Stops before spawning any agents**
4. Prints a human-readable breakdown of the plan

## Output format

```
## Plan for: <task>

Complexity: medium | high
Type: backend | frontend | fullstack

Agents (in execution order):
  1. [parallel] db-architect      model: sonnet  skills: postgres-patterns
  2. [parallel] backend-developer model: sonnet  skills: fastapi-patterns, security-patterns
  3. [after 1,2] pr-creator       model: haiku   mcps: filesystem, github
  4. [after 3]   pr-reviewer      model: sonnet  skills: security-patterns
  5. [after 4]   synthesizer      model: sonnet

Estimated agents: 5
Registry hits: db-architect (reused from 2026-04-07-001)

Run /tos <task> to execute.
```

## When to use

- Before running a `high` complexity task you're unsure about
- To debug how the orchestrator decomposes a task
- To understand which agents and skills would be selected

---

$ARGUMENTS
