---
name: bisect-a-regression-with-git-bisect
description: Use when something worked at an earlier commit or release and is broken now. Uses git bisect to name the exact commit that introduced the regression.
---

# Bisect a Regression with git bisect

Between "it used to work" and "it is broken now" sits one commit. `git bisect` finds it in log2(N) tests instead of reading every diff.

## Procedure

1. Establish a hard test. It must be non-interactive and return the same verdict every run — `./repro/run.sh` or a single test file, not "click around".
2. Verify the endpoints by hand: the known-good ref must pass the test, the known-bad ref must fail it. A wrong endpoint poisons the whole search.
3. Start: `git bisect start`, then `git bisect bad <known-bad>` and `git bisect good <known-good>`.
4. Automate with `git bisect run ./repro/run.sh`. Exit 0 means good, any other non-zero means bad; exit 125 tells bisect "cannot test, skip this commit".
5. After bisect prints the first bad commit, `git bisect log` and copy the log into the bug note.
6. Reset with `git bisect reset` — this returns you to where you started; confirm with `git status`.
7. Read the suspect commit's diff with the failure in hand: `git show <sha>`.
8. If that commit only *exposed* a bug from an earlier, untested change, bisect again with the earlier endpoint or add a `125` skip rule.

## Pitfalls

- A test that is flaky, so bisect lands on an unrelated commit and wastes an hour.
- Forgetting to mark merges or untestable commits as 125, so the run aborts with an error and you blame the tool.
- Commits that do not build: guard `git bisect run` with a script that returns 125 on a build failure rather than 1.
- Assuming the first bad commit is the root cause — it is often where a latent bug became observable.
- Leaving the repo in bisect state and then editing files, so the reset throws away work.
- Bisecting across a dependency upgrade that cannot build, without stubbing the missing piece.

## Verification

    git bisect start && git bisect bad HEAD~50 && git bisect good HEAD~120
    git bisect run ./repro/run.sh
    # prints "<sha> is the first bad commit" then: git bisect reset

    git bisect log | tail -5
    # the last test line names the committing sha; git show that sha

Report to the user: the first-bad sha, its subject line, and whether it introduced the bug or merely exposed it.
