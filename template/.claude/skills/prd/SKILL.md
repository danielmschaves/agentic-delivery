---
name: prd
description: >-
  Create or revise the hub's product requirements document (product/prd.md) and break it into
  features. Use when the user wants to define the product, start a PRD, update scope, or turn
  notes, meetings or documents into requirements.
argument-hint: "[focus, e.g. 'revise scope after steering meeting']"
---

# PRD

The PRD is the short, current statement of *why* and *what*. Details live in feature files
(`product/features/F-xxx-*.md`), milestones in `product/roadmap.yaml`, decisions in `kb/decisions/`
and risks in `kb/risks/`. Keep the PRD to what a stakeholder reads in ten minutes.

## 1. Gather context before asking

- Read `project.yaml`, the existing `product/prd.md` (if any), `product/roadmap.yaml` and
  `uv run ad list feature`.
- Skim `kb/` for relevant material: meeting notes, sources, decisions, risks.
- If the user points at external material (a Drive or OneDrive doc, an email thread, a Jira epic,
  a meeting transcript), fetch it through the MCP tools available. Save anything you rely on to
  `kb/sources/` with provenance frontmatter (`source`, `retrieved`, `author`), so the PRD can cite it.
- If no PRD exists, run `uv run ad prd init` to create it from the template.

## 2. Interview, one topic at a time

Fill gaps with short, concrete questions; don't ask about anything the context already answers.
Cover, in order:

1. **Problem**: who is struggling with what, and what evidence do we have?
2. **Users and stakeholders**: who uses it, and who decides.
3. **Goals**: outcomes that can be checked. Push back on outputs dressed up as goals.
4. **Non-goals**: what is explicitly out.
5. **Success metrics**: baseline, target, and how each is measured.
6. **Constraints and assumptions**: deadlines, budget, tech, compliance.
7. **Risks and open questions.**

Offer a proposed answer the user can accept or correct whenever you can infer one; that's faster
than open questions.

## 3. Write

- Update `product/prd.md` section by section, keeping the template headings. Link evidence (`kb/...`)
  rather than pasting it.
- For each risk worth tracking, run `uv run ad new risk "<title>"` and fill in the file. Do the same
  for decisions already made: `uv run ad new decision "<title>"`.

## 4. Break down into features

- Propose a feature list (title, one-line intent, MoSCoW priority, milestone) and confirm it with
  the user before creating files.
- Add or update milestones in `product/roadmap.yaml`:
  `milestones: [{id: M1, title: ..., target: YYYY-MM-DD}]`.
- Create each new feature with `uv run ad new feature "<title>"`. Set `priority` and `milestone` in
  its frontmatter, and write a 2–3 line Problem/Proposal. Deeper definition happens with `/feature`.
- Update the PRD's Scope and Milestones sections to link the feature files.

## 5. Check

- Run `uv run ad validate` and fix every error.
- Summarise for the user: what changed in the PRD, which features were created or changed, and the
  open questions still blocking definition.
