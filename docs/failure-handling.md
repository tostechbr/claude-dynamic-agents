# Failure Handling

What happens when something goes wrong.

## Eval-first: capture failures before implementing

Inspired by the Agentic Engineering pattern: before spawning implementation agents, spawn an eval agent that identifies failure signatures upfront.

```
task entra
  → [eval-agent] analisa o task
      - o que pode dar errado?
      - quais edge cases existem?
      - quais dependências podem falhar?
  → orchestrator incorpora os riscos no ExecutionPlan
  → implementação começa com contexto de riscos conhecidos
```

This prevents the most common failure modes before they happen.

## Failure scenarios

### 1. Agent fails mid-task

The agent errors out or produces invalid output.

```
orchestrator detects failure via context.json status: "failed"
  → retries once with same config
  → if fails again → escala para o usuário com context do erro
```

### 2. PR reviewer rejects

The pr-reviewer finds critical issues.

```
pr-reviewer → status: "rejected", issues: [...]
  → fix-loop:
      orchestrator spawns fix-agent with the review issues as context
      fix-agent pushes fixes to the same worktree branch
      pr-reviewer runs again (max 2 retry rounds)
  → if still rejected after retries → escala para o usuário
```

### 3. Worktree conflict

Two parallel agents modify the same file.

```
worktree conflict detected at merge
  → synthesizer receives both versions + conflict context
  → synthesizer resolves conflict and produces merged output
  → if ambiguous → escala para o usuário
```

### 4. Task too complex

The orchestrator cannot confidently decompose the task.

```
orchestrator → confidence: "low"
  → runs /plan (dry-run mode) and shows the proposed plan to the user
  → waits for user confirmation before executing
```

## Escalation rules

The orchestrator escalates (stops and asks the user) when:
- An agent fails twice in a row
- The pr-reviewer rejects after 2 fix rounds
- A worktree conflict cannot be auto-resolved
- Task complexity is ambiguous
- A destructive action is about to happen (e.g., force push to main)

## context.json failure format

```json
{
  "outputs": {
    "backend-developer": {
      "status": "failed",
      "error": "Could not resolve import: app.database",
      "retry_count": 1,
      "worktree": "feat/jwt-auth-backend"
    }
  }
}
```

## Design principle

Fail loud, not silent. Every failure is visible in `context.json` and surfaced to the user if unrecoverable.
