---
name: separate-must-have-from-nice-to-have
description: Use when everything in a request is presented as critical. Split items into must/should/could so the deliverable can flex without renegotiating the whole thing.
---

# Separate must-have from nice-to-have

When everything is a must, nothing is negotiable and the only lever left is overtime. Sorting the list into must, should, and could creates the room to hit the date without breaking a promise.

## Procedure

1. Take the numbered deliverable list and label each item `must`, `should`, or `could`.

2. Test each `must` by removal: if the goal still holds without it, it is a `should`, not a must.

3. Sum the musts against the time box. If musts alone exceed the box, the date or the musts must change; there is no third option.

4. Keep `could` items visibly deferred, never deleted, so they can return later as a change order.

5. Publish the split to the requester: musts shipped, shoulds shipped if time allows, coulds deferred.

6. When time is lost, cut bottom-up. could first, then should, and never a must without re-agreement.

7. Re-rank when the goal changes; a `could` under one goal is a `must` under another.

## Pitfalls

- Accepting the requester's "must" as binding without testing it against the goal.

- An all-musts, no-shoulds split, which is the same as having no split at all.

- Cutting a must silently to hit a date, which is a broken promise dressed as delivery.

- Deleting coulds instead of deferring them, throwing away the negotiating room.

- Re-labelling at the end to match whatever got done.

## Verification

```
    awk '{print $1}' BACKLOG.md | sort | uniq -c   # counts of must/should/could
```

Report the must count against the time box; if the musts do not fit, say so before starting.
