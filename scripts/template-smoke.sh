#!/usr/bin/env bash
# Render the copier template for representative stacks and check each render works:
# tooling installs from this checkout, `ad doctor` passes, and the instance's hooks pass.
set -euo pipefail

src="$(cd "$(dirname "$0")/.." && pwd)"
out="$(mktemp -d)"
trap 'rm -rf "$out"' EXIT

render() {
  local name="$1"; shift
  local dest="$out/$name"
  echo "::group::render $name"
  uv run copier copy --vcs-ref=HEAD --defaults --quiet \
    --data project_name="Smoke $name" --data client=smoke \
    --data tooling_source="file://$src" "$@" "$src" "$dest"
  (
    cd "$dest"
    unset VIRTUAL_ENV
    test -f project.yaml -a -f .mcp.json -a -f .copier-answers.yml -a -f CLAUDE.md
    python3 -c "import json; json.load(open('.mcp.json'))"
    git init -q -b main
    uv sync --quiet
    uv run ad doctor
    git add -A
    uv run pre-commit run --all-files
  )
  echo "::endgroup::"
}

render jira-google   --data tracker=jira --data workspace_suite=google
render ado-microsoft --data tracker=ado --data ado_org=contoso --data workspace_suite=microsoft
render bare          --data tracker=none --data workspace_suite=none --data meetings=none

echo "template smoke: all renders passed"
