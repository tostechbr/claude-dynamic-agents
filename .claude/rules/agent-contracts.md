# Agent Contracts

Rules every agent MUST follow for inter-agent communication.

---

## The shared state: context.json + activity.jsonl

Every run has two shared files at `workspace/{run_id}/`:

| File | Purpose |
|------|---------|
| `context.json` | Single source of truth — plan, outputs, status |
| `activity.jsonl` | Append-only event log — one JSON object per line |

**Agents MUST:**
- Read `context.json` before starting their task
- Write their output summary to `context.json` when done
- Append events to `activity.jsonl` at key moments (start, tool calls, done, error)
- Never read another agent's output files directly — only via `context.json`

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

This makes the activity log traceable without reading full context.

---

## Rules per agent role

### Before starting
Every agent MUST read `context.json` and:
1. Set own status to `"running"`
2. Append to `activity.jsonl`: `{"ts":"<iso>","agent":"<role>","event":"started","trigger_event":"<value or null>"}`
3. Read outputs of all `depends_on` agents for context
4. Check if any dependency has `status: "failed"` → set own status to `"blocked"`, append `blocked` event, stop

### After completing
Every agent MUST update `context.json` and append to `activity.jsonl`:

```json
// context.json update
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

```jsonl
// activity.jsonl append
{"ts":"<iso>","agent":"<role>","event":"done","files_changed":["path/to/file.py"]}
```

### On failure
```json
// context.json update
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

```jsonl
// activity.jsonl append
{"ts":"<iso>","agent":"<role>","event":"failed","error":"specific error message","retry_count":1}
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

## activity.jsonl format

Append-only file. One JSON object per line. Never overwrite.

**Standard events:**

```jsonl
{"ts":"2026-04-07T10:00:00Z","agent":"backend-developer","event":"started","trigger_event":null}
{"ts":"2026-04-07T10:01:30Z","agent":"backend-developer","event":"tool_call","tool":"Write","file":"auth/jwt.py"}
{"ts":"2026-04-07T10:04:00Z","agent":"backend-developer","event":"done","files_changed":["auth/jwt.py","auth/middleware.py"]}
{"ts":"2026-04-07T10:05:00Z","agent":"pr-reviewer","event":"started","trigger_event":null}
{"ts":"2026-04-07T10:06:00Z","agent":"pr-reviewer","event":"rejected","reason":"missing rate limiting on /login"}
{"ts":"2026-04-07T10:06:01Z","agent":"fix-agent","event":"started","trigger_event":"reaction:pr-reviewer-rejected round=1"}
{"ts":"2026-04-07T10:08:00Z","agent":"fix-agent","event":"done","files_changed":["auth/routes.py"]}
```

**Rules:**
- `ts` is always ISO 8601 UTC
- `agent` matches the `role` in the ExecutionPlan
- `event` is one of: `started | tool_call | done | failed | blocked | waiting_input | rejected`
- Optional fields depend on event type

---

## Synthesizer contract

The synthesizer reads ALL `outputs` from `context.json` and `activity.jsonl` and produces:
- A final summary of what was built
- Integration points between components
- Any warnings or unresolved issues
- The PR URL if one was created

The synthesizer writes its result to `outputs.synthesizer` following the same schema.
