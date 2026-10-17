---
id: F-006
title: 'Document ingestion: Google Drive and OneDrive/SharePoint'
status: proposed
priority: should
depends_on:
- F-001
stories: []
tracker: {}
milestone: M5
---

# Document ingestion: Google Drive and OneDrive/SharePoint

## Problem

Requirements and decisions are buried in shared documents.

## Proposal

A `StoragePort` gets Drive and OneDrive/SharePoint adapters. `/ingest` pulls selected documents
into `kb/sources/` with provenance, then extracts decisions, risks and actions into `kb/`. It
works MCP-first; adapters are added where runs must be repeatable.

## User stories

<!-- To be defined with /feature before the milestone starts. -->

## Acceptance criteria

## Out of scope

## Open questions
