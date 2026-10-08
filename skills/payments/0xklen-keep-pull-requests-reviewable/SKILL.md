---
name: keep-pull-requests-reviewable
description: Use when a PR has grown past a few hundred lines and review quality is collapsing. Splits the change into reviewable slices at natural seams and reports review latency per slice.
---

# Keep pull requests reviewable

Defect-detection rate falls off a cliff once a diff exceeds roughly 400 changed lines; reviewers skim and approve. The fix is not more diligence, it is a smaller diff.

## Procedure

1. Measure before splitting: `git diff --stat origin/main...HEAD | tail -1` prints total insertions and deletions. Treat 400 changed lines as the soft ceiling, 800 as blocking.
2. Split along seams that stand alone and can ship independently:
   - pure refactor (no behaviour change) first,
   - then the new behaviour,
   - then tests and docs that depend on both.
3. Build the slices with staged hunks: `git add -p` for chunk selection, or stage whole files with `git add -- path`. Commit the refactor separately so its diff is mechanical and skimmable.
4. If the work cannot ship in slices, use a stacked series: branch `feat/part-1`, then `feat/part-2` off it, and open PRs in order. Reviewers read top to bottom.
5. Keep generated files (lockfiles, snapshots, codegen) in their own commit so the hand-written delta is not buried: `git add package-lock.json && git commit -m 'chore: lockfile'`.
6. Track review latency as a signal, not a scold: `gh pr list --json number,additions,createdAt` and compare time-to-first-review against diff size. Large diffs sit longer.
7. When a slice still exceeds the ceiling, note the reason (a single atomic migration, a generated schema) rather than forcing an artificial split.

## Pitfalls

- Splitting so finely that each slice is not independently meaningful and the series needs six round-trips to test.
- A refactor slice that quietly changes behaviour, which defeats the whole point of separating it.
- Moving the tests into "part 2", so part 1 lands unverified.
- Forgetting to rebase later slices after part 1 merges, producing a wall of conflicts for the reviewer.

## Verification

    git diff --stat origin/main...HEAD | tail -1
    git log --oneline origin/main..HEAD   # one commit per slice, each self-describing

Report the total changed lines per slice and the target ceiling. A PR over 800 hand-written changed lines that cannot ship in pieces should be closed and re-opened as a stack.

## Worked example

A 1,400-line PR "add OAuth login" splits into: (1) `refactor: extract SessionStore`, no behaviour change; (2) `feat: google provider`, the provider plus its tests; (3) `docs: oauth setup`. Each part merges on its own; part 2 depends on part 1 only for the interface. Time-to-first-review drops from two days on the monolith to a few hours per slice.
