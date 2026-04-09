# Agent Registry

Saved agent configs from previous runs. The orchestrator checks here before building from the catalog.

## Structure

Dynamic agents are saved as `.md` files directly inside `.claude/agents/` — the same folder where permanent agents (`orchestrator`, `brainstorm`, `synthesizer`) live. Claude Code reads the `name:` frontmatter from these files and uses it to label subagents in LangSmith traces.

```
.claude/
└── agents/
    ├── orchestrator.md       ← permanent
    ├── brainstorm.md         ← permanent
    ├── synthesizer.md        ← permanent
    ├── backend-developer.md  ← saved after run 2026-04-08-001
    ├── test-developer.md     ← saved after run 2026-04-08-002
    ├── frontend-developer.md ← saved after run 2026-04-09-003
    ├── pr-creator.md         ← saved after run 2026-04-09-005
    ├── pr-reviewer.md        ← saved after run 2026-04-09-005
    └── ...                   ← new roles saved after each successful run
```

`registry/index.md` (this file) maintains the summary index and agent template only.

## How the orchestrator uses this

1. For each needed role, check `.claude/agents/{role}.md` first
2. If found → load it directly, adapt the `context` field for the current task
3. If not found → build from `catalog/`, save after a successful run

---

## Agent .md template

When saving a new dynamic agent after a successful run, use this format:

```markdown
---
name: {role}
description: {one-liner}. First saved from run {run_id}.
model: {claude-haiku-4-5-20251001 | claude-sonnet-4-6 | claude-opus-4-6}
tools: Read, Write, Edit, Bash, {mcp tools — see mapping below}
---

# {Role Title}

You {description} based on the task in your context.

## Before starting

1. Read workspace/{run_id}/context.json
2. Set own status to "running" in outputs.{role}
3. Read dependency summaries from outputs
4. Read target_dir from context.json — write all code there

## After completing

Update context.json outputs for your role — follow rules/agent-contracts.md.

## Saved configuration

| Field | Value |
|-------|-------|
| Skills | {comma-separated} |
| MCPs | {comma-separated} |
| Model | {haiku or sonnet or opus} |
| Task types | {frontend, backend, fullstack, infra, fix} |

## Run history

| Date | Run ID | Task | Skills | Result |
|------|--------|------|--------|--------|
| YYYY-MM-DD | {run_id} | {task} | {skills} | success |
```

---

## MCP → tools mapping

Use this when building the `tools` frontmatter field for a new agent:

| MCP | Tools to include |
|-----|-----------------|
| `filesystem` | `mcp__filesystem__read_file, mcp__filesystem__read_multiple_files, mcp__filesystem__write_file, mcp__filesystem__edit_file, mcp__filesystem__list_directory, mcp__filesystem__directory_tree, mcp__filesystem__search_files` |
| `github` | `mcp__github__create_pull_request, mcp__github__get_pull_request, mcp__github__create_pull_request_review, mcp__github__list_commits, mcp__github__create_issue, mcp__github__get_issue, mcp__github__create_branch` |
| `context7` | `mcp__context7__resolve-library-id, mcp__context7__get-library-docs` |
| `memory` | `mcp__memory__search_nodes, mcp__memory__open_nodes, mcp__memory__create_entities, mcp__memory__add_observations` |

Always include standard tools: `Read, Write, Edit, Bash`

---

## Registry

| Agent | File | Model | Task types | Last used |
|-------|------|-------|-----------|-----------|
| `backend-developer` | [../agents/backend-developer.md](../agents/backend-developer.md) | sonnet | backend, fix | 2026-04-08 |
| `test-developer` | [../agents/test-developer.md](../agents/test-developer.md) | sonnet | backend, fix | 2026-04-08 |
| `frontend-developer` | [../agents/frontend-developer.md](../agents/frontend-developer.md) | sonnet | frontend, fullstack | 2026-04-09 |
| `pr-creator` | [../agents/pr-creator.md](../agents/pr-creator.md) | haiku | frontend, backend, fullstack, infra, fix | 2026-04-09 |
| `pr-reviewer` | [../agents/pr-reviewer.md](../agents/pr-reviewer.md) | sonnet | frontend, backend, fullstack, infra, fix | 2026-04-09 |
| `test-runner` | [../agents/test-runner.md](../agents/test-runner.md) | sonnet | frontend, backend, fullstack, fix | 2026-04-09 |
| `bug-fixer` | [../agents/bug-fixer.md](../agents/bug-fixer.md) | sonnet | frontend, backend, fullstack, fix | 2026-04-09 |
