---
name: feature
description: >-
  Define or refine one feature in product/features/ until it is ready to build: problem, proposal,
  user stories and acceptance criteria. Use when the user wants to specify, groom or refine a
  feature, write user stories, or add acceptance criteria.
argument-hint: "<feature id or title, e.g. F-003>"
---

# Feature definition

A feature is **defined** when someone who wasn't in the room could build and test it from the file
alone. Your job is to get it there.

## 1. Locate

- Find the feature with `uv run ad list feature`, matching on id or title. If the user's feature
  doesn't exist yet, confirm the title and run `uv run ad new feature "<title>"`.
- Read the feature file, the PRD (`product/prd.md`) for the goals it serves, and related `kb/` pages.
- If the product repos are available (see `repos.yaml` or `workspace/`, when present), look at the
  code areas it touches, so stories reflect how the system really works.

## 2. Define

Work through the sections with the user, proposing drafts rather than asking open questions:

- **Problem**: the user pain and which PRD goal it serves.
- **Proposal**: the shape of the solution, readable by a stakeholder.
- **User stories**: `As a <user>, I want <capability>, so that <outcome>`. Keep each story small
  enough for one sprint. Mirror every story in the frontmatter:

  ```yaml
  stories:
    - {id: S1, title: "Sync epics from Jira"}
    - {id: S2, title: "Show sync drift in ad doctor"}
  ```

  Then add one `### S1 — <title>` subsection per story in the body.
- **Acceptance criteria**: Given/When/Then, each checkable, grouped by story.
- **Out of scope** and **Open questions**.
- **Dependencies**: list other feature ids in `depends_on`.

## 3. Finish

- Set `status: defined` only when there are no blocking open questions. Otherwise leave it at
  `proposed` and say what's blocking.
- Run `uv run ad validate` and fix every error.
- If the hub has a tracker configured (`project.yaml` → `integrations.tracker`) and the user asks,
  create or update the matching tracker items via MCP. Record the external ids in the `tracker`
  fields (for example `tracker: {jira: ACME-12}`), so later syncs can reconcile.
