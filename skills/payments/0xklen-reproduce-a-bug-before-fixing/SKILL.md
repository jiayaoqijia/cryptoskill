---
name: reproduce-a-bug-before-fixing
description: Use when a bug is reported or first observed. Builds a deterministic failing reproduction before any source is changed, so the eventual fix is provable.
---

# Reproduce a Bug Before Fixing

A fix you cannot reproduce is a guess. Turn the vague report into a command that fails on demand, every time, before you touch a line of source.

## Procedure

1. Copy the raw report verbatim: exact input, environment, software version, and the full error text. Do not paraphrase yet.
2. Pin the environment that produced it: `git rev-parse HEAD`, `python3 --version`, `uname -a`, and the data snapshot id.
3. Convert the reporter's prose steps into one runnable command. A script that exits non-zero when the bug is present beats a paragraph.
4. Run it at least three times. A repro that fails 1 in 3 is a flaky repro — capture the failing seed or fixture; do not proceed on hope.
5. Shrink the input to the smallest one that still fails (hand large inputs to `shrink-a-repro-by-delta-debugging`).
6. Freeze the repro: commit the fixture and the script under `repro/`, so it is byte-identical later.
7. Confirm it fails on the reported commit and passes on a commit you believe is good. If it fails on both, you have the wrong repro.
8. Only now read the code — with the failure in front of you, not in memory.
9. Capture the exact output as the before-fix baseline: `./repro/run.sh 2>&1 | tee repro/out.txt`.
10. If you genuinely cannot reproduce, say so and list what you ruled out; never guess at a fix.

## Pitfalls

- Fixing from the error message alone, then declaring victory when that message stops appearing.
- A repro that secretly depends on local state (`~/.cache`, an unset env var, a developer database) the report never mentioned.
- Chasing the reported symptom while the stack trace points somewhere else entirely.
- Treating "works on my machine" as proof the bug is gone, rather than proof the repro is too weak.
- Editing the repro until it passes, destroying the only artefact that distinguishes bug from no-bug.
- Marking the ticket fixed while the repro still exits non-zero for a reason you did not check.

## Verification

    for i in 1 2 3; do ./repro/run.sh >/dev/null 2>&1; echo "run $i exit=$?"; done
    # passes when all three runs exit non-zero the same way (the bug reproduces)

    git stash && ./repro/run.sh; echo "clean-tree exit=$?"; git stash pop
    # the clean tree should exit 0 once the fix lands; before it should match the bug

Report to the user: the exact command that reproduces the bug, its exit code, and the smallest input that triggers it.
