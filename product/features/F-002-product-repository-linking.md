---
id: F-002
title: Product repository linking
status: defined
priority: must
depends_on:
- F-001
stories:
- id: S1
  title: Declare product repos in repos.yaml
- id: S2
  title: Mirror repos as blobless sparse clones in workspace/
- id: S3
  title: Sync writes a progress digest and bumps repos.lock
- id: S4
  title: Drift status in ad repos status, ad doctor and a SessionStart hook
tracker: {}
milestone: M2
---

# Product repository linking

## Problem

The product lives in other repositories that change constantly. Without a link the hub's context
goes stale, and the agent can't ground requirements in real code. Plain clones drift, and submodules
add friction for non-engineers.

## Proposal

The link is hybrid (ADR-0001 §7):

- `repos.yaml` declares each repo with its provider (github or ado), URL, branch, `paths` of
  interest, and a `mode`:
  - `remote`: read through the API or MCP only.
  - `mirror`: a blobless, sparse clone into the gitignored `workspace/`.
- `repos.lock` (committed) records the SHA the hub was last reconciled against.
- `ad repos sync` fetches, writes `kb/repos/<name>/changes/<date>.md` (commits, merged PRs, touched
  paths since the locked SHA), then bumps the lock. The hub's git history becomes a timeline of
  product change.
- A new `RepoPort` has GitHub and ADO Repos adapters for metadata (merged PRs) that `git log` can't
  provide.

## User stories

### S1 — Declare

As a delivery lead, I want to run `ad repos add <url> --mode mirror --path src/`, so the hub knows
about a product repo.

### S2 — Mirror

As the agent, I want a local, sparse, up-to-date checkout, so I can read code cheaply even in large
repos.

### S3 — Digest

As a delivery lead, I want each sync to record what changed, so the team can review product
progress in the hub's PRs.

### S4 — Drift

As anyone opening the hub, I want to see when its context lags the product, so I know to sync.

## Acceptance criteria

- Given a repo in `repos.yaml` with `mode: mirror`, when I run `ad repos sync`, then `workspace/<name>`
  holds a blobless clone with only the declared paths checked out.
- Given a lock at SHA A and a remote HEAD at B, when I sync, then a digest covering A..B is written
  and the lock records B.
- Given no new commits, when I sync, then no digest is written and the lock is unchanged.
- Given remote HEAD ≠ lock, when I run `ad repos status` or `ad doctor`, then the repo shows as
  behind, with a commit count.
- Given `mode: remote`, when I sync, then no clone is made and the digest comes from the API.

## Out of scope

- GitLab. The provider field allows it; the adapter comes later.
- Writing to product repos.

## Open questions

- Should digests be summarised by the agent (LLM) or kept purely mechanical? Proposal: mechanical
  digest from `ad`, with optional agent summaries via a skill.
