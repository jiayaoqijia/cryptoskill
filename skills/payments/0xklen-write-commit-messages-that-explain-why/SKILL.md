---
name: write-commit-messages-that-explain-why
description: Use when committing code and the history must be readable years later. Writes a summary line plus the motivation and the tradeoff, not a restatement of the diff.
---

# Write Commit Messages That Explain Why

The diff shows what changed; the message must say why, and why this way. A future `git log` reader has the code, not your memory.

## Procedure

1. Summary line in the imperative, under 50 characters: `fix: reject expired tokens at the edge`, not `fixed a bug`.
2. Blank line, then a body that explains the problem and the reasoning. The body answers why; the diff answers what.
3. Name the tradeoff you rejected: "Used a denylist here because the token list exceeds cache size; revisit at 1M entries."
4. Reference the issue so the context is one hop away: `Refs #1423`.
5. Keep one logical change per commit; a message forced to say "and also" means a commit to split.
6. For a revert, explain what broke: `Revert "add caching": cache invalidation race caused stale reads in prod`.
7. Mark a breaking change with `BREAKING CHANGE:` in the footer and a migration line, so tooling and humans both see it.
8. Do not narrate the mechanics (changing a variable name); narrate the intent.
9. Use a consistent prefix convention if the repo has one (`fix:`, `feat:`, `chore:`); match the repo, do not invent a third.
10. Mention the measured effect when you have it: "cuts p99 from 640ms to 210ms".
11. Write it with `git commit -F -` for multi-line messages so the formatting is deliberate.

## Pitfalls

- "fixed stuff" or "wip", which force archaeology through diffs to reconstruct intent.
- Restating the diff line by line, spending the message on what it already shows.
- Mixing a refactor and a behaviour change in one commit, so neither can be reverted cleanly.
- Past tense and vague voice ("updated", "improved") that hide the direction of the change.
- A breaking change with no `BREAKING CHANGE:` footer, so release tooling misses it.
- Referencing a ticket number that only resolves inside a private tracker no reader can open.
- A summary line over 72 characters that truncates in every git UI.

## Verification

    git log --format='%s' -1 | awk '{ if (length($0) > 50) print "TOO LONG"; else print "OK" }'
    git log --format='%s%n%b' -1

The summary line is within 50 characters and a body is present for non-trivial commits. Sample the last twenty commits and report how many would be actionable to a reader who lacks the original context.
