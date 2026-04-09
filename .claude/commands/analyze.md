---
description: Spawns an Agent Team to run a parallel, multi-specialist analysis of any project. Each teammate audits a different dimension independently, shares findings with the team, and the lead synthesizes everything into a scored report.
---

# /analyze

You are the team lead. Your job is to coordinate a team of specialized analysts that run in parallel, then synthesize their findings into a single unified report.

## Step 1 — Read the project

```
Read: $ARGUMENTS/  (directory tree)
```

Identify what layers exist in the project:
- Does it have a frontend? (React, TypeScript, Vue)
- Does it have a backend? (FastAPI, Express, Django)
- Does it have a test suite? (pytest, vitest, jest)

Always include security analysis regardless.

## Step 2 — Create the agent team

Create an agent team to analyze the project at `$ARGUMENTS`. Spawn the following teammates in parallel based on what you found in Step 1:

- **Spawn a teammate using the `security-analyzer` agent type** — audit `$ARGUMENTS` for security vulnerabilities: injection, XSS, hardcoded secrets, missing auth, insecure deps, CORS, missing rate limiting. Rate each finding CRITICAL / HIGH / MEDIUM / LOW with file and line. End with: **Security Score X/10**.

- **Spawn a teammate using the `frontend-analyzer` agent type** (only if a frontend exists) — audit the React/TypeScript code in `$ARGUMENTS` for component complexity, performance issues, TypeScript quality, React anti-patterns, accessibility, dead code, and missing tests. End with: **Frontend Health Score X/10**.

- **Spawn a teammate using the `backend-analyzer` agent type** (only if a backend exists) — audit the FastAPI/Python backend in `$ARGUMENTS` for API design, error handling, input validation, data layer risks, missing endpoints, and documentation gaps. End with: **Backend Health Score X/10**.

- **Spawn a teammate using the `test-coverage-analyzer` agent type** — audit test coverage in `$ARGUMENTS` for missing test files, untested endpoints/components, test quality, missing edge cases, and test isolation issues. Also run the test suite if possible and report results. End with: **Test Score X/10 — N tests found, N passing**.

## Step 3 — Team coordination

Assign each teammate a task via the shared task list with these rules:
- All teammates work in parallel — no blocking on each other at start
- Each teammate should **broadcast their key findings** to the team when done, so others can **challenge or confirm** related issues they found
- If a security finding touches the frontend or backend code, that teammate should **message the relevant specialist** to cross-check
- Use the task list to track: `security-audit`, `frontend-audit`, `backend-audit`, `test-audit`

After all teammates complete their tasks, collect their reports.

## Step 4 — Synthesize into a unified report

Once all teammates are done, produce this report:

```markdown
# Project Analysis Report — {project name}
Generated: {date}
Analyzed by: Claude Agent Team (security-analyzer, frontend-analyzer, backend-analyzer, test-coverage-analyzer)

## Executive Summary
[2-3 sentences: overall health, biggest risks, top priorities]

## Scores
| Area     | Score | Top Issue |
|----------|-------|-----------|
| Security | X/10  | ...       |
| Frontend | X/10  | ...       |
| Backend  | X/10  | ...       |
| Tests    | X/10  | ...       |
| **Overall** | **X/10** | |

## Critical Issues (fix immediately)
[Only CRITICAL and HIGH severity findings across all reports]

## High Priority Improvements
[Top 5 items across all reports, ranked by impact]

## Cross-cutting Findings
[Issues that multiple teammates flagged — these are the most confident findings]

## Full Findings by Area

### Security Audit
[Full report from security-analyzer]

### Frontend Audit
[Full report from frontend-analyzer]

### Backend Audit
[Full report from backend-analyzer]

### Test Coverage Audit
[Full report from test-coverage-analyzer]

## Recommended Next Steps
1. ...
2. ...
3. ...
```

## Step 5 — Clean up the team

After delivering the report, ask the team to shut down and clean up:
- Tell each teammate to shut down gracefully
- After all teammates idle, run team cleanup

---

$ARGUMENTS
