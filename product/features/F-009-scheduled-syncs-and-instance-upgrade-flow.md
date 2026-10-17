---
id: F-009
title: Scheduled syncs and instance upgrade flow
status: proposed
priority: should
depends_on:
- F-002
- F-003
stories: []
tracker: {}
milestone: M6
---

# Scheduled syncs and instance upgrade flow

## Problem

Context only refreshes when someone remembers to sync, and template upgrades are ad hoc.

## Proposal

CI cron jobs run repo and tracker syncs and open "context refresh" PRs. A documented, tested
`copier update` plus tooling-bump flow covers client hubs.

## User stories

<!-- To be defined with /feature before the milestone starts. -->

## Acceptance criteria

## Out of scope

## Open questions
