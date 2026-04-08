# Failure Handling Rules

Rules the orchestrator MUST follow when something goes wrong.

---

## Rule 1 — Fail loud, never silent

Every failure MUST be written to `context.json` immediately.
Never swallow an error or mark a failed task as done.

---

## Rule 2 — Agent failure retry (Reaction: agent-failed)

**Trigger:** agent sets `status: "failed"` in `context.json`

**Reaction routing:**

```
retry_count == 0:
  → set trigger_event: "retry:failed(<role>) attempt=1"
  → spawn same agent with original config + error appended to context

retry_count == 1:
  → set status: "failed" (final)
  → escalate to user (Rule 5)
```

**Context passed to retry agent:**
```json
{
  "retry_for": "<role>",
  "previous_error": "<error from failed run>",
  "files_changed_so_far": ["<any partial work>"]
}
```

Never retry more than once automatically.

---

## Rule 3 — PR reviewer rejection loop (Reaction: pr-reviewer-rejected)

**Trigger:** `pr-reviewer` sets `status: "rejected"` in `context.json`

**Reaction routing:**

```
round 1:
  → set trigger_event: "reaction:pr-reviewer-rejected round=1"
  → spawn fix-agent with:
      worktree: same branch as original code
      context: {
        "reviewer_comments": "<comments from context.json outputs.pr-reviewer.summary>",
        "pr_url": "<url>",
        "files_to_fix": "<files_changed from rejected agent>"
      }
  → fix-agent pushes fixes
  → spawn pr-reviewer again with trigger_event: "reaction:pr-reviewer-rejected round=1"

round 2 (if still rejected):
  → escalate to user (Rule 5) with:
      - round 1 reviewer comments
      - what fix-agent changed (files_changed)
      - remaining issues from round 2 review
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
