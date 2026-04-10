# Tech Talk — Slide Content

---

## Slide 1 — Hook

**Title:** Most developers use Claude Code the best blogging systems with it

**Body:**
```
Average setup:
→ Open terminal
→ Type a prompt
→ Copy-paste the output
→ Repeat

System-level setup:
→ CLAUDE.md as persistent agent memory
→ Skills & Commands as reusable playbooks
→ Hooks for event-driven automation
→ MCP Servers as an external tool ecosystem
→ Agents that grow smarter with every run
```

---

## Slide 2 — Claude Code Project Structure

**Title:** The Complete Directory

```
your-project/
├── CLAUDE.md              ← Agent memory. Loaded at every session.
├── CLAUDE.local.md        ← Personal overrides. Never committed.
├── mcp.json               ← External tools: GitHub, Slack, databases.
└── .claude/
    ├── settings.json      ← Permissions, model routing, hooks config.
    ├── settings.local.json← Developer overrides.
    ├── rules/             ← Modular rules by topic.
    │   ├── code-style.md
    │   ├── testing.md
    │   └── api-design.md
    ├── commands/          ← Custom slash commands (/project:name).
    │   ├── review.md
    │   └── fix-issue.md
    ├── skills/            ← Auto-triggered contextual knowledge.
    │   └── deploy/SKILL.md
    ├── agents/            ← Specialized sub-agents with roles.
    │   ├── code-reviewer.md
    │   └── security-auditor.md
    └── hooks/             ← Event-driven scripts (pre/post tool use).
        └── validate-bash.sh
```

**Key message:** The quality of Claude Code's output is directly proportional to the quality of your project structure.

---

## Slide 3 — What Each Layer Does

**Title:** Structure vs What It Actually Does

| Layer | What it is | What it does |
|---|---|---|
| `CLAUDE.md` | Agent memory | Persistent context loaded every session |
| `rules/` | Guardrails | Code style, testing standards, API design |
| `commands/` | Playbooks | Reusable slash commands for any workflow |
| `skills/` | Knowledge | Domain expertise injected at runtime |
| `agents/` | Specialists | Isolated context, custom tools, own model |
| `hooks/` | Automation | Pre/post tool validation and formatting |
| `settings.json` | Governance | Permissions, model routing, team config |
| `mcp.json` | Tool ecosystem | GitHub, databases, Slack, custom APIs |

---

## Slide 4 — claude-dynamic-agents: The Unique Part

**Title:** What This Project Adds

```
.claude/
├── agents/                    ← REGISTRY — grows with every run
│   ├── orchestrator.md        (permanent — THE brain)
│   ├── brainstorm.md          (permanent — pre-analysis)
│   ├── synthesizer.md         (permanent — final report)
│   └── [created at runtime]   ← new specialists saved after each run
│
├── commands/
│   ├── tos.md     → /tos  — orchestrates full implementation pipeline
│   ├── team.md    → /team — spawns dynamic Agent Teams
│   └── analyze.md → /analyze — parallel specialist analysis
│
├── skills/                    ← knowledge injected into agents
│   ├── fastapi-patterns/      → backend agents
│   ├── react-patterns/        → frontend agents
│   ├── security-patterns/     → security agents
│   └── verification-loop/     → review agents
│
└── rules/                     ← contracts between agents
    ├── orchestration.md       → how the orchestrator plans
    ├── agent-contracts.md     → how agents communicate
    └── failure-handling.md    → what happens when things break
```

---

## Slide 5 — The Rules Layer

**Title:** Rules — Contracts Between Agents

**What lives in `.claude/rules/`:**

```
orchestration.md     → How the orchestrator classifies tasks,
                        builds ExecutionPlans, and spawns agents.
                        Defines: task types, complexity levels,
                        agent limits (max 5 task agents per run).

agent-contracts.md   → How agents read and write context.json.
                        Defines: output format, status values,
                        trigger_event for causal chain tracking.
                        Rule: pr-creator must use GitHub MCP,
                        never gh CLI.

failure-handling.md  → What happens when something breaks.
                        Rule 2: retry once, then escalate.
                        Rule 8: test-runner fails → bug-fixer →
                        re-run test-runner (max 2 rounds).
```

**Key message:** Rules are not prompts. They are contracts the system enforces on itself.

---

## Slide 6 — The /team Command Flow

**Title:** Dynamic Agent Teams

```
/team [any prompt]
         ↓
Step 1 — Read prompt
  "adiciona contador e modo dark no todo-app"
         ↓
Step 2 — Detect intent
  IMPLEMENTATION mode detected
         ↓
Step 3 — Decide team
  counter-implementer → owns App.tsx, useTasks.ts
  darkmode-implementer → owns App.css, index.css
         ↓
Step 4 — Check registry + load skills
  🆕 counter-implementer — building dynamically
  🆕 darkmode-implementer — building dynamically
  📚 both get: react-patterns + frontend-design injected
         ↓
Step 5 — Save agents to disk BEFORE spawning
  Write: .claude/agents/counter-implementer.md ✅
  Write: .claude/agents/darkmode-implementer.md ✅
         ↓
Step 6 — Spawn Agent Team (parallel)
  @counter-implementer  →  App.tsx + useTasks.ts
  @darkmode-implementer →  App.css + index.css
         ↓
Step 7 — Pipeline
  test-runner → pr-creator → pr-reviewer
         ↓
Step 8 — Registry after run
  3 agents → 5 agents
```

---

## Slide 7 — Agent Teams vs Subagents

**Title:** Two Ways to Parallelize

| | Subagents (`/tos`) | Agent Teams (`/team`) |
|---|---|---|
| How | `Agent` tool | Separate Claude Code instances |
| Communication | Only back to lead | Direct messaging between teammates |
| LangSmith | Nested hierarchy | Separate top-level traces |
| Best for | Sequential pipeline | Parallel independent work |
| Token cost | Lower | Higher — each teammate is full Claude |

**Key message:** Use subagents when only the result matters. Use Agent Teams when teammates need to share findings and collaborate.

---

## Slide 8 — Live Demo

**Title:** Live — registry growing in real time

**Step 1 — Show empty registry:**
```bash
ls .claude/agents/
# brainstorm.md  orchestrator.md  synthesizer.md
```

**Step 2 — Run analysis:**
```
/team review projects/todo-app/routers/tasks.py
```

**Step 3 — Show registry after:**
```bash
ls .claude/agents/
# 3 → 5 files
```

**Step 4 — Run feature:**
```
/team adiciona contador de tasks completas e modo dark no todo-app
— counter-implementer owns App.tsx e useTasks.ts,
darkmode-implementer owns App.css e index.css
```

**Step 5 — Show result:**
- Browser: counter + dark mode live
- GitHub: PR created automatically
- Registry: 3 → 7 agents

---

## Slide 9 — Key Takeaways

**Title:** What to take home

```
1. Structure is everything
   CLAUDE.md + rules + skills = consistent output every run

2. Skills are not prompts
   They inject domain knowledge — fastapi-patterns teaches
   the agent HOW to think about FastAPI, not what to do

3. Agents are reusable
   Every run saves new specialists. The system gets smarter.

4. Rules are contracts
   failure-handling.md means the system self-heals.
   You don't babysit — it governs itself.

5. Agent Teams = real parallelism
   Two implementers, zero conflict, half the time.
```

---

## Prompt for the live demo

```
/team adiciona contador de tasks completas e modo dark no todo-app
— counter-implementer owns App.tsx e useTasks.ts,
darkmode-implementer owns App.css e index.css
```
