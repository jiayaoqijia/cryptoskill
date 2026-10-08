---
name: get-a-blocker-unblocked
description: Use when progress is stopped by a dependency you do not own, such as access, a review, or an upstream fix. Drive it to resolution with a named owner, an ask, and a follow-up cadence.
---

# Get a blocker unblocked

A blocker left as a status update never clears; it waits behind louder work. Driving it means asking for the specific action, with a deadline, and working around it meanwhile.

## Procedure

1. State the blocker as a dependency: what you need, from whom, and by when.

2. Confirm you have done your part and that the blocker is genuinely the gate, not a convenient excuse.

3. Ask the owner for the specific unblock (grant access, approve the PR, ship the fix), not for a status update.

4. Give the deadline it must beat and name what slips if it does not.

5. Reduce their cost: a minimal PR to review, a script that does the work, or a narrower request.

6. Set a check-in. If there is no answer by time T, escalate one level (see `pick-the-right-escalation-path`).

7. Work the unblocked parts meanwhile; one dependency need not stop all progress.

8. When it clears, close the loop and record what unblocked it, so the same wall is bypassed next time.

## Pitfalls

- Waiting on a request with no deadline, so it sits forever behind louder work.

- Asking for a status update when you need an action.

- Blocking every task on one dependency instead of sequencing around it.

- Escalating without first asking the owner directly.

- Re-asking the same way that already failed instead of shrinking the ask.

## Verification

```
    grep -nE 'owner:|by [0-9]{2}:' blockers.md   # each blocker has a named owner and a deadline
```

Report the blocker, the owner asked, the deadline set, and what you are doing around it.
