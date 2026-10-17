# Agentic Delivery — Product Requirements

<!-- Status: draft v0.1 (2026-10-17). Detail lives in product/features/. -->

## Problem

Delivery context is scattered across several places:

- trackers (Jira, Azure DevOps);
- documents (Drive, OneDrive/SharePoint);
- mail, calendars and meeting recordings;
- the product repositories themselves.

Claude Projects and similar tools can hold context, but they don't version it and can't be reviewed
like code. They don't plug into each client's own tool stack, and they don't produce delivery
material on demand. Each new client engagement rebuilds this setup by hand.

## Users and stakeholders

- **Delivery lead / PM**: owns the PRD, backlog and roadmap. Needs one place to ask questions of
  the project and to produce status material.
- **Engineers on the product**: need requirements and decisions that link to the code they change.
- **Client stakeholders**: get access to the hub, or to the material it produces.
- **Template maintainer**: evolves the tooling and template, and rolls improvements out to every hub.

## Goals

1. A new client hub is running, connected to that client's tracker, docs suite and product repos, in
   under an hour (`copier copy` → `ad doctor` all green).
2. Project context (PRD, features, decisions, risks, sources) is versioned and reviewed through PRs,
   and the agent can use it.
3. Delivery material (roadmap, backlog exports, status documents) is generated from that context,
   never maintained by hand.
4. The hub follows how the product evolves: every sync records what changed in the product repos.
5. Swapping a client's tools (for example Jira to Azure DevOps, or Drive to OneDrive) means changing
   configuration, not code.

## Non-goals

- Replacing the tracker or wiki. They stay the system of record for their teams; the hub syncs with
  them.
- A hosted web app. Git hosting provides collaboration and access control.
- Coding every integration up front. MCP covers interactive access; coded adapters are written only
  when work must be repeatable, auditable or two-way.

## Success metrics

| Metric                                     | Baseline     | Target          | How measured             |
|--------------------------------------------|--------------|-----------------|--------------------------|
| Time to a working client hub               | days, manual | < 1 hour        | timed instance setup     |
| Hand-edited status artifacts per month     | n/a          | 0               | outputs/ generated in CI |
| Template upgrades applied without conflict | n/a          | ≥ 90%           | `copier update` results  |
| Product changes reflected in the hub       | none         | every merged PR | `kb/repos/` digests      |

## Scope

- [F-001 PRD and feature definition](features/F-001-prd-and-feature-definition.md): must, M1
- [F-002 Product repository linking](features/F-002-product-repository-linking.md): must, M2
- [F-003 Tracker sync: Jira and ADO Boards](features/F-003-tracker-sync-jira-and-azure-devops-boards.md): must, M3
- [F-004 Wiki publishing](features/F-004-wiki-publishing-confluence-and-azure-devops-wiki.md): should, M3
- [F-005 Delivery outputs](features/F-005-delivery-outputs-html-roadmap-csv-markdown.md): must, M4
- [F-006 Document ingestion](features/F-006-document-ingestion-google-drive-and-onedrive.md): should, M5
- [F-007 Communication ingestion](features/F-007-communication-ingestion-mail-calendar-meeting.md): should, M5
- [F-008 Hub tools as an MCP server](features/F-008-hub-tools-as-an-mcp-server.md): could, M6
- [F-009 Scheduled syncs and instance upgrades](features/F-009-scheduled-syncs-and-instance-upgrade-flow.md): should, M6

## Milestones

The milestones are M1 to M6 in [roadmap.yaml](roadmap.yaml), in delivery order. Each milestone ships
as reviewed PRs with green CI and a tagged tooling release.

## Constraints and assumptions

- Claude Code is the primary interface. The `ad` CLI (Python, uv) holds the deterministic tools; see
  [ADR-0001](../docs/adr/0001-architecture.md).
- Client hubs install the tooling as a pinned package, and template files come from Copier.
- Credentials live only in env / `.env`, never in git.
- Client hubs may sit on GitHub or Azure DevOps, and CI must work on both.

## Risks and open questions

- [R-001](../kb/risks/R-001-client-confidential-data-leaking-from-hub-repos.md): client-confidential
  data leaking from hub repos.
- [R-002](../kb/risks/R-002-third-party-mcp-endpoints-change-or-disappear.md): third-party MCP
  endpoints change or disappear.
- Open: Does the tooling stay public, or move to a private repo or index? A private source needs
  read credentials in every client's CI.
- Open: For hubs with several product repos, is one hub per client or one per product the better
  unit?
