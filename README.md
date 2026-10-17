# agentic-delivery

A template for **agentic delivery hubs**. A hub is a git repo that is the central, collaborative home
for a project's context. Claude Code drives it, and it has its own tools and integrations (Jira /
Confluence, Azure DevOps, Google Workspace, Microsoft 365, Zoom / Teams). It links to the repositories
where the product lives, and it produces delivery material: roadmaps, CSV exports and documents.

This repo is both the **Copier template** and a working hub. Its own PRD and backlog live in `product/`.

## Create a client hub

```bash
uvx copier copy gh:danielmschaves/agentic-delivery ./acme-hub
cd acme-hub && git init && uv sync && uv run ad doctor
```

Pull later template improvements into a hub with `uvx copier update`.

## Develop the template

```bash
uv sync
uv run pre-commit install --install-hooks
uv run poe check     # ruff, mypy --strict, pytest (≥80% coverage)
uv run poe smoke     # render the template for several stacks and run checks inside each
uv run ad doctor
```

## Architecture

The architecture is recorded in [ADR-0001](docs/adr/0001-architecture.md). In short:

- **Agent layer**: `CLAUDE.md`, `.claude/`, `.mcp.json`.
- **Tool layer**: the `ad` CLI in `src/delivery/`. Ports and adapters, with adapters discovered through
  the `delivery.adapters` entry points.
- **Content layer**: `kb/`, `product/`, `docs/`. Generated material goes to `outputs/`.

| Phase | Scope                                                                 | Status |
|-------|-----------------------------------------------------------------------|--------|
| 0     | Scaffold: uv, CLI + `ad doctor`, lint/type/test, CI, copier template  | done   |
| 1     | PRD and feature definition (`/prd`, `/feature`), canonical models     | next   |
| 2     | Product-repo linking: `repos.yaml` / `repos.lock`, sync digests       |        |
| 3     | Trackers: Jira, ADO Boards (two-way sync); Confluence / ADO Wiki      |        |
| 4     | Outputs: HTML roadmap, CSV, Markdown                                  |        |
| 5     | Knowledge ingestion: Drive / OneDrive, mail, calendar, transcripts    |        |
| 6     | `ad` as an MCP server, scheduled syncs, instance update flow          |        |
