# Delivery hub — agent guide

This repo is a **delivery hub**: the central, versioned home for a project's context. It holds the
knowledge base, PRD, backlog and decisions, plus links to the product repositories and generated delivery
material. Project specifics (name, client, which tools are in use) live in `project.yaml`.

The tooling (`ad` CLI) comes from the `agentic-delivery` package, pinned in `pyproject.toml`. This
repo's own files (this guide, `.claude/`, CI) come from the agentic-delivery Copier template.

## Layout

- `project.yaml`: project identity and which adapter fills each integration port.
- `kb/`: knowledge base, Markdown with YAML frontmatter. `kb/sources/` holds raw material pulled from
  external systems.
- `product/`: PRD (`prd.md`), features (`features/*.md`), and later epics and roadmap.
- `docs/adr/`: decision records for this project.
- `outputs/`: generated material (gitignored).
- `workspace/`: product-repo mirrors (gitignored).

## Commands

- `uv run ad doctor`: check config, adapters, credentials.
- `uv run ad --help`: list all hub tools.
- `uvx copier update`: pull template improvements. Review the diff before committing.

## MCP or coded adapter

- **Use MCP** for interactive, one-off access: looking up an email, reading a Drive file, checking a
  ticket. A port whose adapter is `mcp` in `project.yaml` is served this way (servers in `.mcp.json`,
  or the user's claude.ai connectors).
- **Use an `ad` command** when the work must be repeatable, auditable, bulk, or two-way. Examples are
  backlog sync, exports and scheduled ingestion. If no command exists yet, propose one upstream in
  agentic-delivery rather than writing one-off scripts here.

## Knowledge conventions

- Everything brought in from outside gets provenance frontmatter: `source` (system plus URL/id),
  `retrieved` (ISO date), `author` if known.
- Prefer updating an existing KB page over creating a near-duplicate.
- Don't copy client-confidential material into commit messages, PR descriptions or issue titles.
- Never read or print `.env`. Credentials are only for the `ad` tools.

## Conventions

- Conventional Commits (`feat:`, `docs:`, `chore:`…), enforced by a commit-msg hook.
- Changes go through PRs so the team reviews context changes like code.
