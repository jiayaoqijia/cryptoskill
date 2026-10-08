---
name: bound-an-open-ended-investigation
description: Use when a task is research-shaped, such as "look into" or "figure out why". Set a time box, an output, and a stop condition up front so investigation cannot absorb the deadline.
---

# Bound an open-ended investigation

"Look into it" has no natural end, so it expands to fill whatever time exists. A time box, a fixed output, and a stop condition give it a boundary that forces a decision.

## Procedure

1. Rewrite the ask as a question with a decision attached: "why is p99 slow" becomes "decide whether to rewrite the cache".

2. Set a time box before starting: 90 minutes, or 10% of the remaining budget.

3. Fix the output shape up front: a one-page finding, a recommendation, or a Go/No-Go. Not "more investigation".

4. Define the stop condition: the answer is found, the box expires, or two independent paths dead-end.

5. At the box's midpoint, check whether a decision is reachable; if not, narrow the question rather than widening the search.

6. When the box expires without an answer, report what was learned and recommend the next bounded step, never an unbounded continuation.

7. If the answer is "this needs to be built", stop: that is a new scoped deliverable, not more research.

## Pitfalls

- "Looking into" something until the deadline with nothing to show.

- A time box with no defined output, so stopping still produces nothing usable.

- Extending the box "just a bit more" because the answer feels close; that is the sunk-cost trap.

- Reporting a pile of observations with no recommendation or decision.

- Letting the investigation branch into three unrelated questions.

## Verification

```
    grep -nE 'stop condition|time box' spike.md   # box and stop condition set before start
```

Report the box, what the investigation found, and the single decision it enables.
