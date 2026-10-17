# ADR-0001: Hub architecture

- Status: accepted
- Date: 2026-10-17

## Context

We need a git-native, collaborative home for a project's delivery context, similar to a Claude Project
but owned by the team. It has to:

- work with whichever tools a client uses (Jira or Azure DevOps, Google Workspace or Microsoft 365, Zoom
  or Teams);
- link to the repositories where the product is built;
- produce delivery material (roadmaps, exports, documents);
- be reusable across clients and receive improvements over time.

## Decision

1. **Claude Code is the primary interface.** Repo-level `CLAUDE.md`, `.claude/` (skills, commands,
   subagents, hooks) and `.mcp.json` define how the agent works in the hub.
2. **A Python CLI (`ad`, managed with uv) holds the deterministic tools.** Both people and the agent
   call it.
3. **Ports and adapters.** Each integration is a port (a Protocol in `delivery.ports`). An adapter is
   registered under the `delivery.adapters` entry-point group and selected per port in `project.yaml`.
   The reserved values `mcp` (served by an MCP server) and `none` (disabled) let a port work before a
   coded adapter exists. New providers can ship as separate packages.
4. **MCP or code rule.** MCP covers interactive, one-off access. Coded adapters cover anything
   repeatable, auditable, bulk, in CI, or two-way.
5. **Content is plain files in git.** The KB and product docs are Markdown/YAML, reviewed through PRs.
   Generated outputs are pure functions of that content.
6. **Tooling is a package; the template is thin.** This repo is the `agentic-delivery` package
   and a working hub. `template/` (Copier `_subdirectory`) holds only the instance layer:
   `project.yaml`, `.mcp.json`, `CLAUDE.md`, `.claude/`, KB/product scaffolding and CI.
   - Instances depend on the tooling through a pinned direct reference
     (`agentic-delivery @ git+…@vX.Y.Z`). Tooling upgrades arrive as dependency bumps
     (Dependabot); template upgrades arrive through `copier update`.
   - Client repos never carry forked tooling code.
   - A CI smoke job renders several stacks, installs the local checkout into each, and runs
     `ad doctor` and the instance hooks.
   - We first tried making the repo root both template and hub, with `X` / `X.jinja` pairs. It was
     rejected because Copier applies `_exclude` to rendered paths, so excluding the hub's own `X`
     also dropped the rendered one.
7. **Product repos are linked in a hybrid way** (implemented in a later phase).
   - `repos.yaml` declares each repo as `remote` (API/MCP reads) or `mirror` (a blobless, sparse clone
     in a gitignored `workspace/`).
   - A committed `repos.lock` pins the SHA the hub's context was last reconciled against.
   - Each sync writes a progress digest to `kb/repos/`, giving a versioned timeline of product change
     without submodules.

## Consequences

- Most integrations work on day one through MCP. Coded adapters are written only when they pay off.
- The root `CLAUDE.md` and `template/CLAUDE.md` overlap and must be kept in step by review.
- The CLI must stay backwards compatible with config rendered by older template versions.
- Private tooling repos need read access from instance CI (deploy key or token) to install the
  package.
- Client data stays in the client's instance repo, so access is managed with normal repo permissions.
