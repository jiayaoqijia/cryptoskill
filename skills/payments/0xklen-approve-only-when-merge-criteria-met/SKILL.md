---
name: approve-only-when-merge-criteria-met
description: Use when tempted to approve a PR to unblock a teammate. Applies an explicit merge-criteria checklist and withholds approval if any item fails, regardless of pressure.
---

# Approve only when merge criteria are met

An approval is a claim you have verified the change. Approving to be helpful transfers your name onto code you did not check, and the incident lands on both of you.

## Procedure

1. Fix the criteria in writing, per repo, in `CONTRIBUTING.md` or the PR template. A workable default:
   - CI green on the exact head commit,
   - every `blocking:` thread resolved,
   - tests cover the changed lines,
   - no new high/critical dependency advisory,
   - the change matches its stated intent.
2. Verify CI ran on the head SHA, not a parent: `gh pr checks 482` and confirm the runs are for `git rev-parse HEAD`.
3. Confirm there are no unresolved threads: `gh api repos/:owner/:repo/pulls/482/comments --paginate` and check each thread's resolution state.
4. Reject the approval if the diff you are approving is not the diff you read — a new push after your review invalidates it unless it is a trivial rebase.
5. If you cannot verify an item, do not approve; comment `blocking:` with what is missing and move on.
6. When a teammate asks for a rubber stamp under deadline, offer the honest alternative: a scoped review of the risky paths, done now, rather than a blanket approval.
7. Record what you actually checked in the approval message, so the approval is auditable.

## Pitfalls

- Approving from the notification without opening the diff.
- Approving on a stale head after the author pushed a fix, so the last commit is unreviewed.
- Conditional approvals ("approve once tests pass") that nobody re-checks.
- Treating a maintainer's approval of a different PR as a reason the pattern here is fine.

## Verification

    gh pr view 482 --json headRefOid,reviewDecision,statusCheckRollup \
      | jq '{head: .headRefOid, decision: .reviewDecision,
             checks_ok: ([.statusCheckRollup[] | select(.conclusion=="SUCCESS")] | length)}'
    # Confirm the head OID matches the commit your review comments reference.

Report the five criteria and their pass/fail. An approval submitted with any criterion unverified is not an approval — it is a favour, and it should be withdrawn.
