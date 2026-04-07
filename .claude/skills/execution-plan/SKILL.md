---
name: execution-plan
description: "Use when generating or validating the ExecutionPlan JSON that the orchestrator must produce before spawning any agents"
---

# Execution Plan

## Overview

The orchestrator MUST always produce a valid ExecutionPlan JSON before spawning any agents. This is the contract between the orchestrator and the rest of the system.

## Schema

```json
{
  "run_id": "string",
  "task": "string",
  "task_brief": {
    "type": "string (frontend|backend|fullstack|infra|fix|other)",
    "complexity": "string (low|medium|high)",
    "inferred": {},
    "explicit_requirements": ["string"],
    "implicit_requirements": ["string"],
    "ambiguities": ["string"],
    "out_of_scope": ["string"]
  },
  "agents": [
    {
      "role": "string",
      "model": "string (haiku|sonnet|opus)",
      "skills": ["string"],
      "mcps": ["string"],
      "depends_on": "string | string[] | null",
      "worktree": "string | null",
      "context": "string"
    }
  ]
}
```

## Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `run_id` | yes | Unique identifier: `YYYY-MM-DD-NNN` format |
| `task` | yes | Original user input, verbatim |
| `task_brief` | yes | Structured breakdown produced by brainstorm agent (or orchestrator directly for low complexity) |
| `task_brief.type` | yes | Task domain classification |
| `task_brief.complexity` | yes | Used to decide model selection and whether brainstorm was needed |
| `agents[]` | yes | Ordered list of agents to spawn. At least 1 required. |
| `agents[].role` | yes | Descriptive name: `backend-developer`, `pr-creator`, `pr-reviewer`, `db-architect`, `synthesizer` |
| `agents[].model` | yes | Model to use. See `catalog/models.md` for selection rules |
| `agents[].skills` | yes | Skills to inject. Empty array `[]` if none needed |
| `agents[].mcps` | yes | MCPs available to this agent. Empty array `[]` if none needed |
| `agents[].depends_on` | yes | `null` = runs immediately. String = waits for that role. Array = waits for all |
| `agents[].worktree` | no | Branch name for isolated execution. Set when agent writes code |
| `agents[].context` | yes | What this agent needs to know. Include outputs from dependency agents |

## Execution Rules

- Agents with `depends_on: null` run immediately and in parallel with each other
- Agents with `depends_on: "role-name"` wait for that role to complete
- Agents with `depends_on: ["role-a", "role-b"]` wait for ALL listed roles (barrier)
- The `synthesizer` always runs last — set `depends_on` to all other agent roles

## Example: Full-stack feature

```json
{
  "run_id": "2026-04-06-001",
  "task": "add JWT auth to the FastAPI backend",
  "task_brief": {
    "type": "backend",
    "complexity": "medium",
    "inferred": {
      "auth_type": "JWT",
      "reason": "FastAPI stack detected, no OAuth mentioned"
    },
    "explicit_requirements": ["login endpoint", "refresh token"],
    "implicit_requirements": ["users table", "password hashing", "rate limiting"],
    "ambiguities": [],
    "out_of_scope": ["OAuth providers", "2FA"]
  },
  "agents": [
    {
      "role": "backend-developer",
      "model": "sonnet",
      "skills": ["fastapi-patterns", "security-patterns"],
      "mcps": ["filesystem"],
      "depends_on": null,
      "worktree": "feat/jwt-auth",
      "context": "Implement JWT auth per the task_brief. Use FastAPI dependency injection for auth middleware."
    },
    {
      "role": "pr-creator",
      "model": "haiku",
      "skills": [],
      "mcps": ["filesystem", "github"],
      "depends_on": "backend-developer",
      "worktree": null,
      "context": "Create PR from feat/jwt-auth branch. Use outputs from backend-developer in context.json."
    },
    {
      "role": "pr-reviewer",
      "model": "sonnet",
      "skills": ["security-patterns"],
      "mcps": ["github"],
      "depends_on": "pr-creator",
      "worktree": null,
      "context": "Review the PR for security issues. Focus on JWT implementation, token storage, and rate limiting."
    },
    {
      "role": "synthesizer",
      "model": "sonnet",
      "skills": [],
      "mcps": [],
      "depends_on": ["pr-reviewer"],
      "worktree": null,
      "context": "Aggregate all outputs from context.json and produce final run summary."
    }
  ]
}
```

## Validation Checklist

Before finalizing the ExecutionPlan, verify:
- [ ] Every agent has a unique `role`
- [ ] `depends_on` references valid role names in the same plan
- [ ] No circular dependencies
- [ ] `synthesizer` is always last
- [ ] Agents that write code have `worktree` set
- [ ] `context` field is specific — not generic filler
