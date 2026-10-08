---
name: decline-work-outside-your-mandate
description: Use when a request exceeds the permissions or role you were given, such as another team's system or another user's data. Decline the overstep and route it to the rightful owner.
---

# Decline work outside your mandate

A mandate is the set of systems, accounts, and data you were authorised to touch. Acting past it on a colleague's casual "sure, it's fine" converts their opinion into an incident with your name on it.

## Procedure

1. Check the mandate: which repo, account, environment, and data were you authorised to touch?

2. Identify the specific overstep: a system you do not own, another user's data, or an action reserved for a role.

3. Decline the overstep while doing the part that is in mandate: "I can update our service; the shared gateway is owned by platform."

4. Route to the owner by name and hand over the context needed to act, not just a pointer to the ticket.

5. Do not accept a verbal grant when the permission lives in a system of record; get it recorded where it counts.

6. If the mandate is genuinely ambiguous, ask the grantor to widen it in writing rather than inferring.

7. Log where the boundary sits, so the next similar ask is answered from a record, not a fresh argument.

## Pitfalls

- Acting on borrowed authority because a colleague said it was fine.

- Declining the whole request when part of it is legitimately yours to do.

- Routing with no context, which just relocates the delay downstream.

- Treating a mandate as permanent; it expires with the engagement or the role.

- Widening your own access because it would make the work easier.

## Verification

```
    grep -nE 'in-mandate|owner:' handoff.md   # the split and the named owner are recorded
```

Report the part you can do, the part you declined, and the owner it was routed to.
