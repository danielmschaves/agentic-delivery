#!/usr/bin/env bash
# Render the copier template for representative stacks and run the checks inside each render.
set -euo pipefail

src="$(cd "$(dirname "$0")/.." && pwd)"
out="$(mktemp -d)"
trap 'rm -rf "$out"' EXIT

render() {
  local name="$1"; shift
  local dest="$out/$name"
  echo "::group::render $name"
  uv run copier copy --vcs-ref=HEAD --defaults --quiet \
    --data project_name="Smoke $name" --data client=smoke "$@" "$src" "$dest"
  (
    cd "$dest"
    git init -q -b main
    uv sync --quiet
    uv run poe check
    uv run ad doctor
    python3 -c "import json,sys; json.load(open('.mcp.json'))"
  )
  echo "::endgroup::"
}

render jira-google   --data tracker=jira --data workspace_suite=google
render ado-microsoft --data tracker=ado --data ado_org=contoso --data workspace_suite=microsoft
render bare          --data tracker=none --data workspace_suite=none --data meetings=none

echo "template smoke: all renders passed"
