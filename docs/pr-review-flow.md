# PR + Review Flow

One of the most powerful patterns: the orchestrator spawns a full git workflow with separate agents for coding, PR creation, and code review.

## Example

Input:
```
/tos "add JWT auth to the FastAPI backend"
```

Generated plan:
```json
{
  "run_id": "2026-04-07-001",
  "task": "add JWT auth to the FastAPI backend",
  "target_dir": "projects/fastapi-backend",
  "agents": [
    {
      "role": "backend-developer",
      "model": "sonnet",
      "skills": ["fastapi-patterns", "security-patterns", "api-design"],
      "mcps": ["filesystem", "context7"],
      "depends_on": null,
      "worktree": "feat/fastapi-backend-jwt-auth"
    },
    {
      "role": "pr-creator",
      "model": "haiku",
      "skills": [],
      "mcps": ["filesystem", "github"],
      "depends_on": "backend-developer",
      "worktree": null
    },
    {
      "role": "pr-reviewer",
      "model": "sonnet",
      "skills": ["security-patterns", "verification-loop"],
      "mcps": ["github", "context7"],
      "depends_on": "pr-creator",
      "worktree": null
    },
    {
      "role": "synthesizer",
      "model": "sonnet",
      "skills": [],
      "mcps": ["filesystem"],
      "depends_on": ["pr-reviewer"],
      "worktree": null
    }
  ]
}
```

## Flow

```
[backend-developer]
  writes the feature in worktree feat/fastapi-backend-jwt-auth
        ↓
[pr-creator]
  git commit + git push
  gh pr create → returns PR URL
        ↓
[pr-reviewer]
  gh pr diff
  analyzes code quality + security (verification-loop skill)
  gh pr review --comment
        ↓
  if rejected → fix-loop (max 2 rounds)
        ↓
[synthesizer]
  summary: PR #42 created, review passed, 2 comments addressed
```

## Fix loop

When `pr-reviewer` rejects:

```
round 1:
  orchestrator spawns fix-agent
    context: reviewer comments from context.json
    worktree: feat/fastapi-backend-jwt-auth (same branch)
  fix-agent pushes fixes
  pr-reviewer runs again

round 2 (if still rejected):
  escalate to user with:
    - original reviewer comments
    - what fix-agent changed
    - remaining issues
```

## Why separate agents?

- **pr-creator** only needs filesystem + github — no domain knowledge, uses haiku (cheap)
- **pr-reviewer** gets security + verification-loop skills injected — focused on that lens
- Each agent does one thing well — smaller context, better output
