# Context Propagation

How outputs from one agent become inputs to the next.

## The problem

When agents run sequentially, agent B needs to know what agent A produced. Without a defined format, the orchestrator has to guess or re-read files.

## Solution: shared context.json

Each run has a `workspace/{run-id}/context.json` that agents read and write to. It is the single source of truth for the entire run.

```json
{
  "run_id": "2026-04-07-001",
  "task": "add JWT auth to FastAPI backend",
  "target_dir": "projects/fastapi-backend",
  "status": "running",
  "task_brief": {
    "explicit_requirements": ["JWT tokens", "login endpoint", "refresh endpoint"],
    "implicit_requirements": ["HTTP-only cookies", "token expiry"],
    "ambiguities": [],
    "suggested_agents": ["backend-developer", "pr-creator", "pr-reviewer"],
    "suggested_skills": ["fastapi-patterns", "security-patterns", "api-design"],
    "complexity": "medium"
  },
  "plan": {
    "agents": [
      {
        "role": "backend-developer",
        "model": "sonnet",
        "skills": ["fastapi-patterns", "security-patterns", "api-design"],
        "mcps": ["filesystem", "context7"],
        "depends_on": null,
        "worktree": "feat/fastapi-backend-jwt-auth"
      }
    ]
  },
  "outputs": {
    "backend-developer": {
      "status": "done",
      "summary": "JWT auth implemented with /login and /refresh endpoints. Used HTTP-only cookies for token storage. users table reused from existing schema.",
      "files_changed": ["projects/fastapi-backend/app/auth.py", "projects/fastapi-backend/app/models.py"],
      "worktree": "feat/fastapi-backend-jwt-auth",
      "error": null,
      "retry_count": 0,
      "trigger_event": null
    },
    "pr-creator": {
      "status": "done",
      "summary": "PR #42 created at https://github.com/org/repo/pull/42",
      "files_changed": [],
      "worktree": null,
      "error": null,
      "retry_count": 0,
      "trigger_event": null
    }
  }
}
```

## Rules

- Each agent reads `context.json` before starting and sets its own status to `"running"`
- Each agent writes its output summary to `context.json` when done
- Agents that `depends_on` another agent read that agent's `summary` field for context — never the actual files directly
- The synthesizer reads all `outputs` from `context.json` to produce the final result
- `target_dir` is read from `context.json` — it is not passed per-agent

## The summary field

The `summary` is the primary way agents communicate with each other. It must include:
- What was accomplished (not what was attempted)
- Key decisions made (e.g. "used JWT with HTTP-only cookies")
- Constraints discovered (e.g. "users table already exists, reused it")
- What the next agent needs to know

## trigger_event

The `trigger_event` field tracks the causal chain — what caused this agent to run:

```json
"fix-agent": {
  "status": "done",
  "trigger_event": "reaction:pr-reviewer-rejected round=1",
  "summary": "Added input validation to /login endpoint"
}
```

Values: `null` (normal spawn), `"retry:1"` (first retry), `"reaction:pr-reviewer-rejected round=1"` (fix loop).

## Why not just pass files?

- File paths are fragile (agent might not find the file)
- Summaries are cheaper to inject into context than full file contents
- `context.json` is the single source of truth for plan, state, and causal chain
