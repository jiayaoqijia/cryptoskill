# Jira filing

Phase 6 only, after the user approves the plan and says to file.

## Assets team settings

| Setting | Value |
| --- | --- |
| Jira site | `consensyssoftware.atlassian.net` |
| Project | `ASSETS` |
| CODEOWNERS team | `@MetaMask/metamask-assets` |
| Repos | `MetaMask/metamask-mobile`, `MetaMask/metamask-extension`, `MetaMask/core` |
| Epic labels | `quality` or `tech-debt`, plus a work-type label (for example `react-compiler`, `test-quality`) and the platform (`mobile`, `extension`, `core`) |
| Child labels | the epic's labels |
| Not agent-eligible | add `human-only` |
| Release Number | set it on every child, or a team automation comments on each one. Core is a library: `Not applicable` |
| Assignee | leave empty |
| GitHub PR labels (in ticket text) | core: `team-assets`, `agent-assets`, `no-changelog` for test-only work |

**Never add `ai-agent`.** If the user's label list contains it, drop it and say so. A human adds it to the epic when they want agents to start.

## Steps

1. **Dry run.** For the epic and each child, show: summary, labels, parent, Blocks edges, and the first lines of the description. Confirm the count matches `plan.json`. Write nothing.
2. **Epic.** Create it (type Epic) from `epic.md`, or update the description of the epic the user gave you.
3. **Children.** Create each ticket (type Task) with `parent` = the epic key, its labels and Release Number. Create in wave order so blockers get keys first, and record each key in `plan.json` as you go, so a failed run can resume without duplicates.
4. **Placeholders.** Replace placeholder ids (`<P2-A1>`) in "Start only after" lines with real keys and update those descriptions.
5. **Links.** For each edge, create an issue link of type `Blocks`, outward from the blocker to the blocked ticket.
6. **Epic tables.** Fill the keys into the epic's phase tables and update its description.
7. **Report.** The epic URL, the number of children per wave, and: "Add `ai-agent` to the epic to start dispatch."

## Description format

Jira Cloud descriptions are Atlassian Document Format (ADF). Convert the ticket markdown to ADF, keeping headings, tables, fenced code, inline code, links, bold and quote panels. Keep the markdown as the source of truth in `tickets/` so tickets can be regenerated. Check one filed ticket in the browser before filing the rest: tables and links must render.

Descriptions are limited to 32,767 characters of ADF. A ticket that comes near that is too big; split it.

## After filing

- A ticket whose PR a reviewer closed without merging gets `human-only` and a comment; do not re-dispatch it.
- A ticket whose finding no longer reproduces is cancelled with the evidence, not rewritten.
