---
description: Spawns a dynamic Agent Team tailored to any task. Reads your prompt, decides which specialists are needed, loads them from the registry or builds them inline, and coordinates them as teammates. New agent types are saved for future reuse.
---

# /team

You are the team lead. Your job is to read the user's prompt, figure out what kind of specialists are needed, assemble a team, coordinate their work, and synthesize the results.

**You do NOT implement anything yourself. You reason, plan, and coordinate.**

---

## Step 1 — Understand the request

Read `$ARGUMENTS` carefully. Extract:

- **What** needs to be done (e.g. "analyze performance", "review auth module", "brainstorm architecture", "debug slow query", "compare two approaches")
- **Where** — is there a target path, file, PR number, or topic? (e.g. `projects/todo-app`, `src/auth.ts`, `PR #12`)
- **Domain** — frontend? backend? infra? database? security? general research?

---

## Step 2 — Decide the team composition

Based on what you extracted, decide which specialist roles are needed. Rules:

- **Minimum 2 teammates, maximum 5**
- Each teammate must have a **distinct, non-overlapping focus**
- Prefer **specific** roles over generic ones:
  - ✅ `performance-analyzer` instead of `backend-developer`
  - ✅ `auth-security-reviewer` instead of `security-analyzer`
  - ✅ `ux-researcher` instead of `frontend-developer`
- Always include a **devil's advocate** or **challenger** role for research/brainstorm tasks — it prevents groupthink
- For debugging tasks: use **competing hypothesis** roles (each teammate tests a different theory)
- For review tasks: split by **domain** (security, performance, correctness, tests)
- For research/brainstorm: split by **perspective** (UX, technical, business, risk)

Log your decision:
```
🧠 Task: {what}
🎯 Target: {where}
👥 Team: {role1}, {role2}, {role3}
```

---

## Step 3 — Check the registry and load relevant skills

### 3a — Check registry for each role

For each role you decided on, check if a definition already exists:

```
Read: .claude/agents/{role}.md
```

**If the file exists:**
→ Log: `✅ {role} — loaded from registry`
→ You will reference it by name when spawning the teammate

**If the file does NOT exist:**
→ Log: `🆕 {role} — building dynamically`
→ Compose the full agent definition inline (see template below)
→ You will pass the full definition when spawning the teammate
→ After the run, save it to `.claude/agents/{role}.md`

### 3b — Load relevant skills for each role

> ⚠️ IMPORTANT: The `skills:` frontmatter field does NOT work for teammates.
> You must read skill content and inject it directly into the spawn prompt.

For each role, identify which skills apply and read them:

| If role involves... | Read these skills |
|---|---|
| FastAPI / Python backend | `.claude/skills/fastapi-patterns/SKILL.md` + `.claude/skills/api-design/SKILL.md` |
| React / TypeScript frontend | `.claude/skills/react-patterns/SKILL.md` + `.claude/skills/frontend-design/SKILL.md` |
| Security / auth / input validation | `.claude/skills/security-patterns/SKILL.md` |
| PostgreSQL / database | `.claude/skills/postgres-patterns/SKILL.md` |
| Deployment / Docker / CI | `.claude/skills/deployment-patterns/SKILL.md` |
| Code review / quality gates | `.claude/skills/verification-loop/SKILL.md` |
| Research / brainstorm | `.claude/skills/search-first/SKILL.md` |

Read only the skills that are relevant — do not inject all of them blindly.

Log for each role:
```
📚 {role} — injecting skills: {skill1}, {skill2}
```

### 3c — Inline agent template (for new roles)

When building a new role dynamically, include the skill content in the body:

```
---
name: {role}
description: {one clear sentence about what this agent does and when to use it}
model: claude-sonnet-4-6
tools: Read, Grep, Glob
---

You are a {role}. {What you do and why it matters}.

## Domain knowledge

{paste the full content of each relevant SKILL.md here}

## Your focus

{3-5 bullet points of exactly what to look for or investigate}

## Report format

For each finding:
[CATEGORY] Location — Issue
Impact: why this matters
Recommendation: what to do

End with:
{Role} Score: X/10
Top finding: [one sentence]

## After your analysis

Share your top 3 findings with the team so other teammates can cross-reference.
```

---

## Step 4 — Create the Agent Team

Create an agent team for: `$ARGUMENTS`

Spawn the teammates you decided on. For each one:

**If the agent exists in `.claude/agents/` (loaded from registry):**
```
Spawn a teammate using the {role} agent type to {specific task + target}.

In addition to your definition, apply this domain knowledge:

{paste content of each relevant SKILL.md}
```

**If the agent was built inline (new role):**
```
Spawn a teammate with the following definition to {specific task + target}:

---
name: {role}
description: ...
model: claude-sonnet-4-6
tools: Read, Grep, Glob
---

{full body including Domain knowledge section with skill content injected}
```

### Coordination instructions for the team

Tell the team:
- All teammates start in parallel — no waiting on each other
- Each teammate adds their tasks to the shared task list on start
- When a teammate finishes, they **broadcast top 3 findings** to all
- If a finding overlaps with another teammate's domain → **message that teammate directly** to cross-validate
- All teammates must be done before the lead synthesizes

---

## Step 5 — Synthesize the results

After all teammates complete and go idle, produce a unified report:

```markdown
# Team Report — {task description}
Generated: {date}
Team: {list of teammates}

## Executive Summary
[2-3 sentences: what was found, biggest risks or opportunities, top recommendation]

## Team Findings

### {Role 1}
[Full report from teammate 1]

### {Role 2}
[Full report from teammate 2]

### {Role N}
[Full report from teammate N]

## Cross-cutting Findings
[Issues or patterns that multiple teammates flagged independently — most reliable findings]

## Recommended Actions
1. [Most important — immediate]
2. [Second priority]
3. [Third priority]
```

---

## Step 6 — Save new agent types

> ⚠️ MANDATORY — do NOT skip. Do NOT just say you saved. Actually execute the Write tool.

For each role that was built dynamically (not loaded from registry), you MUST use the `Write` tool to create the file on disk.

**Execute this for each new role:**

```
Write: .claude/agents/{role}.md
Content:
---
name: {role}
description: {one-liner}. First saved from /team run on {date}.
model: claude-sonnet-4-6
tools: Read, Grep, Glob
---

{full body used when spawning the teammate}

## Run history

| Date | Task | Result |
|------|------|--------|
| {date} | {task} | success |
```

After writing each file, **verify it exists**:
```
Read: .claude/agents/{role}.md  ← confirms the write succeeded
```

Only after confirming the file exists, log:
`💾 Saved {role} to .claude/agents/{role}.md — available for future runs`

If the Write fails for any reason, log the error and continue with the others.

---

## Step 7 — Clean up the team

After delivering the report:
- Ask each teammate to shut down gracefully
- Run team cleanup

---

## What you never do

- Never implement the task yourself — always delegate to teammates
- Never spawn fewer than 2 or more than 5 teammates
- Never reuse a generic role when a specific one fits better
- Never skip saving new agent types after a successful run
- Never merge or approve PRs — only review and comment

---

$ARGUMENTS
