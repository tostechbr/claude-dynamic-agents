# Agent Contracts

Rules every agent MUST follow for inter-agent communication.

---

## The shared state: context.json

Every run has a single source of truth at `workspace/{run_id}/context.json`.

**Agents MUST:**
- Read `context.json` before starting their task
- Write their output summary to `context.json` when done
- Never read another agent's output files directly — only via `context.json`

---

## context.json schema

```json
{
  "run_id": "2026-04-07-001",
  "task": "original user input",
  "task_brief": { },
  "plan": { },
  "status": "running | completed | failed",
  "outputs": {
    "{role}": {
      "status": "pending | running | done | failed",
      "summary": "string — what was accomplished",
      "files_changed": ["path/to/file.py"],
      "worktree": "feat/branch-name | null",
      "error": "string | null",
      "retry_count": 0
    }
  }
}
```

---

## Rules per agent role

### Before starting
Every agent MUST read `context.json` and:
1. Set own status to `"running"`
2. Read outputs of all `depends_on` agents for context
3. Check if any dependency has `status: "failed"` — if so, stop and report

### After completing
Every agent MUST update `context.json` with:
```json
{
  "outputs": {
    "{my-role}": {
      "status": "done",
      "summary": "concise description of what was done",
      "files_changed": ["list of files written or modified"],
      "worktree": "branch name if applicable, else null",
      "error": null,
      "retry_count": 0
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
      "retry_count": 1
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

## Synthesizer contract

The synthesizer reads ALL `outputs` from `context.json` and produces:
- A final summary of what was built
- Integration points between components
- Any warnings or unresolved issues
- The PR URL if one was created

The synthesizer writes its result to `outputs.synthesizer` following the same schema.
