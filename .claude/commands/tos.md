---
description: Dynamic agent orchestration — analyzes your task, builds an ExecutionPlan, and spawns specialized agents to carry it out.
---

# /tos

Runs the full dynamic orchestration pipeline for any development task.

## Usage

```
/tos <task description>
```

## Examples

```
/tos add JWT auth to the FastAPI backend
/tos create a submit button component with tests
/tos build a user profile page with avatar upload
/tos fix the 500 error on the /users endpoint
```

## What happens

1. The **orchestrator** receives your task
2. Classifies complexity and type
3. Optionally runs **brainstorm** to structure requirements
4. Checks the **registry** for reusable agent configs
5. Generates an **ExecutionPlan**
6. Spawns specialized agents (in parallel or sequentially)
7. Monitors execution via `workspace/{run_id}/context.json`
8. **Synthesizer** aggregates all outputs
9. Returns a final report with what was built, files changed, and PR URL if created

## Notes

- For `high` complexity tasks, the orchestrator will show the plan and ask for confirmation first
- Run outputs are saved to `workspace/{run_id}/` for full observability
- Use `/plan <task>` to preview the ExecutionPlan without executing

---

$ARGUMENTS
