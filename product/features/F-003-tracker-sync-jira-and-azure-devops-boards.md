---
id: F-003
title: 'Tracker sync: Jira and Azure DevOps Boards'
status: proposed
priority: must
depends_on:
- F-001
stories: []
tracker: {}
milestone: M3
---

# Tracker sync: Jira and Azure DevOps Boards

## Problem

Backlogs live in Jira or Azure DevOps Boards, while the hub holds the definitions. Without sync,
they drift.

## Proposal

Add a `TrackerPort` with Jira and ADO Boards adapters, and `ad tracker pull` / `ad tracker push`.
Push shows a dry-run diff before it applies anything. Features map to epics (Jira) or features
(ADO), and stories to stories. External ids are recorded in `tracker:`.

## User stories

<!-- To be defined with /feature before the milestone starts. -->

## Acceptance criteria

## Out of scope

## Open questions
