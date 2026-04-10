#!/bin/bash
# Stop hook — runs when Claude finishes a response.
# Checks if any agents are pending save in .claude/agents-pending/
# and reminds Claude to save them if found.

PENDING_DIR=".claude/agents-pending"

if [ -d "$PENDING_DIR" ] && [ "$(ls -A $PENDING_DIR 2>/dev/null)" ]; then
  PENDING=$(ls "$PENDING_DIR"/*.md 2>/dev/null | xargs -I{} basename {})
  echo "⚠️  UNSAVED AGENTS DETECTED in .claude/agents-pending/:"
  echo "$PENDING"
  echo ""
  echo "You must move these to .claude/agents/ before finishing:"
  echo "  cp .claude/agents-pending/*.md .claude/agents/"
  echo "  rm -rf .claude/agents-pending/"
  # Exit code 2 = send feedback to Claude and keep it working
  exit 2
fi

exit 0
