---
name: clarify-who-owns-a-decision
description: Use when a choice is needed and it is unclear who can make it. Name the single decider before work proceeds, so approval does not arrive after the fact from someone new.
---

# Clarify who owns a decision

A decision with no named owner cannot be closed; it can only be reversed. Naming the decider before building turns a future veto into an earlier approval.

## Procedure

1. Name the decision in one line: what must be chosen, and by when.

2. Sort the people involved into three roles: Decider (exactly one name), Consulted (input needed), Informed (told after).

3. If there is no single decider, that is the problem; resolve it upward before building. Two owners means none.

4. Confirm with the decider directly, not through a chain: "you own the call on the schema, is that right?"

5. Get consent decisions before irreversible steps, not after; a review that can only rubber-stamp is not a decision.

6. Record the decider's name and the date beside the decision, so a later reversal points to a named moment.

7. When the decider is unreachable past the deadline, fall back to the stated default from the ask, in writing.

## Pitfalls

- Building the whole feature, then discovering the architecture owner disagrees.

- "The team decided" with nobody accountable, so nobody can be wrong and nobody can be right.

- Consulting everyone and calling the consensus the decision; consultation is not decision rights.

- Confusing the requester with the decider; the asker may only be the messenger.

- Deciding silently to avoid a meeting, then defending it as a fait accompli.

## Verification

```
    grep -nE '^Decider:' decisions.md   # one named decider per decision, with a date
```

Report the decision, the named decider, and the deadline they must decide by.
