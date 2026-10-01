# review-pr

Authoring record for the `review-pr` skill. This file stays in the skills repository. `tools/install` copies `skill.md`, merges `repos/<repo>.md` into the generated skill, and copies `references/`, `scripts/`, `assets/`, `adapters/`, and `workflows/`. A markdown file beside `skill.md` is outside that set, so this README is not installed into Mobile or Extension.

The agent follows `skill.md`, `references/`, and the repo overlay. This README records why those rules exist and how to change them. A behavior change updates the agent file and this README in the same edit.

## What the skill is

One evidence-guided peer review of a MetaMask pull request or current local changes. It freezes a diff, separates author validation evidence, maps important claims, routes installed specialist skills, and returns reviewer guidance with paste-ready GitHub comments. Analysis is read-only; an explicitly approved follow-up can create a pending GitHub review.

The skill helps a peer decide what to examine or request next. The human reviewer owns the approval decision. A quiet report records the claims examined and evidence boundaries so it does not read as a certification.

It aggregates specialist skills. Each specialist remains the source of truth for its rules. `pr-guidelines`, `coding-guidelines`, testing, performance, and domain skills keep ownership of their checks.

`maturity: stable` and `base: true` put it in every consumer checkout, including `yarn skills` and an install filtered to domain `none`. The default installer uses `--maturity stable` before the base bypass, so an experimental base skill would be left out.

## How to run it

In a Cursor chat opened on the consumer repo:

```text
/mms-review-pr https://github.com/MetaMask/metamask-mobile/pull/12345
```

A pull request URL or number is a peer review of that repository. "Review my branch" or "review my changes" with no URL is a self-review of the current checkout.

The default reply is a completion card with finding counts. Cursor then calls `AskQuestion`, and Claude calls `AskUserQuestion`, with the question `What would you like to do next?` and the options Review findings, Review evidence, Suggested comments, and Output full review. Every later reply uses that same question and those same options. A finding id, `Frozen state`, or `Create the pending review` is free text on that question. **Output full review** prints the stored report in the chat. A request that includes `non-interactive` returns that same full report in the first message, including the sanitized review body and inline placements, and asks the pending-review question in text. Approval creates pending line comments only. The chat then shows the summary to paste into GitHub's review submission box.

Run it from the repo that owns the pull request. The Mobile overlay and the Extension overlay are different skills after install.

## Decisions



### 1. Freeze the target before any finding

The report stores this block once as its first section. The default display shows it when the developer asks for the frozen state. A review started with `non-interactive` prints it first:

```text
review-pr target
repository: <owner>/<name>
provider: gh | github-mcp | local-git
base: <40-char SHA>
head: <40-char SHA>
workingTree: included | excluded
```

SHAs come from command output. `HEAD` or `main` is not a frozen SHA.

`workingTree: included` only when the user asks to review current uncommitted changes. The reviewed diff is then the branch diff plus staged and unstaged diffs. A peer review sets `workingTree: excluded`.

### 2. Provider order

1. Authenticated `gh` when the user gives a pull request URL or number.
2. A GitHub MCP tool only when `gh` cannot authenticate and that one tool returns every peer field: repository, number, URL, title, body, base SHA, head SHA, diff, checks, and existing review comments. The report names the tool. A partial MCP response does not replace `gh`.
3. `local-git` for a self-review. For a peer review, only when the exact pull request diff is already in the checkout and GitHub data could not be read. That run is `DEGRADED`.

The minimum machine is a local checkout, `git`, Node.js, a shell, and file reads.

Every terminal call during a review is one invocation of a checked-in script from this skill. `references/operations.md` is the complete allowlist. Native file reads, native searches, and read-only MCP calls remain available. A missing operation returns `BLOCKED` with the scripted capability that the skill needs; the agent runs approved operations itself.

### 3. The diff is the pull request branch

A peer review resolves the checked-in collector relative to the installed skill root and runs:

```bash
node <skill-root>/scripts/collect-pr-context.mjs <number-or-url>
```

The collector contains the fixed, read-only `gh pr view`, `gh pr diff`, and paginated `gh api` calls. It validates the frozen SHAs and diff, then emits one normalized JSON document with the metadata, commits, check names and states, reviews, issue references, conversation comments, inline comments, and exact diff. Keeping collection and parsing in a reviewed script gives the agent one explicit operation instead of generated inline Python, Node, shell parsers, pipelines, or chained commands.

That diff is the review. The local branch, the working tree, and a different checkout are not substitutes.

Cited repository files are read at the frozen head:

```bash
node <skill-root>/scripts/read-frozen-file.mjs <head-sha> <repository-path>
```

When the head SHA is not local, the agent runs `ensure-pr-head.mjs` first. The scripts leave the working tree unchanged. A path that cannot be read at that SHA is `unavailable` for that file.

A `github.com` or `raw.githubusercontent.com` page is outside the provider order, including blob, pull, commit, and files views. Peer data comes from the collector, or from one GitHub MCP tool when `gh` cannot authenticate and that tool returns every required peer field. A failed read stays `failed` or `BLOCKED`.

### 4. Every source is available, unavailable, or failed


| Source                      | available                                                                                                | unavailable                                  | failed                                         |
| --------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ---------------------------------------------- |
| Local diff                  | Peer or self-review collector returned the frozen requested scope                                       | No diff for that scope                       | Script error, or the base SHA did not resolve  |
| Repository files            | `read-frozen-file.mjs` returned the path at the frozen head                                              | Cannot be read at the frozen head            | Script exited non-zero                         |
| Pull request title and body | `gh` or the equivalent MCP returned both                                                                 | Self-review has no pull request              | Command or tool error                          |
| Linked issue context        | A GitHub issue body or a Jira issue body was read                                                        | Neither was returned                         | Lookup error                                   |
| Checks                      | `statusCheckRollup` or the MCP equivalent was returned                                                   | Self-review, or the payload listed no checks | Command or tool error                          |
| Existing review comments    | Review and inline comment payloads were returned                                                         | Payloads were empty                          | Command or tool error                          |


A GitHub closing issue or a Jira issue is enough for linked issue context. The agent reads GitHub from `closingIssuesReferences`. When that list is empty, it reads a Jira key in the title or body with the installed Atlassian tool. One successful read makes the source `available`.

### 5. BLOCKED and source coverage

`BLOCKED` when the repository identity is missing, a SHA is missing, the diff is empty, or required terminal evidence has no registered script. The report names the status, missing evidence or scripted capability, and the checked-in recovery capability.

`Source coverage: DEGRADED` when the exact diff exists and any optional source is `unavailable` or `failed`. The conclusion names what that unread source blocked, including comment deduplication.

`Source coverage: complete` means every source is `available`.

An unread check, test, comment, or pull request body stays unknown. The report does not call it passed, unique, or ready.

### 6. What "checks" means

Checks are the pull request `statusCheckRollup`: each check's name and conclusion (success, failure, pending, skipped). The skill does not open workflow run logs.

`yarn lint`, `yarn lint:tsc`, and `yarn jest <file>` on Mobile, and `yarn lint:changed` and `yarn test:unit <file>` on Extension, stay unknown unless that rollup or the pull request body shows their result. A green app unit-test shard is not evidence that a script test file ran.

### 7. Fixed reasoning flow

Before specialist routing, `references/reasoning.md` gives every review the same fixed-cost process:

1. Extract explicit claims from the pull request, linked issue, diff, and tests.
2. Infer implicit safety claims such as preserved behavior, bounded failure, persistence, authorization, performance, and test coverage.
3. Draft a concise reviewer TL;DR in original agent wording from all available sources.
4. Rank claims by impact, reach, uncertainty, reversibility, and evidence strength.
5. Name a concrete counterexample or failure condition for each high-ranked claim.
6. Select evidence capable of examining that condition.
7. Route repository preferences and domain capabilities.
8. Record the evidence boundary and reviewer next step.

### 8. Skill taxonomy and routing

**Repository preference skills** encode norms, conventions, and rules. Examples: `pr-guidelines`, `coding-guidelines`, testing conventions, controller conventions, content guidance, and repo overlays.

**Domain capability skills** provide specialized knowledge. Examples: performance, analytics, feature flags, navigation, perps, flaky-test detection, observability, and high-cardinality review.

Every routing decision gets an independent per-skill block with class, matching paths, semantic signal, required inputs, and `applied` or `skipped` with the reason. Applied and skipped skills use the same block format so a class or reason always belongs to one named skill.

| Surface | Class | Module |
| --- | --- | --- |
| Pull request template and repository process | preference | `pr-guidelines`; Mobile `pr-readiness-check` feeds Author evidence |
| Source and test conventions | preference | `coding-guidelines`, repository testing skill |
| Mobile React Native rendering, effects, lists, data flow, or interaction cost | capability | `performance` |
| Extension rendering, effects, compiler behavior, or Redux identity | capability | Matching Extension performance skill |
| Analytics, flags, navigation, or installed domain behavior | capability | Matching installed domain skill |
| Mobile flaky detector scripts and workflows | capability | `flaky-test-detection` |
| Extension controllers | preference | `controller-guidelines` |
| User-facing strings | preference | `content-guidelines` |
| Metrics, traces, logs, or metric labels | capability | Installed observability skill |

A capability requires both a changed path and a semantic match. Copy-only component changes select content guidance; rendering behavior selects performance.

Tooling, CI, build, and documentation changes under `.github/`, `scripts/`, `development/`, and equivalent paths use matching repository preferences and tooling-domain capabilities. Their collocated tests are reviewed. Application-specific capabilities apply when application code also changed.

Mobile screen or view tests cite `docs/testing/component-view-tests.md`. Layer order comes from `mobile-testing`: component-view, integration, then unit. Extension unit tests cite `docs/testing.md` (favor Jest).

### 9. Existing comments are references

When review comments were read, the report cites them by id or URL and uses them to avoid repeating the same point. They are not new findings and they are not blockers. A blocker is a new issue in the frozen diff that those comments do not already state.

### 10. Author evidence

Author evidence describes how the author prepared and validated the pull request:

- manual testing;
- screenshots or recordings;
- changelog;
- linked issue;
- template coverage;
- check rollup;
- Mobile `pr-readiness-check` guidance.

Each is `provided`, `needs author evidence`, or `unread`. These statuses are separate from code-finding severity.

### 11. The report and comments to paste

The analysis still finishes every section in one pass. `write-temp-json.mjs` creates `temp/review-pr-<head-sha>.json` inside the repository when `temp/` is gitignored. The agent reads that file and overwrites it with the report, so a later reply can open one slice of that same review.

The default first message is the completion card: repository, short head SHA, coverage, and finding counts. The question tool then asks `What would you like to do next?` with these options, in this order, after the card and after every slice:

1. Review findings — titles of the issues found in this review, one `<SEVERITY>-<n> — <subject>` line each. The linked GitHub or Jira issue stays in review evidence.
2. Review evidence — author evidence, source availability, and the TL;DR.
3. Suggested comments — the paste-ready review body and inline comments.
4. Output full review — every stored section in one message.

A finding id, `Frozen state`, and `Create the pending review` are free-text replies on that question. A finding id opens that finding's record and its inline comment. The record uses a blank line between sections, and each evidence citation is its own line. A request that includes `non-interactive`, and the **Output full review** reply, print the stored sections in one message.

A report with an exact diff stores:

1. Target and frozen scope.
2. Data availability and coverage, one line per source.
3. TL;DR: two to four agent-rephrased bullets synthesized from the description, frozen changes, changed-code comments, existing review comments, and linked issue.
4. Author evidence.
5. Routing decisions with preference/capability classification.
6. Guided claim checks.
7. Existing comments as references.
8. Review coverage and conclusion.
9. Comments to add.

Each finding has a stable `<SEVERITY>-<n>` id, claim, risk checked, evidence type and citation, evidence boundary, severity, reviewer guidance, and exact requested edit. `SEVERITY` is `HIGH`, `MEDIUM`, or `LOW`; `n` is one report-wide sequence across all severities. For example, a low-severity first finding followed by a high-severity second finding uses `LOW-1` and `HIGH-2`. The finding record, inline comment, and later outcome row keep the same id.

Each new finding is one inline comment:

- Finding id.
- Where: file path and line on the frozen head.
- Severity: `HIGH`, `MEDIUM`, or `LOW`.
- Why it matters from the evidence.
- Exact requested edit: what to add, remove, replace, or verify.

The conclusion describes preparation with `Readiness evidence reviewed; open author evidence is listed above.` Approval remains the human reviewer's decision.


| Severity | Conventional comment        | Use for                                                          |
| -------- | --------------------------- | ---------------------------------------------------------------- |
| `HIGH`   | `issue (blocking)`          | A demonstrated material defect that requires a change            |
| `MEDIUM` | `suggestion (non-blocking)` | A demonstrated concern with a concrete improvement               |
| `LOW`    | `nitpick (non-blocking)`    | Wording, a comment, or a small consistency fix                   |


There is no numeric review score.

### 12. Later outcome assessment

When requested, a later pass classifies each finding:

- `confirmed`: later evidence supports it;
- `rejected`: later evidence shows it was unfounded;
- `unresolved`: later evidence has not settled it;
- `missed`: a later defect in the frozen diff was outside the findings.

Confirmed findings are true positives, rejected findings are false positives, and missed defects are false negatives.

```text
precision = confirmed / (confirmed + rejected)
recall = confirmed / (confirmed + missed)
```

Unresolved findings stay outside both formulas. A ledger row is persisted only after an explicit request to a destination outside the reviewed checkout.

Recall requires a defined later defect inventory from an adjudicator, accepted follow-up fixes, incident review, or equivalent evidence. An assessment of the reported findings alone uses `missed: unknown` and `recall: unknown`.

### 13. Read-only analysis and pending review

The analysis does not edit, commit, or push the checkout, and it does not run the app. An existing GitHub pull request gets one optional write flow. The default mode starts it when the developer asks for suggested comments, and at the end of **Output full review**. A review started with `non-interactive` starts it at the end of the full report:

1. Display the exact sanitized review summary and every inline path, line, side, and body.
2. Ask `Create these comments as a pending GitHub review?`.
3. After explicit approval, create `review-pr-pending-<head-sha>.json` with `write-temp-json.mjs`, then read and overwrite it with the approved manifest.
4. Run `create-pending-review.mjs`. It rechecks the frozen head, detects an existing pending review for the authenticated reviewer, and sends one atomic create-review request. The manifest keeps the review summary. The GitHub request sends an empty `body` and omits `event`.
5. Remove the temporary manifest and return the pending review URL.
6. Print the summary under **Paste into Leave a comment**. The reviewer opens **Files changed**, pastes that summary, chooses Comment, Approve, or Request changes, and presses **Submit review**.

The pending review contains only the line comments. Self-reviews remain conversation-only.

## Evaluation preregistration

Registered on 2026-09-25 before treatment installation.

### Control and treatment

- **Control:** source bundle SHA-256 `804ea603866dc15dbfa307d2126fef91ddf10578bc7fa4a1898c57ab96ba0997`, authored on repository base `45730f8`.
- **Treatment:** the evidence-guided reasoning, routing taxonomy, author-evidence split, and finding record documented above.
- **Runner:** matching Mobile or Extension consumer agent with the inherited session model.
- **Provider:** authenticated `gh`, local frozen-head reads, installed repository skills, and issue context when available.

### Frozen corpus

| Repository | Pull request | Surface | Frozen head | Control output SHA-256 |
| --- | --- | --- | --- | --- |
| MetaMask Mobile | `#36273` | application | `ef52f03e68d32585145cf547051e7c240b0bdafa` | `ab16ebd34781721dd6c3728f4070ed9c79f359f46da488790efd88b317384686` |
| MetaMask Mobile | `#36337` | CI/tooling | `bc0f177ad0d30c2fa04f0cb6de9aeb9e766217ca` | `a3a6af98c51915f99926ae2cb671a8a89aa092c88d9740071efb141a248a05a6` |
| MetaMask Extension | `#46630` | application | `117ecb5929a462075a351e6c449b2f86b40dbad5` | `14c5be7fd69dfe5ef108a7d6408fe2e2d025e4dcfed5da2c27c303727451f981` |
| MetaMask Extension | `#46562` | build tooling | `cb9d09dd66d94a06cfa965d7f7603d8a9f4249ca` | `72e4e62cebe180056d8ec132bad2ea14dff54fb5941026353c6548d0a86a408e` |

The treatment uses the same four pull requests, frozen heads, consumer types, model inheritance, and providers.

### Metrics

One unique finding against one frozen head is the measurement unit.

Primary:

- precision;
- recall;
- unsupported-finding rate;
- duplicate-finding rate.

Secondary:

- reviewer usefulness;
- actionable-comment rate;
- token cost;
- duration.

Outcome labels are `confirmed`, `rejected`, `unresolved`, and `missed`. Human adjudication uses the frozen diff and later evidence. Review usefulness asks whether the guidance helps the reviewer decide what to inspect or request next.

## Files


| File                          | Role                                                       |
| ----------------------------- | ---------------------------------------------------------- |
| `skill.md`                    | Workflow, require, and reject. Installed as the skill body |
| `references/providers.md`     | Provider order, freeze block, commands, source table       |
| `references/operations.md`    | Complete reviewed terminal-operation allowlist             |
| `references/reasoning.md`     | Fixed claim, risk, and evidence reasoning flow             |
| `references/routing.md`       | Which installed skill runs for which surface               |
| `references/report.md`        | `BLOCKED`, `DEGRADED`, sections, comment text              |
| `scripts/*.mjs`               | Peer, self-review, frozen evidence, search, and pending-review operations |
| `scripts/*.test.mjs`          | Unit and terminal-policy tests for the operation surface   |
| `repos/metamask-mobile.md`    | Mobile paths, commands, and app-vs-script routing          |
| `repos/metamask-extension.md` | Extension paths, commands, and app-vs-script routing       |
| `README.md`                   | This record. Not installed                                 |




## How to change it

1. Edit the agent file that owns the rule (`skill.md`, a reference, or a repo overlay) and update this README to match.
2. From the skills repo root, lint this skill:

```bash
node .github/scripts/lint-skill-entry.mjs domains/pr-workflow/skills/review-pr/skill.md
```

1. Reinstall into each consumer so the generated `mms-review-pr` files match:

```bash
./tools/install --repo metamask-mobile --target "$METAMASK_MOBILE" --include pr-workflow/review-pr
./tools/install --repo metamask-extension --target "$METAMASK_EXTENSION" --include pr-workflow/review-pr
```

Generated files under the consumer `.cursor/`, `.claude/`, and `.agents/` trees are overwritten on the next install. Edit this directory, then install again.