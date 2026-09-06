---
name: address-code-review-comments
description: Enter the worktree of a GitHub PR, validate the code-review comments raised on it against what the code actually does and the repo rules, fix the valid ones directly in the PR's source/tests, and report in chat — a brief note per closed comment and a detailed plain-language explanation of every comment left unclosed and why. For code-review comments on a PR. Invoke manually.
argument-hint: "<PR number or URL>  (then paste the review comments — plain text and/or #discussion_r… links)"
disable-model-invocation: true
---

# Address Code Review Comments

A reviewer (a human, or a tool like CodeRabbit) left a set of **comments** on a pull request — each a claimed bug, omission, style violation, or risk in the diff. Your job is to **judge each comment on its merits** against the actual code in the PR, **fix the ones that are genuinely valid** by editing the PR's own source and tests, and then **report your decisions in chat**.

Two things make this skill what it is, and you must hold both:

- **You edit the *code*, in the PR's worktree.** These comments are about a code diff on a branch, so "fixing" one means changing the application code, tests, or docs on that branch.
- **A comment is a hypothesis, not a fact.** Reviewers — human or bot — are often wrong: they misread the code, misremember a convention, or flag something the diff already handles correctly. Verify every claim against ground truth before acting. Rubber-stamping a wrong comment damages the code just as much as ignoring a right one; a confident or automated comment is not automatically correct.

## Inputs

- **PR**: a number (resolved against the current repo) or a full URL.
- **Comments**: the review comments, supplied in the invocation as plain text and/or as links to specific review comments.

If the PR or the comments are missing, ask — do not invent comments or guess the PR.

## Workflow

### 0. Enter the PR's worktree (do this first)

The whole point of this step is to get onto the exact code the reviewer saw, locally, so the rest of the work reads files straight from disk instead of round-tripping through the GitHub API.

1. **Read the PR's branch, head, and closing issue** (`<pr>` is the number or URL from the invocation — with a bare number, run this from inside the target repo so `gh` resolves it):

   ```bash
   gh pr view <pr> --json number,title,headRefName,headRefOid,url,closingIssuesReferences
   ```

   Note the `closingIssuesReferences` — the issue this PR is meant to close. It carries the real intent and acceptance criteria, which is often what decides whether a comment is valid (a "fix" that fights the issue's goal is not a fix). Read that issue when a comment's validity turns on original intent; don't read it just to read it.

2. **Find the local worktree for `headRefName`:**

   ```bash
   git worktree list
   ```

   Pick the worktree whose checked-out branch equals the PR's `headRefName`.

3. **Switch into it** with the `EnterWorktree` tool, passing that worktree's path (`path: <worktree dir>`).

4. **Double-check you are on the PR's head.** Compare the worktree's HEAD to the PR's `headRefOid`:

   ```bash
   git rev-parse HEAD
   ```

   It must equal `headRefOid` from step 1. **Once it matches, trust the working tree:** every file the PR changed is present locally, so read and edit it directly with `Read`/`Edit` — do **not** pull diffs or file contents through `gh`/the git API. That round-tripping is the waste this step exists to avoid.

**If something doesn't line up, stop and ask instead of guessing:**
- No worktree exists for the branch → say so; the skill needs the prepared worktree (don't silently create or check one out).
- HEAD ≠ `headRefOid` (worktree is behind/ahead of the PR) → report the mismatch and ask how to proceed (e.g. pull). Working on stale code would invalidate every judgment below.

### 1. Resolve the comments into concrete claims

For comments pasted as text, take them as-is. For **links** to specific review comments, fetch the body via the GitHub API so you act on the reviewer's actual words rather than the URL — the numeric id in a comment link's anchor is the comment id. For an inline review comment:

  ```bash
  gh api repos/{owner}/{repo}/pulls/comments/<ID> --jq '{path, line, body}'
  ```

`gh` fills `{owner}`/`{repo}` from the repo you're in (the PR's worktree, after step 0). Other link kinds resolve through their matching endpoint; if a link won't resolve, ask rather than guess what it said.

Extract the concrete claim from each: the file/symbol/line it names, what it asserts is wrong, and the change it recommends. Treat each as a hypothesis to confirm.

### 2. Validate each comment independently

Confirm or refute each comment against the real code and the repo's own conventions:

- Open the **actual** files, symbols, and tests the comment names, plus the obvious neighbors (the test module, the place a convention is defined or documented). Reason from what the code and rules say *today*, not from the comment's paraphrase.
- When a claim is checkable, **check it empirically** rather than by eye — run the snippet, the failing test, the `rg` search. A 30-second experiment beats a confident guess (e.g. proving two fixtures are not interchangeable by actually constructing both).
- Decide: **valid** (a real problem worth fixing), **invalid** (the claim doesn't hold, or the diff already handles it), or **partially valid** (part warrants a change, part doesn't).
- Be skeptical in both directions and stay proportional. A bot's or a senior's comment can still be wrong; a nit can still be right. The reviewer's severity/tone is an opinion, not a verdict.

### 3. Fix the valid comments

Edit the code on the PR's branch to close every valid (or partially-valid) comment:

- Make the **smallest change that genuinely closes the comment**, written to read like the surrounding code — match its naming, imports, structure, and the repo's documented conventions. You're adding to someone's PR; the edit should be indistinguishable from the original author's hand.
- For a partially-valid comment, apply the warranted part and explain the rejected part in the report.
- Leave invalid comments unchanged — their justification lives in the report, not in an edit.
- **Don't bump the version** (or make other unrelated changes) for review-comment fixes — they're follow-up edits within a PR that's already been opened and versioned.

### 4. Verify your changes

Don't hand back edits you haven't checked. For the files you touched, run the project's own lint/format and the relevant tests, using its standard tooling and environment (its virtualenv, task runner, or scripts) rather than global interpreters. If a fix breaks something, fix it or reconsider whether the comment was really valid. Report honestly if something still fails.

### 5. Report in chat

Reply in the chat (no file is written). Keep the two halves deliberately asymmetric — the diff already shows *what* you changed, but a rejection leaves no trace, so it needs your full reasoning:

- **Closed** — one *brief* bullet per comment you fixed: the comment, and one line on the edit that closed it. The code change speaks for itself; don't narrate it at length.
- **Not closed** — one *detailed, plain-language* bullet per comment you did **not** action (invalid, or the rejected part of a partial), explaining **why** in terms someone who never saw your tool calls can follow: what you checked, what it actually showed, and why no change was warranted. This is the part the reviewer needs in order to accept your rejection or push back, so make it stand on its own and ground it in what the code/rule/issue really says.

Key each bullet to the comment (its file:line or a short quote) so the mapping is unambiguous. If every comment was valid, say so under **Not closed** (`- None — every comment was valid and addressed.`); if none were, say so under **Closed**.

End by stating that you have **not committed or pushed** — the edits sit in the worktree for the user to review — unless they explicitly ask you to commit.

## Notes

- **Read from the verified worktree, not the API.** After step 0's head check, the changed files are on disk; reading them through `gh`/git is wasted effort.
- **Don't pad the verdict.** Closing zero comments (all invalid) or all of them is a perfectly valid outcome — report it honestly. Validity is decided by the code, the rules, and the issue, not by how many comments "should" be real.
- **Stay in scope.** Fix the comments raised; don't opportunistically refactor untouched code. If you spot a real, unrelated problem, mention it in the report rather than folding it into the diff.
