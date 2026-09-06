---
name: acceptance-criteria-doc
description: Generate an Acceptance Criteria (AC) live Confluence doc for a Jira epic, following the Assets team's standard structure (Overview, Documentation table, Testing Scenarios table with Given/When/Then criteria and QA sign-off checkboxes), then link it from the epic and its stories. Use this whenever the user asks to create acceptance criteria, ACs, an "AC doc", testing scenarios, or QA sign-off criteria for an epic or feature — even if they only paste a Jira epic link and say "create the ACs for this". Also use it when asked to update or regenerate an existing "<EPIC-KEY> - ACs" Confluence page.
maturity: experimental
---

# Acceptance Criteria Doc Generator

Produce three things for a given Jira epic:

1. A **live Confluence page** titled `<EPIC-KEY> - ACs` in the **TL1** space, inside the [Assets - Acceptance Criteria folder](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/folder/401775165477) (`parentId: 401775165477`), on cloud `consensyssoftware.atlassian.net`.
2. A **Jira comment on the epic** linking the doc.
3. The **AC doc link appended to every child issue's description** (stories, tasks, spikes — all children).

Example outputs: [ASSETS-3647 - ACs](https://consensyssoftware.atlassian.net/wiki/x/GoC_i10) (Market Insights), [ASSETS-3645 - ACs](https://consensyssoftware.atlassian.net/wiki/x/L4C7i10) (CTA Optimisation).

## Inputs

Required: the **epic** (key or URL). Everything else is optional and should be mined rather than requested:

- **Epic description & remote links** — often contain the feature flag name, Definition of Done link, PRD, ADR/tech-spec, Figma/Replit links, and a "source epic" (e.g. the Mobile epic a parity feature is ported from). Extract all of these.
- **Repositories** — if the user names repos, investigate them; if the feature is a port/parity of an existing implementation, the source repo is the primary investigation area even if unnamed.
- **PRD / Figma / Replit / ADR** — link them in the Documentation table when available. Don't block on missing ones; note the gap to the user in your final summary instead of padding the doc.

## Workflow

### 1. Gather Jira context

- `getJiraIssue` on the epic (markdown format) — read the description carefully for flags, links, and scope checklists.
- `searchJiraIssuesUsingJql` with `parent = <EPIC-KEY> ORDER BY created ASC` to get the child issues. Each testable story becomes a criteria group; spikes/discovery tasks get the AC link but **not** a criteria row (they aren't testable).
- If the epic references a source epic (ported feature), fetch its children too — their titles reveal the real scope (analytics, e2e tests, edge cases) that the new epic's stories may summarize away. Large JQL responses get saved to a file; extract just `key/status/summary` with `jq` rather than reading the whole payload.

### 2. Fetch the structural reference

The house style lives in the previous AC docs, not in this skill. Call `getConfluencePageDescendants` on the folder (`pageId: 401775165477`) and pick the most recently created `<KEY> - ACs` page, then fetch it with `getConfluencePage` (`contentFormat: "html"`). Mirror its structure, heading order, table layouts, and cell markup **exactly** — this keeps every new doc consistent with whatever the team's current format is, even as it evolves. When reusing its markup as a scaffold, strip all `data-local-id` attributes (Confluence assigns fresh ones).

### 3. Investigate repositories

In parallel with the above, spawn a `general-purpose` subagent to research the reference implementation — this is what makes the criteria concrete instead of generic. Have it use `gh` (PR search, code search) rather than cloning. Ask it to report, with exact names and file paths:

- Merged PRs (number, title, URL, one-liner) that built the feature
- Component names/paths
- Feature flag names (both the new surface's flag and the reference implementation's)
- Analytics event names and their properties, and where they fire
- Data source (API/controller/package)
- Empty/error/loading state handling worth testing

### 4. Compose the document

The structure (matching the reference doc from step 2) is:

1. `h1` — "Acceptance Criteria for <Epic title>"
2. `h1 Overview` — one paragraph: what the epic delivers, referencing the source implementation if it's a port.
3. `h2 Documentation` — two-column table (Document Type | Link): epic, Definition of Done, source epic, repo(s), data source, feature flag, plus PRD/Figma/ADR when available.
4. `h1 Testing Scenarios` — intro sentence ("must be tested successfully prior to feature release…"), then the criteria table with columns: Criteria (500) | Expected Result (220) | one 90-wide checkbox column per platform.

**Choosing QA sign-off columns:** infer from the epic's scope. A parity/port epic gets a column per platform (e.g. Extension + Mobile); a single-platform epic gets one column. If genuinely ambiguous, ask the user before creating the page.

**Writing the criteria** — the audience is devs, PMs, EMs, and QA skimming during sign-off. Criteria that are long or clever get ignored, so:

- **Group rows by story.** First row of each group starts with a bold group title linking the story (e.g. `**Market Insights entry card** — see ASSETS-3682`). Follow-up rows in the group have no title.
- **One behavior per row**, written as three Given/When/Then bullets. If a Then clause needs an "and… and… and…", split the row.
- **Expected Result is one plain sentence** — the thing QA verifies, no restating the Given/When.
- **Cite evidence inline**: reference PRs, exact event names, flag names, and property names in `code` formatting. Concrete names are what let QA actually verify parity.
- **Always include** a feature-flag gating row (flag off → no UI, no events) and a performance row (no regression vs. current experience) at the end.
- **Target 8–12 rows total.** If the epic is bigger than that, tighten the Expected Results before adding rows; a doc nobody reads verifies nothing.

### 5. Create the page and link everywhere

1. `createConfluencePage` with `spaceId: "TL1"`, `parentId: "401775165477"`, `subtype: "live"`, `contentFormat: "html"`, title `<EPIC-KEY> - ACs`.
2. Take the **tiny link** from the response (`_links.tinyui`, e.g. `/x/GoC_i10` → `https://consensyssoftware.atlassian.net/wiki/x/GoC_i10`) and use it in all Jira writes.
3. `addCommentToJiraIssue` on the epic (`contentFormat: "markdown"`): link the doc and one sentence on what it covers, linking the stories.
4. For **each child issue**: append `**Acceptance Criteria:** [<EPIC-KEY> - ACs](<tiny link>)` to its description via `editJiraIssue` — but only after fetching the current description in-context, so existing text is preserved verbatim (and so the write isn't blocked as a blind overwrite; see Gotchas).

### 6. Report

End with: the doc link, the epic comment confirmation, which issues were updated, and anything discovered in the repo investigation that the epic's stories **don't** cover (candidate out-of-scope items). That last part regularly surfaces real scope gaps — don't skip it.

## Gotchas (all hit in practice)

- **`editJiraIssue` responses can echo the wrong issue.** After batch description updates, verify with one `searchJiraIssuesUsingJql` read of the edited keys instead of trusting the write responses.
- **Blind description writes get blocked.** The permission layer rejects `editJiraIssue` description writes when the current description wasn't visibly fetched first. Fetch, then write fetched-text + appended link.
- **Checkbox cells** must be exactly `<ul data-type="task-list"><li data-type="task-item"><input type="checkbox"> </li></ul>` — anything else silently fails to become a Confluence task. Verify this matches the reference doc fetched in step 2.
- **Never invent `data-local-id`** attributes; omit them on new content and strip them from copied scaffold markup.
- **Don't wrap the body** in `<html>/<head>/<body>`, and keep Given/When/Then bullets as plain `<li><p>…</p></li>` (list items can't contain headings/tables/panels).

## Reusing this for another team

Everything above is team-agnostic except three values: the space key (`TL1`), the AC folder `parentId` (`401775165477`), and the example links. Change those to your team's equivalents and the rest applies unchanged.

Written up for humans at [Skill - Acceptance Criteria Creation](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/401778016257/Skill+-+Acceptance+Criteria+Creation), which is the page to point teammates at.
