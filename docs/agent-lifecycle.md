# Agent Lifecycle

Agents in this system are **ephemeral** — they are spawned at runtime and do not persist as files.

## Where agents come from

The orchestrator reads the `catalog/` and assembles a config for each agent on-the-fly:

```
catalog/skills.md + catalog/mcps.md + catalog/models.md
        ↓
orchestrator generates ExecutionPlan JSON
        ↓
Claude Code Agent tool spawns each agent with its config
```

No agent file is written to disk. The agent exists only for the duration of its task.

## Git worktrees for isolation

Each agent that writes code runs in its own git worktree — not just a folder. This prevents conflicts between parallel agents touching the same files:

```
main branch
├── worktree: feat/todo-app-backend   ← backend-developer agent
└── worktree: feat/todo-app-frontend  ← frontend-developer agent
```

In monorepo mode, worktrees branch off this repo as `feat/{project-name}-{feature}`.

## Where outputs go

Each run creates a folder under `workspace/`:

```
workspace/
└── {run-id}/
    ├── context.json      ← shared state: plan, outputs, status per agent
    └── activity.jsonl    ← append-only event log (observability)
```

Agents write their output summaries to `context.json` — not as individual files. Full code changes live in the worktree branches, not in `workspace/`.

### context.json structure

```json
{
  "run_id": "2026-04-07-001",
  "task": "original user input",
  "target_dir": "projects/todo-app",
  "status": "running | completed | failed",
  "outputs": {
    "backend-developer": {
      "status": "done",
      "summary": "JWT auth implemented with /login and /refresh endpoints",
      "files_changed": ["projects/todo-app/app/auth.py"],
      "worktree": "feat/todo-app-auth",
      "error": null,
      "retry_count": 0,
      "trigger_event": null
    }
  }
}
```

### activity.jsonl structure

```jsonl
{"ts":"2026-04-07T10:00:00Z","agent":"orchestrator","event":"started","run_id":"2026-04-07-001"}
{"ts":"2026-04-07T10:00:01Z","agent":"orchestrator","event":"spawned","role":"backend-developer"}
{"ts":"2026-04-07T10:01:00Z","agent":"backend-developer","event":"started","trigger_event":null}
{"ts":"2026-04-07T10:04:00Z","agent":"backend-developer","event":"done","files_changed":["app/auth.py"]}
{"ts":"2026-04-07T10:04:01Z","agent":"orchestrator","event":"spawned","role":"synthesizer"}
{"ts":"2026-04-07T10:05:00Z","agent":"orchestrator","event":"completed","status":"completed"}
```

## Static vs dynamic agents

| Type | Location | Lifespan |
|------|----------|----------|
| Orchestrator | `.claude/agents/orchestrator.md` | Permanent |
| Brainstorm | `.claude/agents/brainstorm.md` | Permanent |
| Synthesizer | `.claude/agents/synthesizer.md` | Permanent |
| Task agents | Generated from catalog at runtime | Ephemeral (per run) |
