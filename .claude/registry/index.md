# Agent Registry

Saved agent configs from previous runs. The orchestrator checks here before building from the catalog.

## How to read this

Each entry is an agent config that was used successfully. On new runs, the orchestrator can reuse and adapt these instead of starting from scratch.

## Format

```
### {role}
- **model**: sonnet | haiku | opus
- **skills**: [list]
- **mcps**: [list]
- **task_types**: [frontend | backend | fullstack | infra | fix]
- **status**: active | deprecated
- **last_used**: YYYY-MM-DD
- **run_id**: first run that created this entry
- **notes**: anything worth knowing about this config
```

---

## Registry

_Empty — grows automatically as /tos runs complete successfully._

<!-- 
Example entry (added after first successful run):

### backend-developer
- **model**: sonnet
- **skills**: [fastapi-patterns, security-patterns, using-git-worktrees]
- **mcps**: [filesystem, context7]
- **task_types**: [backend, fullstack]
- **status**: active
- **last_used**: 2026-04-07
- **run_id**: 2026-04-07-001
- **notes**: used for JWT auth implementation, worked well with postgres-patterns from db-architect output
-->
