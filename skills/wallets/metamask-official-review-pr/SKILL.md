---
name: review-pr
description: >-
  Run an evidence-guided MetaMask pull request review or self-review in one
  static pass, with an optional approved pending GitHub review. Use when asked
  to review a PR, review my branch, assess review findings, or review a peer
  pull request URL or number. Separate author evidence from peer guidance,
  route installed specialist skills, and preserve the human review decision.
maturity: stable
base: true
---

# Review a pull request

One evidence-guided review of the current checkout or an existing pull request. Analysis stays read-only. After a peer GitHub review, the user may approve pending inline comments for inspection in GitHub. The reviewer pastes the summary into GitHub's **Finish your review** box and submits there. The human reviewer owns that decision.

This skill selects installed specialist skills and aggregates their results. Each specialist remains the source of truth for its rules.

## When to use

- Review the current branch or working tree before opening a pull request.
- Review a peer pull request by URL or number.
- Ask which checks ran, which were skipped, and which sources could not be read.
- Assess the later outcome of findings from an earlier `review-pr` report.
- Add `non-interactive` to the review request for the full report in one message. The default shows a completion card, then asks `What would you like to do next?` with `AskQuestion` in Cursor or `AskUserQuestion` in Claude.

## Workflow

1. **Resolve the target.** A pull request URL or number is a peer review. "This branch", "my changes", or no target is a self-review of the current checkout. Open every `references/*.md` link from the directory of this instruction file with the native file read tool, including [references/providers.md](references/providers.md) and [references/operations.md](references/operations.md). Those links enumerate the skill tree. Then run the matching checked-in preflight script.
2. **Freeze the target before reviewing.** Resolve the repository, provider, base SHA, head SHA, and working-tree inclusion. Store this frozen target as the report's first section, followed by every source as `available`, `unavailable`, or `failed`.
3. **Stop when the target is blocked.** A missing repository identity or an empty diff returns the `BLOCKED` report from [references/report.md](references/report.md). Do not open specialist skills and do not write findings.
4. **Separate author evidence.** Report pull request template coverage, manual testing, screenshots, linked issue, changelog, checks, and repository readiness guidance under **Author evidence**. These inputs describe preparation and validation; they do not become code findings or an approval.
5. **Map and rank claims.** Open [references/reasoning.md](references/reasoning.md). Extract explicit and implicit claims, rank them, and choose concrete risks or counterexamples to examine.
6. **Route the diff.** Open [references/routing.md](references/routing.md) and the repository overlay. Classify each selected skill as a repository `preference` or domain `capability`. Invoke it only when installed and its required inputs are `available`. Record paths, semantic signal, inputs, and the skip or apply result.
7. **Run one guided static pass.** Read the frozen diff and cited files. For each substantive observation, record the claim, risk checked, evidence, evidence boundary, severity, and reviewer guidance. Keep existing comments as references.
8. **Aggregate and store.** Copy specialist results with their source into the stable sections in [references/report.md](references/report.md). Include GitHub-ready comments with exact requested changes. Store the finished report with `write-temp-json.mjs` from [references/operations.md](references/operations.md), then read and overwrite that file.
9. **Display the stored report.** Follow **Presentation** in [references/report.md](references/report.md). The default prints the completion card, then asks `What would you like to do next?` with `AskQuestion` in Cursor or `AskUserQuestion` in Claude. The options are Review findings, Review evidence, Suggested comments, and Output full review, in that order. Every later interactive reply prints one requested slice and asks again with that same question and those same four options. A free-text finding id prints that finding. A free-text `Frozen state` prints the frozen target. A free-text `Create the pending review`, after Suggested comments or Output full review for an existing GitHub pull request, is the approval. A review started with `non-interactive` prints every section in order and asks `Create these comments as a pending GitHub review?` in text at the end. After explicit approval, write the approved manifest to `temp/review-pr-pending-<head-sha>.json`, including the review summary in `body`. Run `create-pending-review.mjs`, which sends an empty `body` to GitHub, remove the manifest, and return the pending review URL. Then print the summary under **Paste into Leave a comment** and tell the reviewer to submit from GitHub's **Finish your review** control. Self-reviews and other targets finish in the conversation.

When the user asks to assess an earlier report, follow **Later outcome assessment** in [references/report.md](references/report.md). Use later evidence to classify findings and calculate correctness metrics.

## Require

- Capture the frozen target before the first specialist skill or finding, and store it as the report's first section.
- Run every terminal operation as one invocation of a documented script under this skill's `scripts/` directory. Native file reads, native searches, and read-only MCP tools remain available. Create the stored report and the approved review manifest with `write-temp-json.mjs`, then read and overwrite that file with the native file tool.
- Store the finished report before the first user-visible review message. The default first message is the completion card in [references/report.md](references/report.md), followed by one question, `What would you like to do next?`, through `AskQuestion` in Cursor or `AskUserQuestion` in Claude. The options are Review findings, Review evidence, Suggested comments, and Output full review. Each later interactive reply prints one requested slice and asks again with that same question and those same options.
- When the message that starts the review contains `non-interactive` as its own word, ignoring case, print the nine report sections in order in that first message. The **Output full review** reply prints those same nine sections from the stored report.
- Use `check-worktree.mjs` for checkout status. When terminal invocations are reported, every ledger entry names a checked-in script.
- Return `BLOCKED` with the missing scripted capability when the operation registry does not cover required terminal evidence.
- Classify the local diff, repository files, pull request title and body, linked issue context, checks, and existing review comments.
- Treat linked issue context as available when a GitHub issue or a Jira issue was read. Either one is enough.
- For a peer review, review the exact `gh pr diff` between the frozen pull request base and head. Read cited files at that head SHA through `read-frozen-file.mjs`, `read-frozen-json.mjs`, or `search-frozen-tree.mjs`.
- For a peer review through `gh`, run the checked-in `scripts/collect-pr-context.mjs` collector so data collection and parsing use one reviewed command.
- Include a two-to-four-bullet TL;DR in original agent wording, synthesized from the available pull request description, frozen diff, comments within changed code, existing review comments, and linked issue context.
- Keep author evidence separate from peer-review findings and severity.
- Follow the fixed reasoning flow before routing specialist skills.
- Record every routing decision in a separate per-skill block with skill class, paths, semantic signal, required inputs, and result.
- Cite a diff hunk, file and line, repository rule, specialist result, or command output for every finding.
- Cite existing review comments as references. Do not report those comments as blockers.
- When the diff is tooling, CI, build, or documentation and not application code, apply matching repository preferences and domain capabilities, and review the tests for that tooling.
- Keep an unread source unknown. Say that the source was unavailable or failed.
- State what the evidence establishes and what remains open.
- Limit the conclusion to the claims and checks examined.
- In an outcome assessment, report zero misses and recall only when later evidence defines the defect inventory.
- Ask before posting a GitHub review comment.
- Include paste-ready comments: one review summary and one inline comment per new finding. Each comment states the severity, rationale, and exact requested change.
- Before the pending-review prompt, show the exact sanitized summary and every path, line, side, and comment body.
- Create GitHub inline comments only through `create-pending-review.mjs`, with the frozen head SHA and an approved manifest at `temp/review-pr-pending-<head-sha>.json`. The manifest `body` is the review summary. The GitHub request sends an empty `body`.
- After the pending review is created, print the summary for the reviewer to paste into **Leave a comment**. The reviewer submits from GitHub.

## Reject

- Editing, committing, pushing, or otherwise changing the reviewed checkout.
- A terminal command that is not `node <skill-root>/scripts/<name>.mjs`, including `ls`, `find`, `cat`, `git`, `gh`, and pipelines used to discover or read this skill's files. Checked-in scripts call `git` and `gh` themselves.
- Fetching a `github.com` or `raw.githubusercontent.com` page, including blob, pull, commit, and files views, to read a file, diff, check, or review comment. Peer data comes from `collect-pr-context.mjs`, or from one GitHub MCP tool when `gh` cannot authenticate and that tool returns every required peer field. Frozen file contents come from `read-frozen-file.mjs`, `read-frozen-json.mjs`, or `search-frozen-tree.mjs`. A failed read stays `failed` or `BLOCKED`.
- In the default display, printing the full report in the first message.
- In the default display, printing a numbered reply menu, a second question in the tool call, or any option other than Review findings, Review evidence, Suggested comments, and Output full review. Finding ids, `Frozen state`, and `Create the pending review` stay free text on that question.
- Creating the stored report or the pending-review manifest with shell redirection, a heredoc, or a file write to a path the script has not created.
- Re-running collection scripts or specialist skills to answer a menu choice or to switch display mode.
- A global review score.
- A finding with no citation.
- Treating an unread check, test, comment, or pull request body as passed, unique, or ready.
- Treating author validation evidence or green checks as a peer-review approval.
- Treating a quiet review as evidence that the pull request is correct.
- Inferring zero missed defects from the findings that were assessed.
- Publishing to GitHub before explicit approval.
- Sending the review summary as the pending review `body`. GitHub's **Finish your review** box does not load that field, and submitting the box replaces it.
- Running `submit-pending-review.mjs`. The reviewer pastes the summary and submits in GitHub.
- Replacing a specialist skill's rule with a summary written from memory.
- Reviewing the local checkout diff in place of the pull request branch diff.
- Applying app test-layer, screen, or component skills to a script-only diff.
- A paste-ready comment that does not state the change to make.
