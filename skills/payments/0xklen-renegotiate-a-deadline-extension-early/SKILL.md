---
name: renegotiate-a-deadline-extension-early
description: Use when progress shows the date will slip. Raise it the moment the trend is visible, with the cause, a new date range, and what the extra time buys, not on the day it is missed.
---

# Renegotiate a deadline extension early

A slip announced early is a re-plan; a slip announced on the due date is a failure. The information is available at the midpoint of the time box, and that is when it must be raised.

## Procedure

1. Track burn against the date: at 50% of the time box, a must that has not started is a slip signal.

2. Raise it at the first credible signal, not at 90% when there is no room left to replan.

3. State three things: the cause in one line, the new realistic date as a range, and what the extra time delivers.

4. Never ask for "more time" bare; ask for a specific extension in exchange for a specific outcome.

5. Offer the alternative: what you can ship by the original date if scope flexes instead (see `trade-scope-quality-time`).

6. Get the decision recorded; a slip agreed verbally is remembered later as a failure to deliver.

7. Do not ask for a second extension for the same cause; the second time the plan was wrong, not the estimate.

## Pitfalls

- Delaying the bad news to look competent, which destroys trust when the date passes anyway.

- Asking for an open-ended extension instead of a number with a range.

- Raising the slip with no cause, so it reads as poor work rather than a changed fact.

- Slipping quietly and letting the deadline fail without a word.

- Requesting a second extension on the same task, signalling the first plan was never real.

## Verification

```
    grep -nE 'cause:|new date' slip.md   # a dated cause and a new date range are stated
```

Report the slip signal, the cause, the new date range, and what the extra time buys.
