---
name: review-diff-against-stated-intent
description: Use when a PR's title and body may not describe what the code actually does. Reconstruct the stated intent, then check every changed file against it and flag scope drift before approving.
---

# Review the diff against its stated intent

Code that is correct but does not do what the PR claims is unreviewable: neither you nor the author knows which is the mistake. Pin the intent first, then diff against it.

## Procedure

1. Read the linked issue, PR title, and body. Write the intent as one sentence with a verb and a user-visible effect: "reject a login after 5 failed attempts within 15 minutes".
2. List what changed: `gh pr view 482 --json files -q '.files[].path'` or `git diff --name-status origin/main...HEAD`.
3. Classify each changed path as in-scope or out-of-scope for that sentence. Config, CI, dependency, and lockfile changes are the ones most likely to ride along unnoticed — inspect each.
4. For each file, ask whether the change is required by the intent. If not, it is scope creep; request it be split into its own PR.
5. Confirm the tests assert the intent, not an adjacent behaviour. A test named `test_login_attempts` that checks only the happy path does not cover the claim.
6. When intent and implementation disagree, one of them must change. Surface it explicitly; never silently accept the code and rewrite the intent later.
7. Verify no drive-by refactor hides inside the change: `git diff -w --stat` shows whitespace-only noise separately from real edits.

## Pitfalls

- The title says "fix typo" while 400 lines across nine files changed.
- A "bug fix" that also alters behaviour for existing callers of the same function.
- The PR body was written before the last three commits, so it describes an earlier design.
- Renaming a public export inside a bug-fix PR, which is a breaking change the changelog will miss.

## Verification

    gh pr view 482 --json title,body,files | jq -r '.title, (.files[].path)'
    git log origin/main..HEAD --oneline --no-merges

Report the one-sentence intent, the in-scope file count, and any file you could not tie back to the intent. Out-of-scope files that remain in the PR are a blocking finding.

## Worked example

PR titled "add rate limiting to /login". Changed files: `auth/limiter.go`, `auth/limiter_test.go`, and `Dockerfile`. The Dockerfile adds a Redis sidecar — in scope, the limiter needs a store, but note it in the body. Then `go.mod` bumps an unrelated logging library: out of scope, request it split. The tests assert five attempts then a lock, which matches the title.

If a changed file has no line you can tie to the intent, ask the author to justify it in the PR body or split it out before you approve.
