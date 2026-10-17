# Delivery hub — agent guide

This repo is a **delivery hub**: the central, versioned home for a project's context. It holds the
knowledge base, PRD, backlog and decisions, plus links to the product repositories and generated delivery
material. Project specifics (name, client, which tools are in use) live in `project.yaml`.

## Layout

- `project.yaml`: project identity and which adapter fills each integration port.
- `kb/`: knowledge base, Markdown with YAML frontmatter. `kb/sources/` holds raw material pulled from
  external systems.
- `product/`: PRD (`prd.md`), features (`features/*.md`), and later epics and roadmap.
- `docs/adr/`: architecture decision records. Add one for any non-trivial design decision.
- `src/delivery/`: the `ad` CLI (ports and adapters). `tests/` mirrors it.
- `outputs/`: generated material (gitignored).
- `workspace/`: product-repo mirrors (gitignored).

## Commands

- `uv run ad doctor`: check config, adapters, credentials.
- `uv run poe check`: lint, type check and tests. Run it before saying code work is done.
- `uv run poe fmt`: auto-format and fix lint.
- Add dependencies with `uv add <pkg>` (or `uv add --dev`). Never use pip.

## MCP or coded adapter

- **Use MCP** for interactive, one-off access: looking up an email, reading a Drive file, checking a
  ticket. A port whose adapter is `mcp` in `project.yaml` is served this way.
- **Write a coded adapter** (`src/delivery/adapters/`, registered under the `delivery.adapters` entry
  point) when the work must be repeatable, auditable, bulk, run in CI, or two-way. Examples are backlog
  sync, exports and scheduled ingestion.
- Write the adapter against the port Protocol in `src/delivery/ports.py`. Credentials come from env
  vars listed in the adapter's `required_env`; never hard-code or commit them.

## Knowledge conventions

- Everything brought in from outside gets provenance frontmatter: `source` (system plus URL/id),
  `retrieved` (ISO date), `author` if known.
- Prefer updating an existing KB page over creating a near-duplicate.
- Don't copy client-confidential material into commit messages, PR descriptions or issue titles.

## Engineering conventions

- Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`…), enforced by a commit-msg hook.
- Python 3.12, ruff, mypy strict, pytest. Coverage must be at least 80%.
- Template files: `X.jinja` renders into client instances as `X`. Keep the hub's own `X` and the
  `.jinja` version in step (see `copier.yml`). Run `uv run poe smoke` after changing the template.
