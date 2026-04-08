# Observability

Run observability for `claude-dynamic-agents` is provided by [LangSmith](https://smith.langchain.com) via the official Claude Code plugin.

Once installed, every `/tos` run is automatically traced — no code changes needed. The LangSmith plugin hooks into Claude Code's native lifecycle events and captures everything: user prompts, tool calls, subagent runs, LLM responses, and token usage.

---

## What you see in LangSmith

For a typical `/tos` run, the trace hierarchy looks like this:

```
Claude Code Turn  (root)
├── Claude  (LLM call — orchestrator reasoning)
├── Agent tool  (spawning brainstorm)
│   └── Claude Code Turn  (brainstorm subagent)
│       └── Claude  (LLM call)
├── Agent tool  (spawning backend-developer)
│   └── Claude Code Turn  (backend-developer subagent)
│       ├── Claude  (LLM call)
│       ├── Write: auth/jwt.py  (tool call)
│       └── Claude  (LLM call)
├── Agent tool  (spawning synthesizer)
│   └── Claude Code Turn  (synthesizer subagent)
│       └── Claude  (LLM call)
└── Claude  (LLM call — final report)
```

Each turn from the same Claude Code session is grouped using a shared `thread_id`, visible in the **Threads** tab of your LangSmith project.

---

## Installation

From within Claude Code, run:

```bash
/plugin marketplace add langchain-ai/langsmith-claude-code-plugins
/plugin install langsmith-tracing@langsmith-claude-code-plugins
/reload-plugins
```

To update:

```bash
/plugin marketplace update langsmith-claude-code-plugins
/reload-plugins
```

---

## Configuration

Create `.claude/settings.local.json` in this repo (already gitignored):

```json
{
  "env": {
    "TRACE_TO_LANGSMITH": "true",
    "CC_LANGSMITH_API_KEY": "<your-langsmith-api-key>",
    "CC_LANGSMITH_PROJECT": "claude-dynamic-agents"
  }
}
```

See `.claude/settings.local.json.example` for a ready-to-copy template.

Get your API key at [smith.langchain.com/settings/apikeys](https://smith.langchain.com/settings/apikeys).

---

## Debug mode

To see detailed API activity when traces aren't appearing:

```json
{
  "env": {
    "CC_LANGSMITH_DEBUG": "true"
  }
}
```

Check logs at `~/.claude/state/hook.log`:

```bash
tail -f ~/.claude/state/hook.log
```

---

## Without LangSmith: activity.jsonl

Even without LangSmith configured, every run produces an append-only event log at `workspace/{run_id}/activity.jsonl`. Agents write to it during execution — it is never read by agents, only written.

```jsonl
{"ts":"2026-04-07T10:00:00Z","agent":"orchestrator","event":"started","run_id":"2026-04-07-001"}
{"ts":"2026-04-07T10:00:01Z","agent":"orchestrator","event":"spawned","role":"backend-developer"}
{"ts":"2026-04-07T10:01:00Z","agent":"backend-developer","event":"started","trigger_event":null}
{"ts":"2026-04-07T10:04:00Z","agent":"backend-developer","event":"done","files_changed":["app/auth.py"]}
{"ts":"2026-04-07T10:04:01Z","agent":"orchestrator","event":"spawned","role":"synthesizer"}
{"ts":"2026-04-07T10:05:00Z","agent":"orchestrator","event":"completed","status":"completed"}
```

Standard events: `started`, `spawned`, `done`, `failed`, `retrying`, `escalated`.

The `context.json` in the same folder provides the structured state (plan, outputs, summaries). `activity.jsonl` provides the event timeline. Together they give you full run observability without any external tooling.

---

## Known limitations

- **Subagents are traced only on completion.** If you interrupt a `/tos` run mid-execution, in-progress subagent traces will only appear after the next message or session end.
- System prompts are not included — Claude Code does not expose them in transcripts.

---

## Causal chain in context.json

Even without LangSmith, the `context.json` for each run captures the causal chain via the `trigger_event` field on every agent output:

```json
"fix-agent": {
  "status": "done",
  "trigger_event": "reaction:pr-reviewer-rejected round=1",
  "summary": "Added input validation to /login endpoint"
}
```

This makes retries and reactions traceable directly in `workspace/{run_id}/context.json`.
