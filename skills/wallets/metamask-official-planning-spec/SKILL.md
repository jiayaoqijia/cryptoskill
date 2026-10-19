---
name: planning-spec
description: >-
  Use after mms-planning recommends a spec and the engineer confirms, and
  when the user asks for a planning spec. Ask one unblocked product or
  engineering question at a time, the one that most reduces uncertainty,
  then write one English file at
  .specs/spec-XXX-short-description.md in the MetaMask Mobile checkout. Do
  not edit product code, and do not say that in chat. Do not write a -pt.md
  sibling.
base: true
maturity: stable
---

# Planning spec

Installed name: `mms-planning-spec`. Use it only after `mms-planning` recommends a spec and the engineer confirms, or when the engineer asks for a planning spec. Do not edit product code in the turn that writes the file, and do not say that in chat.

## When to use

- The engineer confirmed a spec recommendation from `mms-planning`.
- The engineer asked for a planning spec.

## Workflow

1. Ask one question at a time. Choose the unblocked question that most reduces uncertainty. A question is unblocked when it can be stated precisely without an answer that is still open. Cover product unknowns and engineering unknowns. Product includes who is affected, what they see, scope, and non-goals. Engineering includes where the change lives, compatibility, and how it will be tested.
2. Ask when the question can be stated precisely now, even if the answer is unknown. When an in-scope area cannot be stated precisely because it depends on an open answer, keep it as not yet specified. Do not split that area into questions. When the blocking answer arrives, state any question that is now precise, then ask the unblocked one that most reduces uncertainty.
3. Stop asking when every precise unknown is decided, explicitly deferred, or recorded as an open question, and every remaining in-scope area is not yet specified. State the direction.
4. When the direction is ready, state it and wait. Write the file only after the engineer approves. If they do not approve, ask the next unblocked question.
5. After approval, and before writing, use the same catalog rule as `mms-planning`. Read the installed `mms-*` catalog. Read every skill whose area the spec touches, including a partial fit. Skip a skill only when the spec has no surface for it. Run an explicit performance check. Read `mms-performance` when the change has a performance surface. The named routing list in `mms-planning` is a floor, not an allowlist. Name a matching skill that is unavailable. Do not pretend it was applied.
6. Write one English file at `.specs/spec-XXX-short-description.md` in the checkout. `.specs/` is local and not team-shared storage. Do not stage it. Sharing the file is a manual step outside this skill.

Numbering is the highest existing `.specs/spec-*.md` plus one. If none exist, start at `001`. The slug is two to five kebab-case words. The H1 is `# spec-XXX: <short name>`.

Section order:

1. `## Summary`
2. `## Copy Prompt for Implementation`
3. `## Context`
4. `## Hypothesis`
5. `## Decisions`
6. `## Implementation Details`
7. `## Development Flow`
8. `## Performance`
9. `## Security`
10. `## UX`
11. `## Open Questions`
12. `## Not yet specified`
13. `## Acceptance Criteria`
14. `## How to Test`, with `### Agent`, `### Human — Android`, `### Human — iOS`, and `### Optional`
15. `## Log`

Keep every heading. When Performance, Security, or UX has no surface, the body of that section is `N/A`. The chat brief from `mms-planning` still omits empty areas. This file does not.

`## Open Questions` lists questions that can be stated precisely and are still open or deferred. When there are none, the body is `None`. 

`## Not yet specified` lists in-scope areas that cannot yet be stated as a question. When there are none, the body is `None`. An area lives in only one of those sections. Work ruled out of this spec is recorded under Decisions.

`## Development Flow` is one Mermaid diagram of the change being specified: sequence, decisions, loops, and any path that does not reach implementation. The diagram describes that feature. It does not describe `mms-planning`, `mms-planning-spec`, or `mms-jira-brief`. If the diagram disagrees with Decisions or Implementation Details, the prose wins and the diagram is corrected before approval. Do not embed a diagram of this skill's own procedure.

UX states who is affected and what they see. Include empty, error, and loading states when the change has them. State iOS versus Android when they differ.

Copy Prompt for Implementation is one or more fenced `text` blocks. Labels, in order, omitting an empty optional label: `LOCK`, optional `BASELINE`, `CHANGE`, `VERIFY`, `CLOSEOUT`, `HARD STOPS`, `IF STUCK`. `LOCK` points at the `.specs/` file inside the checkout. `IF STUCK` is exactly `Ask any questions needed if anything ambiguous.`

`VERIFY` and `CLOSEOUT` name what the spec says to check. They do not run a quality pipeline and they do not set a retry policy. `VERIFY` points at `## How to Test`. `CLOSEOUT` points at `## Acceptance Criteria` and the evidence to record in `## Log`. `### Agent` under How to Test names the checks for this change. It does not name a runner.

After the file is written, stop. Do not edit product code. Do not say that code will not change.