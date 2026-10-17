# agentic-delivery — agent guide

This repo has two roles:

1. It is the **`agentic-delivery` package**: the `ad` CLI in `src/delivery/`, which client hubs
   install as a pinned dependency.
2. It is the **Copier template** in `template/`, the thin layer each client hub is generated from.

It is also a working hub for its own product (PRD and backlog in `product/`). A hub is the central,
versioned home for a project's context. It holds the knowledge base, PRD, backlog and decisions, plus
links to the product repositories and generated delivery material. Project specifics (name, client,
which tools are in use) live in `project.yaml`.

## Layout

- `project.yaml`: project identity and which adapter fills each integration port.
- `kb/`: knowledge base, Markdown with YAML frontmatter. `kb/sources/` holds raw material pulled from
  external systems.
- `product/`: PRD (`prd.md`), features (`features/*.md`), and later epics and roadmap.
- `docs/adr/`: architecture decision records. Add one for any non-trivial design decision.
- `src/delivery/`: the `ad` CLI (ports and adapters). `tests/` mirrors it.
- `outputs/`: generated material (gitignored).
- `template/`: what client hubs get (Copier `_subdirectory`; `*.jinja` files are rendered). Its
  `CLAUDE.md` is the operating guide for hub users and agents. Keep it in step with this file.
- `workspace/`: product-repo mirrors (gitignored).

## Commands

- `uv run ad doctor`: check config, adapters, credentials.
- `uv run ad new feature|decision|risk "<title>"`: scaffold content with the next free id.
- `uv run ad list feature [--status defined]`: list content.
- `uv run ad validate`: check content schemas, ids and cross-references (also runs in hooks and CI).
- `uv run ad prd init`: create `product/prd.md` from the template.
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
- Skills and agents are authored in `template/.claude/` and copied to the root `.claude/` by
  `scripts/sync-agent-files.sh`. A hook fails if the copies differ, so never edit the root copies.
- After changing `template/` or `copier.yml`, run `uv run poe smoke`. It renders several stacks and
  checks that each installs this checkout's tooling and passes `ad doctor` and its hooks.
- Tooling changes reach client hubs through a release tag, not `copier update`. Keep the CLI
  backwards compatible with `project.yaml` files rendered by older template versions.
