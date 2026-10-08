---
name: detect-spec-drift-against-the-build
description: Use when code and spec may have diverged mid-build, or before a release review. Diffs implemented behaviour against the frozen spec and logs each divergence with its owner.
---

# Detect spec drift against the build

Specs rot while code moves. This skill compares what the build does against the spec it was frozen from, so silent divergence is caught before users find it.

## Procedure

1. Pin the spec revision you are comparing against: `git log -1 --format=%H -- AC.md`, and record the hash in `drift.md`.
2. Walk each acceptance criterion in `AC.md` and mark it `met`, `diverged`, or `absent`, driven by running the criterion, not by reading the ticket.
3. For each `diverged` item, quote both sides under `spec:` and `build:` so the gap is legible without the original authors present.
4. Classify the cause: `spec changed and code did not`, `code changed and spec did not`, or `both changed differently`. These need different fixes.
5. Decide the resolution per row — update the spec, revert the code, or defer with a ticket — and never leave a divergence unflagged.
6. Get the decision recorded with a name and a date; an undocumented reconciliation becomes drift again by the next sprint.
7. Re-run the criterion after the fix and flip the row to `met` only then.
8. If the same class of divergence recurs, add a CI check (a contract test or a snapshot) so it is caught automatically next time.
9. Check the changelog and ticket comments for decisions made after the freeze; drift often starts as a spoken agreement.
10. Diff the API or UI surface, not just the criteria: renamed fields and moved buttons are drift too.

11. Ask each criterion's author whether it still holds; the person who wrote it often knows of a change nobody logged.

## Pitfalls

- Comparing the latest spec to the latest code after both moved, which hides which side drifted.
- Reading the code to decide a criterion is met instead of running the observable behaviour.
- Fixing the spec to match a bug; a divergence is not automatically a spec error.
- Marking an item `absent` when it is only untested; distinguish missing from unverified.
- Leaving drift in a doc nobody reads because it "doesn't block"; drift compounds into rework.
- Assuming drift is always the code's fault; the spec may have quietly lost a requirement.
- Only checking at release time, when drift has already compounded across several features.

- Trusting a passing test suite when the test was written to match the drifted behaviour.

## Verification

    grep -c 'diverged' drift.md; grep -cE '^spec:|^build:' drift.md

Report each diverged criterion, its cause class, and the named decision that resolved it.
