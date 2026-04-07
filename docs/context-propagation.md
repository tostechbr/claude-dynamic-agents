# Context Propagation

How outputs from one agent become inputs to the next.

## The problem

When agents run sequentially, agent B needs to know what agent A produced. Without a defined format, the orchestrator has to guess or re-read files.

## Solution: shared context.json

Each run has a `workspace/{run-id}/context.json` that agents read and write to:

```json
{
  "run_id": "2026-04-06-001",
  "task": "add JWT auth to FastAPI backend",
  "outputs": {
    "db-architect": {
      "status": "done",
      "schema_file": "workspace/2026-04-06-001/schema.sql",
      "summary": "users table with id, email, hashed_password, created_at"
    },
    "backend-developer": {
      "status": "done",
      "files_changed": ["app/auth.py", "app/models.py"],
      "summary": "JWT auth implemented with /login and /refresh endpoints"
    }
  }
}
```

## Rules

- Each agent reads `context.json` before starting
- Each agent writes its output summary to `context.json` when done
- The synthesizer reads all outputs from `context.json` to produce the final result
- Agents never read each other's files directly — only through `context.json`

## Why not just pass files?

- File paths are fragile (agent might not find the file)
- Summaries are cheaper to inject into context than full file contents
- `context.json` is the single source of truth for the run state
