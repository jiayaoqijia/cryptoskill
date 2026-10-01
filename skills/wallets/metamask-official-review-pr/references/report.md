# Report

Finish one report that guides a human reviewer, then display it with **Presentation**. A `BLOCKED` report stops before claim checks and is shown in full. A report with an exact diff stores every section below and states `Source coverage: complete` or `Source coverage: DEGRADED`.

## Presentation

Finish every section, including **Comments to add**, before the first user-visible review message. Store that report with `write-temp-json.mjs` from [operations.md](operations.md), then read the created file and overwrite it with the report JSON. The file is `temp/review-pr-<40-character-head-sha>.json` inside the repository.

Choose the mode from the message that starts the review:

- **Default.** Print the completion card, then ask what to open with the question tool in **Interactive questions**.
- **Non-interactive.** The starting message contains `non-interactive` as its own word, ignoring case. Print every section in **Reports with an exact diff**, in that order, in the same message, including **Comments to add**. For an existing GitHub pull request, ask `Create these comments as a pending GitHub review?` in that message. Do not call the question tool.

A later reply reads the stored file and prints one slice of the finished review. In the default mode, the question tool asks for the next action after that slice. Routing decisions, existing review comments, and the coverage conclusion are printed when the user asks for them, and they are included when the user asks for the full review.

### Completion card

```text
Review complete.
<repository> · <pr number or branch> · <head SHA, 12 chars>
Coverage: complete | DEGRADED
Findings: HIGH <n> · MEDIUM <n> · LOW <n>
```

The counts are the only finding content on the card. The next action is the question tool, not a menu printed under the card.

### Interactive questions

In the default mode, ask with the harness question tool. Cursor calls `AskQuestion`. Claude calls `AskUserQuestion`. The call contains one question. The question text is `What would you like to do next?`. The options are these four labels, in this order, after the completion card and after every later slice:

1. Review findings
2. Review evidence
3. Suggested comments
4. Output full review

A finding id such as `HIGH-1`, the words `Frozen state`, and the words `Create the pending review` are free-text replies on that same question. `Create the pending review` is the approval after **Suggested comments** or **Output full review** for an existing GitHub pull request. A review started with `non-interactive` asks `Create these comments as a pending GitHub review?` in text at the end of the full report.

### Slices

1. **Review findings.** One line per issue this review found in the frozen diff: `<SEVERITY>-<n> — <subject>`. The linked GitHub or Jira issue the pull request addresses stays in Review evidence.
2. **Review evidence.** Author evidence, source availability, and the TL;DR. Evidence for one finding stays on that finding.
3. **Frozen state.** The frozen target block from [providers.md](providers.md).
4. **Suggested comments.** The paste-ready review body and inline comments. For an existing GitHub pull request, end the slice with `Reply Create the pending review to create the pending line comments.`
5. **Output full review.** Print every section in **Reports with an exact diff**, in that order, in the chat. Include **Comments to add**. For an existing GitHub pull request, end that message with `Reply Create the pending review to create the pending line comments.` This reply is the stored review, not the completion card.

A finding id prints that finding's record in the expanded layout below, then its inline comment.

### Stored report

```json
{
  "schemaVersion": 1,
  "displayMode": "default",
  "target": {
    "repository": "<owner>/<name>",
    "provider": "gh",
    "base": "<40-character SHA>",
    "head": "<40-character SHA>",
    "workingTree": "excluded",
    "sourceCoverage": "complete"
  },
  "dataAvailability": [],
  "tldr": [],
  "authorEvidence": [],
  "routingDecisions": [],
  "findings": [],
  "claimsExamined": [],
  "openQuestions": [],
  "existingComments": [],
  "conclusion": "",
  "commentsToAdd": {
    "body": "",
    "comments": []
  }
}
```

`displayMode` is `default` or `non-interactive`. `findings` keeps each `<SEVERITY>-<n>` id, subject, severity, claim, risk checked, evidence type, evidence boundary, and reviewer guidance. Store `evidence` as a list of citations, each with a source and what that source shows, so a finding reply prints one citation per line. `commentsToAdd.comments` keeps path, line, side, and body for each new finding.

## BLOCKED

```text
review-pr status: BLOCKED
missing: <repository | exact diff | scripted operation capability>
attempted: <checked-in script or read-only tool>
recovery: <the checked-in script or skill capability required>
```

Do not add findings, specialist results, or a review conclusion.

## Reports with an exact diff

Store the frozen target block from [providers.md](providers.md) as the first section. Then store these sections, in order:

1. **Target and frozen scope.** Repository, provider, base SHA, head SHA, working-tree inclusion, and `Source coverage: complete` or `Source coverage: DEGRADED`.
2. **Data availability and coverage.** One line per source: local diff, repository files, pull request title and body, linked issue context, checks, and existing review comments. Each line is `available`, `unavailable`, or `failed`, plus the command or tool that established it.
3. **TL;DR.** In two to four concise bullets, synthesize the available pull request description, frozen code changes, comments within changed code, existing review comments, and linked issue context. State the intended outcome, implementation approach, and reviewer-relevant constraints or dependencies. Use original agent wording from the reviewer-assistance perspective. Rephrase the source material and mark material source gaps as unread.
4. **Author evidence.** For each item below, use `provided`, `needs author evidence`, or `unread`, followed by the source:
   - manual testing;
   - screenshots or recordings;
   - changelog;
   - linked issue;
   - pull request template coverage;
   - check rollup;
   - repository readiness guidance.
   These are preparation and validation inputs. Keep them separate from peer-review findings and severity.
5. **Routing decisions.** Give each selected or considered skill its own block in this format:
   ```text
   skill: <installed skill name>
   class: preference | capability
   matching paths: <paths or none>
   semantic signal: <signal or none>
   required inputs: <inputs>
   result: applied | skipped — <reason>
   ```
   Use an independent block for every skipped skill so each class, path match, signal, input set, and reason remains attributable to one skill.
6. **Guided claim checks.** Start with the high-impact claims selected from [reasoning.md](reasoning.md). Use the finding record below for every new concern. Then list **Claims examined** with their evidence boundaries and **Open questions** whose evidence remains unread.
7. **Existing comments as references.** Cite comment ids or URLs, state whether each point remains present at the frozen head, and use it for deduplication. Existing comments stay outside the new-finding count and severity.
8. **Review coverage and conclusion.** Name the claims examined, important claims left open, and the completed checks. For `Source coverage: DEGRADED`, name the guidance affected by each unread source. Describe author preparation as: `Readiness evidence reviewed; open author evidence is listed above.` Reserve approval for the human reviewer.
9. **Comments to add.** Paste-ready GitHub comments for new findings plus an author-evidence follow-up when useful. A review started with `non-interactive`, and the **Output full review** reply, include this section with the other sections. The default display also includes it when the user asks for Suggested comments.

## Finding record

Give each new finding a stable `<SEVERITY>-<n>` id. `SEVERITY` is `HIGH`, `MEDIUM`, or `LOW`. `n` is the finding's order in one report-wide sequence starting at 1 across all severities. For example, a low-severity first finding followed by a high-severity second finding uses `LOW-1` and `HIGH-2`.

Print the record with a blank line between sections. Put each evidence citation on its own line.

```text
HIGH-1 — <short subject>

Severity
HIGH | MEDIUM | LOW

Claim
<behavior or safety claim, as its own paragraph>

Risk checked
<specific counterexample or failure condition, as its own paragraph>

Evidence
Type: diff | check-rollup | visual | runtime | unread
- <path:line or source> — <what that citation shows>
- <path:line or source> — <what that citation shows>

Evidence boundary
<what this establishes, as its own paragraph>

<what remains open, as its own paragraph>

Reviewer guidance
<request a change, ask a question, or inspect a named path, as its own paragraph>
```

Severity describes impact if the concern is confirmed:

| Severity | Conventional comment | Use for |
| --- | --- | --- |
| `HIGH` | `issue (blocking)` | A demonstrated defect with material impact that requires a change before merge |
| `MEDIUM` | `suggestion (non-blocking)` | A demonstrated concern with a concrete improvement |
| `LOW` | `nitpick (non-blocking)` | Wording, a comment, or a small consistency fix |

Template coverage and author-evidence gaps keep their preparation status instead of finding severity.

## Comments to add

One summary goes in the pull request review body:

```text
Review scope: <highest-impact claims and evidence examined>.
Author evidence: <provided items and requested follow-ups>.
New findings: <count by severity, with ids>.
Reviewer guidance: <highest-value next step and important open evidence>.
```

Then one inline comment per new finding:

- Finding: `<SEVERITY>-<n>`.
- Where: `<path>` line `<n>` on side `LEFT` or `RIGHT` of the frozen diff.
- Severity: `HIGH`, `MEDIUM`, or `LOW`.
- Paste this text on that line:

```text
<issue|suggestion|nitpick|question> (<blocking|non-blocking>): <subject>

<Why this matters, grounded in the cited evidence.>

<Exact requested change: what to add, remove, replace, or verify.>
```

When the fix is a short replacement, add a GitHub suggestion block with the replacement text. Link an existing comment when it already requests the same change.

Author-evidence follow-ups belong in the review body:

```text
Author evidence follow-up: <specific template, validation, screenshot, linked-issue, or check evidence requested>.
```

## Citations and unknown data

An unread check stays `unknown`. Tests are called successful only when the named check or command output supports that conclusion. Existing comments classified `available` are cited as references.

Do not add a numeric review score.

## Later outcome assessment

Use this section only when the user asks to assess a previous `review-pr` report. Freeze the prior report's repository, base SHA, and head SHA. Read later evidence such as an author reply, follow-up commit, resolved conversation, or later defect tied to that frozen diff.

Classify every finding:

| Outcome | Meaning |
| --- | --- |
| `confirmed` | Later evidence supports the concern |
| `rejected` | Later evidence shows the concern was unfounded |
| `unresolved` | Available later evidence has not settled it |
| `missed` | A later defect in the frozen diff was outside the report's findings |

Print one row per finding with its original `<SEVERITY>-<n>` id, outcome, and evidence. A `missed` count requires a defined later defect inventory supplied by an adjudicator, incident review, accepted follow-up fix, or equivalent evidence. When that inventory is unavailable, use `missed: unknown` and `recall: unknown`; never infer zero misses from the assessed findings.

Then print:

```text
confirmed: <count>
rejected: <count>
unresolved: <count>
missed: <count>
precision: confirmed / (confirmed + rejected)
recall: confirmed / (confirmed + missed)
```

Calculate precision when its denominator is greater than zero. Calculate recall when the missed-defect inventory is defined and its denominator is greater than zero. Exclude unresolved findings from both formulas. Return the assessment in the conversation. Persist a ledger row only after the user explicitly requests a destination outside the reviewed checkout.

## Pending GitHub review

The stored report remains the review record. For an existing GitHub pull request, inspect the review body and inline comments for sensitive chat context, then display the exact sanitized content and frozen placements. In the default mode, do that inside the Suggested comments slice and at the end of **Output full review**, and end that text with `Reply Create the pending review to create the pending line comments.` The question tool stays the four options in **Interactive questions**. In a review started with `non-interactive`, ask `Create these comments as a pending GitHub review?` in text at the end of the full report.

After explicit approval, write the approved review summary, frozen head SHA, and inline placements to the temporary manifest defined in [operations.md](operations.md). Run `create-pending-review.mjs`, which sends an empty `body` to GitHub, remove the temporary manifest, and return the pending review URL. A review with zero inline findings stays in the conversation and does not call the script. Then print:

```text
Paste into Leave a comment
<exact sanitized review summary>

Open Files changed, choose Comment, Approve, or Request changes, and press Submit review.
```

The pending review contains only the line comments. The reviewer submits it from GitHub's **Finish your review** control.

Self-reviews and other targets finish with the conversation report.
