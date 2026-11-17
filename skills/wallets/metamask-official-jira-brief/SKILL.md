---
name: jira-brief
description: >-
  Use when the engineer asks to understand a Jira ticket, explicitly
  refers to one, or the message contains a Jira browse URL
  (/browse/<KEY>). Do not hunt for a ticket, ask
  whether a token is a ticket, or suggest creating one. Write
  .briefs/<ISSUE-KEY>.md with the Goal, Decisions Already Made, Open
  Decisions, and Code Surfaces sections. Name the path in chat. Do not paste
  the file or write to Jira. Do not edit product code, and do not say that
  in chat.
maturity: stable
base: true
---

# Jira brief

Installed name: `mms-jira-brief`. The engineer can invoke it directly. `mms-planning` calls it only when the message has a Jira browse URL or the engineer explicitly refers to a Jira ticket. Do not edit product code, and do not say that in chat. Do not write to Jira. Do not embed a Mermaid diagram of this procedure, and do not put one in `.briefs/`.

## When to use

- The message contains a Jira browse URL (`/browse/<KEY>`).
- The engineer asks to understand a Jira ticket, or otherwise explicitly refers to a Jira ticket.
- `mms-planning` delegates because a browse URL or an explicit Jira reference is present.

## Workflow

1. When the engineer invokes this skill directly and there is no browse URL and no key, ask which ticket. Then continue with the answer. When `mms-planning` delegates and there is no candidate browse URL or key, return no ticket identified. Do not ask.
2. A browse URL whose path contains `/browse/<KEY>` is a ticket. Do not ask.
3. A bare `<PROJECT>-<number>` token is not a ticket from the pattern alone. `MCWP` is the mobile platform project, not the only valid project. There is no project allowlist.
4. Ignore tokens that are clearly not Jira issues, without a question. Examples: `EIP-7702`, `CAIP-19`, and `HIP-3`.
5. A bare token is a ticket when Jira resolves it. When the engineer invoked this skill directly, no URL is present, and a token might be a Jira issue but Jira does not resolve it or the lookup is inconclusive, infer from surrounding words such as ticket, Jira, or issue. If still unsure, ask whether that token is a Jira issue. Yes continues the brief flow. No treats it as not a ticket. When `mms-planning` delegates, do not ask. An unresolved or unsure token returns no ticket identified.
6. Not a ticket: stop. Do not write a file.
7. Each resolved key produces one `.briefs/<ISSUE-KEY>.md`. Several keys produce one file each. `.briefs/` is local and not team-shared storage. Do not stage it.
8. If `.briefs/<ISSUE-KEY>.md` already exists and the engineer did not ask to regenerate it, open the issue and compare its updated time with the `Jira updated:` line in the brief. A failure file is never a fresh brief. It has no `Jira updated:` line. If the times match, read the file and do not regenerate it. If they differ, or the line is missing, regenerate the file. If the issue does not open, read the existing file and say that freshness was not checked.
9. Otherwise open the issue in Jira. If it opens, write the file with these headings, in this order: `## Goal`, `## Decisions Already Made`, `## Open Decisions`, `## Code Surfaces`. End the file with `Jira updated:` and the updated time Jira returned. If it does not open, do not block. Write `.briefs/<KEY>.md` that records the key, the failure, and any ticket text the user already provided. Say what was missing. A failure file has no `Jira updated:` line.
10. Do not copy secrets, tokens, credentials, or customer data into the file.
11. In chat, name the path. Do not paste the file. Do not write to Jira. Do not say that code will not change.

When `mms-planning` delegates and no ticket is identified, return no ticket identified and stop. Do not ask for a ticket. Do not suggest creating one. `mms-planning` then continues. A revert does not call this skill.
