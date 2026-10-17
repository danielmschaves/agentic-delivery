---
id: F-008
title: Hub tools as an MCP server
status: proposed
priority: could
depends_on:
- F-003
- F-005
stories: []
tracker: {}
milestone: M6
---

# Hub tools as an MCP server

## Problem

Only Claude Code sessions in the hub can use `ad`. Other clients and SDK agents can't.

## Proposal

`ad mcp serve` exposes hub tools (validate, list, export, sync) over stdio MCP, so any MCP client
or Agent SDK agent can reuse them.

## User stories

<!-- To be defined with /feature before the milestone starts. -->

## Acceptance criteria

## Out of scope

## Open questions
