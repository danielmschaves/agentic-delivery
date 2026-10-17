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
6. **Copier template, with the root doubling as a working hub.** Files that differ between the template
   and the hub exist twice: `X` (the hub's own, excluded) and `X.jinja` (rendered into instances).
   `copier update` carries template improvements into client instances. A CI smoke job renders several
   stacks and runs the checks inside each render.
7. **Product repos are linked in a hybrid way** (implemented in a later phase).
   - `repos.yaml` declares each repo as `remote` (API/MCP reads) or `mirror` (a blobless, sparse clone
     in a gitignored `workspace/`).
   - A committed `repos.lock` pins the SHA the hub's context was last reconciled against.
   - Each sync writes a progress digest to `kb/repos/`, giving a versioned timeline of product change
     without submodules.

## Consequences

- Most integrations work on day one through MCP. Coded adapters are written only when they pay off.
- Two copies of a few root files (`project.yaml`, `.mcp.json`, `README.md`) must be kept in step. The
  smoke test catches render breakage, not drift in meaning.
- Client data stays in the client's instance repo, so access is managed with normal repo permissions.
