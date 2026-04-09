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

Before building agents from scratch, check in this order:

1. **`.claude/agents/{role}.md` exists?**
   → Load it directly — model, tools, skills already defined
   → Only adapt the `context` field for the current task

2. **Else: check memory MCP** for saved config metadata
   → Rebuild agent from saved role + skills + mcps + model

3. **Else: build fresh from catalog**
   → `catalog/skills.md`, `catalog/mcps.md`, `catalog/models.md`

After a successful run, save new agents to `.claude/agents/` (Step 7).

---

## Step 4 — Generate the ExecutionPlan

MUST produce a valid JSON ExecutionPlan (see `skills/execution-plan/SKILL.md`) before spawning any agent.

### Agent limits

| Category | Agents | Limit |
|----------|--------|-------|
| Task agents | backend-developer, frontend-developer, test-developer, db-architect, pr-creator, etc. | max 5 per run |
| Infrastructure | `synthesizer` (always) + `pr-reviewer` (when needs_git: true) | does NOT count toward limit |
| **Total maximum** | | **7 agents** |

If a task naturally requires more than 5 task agents → decompose into sequential /tos runs.

### Plan rules

- Every agent MUST have: `role`, `model`, `skills`, `mcps`, `depends_on`, `context`
- `context` must be specific — what does this agent need to know to do its job?
- Agents that write code MUST have `worktree` set to a branch name
- `synthesizer` is always the last agent, with `depends_on` pointing to all others
- Always use `task_brief` as the key in context.json — never `classification`

### Parallelism rules
- Agents with no shared state → `depends_on: null` → run in parallel
- Agent B needs Agent A's output → `depends_on: "agent-a"`
- Agent C needs both A and B → `depends_on: ["agent-a", "agent-b"]`

### MANDATORY PR review rule

**If `needs_git: true` AND `pr-creator` is in the plan → MUST add `pr-reviewer` after `pr-creator`. No exceptions. `pr-reviewer` does not count toward the 5-agent task limit.**

The pr-reviewer posts review comments (`event: "COMMENT"`) on the GitHub PR — it never approves or requests changes. The human decides what to do with the comments.

---

## Step 5 — Show the plan for complex tasks

If `complexity = high` OR confidence is low:
- Run `/plan` dry-run mode
- Show the ExecutionPlan to the user
- Wait for confirmation before spawning agents

For `low` and `medium` with no ambiguities: execute directly.

---

## Step 6 — Spawn agents and monitor

**Detect target directory first:**

| Condition | Mode | Generated code goes to |
|-----------|------|------------------------|
| `.claude/agents/orchestrator.md` exists in cwd | **Monorepo** | `projects/{project-name}/` |
| Otherwise | **External** | Current working directory |

In monorepo mode, infer project name from task in kebab-case (e.g. "build a todo app" → `projects/todo-app`). Set `target_dir` as a top-level field in `context.json` — agents read it from there, no need to repeat it in each agent's `context` string.

**Spawning named agents (LangSmith naming):**
Pass the full `.md` file content at the start of the Agent prompt so Claude Code can read the `name:` frontmatter and label the subagent correctly in traces. See `agents/orchestrator.md` Step 8 for the exact format.

- Create `workspace/{run_id}/` folder
- Initialize `workspace/{run_id}/context.json` with the plan, `target_dir`, and `status: "running"`
- Spawn agents per the ExecutionPlan
- Monitor `context.json` for status updates
- On failure: follow `rules/failure-handling.md`

---

## Step 7 — Post-run cleanup

After synthesizer completes:

1. **Save dynamic agents to `.claude/agents/`**
   - New role → create `.claude/agents/{role}.md` from template in `registry/index.md`
   - Existing role → append row to its Run History table
   - Skip permanent agents: `orchestrator`, `brainstorm`, `synthesizer`

2. **Update `registry/index.md`** — keep the summary index current

3. **Update `context.json`** with `status: "completed | partial | failed"`

4. **Report run result** to the user
