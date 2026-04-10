# Tech Talk Demo Script

## Setup (before the talk)

```bash
# Terminal 1 — backend
cd projects/todo-app
uvicorn main:app --reload

# Terminal 2 — frontend
cd projects/todo-app/frontend
npm run dev
```

Open: http://localhost:5173 — todo-app running with priority badges.

---

## Live Demo — ~8 minutes

### 1. Show the registry (1min)

```bash
ls .claude/agents/
# brainstorm.md  orchestrator.md  synthesizer.md
```

> "The system starts empty. Every run creates new specialists and saves them here."

---

### 2. Live analysis (2min)

```
/team review projects/todo-app/routers/tasks.py
```

What happens:
- Claude reads the prompt → decides 2-3 specialist roles
- Saves agent `.md` files **before** spawning
- Teammates run in parallel, message each other with findings
- Report delivered in ~90 seconds

Show after:
```bash
ls .claude/agents/
# 3 → 5 files — registry grew live
```

---

### 3. LangSmith (1min)

Open LangSmith → show the run:
- Team lead: ~200k tokens
- Each teammate: ~100k tokens, ~$0.01 each
- "Right model for each role — Sonnet for specialists, not Opus"

---

### 4. Live feature (3min)

```
/team adiciona contador de tasks completas e modo dark no todo-app
— counter-implementer owns App.tsx e useTasks.ts,
darkmode-implementer owns App.css e index.css
```

What happens:
- 2 implementers run in parallel on different files — no conflict
- test-runner gates before PR
- PR created automatically

Show after:
- Browser: counter in header + dark mode toggle
- GitHub: PR with full description

---

### 5. Wrap up (1min)

```bash
ls .claude/agents/
# 3 → 7+ files after both runs
```

> "Each run the system gets smarter. These agents are reused in future runs
> with the same skills and patterns already baked in."

---

## Key talking points

| Point | What to show |
|---|---|
| Dynamic agents | Registry growing from 3 → 7 files live |
| Real parallelism | Two implementers on screen at the same time |
| Self-healing | test-runner → bug-fixer if tests fail |
| Observability | LangSmith traces with per-agent token cost |
| Skills | "fastapi-patterns injected — agent knows FastAPI idioms" |

---

## Fallback if something breaks

- Feature fails → show the analysis run instead (always safe)
- LangSmith empty → show `workspace/{run_id}/context.json` directly
- App won't start → show the generated code + PR on GitHub
