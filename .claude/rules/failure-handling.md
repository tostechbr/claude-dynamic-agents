# Failure Handling Rules

Rules the orchestrator MUST follow when something goes wrong.

---

## Rule 1 — Fail loud, never silent

Every failure MUST be written to `context.json` immediately.
Never swallow an error or mark a failed task as done.

---

## Rule 2 — Agent failure retry

When an agent sets `status: "failed"`:

```
retry_count == 0 → retry once with same config
retry_count == 1 → escalate to user
```

On retry: spawn the same agent with the original config plus the error message added to `context`.

Never retry more than once automatically.

---

## Rule 3 — PR reviewer rejection loop

When `pr-reviewer` sets `status: "rejected"`:

```
round 1:
  → spawn fix-agent with:
      context: reviewer comments from context.json
      worktree: same branch as original code
  → fix-agent pushes fixes
  → spawn pr-reviewer again

round 2 (if still rejected):
  → escalate to user with:
      - original reviewer comments
      - fix-agent changes
      - remaining issues
```

Maximum 2 fix rounds. Never auto-merge a rejected PR.

---

## Rule 4 — Worktree conflict

When two parallel agents produce conflicting changes to the same file:

```
→ pass both versions to synthesizer with conflict flag
→ synthesizer attempts resolution
→ if synthesizer cannot resolve → escalate to user
```

---

## Rule 5 — Escalation conditions

STOP and ask the user when:

| Condition | What to show |
|-----------|-------------|
| Agent failed twice | Error message + context at failure |
| PR rejected after 2 rounds | Review comments + what fix-agent tried |
| Worktree conflict unresolvable | Both versions of the conflicting file |
| Task complexity is `high` and confidence is low | Proposed ExecutionPlan for review |
| Destructive action detected | Exact command + ask for confirmation |

**Destructive actions that always require confirmation:**
- Force push to any branch
- Deleting files or branches
- Dropping database tables
- Overwriting uncommitted changes

---

## Rule 6 — Partial success

If some agents succeeded and one failed:
- Do not discard successful work
- Save successful outputs to `context.json` with `status: "done"`
- Escalate only the failed component to the user
- User can choose: retry failed part, fix manually, or abandon run

---

## Rule 7 — Run timeout

If a run exceeds 15 minutes without a status update from any agent:
- Mark stale agent as `status: "failed"`, `error: "timeout"`
- Apply Rule 2 (retry once)
- If still stalled after retry, escalate to user
