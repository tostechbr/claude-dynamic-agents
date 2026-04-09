---
description: Dynamic agent orchestration. Analyzes the task, builds an ExecutionPlan, and spawns specialized subagents directly from the main session. New agent types are created inline and saved to the registry after a successful run.
---

# /tos — Task Orchestration System

You are the **orchestrator running in the main session**. You do NOT delegate to an orchestrator subagent — you ARE the orchestrator. You spawn specialized subagents directly.

> ⚠️ Subagents cannot spawn other subagents (Claude Code constraint).
> The main session is always the root that spawns all agents.

---

## Step 1 — Read catalog and registry

```
Read: .claude/catalog/skills.md
Read: .claude/catalog/models.md
Read: .claude/registry/index.md
```

Also read the target project structure to understand the codebase.

---

## Step 2 — Classify the task

From the user input: `$ARGUMENTS`

Determine:
- `type`: frontend | backend | fullstack | infra | fix | other
- `complexity`: low | medium | high
- `needs_git`: true | false
- `target_dir`: check if `.claude/agents/orchestrator.md` exists → monorepo mode → `projects/{name}/`

---

## Step 3 — Generate ExecutionPlan

Decide which specialized agents are needed. Example for a frontend task:

```json
{
  "agents": [
    { "role": "frontend-developer", "depends_on": null },
    { "role": "test-runner",        "depends_on": "frontend-developer" },
    { "role": "pr-creator",         "depends_on": "test-runner" },
    { "role": "pr-reviewer",        "depends_on": "pr-creator" }
  ]
}
```

Rules:
- If `needs_git: true` → always include `test-runner` before `pr-creator`
- If `needs_git: true` → always include `pr-reviewer` after `pr-creator`
- Max 5 task agents per run

---

## Step 4 — Check registry, build missing agents inline

For each role in the plan:

```
Read: .claude/agents/{role}.md
```

**If file EXISTS** → log `✅ {role} loaded from registry` → use its frontmatter for model/tools
**If file DOES NOT EXIST** → log `🆕 {role} not found — building dynamically from catalog` → compose full inline definition

---

## Step 5 — Initialize workspace

```bash
mkdir -p workspace/{run_id}
```

Write `workspace/{run_id}/context.json`:
```json
{
  "run_id": "{run_id}",
  "task": "$ARGUMENTS",
  "target_dir": "{target_dir}",
  "status": "running",
  "outputs": {}
}
```

Run ID format: `YYYY-MM-DD-NNN`. Check `ls workspace/` first to avoid collisions.

---

## Step 6 — Spawn agents

Respect `depends_on`. Agents with `depends_on: null` can run in parallel.

### For an EXISTING agent (loaded from .md file):

```
Agent(
  [paste full content of .claude/agents/{role}.md here]

  ---
  ## Current run
  Run ID: {run_id}
  Context JSON: workspace/{run_id}/context.json

  ## Your task
  {specific instructions from ExecutionPlan}
)
```

### For a NEW agent (no .md file — built dynamically):

```
Agent(
  ---
  name: {role}
  description: {one-liner}. Dynamically created for run {run_id}.
  model: {from catalog/models.md — sonnet for coding, haiku for mechanical}
  tools: Read, Write, Edit, Bash, {mcps from registry/index.md MCP mapping}
  ---

  # {Role Title}

  You {description}.

  ## Before starting
  1. Read workspace/{run_id}/context.json
  2. Set own status to "running" in outputs.{role}
  3. Read dependency outputs for context

  ## After completing
  Update context.json — follow .claude/rules/agent-contracts.md

  ---
  ## Current run
  Run ID: {run_id}
  Context JSON: workspace/{run_id}/context.json

  ## Your task
  {specific instructions}
)
```

The `name:` frontmatter ensures Claude Code labels this subagent correctly in LangSmith.

---

## Step 7 — Monitor and handle failures

After each agent completes, read `context.json` and check its status.

If `status: "failed"` → follow `.claude/rules/failure-handling.md`
If `test-runner` fails → spawn `bug-fixer` inline → re-spawn `test-runner`

---

## Step 8 — Post-run (MANDATORY)

After all agents complete:

1. **Save new agents** — for every role that was built dynamically (not loaded from .md):
   - Write `.claude/agents/{role}.md` using the template in `registry/index.md`
   - Add a row to `registry/index.md`
   - Log: `💾 Saved {role} to .claude/agents/{role}.md`

2. **Update existing agents** — for roles loaded from .md:
   - Append a new row to the Run History table

3. **Update context.json** → `"status": "completed"`

4. **Report to user** — print the synthesizer's summary

---

## Model assignment (from catalog/models.md)

| Role | Model |
|------|-------|
| `frontend-developer`, `backend-developer`, `test-developer`, `test-runner`, `bug-fixer`, `pr-reviewer` | `claude-sonnet-4-6` |
| `pr-creator`, `synthesizer` | `claude-haiku-4-5-20251001` |
| Any new specialized role | `claude-sonnet-4-6` (default for unknown roles) |

---

$ARGUMENTS
