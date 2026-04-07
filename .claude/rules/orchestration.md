# Orchestration Rules

Rules the orchestrator MUST follow on every run.

---

## Step 1 — Classify the task

Before anything else, classify the incoming task:

```
type:        frontend | backend | fullstack | infra | fix | other
complexity:  low | medium | high
needs_git:   true | false
```

**Complexity heuristics:**
- `low` — single file, clear scope, no ambiguity (e.g. "fix typo in README", "add a button")
- `medium` — multi-file, clear scope (e.g. "add JWT auth", "create user profile page")
- `high` — cross-system, ambiguous, or architectural (e.g. "add real-time notifications", "migrate to microservices")

---

## Step 2 — Decide if brainstorm is needed

| Complexity | Ambiguities detected? | Action |
|------------|----------------------|--------|
| `low` | no | Skip brainstorm → go to Step 3 |
| `low` | yes | Run brainstorm |
| `medium` | no | Run brainstorm |
| `medium` | yes | Run brainstorm |
| `high` | any | Always run brainstorm |

Ambiguity signals: vague pronouns ("the app", "it"), missing stack info, conflicting requirements, multiple interpretations possible.

---

## Step 3 — Check the registry

Before building agents from scratch, check `.claude/registry/index.md`:

1. Is there a saved agent config that matches the needed role?
2. Does it match the current task's required skills and MCPs?
3. Was it used successfully before (status: `active`)?

If yes → reuse and adapt the config.
If no → build from `catalog/skills.md`, `catalog/mcps.md`, `catalog/models.md`.

After a successful run, save new agent configs to the registry.

---

## Step 4 — Generate the ExecutionPlan

MUST produce a valid JSON ExecutionPlan (see `skills/execution-plan/SKILL.md`) before spawning any agent.

**Rules for building the plan:**

- Every agent MUST have: `role`, `model`, `skills`, `mcps`, `depends_on`, `context`
- `context` must be specific — what does this agent need to know to do its job?
- Agents that write code MUST have `worktree` set to a branch name
- `synthesizer` is always the last agent, with `depends_on` pointing to all others
- Never spawn more than 5 agents per run — decompose large tasks into sequential runs

**Parallelism rules:**
- Agents with no shared state → `depends_on: null` → run in parallel
- Agent B needs Agent A's output → `depends_on: "agent-a"`
- Agent C needs both A and B → `depends_on: ["agent-a", "agent-b"]`

---

## Step 5 — Show the plan for complex tasks

If `complexity = high` OR confidence is low:
- Run `/plan` dry-run mode
- Show the ExecutionPlan to the user
- Wait for confirmation before spawning agents

For `low` and `medium` with no ambiguities: execute directly.

---

## Step 6 — Spawn agents and monitor

- Create `workspace/{run_id}/` folder
- Initialize `workspace/{run_id}/context.json` with the plan
- Spawn agents per the ExecutionPlan
- Monitor `context.json` for status updates
- On failure: follow `rules/failure-handling.md`

---

## Step 7 — Post-run cleanup

After synthesizer completes:
1. Save successful agent configs to `registry/index.md`
2. Write final summary to `workspace/{run_id}/context.json`
3. Report run result to the user
