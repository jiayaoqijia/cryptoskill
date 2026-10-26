---
name: jira-brief
description: >-
  Use when mms-planning delegates ticket identification or a brief, and
  when the engineer asks to understand a Jira ticket. Write
  .briefs/<ISSUE-KEY>.md with the Goal, Decisions Already Made, Open
  Decisions, and Code Surfaces sections. Name the path in chat. Do not paste the
  file or write to Jira. Do not edit product code, and do not say that in chat.
base: true
maturity: stable
---

# Jira brief

Installed name: `mms-jira-brief`. `mms-planning` calls it for ticket identification. The engineer can invoke it directly. Do not edit product code, and do not say that in chat. Do not write to Jira. Do not embed a Mermaid diagram of this procedure, and do not put one in `.briefs/`.

## When to use

- `mms-planning` calls this skill.
- The engineer asks to understand a Jira ticket.

## Workflow

1. When the engineer invokes this skill directly and there is no browse URL and no key, ask which ticket. Then continue with the answer. When `mms-planning` delegates and there is no candidate browse URL or key, return no ticket identified. Do not ask.
2. A browse URL whose path contains `/browse/<KEY>` is a ticket. Do not ask.
3. A bare `<PROJECT>-<number>` token is not a ticket from the pattern alone. `MCWP` is the mobile platform project, not the only valid project. There is no project allowlist.
4. Ignore tokens that are clearly not Jira issues, without a question. Examples: `EIP-7702`, `CAIP-19`, and `HIP-3`.
5. A bare token is a ticket when Jira resolves it, or when the engineer confirms it. When no URL is present and a token might be a Jira issue but Jira does not resolve it, or the lookup is inconclusive, infer from surrounding words such as ticket, Jira, or issue. If still unsure, ask whether that token is a Jira issue. Yes continues the brief flow. No treats it as not a ticket.
6. Not a ticket: stop. Do not write a file.
7. Each resolved key produces one `.briefs/<ISSUE-KEY>.md`. Several keys produce one file each. `.briefs/` is local and not team-shared storage. Do not stage it.
8. If `.briefs/<ISSUE-KEY>.md` already exists and the engineer did not ask to regenerate it, open the issue and compare its updated time with the `Jira updated:` line in the brief. A failure file is never a fresh brief. It has no `Jira updated:` line. If the times match, read the file and do not regenerate it. If they differ, or the line is missing, regenerate the file. If the issue does not open, read the existing file and say that freshness was not checked.
9. Otherwise open the issue in Jira. If it opens, write the file with these headings, in this order: `## Goal`, `## Decisions Already Made`, `## Open Decisions`, `## Code Surfaces`. End the file with `Jira updated:` and the updated time Jira returned. If it does not open, do not block. Write `.briefs/<KEY>.md` that records the key, the failure, and any ticket text the user already provided. Say what was missing. A failure file has no `Jira updated:` line.
10. Do not copy secrets, tokens, credentials, or customer data into the file.
11. In chat, name the path. Do not paste the file. Do not write to Jira. Do not say that code will not change.

`A Jira ticket would improve this context.` belongs to `mms-planning`. That skill adds the line only when no brief was actually read and the change stops for a brief. A revert does not get that line. This skill does not add that line.
