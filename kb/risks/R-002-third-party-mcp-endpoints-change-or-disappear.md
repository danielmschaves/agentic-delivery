---
id: R-002
title: Third-party MCP endpoints change or disappear
status: open
likelihood: high
impact: medium
owner: template maintainer
---

# Third-party MCP endpoints change or disappear

## Description

Vendor MCP servers (Atlassian, Azure DevOps, Microsoft) are young and their URLs and auth flows
change. Atlassian's documentation already lists several endpoint paths.

## Mitigation

- MCP endpoints live in one template file (`.mcp.json.jinja`), so a fix rolls out via
  `copier update`.
- Anything critical or repeatable moves to coded adapters against stable REST APIs.

## Trigger / early warning

- `/mcp` authentication failures in a hub.
- Vendor deprecation notices.
