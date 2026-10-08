---
name: set-a-change-order-threshold
description: Use when work is iterative and small additions keep arriving. Define the size at which a change stops being absorbed and needs re-agreement, so creep cannot hide.
---

# Set a change-order threshold

Without a tripwire, every change is a fresh judgment call and the loudest requester wins. A threshold turns the question from "is this big?" into "does this cross the line?", which is answerable.

## Procedure

1. At kickoff, agree a size on the frozen scope: any change over 4 hours, over 5% of budget, or touching a new subsystem.

2. Write it into `SCOPE.md` under a `Change control` heading, with the approver named.

3. Below the threshold: absorb, log to `CHANGES.md`, and mention it in the next report.

4. At or above: stop, write a change order (scope, cost, schedule impact, approver) and get approval before doing the work.

5. Sum the week's sub-threshold changes; three changes of 3 hours each is a 9-hour change that crossed the line unremarked.

6. Count crossings per iteration. More than two in a week means the original scope was wrong and needs re-baselining, not more policing.

7. The threshold is a tripwire, not a wall: it forces a conversation, it does not forbid the change.

## Pitfalls

- No threshold, so every change becomes a judgment call and precedent drifts.

- A threshold so low that every typo needs a change order, and the process collapses.

- Counting crossings but never re-baselining when the count stays high.

- Applying it to in-scope refinements that are part of an agreed definition of done.

- Hiding a crossing change by describing it as "part of the original work".

## Verification

```
    awk '/Change control/,0' SCOPE.md | head   # threshold defined with a size and approver
    grep -c '^CHANGE-ORDER' CHANGES.md          # each over-threshold change has an order
```

Report the threshold and every crossing this week; re-baseline if there are more than two.
