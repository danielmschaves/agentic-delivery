#!/usr/bin/env bash
# The root hub dogfoods the template's agent files. template/.claude/ is the source of truth;
# this copies it into the root .claude/. With --check, fail instead of copying if they differ.
set -euo pipefail
cd "$(dirname "$0")/.."

dirs=(skills agents commands)
for d in "${dirs[@]}"; do
  src="template/.claude/$d"
  [ -d "$src" ] || continue
  if [ "${1:-}" = "--check" ]; then
    diff -r "$src" ".claude/$d" >/dev/null 2>&1 || {
      echo "$src and .claude/$d differ; run scripts/sync-agent-files.sh" >&2
      exit 1
    }
  else
    rm -rf ".claude/$d"
    cp -R "$src" ".claude/$d"
  fi
done
