---
description: Dynamic agent orchestration — spawns the orchestrator as a subagent to analyze your task, build an ExecutionPlan, and coordinate specialized agents.
---

# /tos

## What you must do — exactly in this order

1. Read the full content of `.claude/agents/orchestrator.md`
2. Use the **`Agent` tool** to spawn the orchestrator as a subagent — pass the full file content as the agent prompt, followed by the task below
3. Wait for the orchestrator subagent to complete
4. Report the final result to the user

## ⚠️ CRITICAL: use the Agent tool, not Bash

```
✅ CORRECT — use this:
Agent(
  [full content of .claude/agents/orchestrator.md]

  ---
  ## Task
  $ARGUMENTS

  ## Run context
  Working directory: <cwd>
  Today's date: <date>
)

❌ WRONG — never do this:
Bash("claude -p '...'")
Bash(PROMPT='...' claude ...)
```

The Agent tool creates a proper nested subagent that appears in LangSmith traces with the correct name (`orchestrator`). Bash creates an invisible isolated process with no tracing.

## Why this matters

- `Agent` tool → subagents appear nested in LangSmith: `orchestrator → frontend-developer → pr-creator`
- `Bash(claude -p)` → runs in isolation, no nesting, no naming in LangSmith

## After spawning

The orchestrator handles everything from here:
- Classifies the task
- Checks the registry for reusable agents
- Generates an ExecutionPlan
- Spawns specialized subagents (each via Agent tool)
- Monitors `workspace/{run_id}/context.json`
- Runs the synthesizer last
- Reports back to you

---

$ARGUMENTS
