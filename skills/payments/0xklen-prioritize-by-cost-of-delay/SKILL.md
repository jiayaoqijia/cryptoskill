---
name: prioritize-by-cost-of-delay
description: Use when ranking a backlog by "impact" or "priority" labels that hide the real tradeoff. Ranks work by the cost of delaying it, backed by the value it unblocks and its expiry.
---

# Prioritize by cost of delay

Priority labels are opinions. Cost of delay is the value lost per week a thing waits, and it makes the ranking argue with numbers instead of volume.

## Procedure

1. For each candidate write two components in `cod.md`: the value delivered (revenue, cost saved, risk removed) and the time sensitivity (whether that value decays and how fast).
2. Classify time sensitivity: `expires on a date` (a contract, a competitor move), `decays` (a growing support load), or `flat` (a nice-to-have that waits).
3. Estimate value in a common unit — currency, hours saved per week, or ticket volume — so items can be compared without a scoring rubric.
4. Compute cost of delay roughly as value times decay rate; a $10k item expiring in two weeks outranks a $40k item with no deadline in most horizons.
5. Account for dependency order: an item that unblocks others carries their cost of delay as well.
6. Bound the estimates as ranges, not points, and note the assumption behind each.
7. Rank, then sanity-check two neighbours by swapping them; if the order does not change the expected outcome, the precision is noise.
8. Record the assumptions so the ranking can be revisited when a fact changes.
9. Re-baseline the value estimates against last quarter's actuals, so the numbers are calibrated rather than asserted.
10. Flag any candidate whose value is entirely speculative, and rank it below items with measured value.

11. Keep the previous ranking and diff it; a large unexplained jump means an input changed without notice.

## Pitfalls

- Using Fibonacci points as if they were value; story points size effort, not cost of delay.
- Ignoring time sensitivity, which treats a deadline-bound item as equal to a timeless one.
- Double-counting value that appears in several candidates under different names.
- Letting the loudest requester's item keep its value while others are discounted.
- Recomputing the ranking weekly with new guesses, which makes it unstable and ignored.
- Averaging away the one item that expires tomorrow by using a smooth score.
- Letting effort estimates leak into a value ranking; they measure different things.

- Ranking an item high because it is easy to do, which is an effort signal, not a delay cost.

## Verification

    grep -c 'value:\|decay:\|cod:' cod.md; grep -c 'range' cod.md

Report the top three by cost of delay with their assumptions and the one dependent item each unblocks.
