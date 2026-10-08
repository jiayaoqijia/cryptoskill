---
name: close-the-loop-on-a-decision
description: Use when a decision was made in conversation or a ticket. Confirm it back in writing — what was decided, by whom, and what changes — so it can be acted on and audited.
---

# Close the loop on a decision

An unrecorded decision gets relitigated and misremembered. Write back what was chosen, who chose it, and what it changes, so the thread can go quiet.

## Procedure

1. Restate the decision in one line, using the decider's own terms.

2. Attribute it: who decided, in which message or meeting, and when.

3. List what changes as a result: files, owners, deadlines, and blocked work now unblocked.

4. List what was explicitly rejected, so it is not reopened next week.

5. Give the trigger that would reopen it: a metric crossing a line, a date, or a scope change.

6. Post it where the affected people will see it, and link it from the ticket as `DECISIONS.md#2026-10-08`.

7. Do not add conditions the decider never stated; that is a new decision, not a summary.

## Pitfalls

- "As discussed" without restating the decision leaves it ambiguous.
- Recording a decision that was never actually made creates false authority.
- Omitting the rejected options invites the same debate to restart.
- Failing to name the owner means nobody executes the decision.
- Slipping in an extra constraint while summarising quietly changes what was decided.

## Verification

    grep -nE "decided by|rejected|reopen" decision.md   # attribution, rejected options, trigger

Confirm the decision, its owner, its effects, and its reopen trigger in writing.
