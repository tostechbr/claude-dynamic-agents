# MCPs Catalog

MCPs let agents *act* on external systems. They are deterministic, API-driven tools — not reasoning context.

## How the orchestrator uses this

Assign MCPs based on what the agent needs to *do*, not what it needs to *know*.
Minimize MCP access — only give an agent what it needs for its specific role.

---

## Available MCPs

### filesystem
**When to assign:** Any agent that reads or writes files on disk.

```json
"mcps": ["filesystem"]
```

Tools available:
- `read_file`, `read_multiple_files` — read source files
- `write_file`, `edit_file` — write generated code
- `list_directory`, `directory_tree` — explore project structure
- `search_files` — find files by pattern

Scope: `/Users/tiago.santos/Documents` (configured globally)

---

### github
**When to assign:** Agents that interact with GitHub — PRs, branches, reviews, issues.

```json
"mcps": ["github"]
```

Tools available:
- `create_pull_request` — open a PR with title, body, labels
- `get_pull_request`, `get_pull_request_diff` — read PR content for review
- `create_pull_request_review` — post line-level review comments
- `merge_pull_request` — merge after approval
- `create_issue`, `get_issue` — issue lifecycle
- `list_commits`, `get_commit` — inspect recent changes

Required for: `pr-creator`, `pr-reviewer`

---

### context7
**When to assign:** Agents that need up-to-date library documentation (not just LLM training knowledge).

```json
"mcps": ["context7"]
```

Tools available:
- `resolve-library-id` — find the library identifier
- `get-library-docs` — fetch current docs for any version

Use when: agent is working with a specific library version and needs accurate, current API reference (e.g. FastAPI 0.115, React 19, SQLAlchemy 2.0).

---

### memory
**When to assign:** Orchestrator only — for persisting run state and registry across sessions.

```json
"mcps": ["memory"]
```

Tools available:
- `create_entities`, `add_observations` — store agent configs in registry
- `search_nodes`, `open_nodes` — retrieve saved agent configs
- `create_relations` — link entities (e.g. skill → agent)

Primary use: the orchestrator reads/writes the agent registry via memory MCP.

---

## Quick Assignment Guide

| Agent Role | MCPs |
|------------|------|
| `orchestrator` | `memory` |
| `brainstorm` | `context7` |
| `db-architect` | `filesystem`, `context7` |
| `backend-developer` | `filesystem`, `context7` |
| `frontend-developer` | `filesystem`, `context7` |
| `devops-agent` | `filesystem` |
| `pr-creator` | `filesystem`, `github` |
| `pr-reviewer` | `github`, `context7` |
| `synthesizer` | `filesystem` |

---

## MCP vs Bash

Some actions can be done via MCP or via `bash` (gh CLI). Prefer MCP when:
- The operation needs structured output (e.g. PR diff as JSON)
- The agent needs to parse and act on the result

Use `bash` (gh CLI) as fallback when MCP tool is not available or insufficient.
