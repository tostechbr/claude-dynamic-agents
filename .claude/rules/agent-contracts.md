# Agent Contracts

Rules every agent MUST follow for inter-agent communication.

---

## The shared state: context.json

Every run has a single source of truth at `workspace/{run_id}/context.json`.

**Agents MUST:**
- Read `context.json` before starting their task
- Write their output summary to `context.json` when done
- Never read another agent's output files directly — only via `context.json`

For run observability (traces, tool calls, subagent nesting), see `docs/observability.md`.

---

## context.json schema

```json
{
  "run_id": "2026-04-07-001",
  "task": "original user input",
  "task_brief": { },
  "plan": { },
  "target_dir": "projects/todo-app | null",
  "status": "running | completed | failed",
  "outputs": {
    "{role}": {
      "status": "pending | running | done | failed | waiting_input | blocked",
      "summary": "string — what was accomplished",
      "files_changed": ["path/to/file.py"],
      "worktree": "feat/branch-name | null",
      "error": "string | null",
      "retry_count": 0,
      "trigger_event": "string | null"
    }
  }
}
```

### Agent status semantics

| Status | Meaning |
|--------|---------|
| `pending` | Not yet started (dependency not done) |
| `running` | Currently executing |
| `done` | Completed successfully |
| `failed` | Errored — see `error` field |
| `waiting_input` | Paused waiting for human confirmation (high complexity plan, destructive action) |
| `blocked` | A dependency failed — cannot proceed |

### trigger_event field

When an agent is retried or spawned as a reaction to an event, set `trigger_event` to describe what caused the spawn:

```
"trigger_event": "retry:failed(backend-developer) attempt=2"
"trigger_event": "reaction:pr-reviewer-rejected round=1"
"trigger_event": "reaction:ci-failed branch=feat/todo-app-auth"
"trigger_event": null   ← normal first-time spawn
```

This makes the causal chain readable in `context.json` without needing an external log.

---

## Rules per agent role

### Before starting
Every agent MUST read `context.json` and:
1. Set own status to `"running"`
2. Read outputs of all `depends_on` agents for context
3. Check if any dependency has `status: "failed"` → set own status to `"blocked"`, stop and report

### After completing
Every agent MUST update `context.json`:

```json
{
  "outputs": {
    "{my-role}": {
      "status": "done",
      "summary": "concise description of what was done",
      "files_changed": ["list of files written or modified"],
      "worktree": "branch name if applicable, else null",
      "error": null,
      "retry_count": 0,
      "trigger_event": null
    }
  }
}
```

### On failure
```json
{
  "outputs": {
    "{my-role}": {
      "status": "failed",
      "summary": "what was attempted",
      "files_changed": [],
      "worktree": "branch name if applicable, else null",
      "error": "specific error message",
      "retry_count": 1,
      "trigger_event": null
    }
  }
}
```

---

## Output summary rules

The `summary` field is the primary way agents communicate with each other.

**Must include:**
- What was accomplished (not what was attempted)
- Key decisions made (e.g. "used JWT with HTTP-only cookies")
- Any constraints discovered (e.g. "users table already exists, reused it")
- What the next agent needs to know

**Must NOT include:**
- Full file contents (use `files_changed` for that)
- Redundant restatement of the task
- Uncertainty ("I think I may have...")

---

## pr-creator contract

When a PR is created, the `summary` field MUST include the `pull_number` and full PR URL so the `pr-reviewer` can access them:

```
"summary": "PR #7 created — pull_number: 7, url: https://github.com/owner/repo/pull/7, branch: feat/todo-app-backend"
```

The pr-reviewer reads this summary to call `mcp__github__create_pull_request_review`.

---

## pr-reviewer contract

The pr-reviewer MUST:
- Use `event: "COMMENT"` only — never `"APPROVE"` or `"REQUEST_CHANGES"`
- Post comments on the actual PR via `mcp__github__create_pull_request_review`
- Write its findings to context.json summary (list of issues found, or "No issues found")
- Never block the run — the PR review is informational only

```json
{
  "status": "done",
  "summary": "Review posted on PR #7. Found 2 comments: missing input validation on POST /tasks, no error handling for 500 responses.",
  "files_changed": [],
  "worktree": null
}
```

---

## Synthesizer contract

The synthesizer reads ALL `outputs` from `context.json` and produces:
- A final summary of what was built
- Integration points between components
- Any warnings or unresolved issues
- The PR URL if one was created

The synthesizer writes its result to `outputs.synthesizer` following the same schema.
