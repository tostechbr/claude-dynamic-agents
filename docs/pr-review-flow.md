# PR + Review Flow

One of the most powerful patterns: the orchestrator spawns a full git workflow with separate agents for coding, PR creation, and code review.

## Example

Input:
```
/orchestrate "add JWT auth to the FastAPI backend"
```

Generated plan:
```json
{
  "agents": [
    {
      "role": "backend-developer",
      "skills": ["fastapi-patterns", "security-patterns"],
      "mcps": ["filesystem"],
      "depends_on": null
    },
    {
      "role": "pr-creator",
      "skills": [],
      "mcps": ["filesystem"],
      "depends_on": "backend-developer"
    },
    {
      "role": "pr-reviewer",
      "skills": ["security-patterns"],
      "mcps": [],
      "depends_on": "pr-creator"
    }
  ]
}
```

## Flow

```
[backend-developer]
  writes the feature
        ↓
[pr-creator]
  git checkout -b feat/jwt-auth
  git commit + git push
  gh pr create
        ↓
[pr-reviewer]
  gh pr diff
  analyzes code quality + security
  gh pr review --comment
        ↓
[synthesizer]
  summary: PR #42 created, 2 review comments added
```

## Why separate agents?

- **pr-creator** only needs filesystem + git — no domain knowledge
- **pr-reviewer** gets the security skill injected — focused on that lens
- Each agent does one thing well
