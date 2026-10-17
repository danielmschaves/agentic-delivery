---
id: F-001
title: PRD and feature definition
status: done
priority: must
depends_on: []
stories:
- id: S1
  title: Canonical models for features, stories, milestones, decisions, risks
  status: done
- id: S2
  title: ad new / list / validate / prd init commands
  status: done
- id: S3
  title: /prd and /feature skills shipped in the template
  status: done
- id: S4
  title: This hub's own PRD and backlog written with the tooling
  status: done
tracker: {}
milestone: M1
---

# PRD and feature definition

## Problem

Every engagement starts by agreeing on *why* and *what*, but that understanding usually lives in
slide decks and people's heads. The agent and the team need a structured, versioned definition that
later features (tracker sync, exports) can build on.

## Proposal

- Canonical pydantic models. Features (with stories), decisions and risks are Markdown files with
  frontmatter; milestones live in `product/roadmap.yaml`.
- `ad` commands to scaffold content from templates and validate it: schemas, id/filename agreement,
  duplicate ids, unknown milestones, unknown dependencies.
- `/prd` and `/feature` skills that interview the user, pull evidence from `kb/` and MCP sources,
  and write through the CLI.

## User stories

### S1 — Canonical models

As a template maintainer, I want one schema for product content so that sync and export code has a
single source of truth.

### S2 — CLI

As a delivery lead, I want `ad new feature "<title>"` to give me a correctly numbered, templated file
so that I never hand-pick ids.

### S3 — Skills

As a delivery lead, I want to run `/prd` and be interviewed into a complete PRD and feature list.

### S4 — Dogfood

As the template maintainer, I want this repo's own PRD to be produced with the tooling, to prove the
workflow end to end.

## Acceptance criteria

- Given a hub, when I run `ad new feature "X"` twice, then I get `F-001-x.md` and `F-002-x.md` with
  valid frontmatter.
- Given a feature that references an unknown milestone or dependency, when I run `ad validate`, then
  it exits 1 and names the file and the problem.
- Given a rendered client hub, when content under `product/` or `kb/` changes, then pre-commit and
  CI run `ad validate`.
- Given a new client hub, when the user types `/prd`, then the skill is available.

## Out of scope

- Epics as a separate level. Features map to Jira epics and ADO features; revisit with F-003.

## Open questions

- None blocking.
