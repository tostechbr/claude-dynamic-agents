# Failure Handling

What happens when something goes wrong.

## Failure scenarios

### 1. Agent fails mid-task

The agent errors out or produces invalid output.

```
orchestrator detects failure via context.json status: "failed"
  → retries once with same config + error message added to context
  → if fails again → escalates to user with full error context
```

### 2. PR reviewer rejects

The pr-reviewer finds critical issues.

```
pr-reviewer → status: "rejected"
  → fix-loop:
      orchestrator spawns fix-agent
        context: reviewer comments from context.json
        worktree: same branch as original code
      fix-agent pushes fixes
      pr-reviewer runs again (max 2 rounds)
  → if still rejected after 2 rounds → escalates to user
```

### 3. Worktree conflict

Two parallel agents modify the same file.

```
conflict detected → both versions passed to synthesizer with conflict flag
  → synthesizer resolves if possible
  → if ambiguous → escalates to user
```

### 4. Task too complex or ambiguous

The orchestrator is not confident about the decomposition.

```
orchestrator → complexity: "high" OR confidence: "low"
  → runs /plan dry-run and shows proposed ExecutionPlan to user
  → waits for confirmation before spawning agents
```

## Escalation conditions

The orchestrator stops and asks the user when:
- An agent fails twice in a row
- The pr-reviewer rejects after 2 fix rounds
- A worktree conflict cannot be auto-resolved
- Task complexity is high and confidence is low
- A destructive action is about to happen (e.g., force push to main)

## context.json failure format

```json
{
  "outputs": {
    "backend-developer": {
      "status": "failed",
      "summary": "Attempted to implement JWT auth — failed on database import resolution",
      "files_changed": [],
      "worktree": "feat/fastapi-backend-jwt-auth",
      "error": "Could not resolve import: app.database — module not found",
      "retry_count": 1,
      "trigger_event": null
    }
  }
}
```

## Partial success

If some agents succeeded and one failed, the orchestrator does not discard the successful work. Successful outputs remain in `context.json` with `status: "done"`. Only the failed component is escalated.

## Design principle

Fail loud, not silent. Every failure is immediately written to `context.json` and surfaced to the user if unrecoverable. No silent swallowing of errors.
