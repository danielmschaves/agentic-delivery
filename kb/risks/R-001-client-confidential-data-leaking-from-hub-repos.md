---
id: R-001
title: Client-confidential data leaking from hub repos
status: open
likelihood: medium
impact: high
owner: delivery lead
---

# Client-confidential data leaking from hub repos

## Description

Hubs hold client documents, transcripts and decisions. A hub repo with the wrong visibility, or
content copied into the public template repo, commit messages or PR descriptions, would expose
client data.

## Mitigation

- Client hubs are private repos in the client's own organisation where possible.
- The template repo holds no client content. Instances are separate repos.
- gitleaks runs in pre-commit and CI. `.env` is gitignored, and the agent is denied from reading it.
- CLAUDE.md tells the agent to keep confidential material out of commit and PR text.

## Trigger / early warning

- A hub repo created as public.
- A secret-scanning alert.
