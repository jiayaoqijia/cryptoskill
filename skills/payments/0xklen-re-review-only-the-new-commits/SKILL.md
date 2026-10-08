---
name: re-review-only-the-new-commits
description: Use when an author pushes changes after your review. Diffs the range since your last-reviewed commit instead of re-reading the whole PR, and confirms each of your findings was addressed.
---

# Re-review only the new commits

Re-reading an entire PR after every push wastes both reviewers and buries the actual change. Diff since your last review, then verify your open findings against the runtime diff.

## Procedure

1. Find the commit you last reviewed. Note it when you first review, or read it from your review's SHA: `gh api repos/:owner/:repo/pulls/482/reviews --jq '.[].commit_id'`.
2. Diff from that commit to the new head: `git diff <last_reviewed_sha>..HEAD` after `git fetch origin pull/482/head`.
3. Confirm the author addressed each prior finding by inspecting the intervening change, not the comment thread alone — a resolved thread may hide code that was reverted.
4. Watch for collateral edits: `git range-diff origin/main..<old_head> origin/main..HEAD` shows whether a force-push or rebase silently altered commits you already approved.
5. If history was rewritten, re-read the rewritten hunks — a rebase can drop or reorder a fix. Do not trust a clean thread state.
6. Re-approve only for the new range and note the new head SHA in your approval.
7. If the diff since your review exceeds the size at which you can still verify it, request a fresh split rather than skimming.

## Pitfalls

- Trusting the "resolved conversation" checkmark without looking at the code change that resolved it.
- A force-push that squashed the fix into an unrelated commit, so a line-by-line diff of the last commit misses it.
- Re-approving the whole PR while only the last commit was actually looked at.
- Reviewing a stale local branch because you did not fetch the updated pull ref.

## Verification

    git fetch origin pull/482/head:pr-482
    git range-diff origin/main..<last_reviewed_sha> origin/main..pr-482
    git diff --stat <last_reviewed_sha>..pr-482

Report the new head SHA, which earlier findings are confirmed fixed, and any hunk you had not seen. Approval covers only the range you diffed; state that range.

## Worked example

You reviewed `a1b2c3d` and left two `blocking:` items. The author force-pushes; `git range-diff origin/main..a1b2c3d origin/main..pr-482` shows the first fix wrapped into an unrelated commit and the second reverted during the rebase. Diffing `a1b2c3d..pr-482` reveals the second finding is unresolved despite its thread being marked resolved — re-request the change rather than re-approving.

A clean re-review reads the intervening diff in under a minute; if it takes longer, the PR has grown past a fix and needs a fresh split rather than another pass.
