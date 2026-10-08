---
name: estimate-in-ranges-not-points
description: Use when asked how long a task will take or what it will cost. Returns an interval with a stated confidence instead of a single number a stakeholder will silently read as a commitment.
---

# Estimate in ranges, not points

A point estimate gets remembered as a promise; the caveat that came with it does not. Give an interval and name the confidence it carries, so the number is usable without being a lie.

## Procedure

1. Split the work into parts you can bound independently (`design`, `build`, `test`, `review`, `deploy`). Do not estimate the blob.
2. For each part write a low (roughly 10th percentile) and a high (90th percentile). The low is "if everything cooperates"; the high is "nothing catches fire."
3. Carry the extremes through, do not average first. Sum the lows for the optimistic bound, sum the highs for the pessimistic bound:

       python3 -c "low=[2,3,2,1,0.5]; high=[4,6,5,3,1]; print(sum(low), sum(high))"
       8.5 19.0

4. Check the spread. If high/low > 4, one part dominates and should be split. A 2x spread on a small task is normal; 10x means you do not understand the task yet.
5. Name the single biggest uncertainty out loud rather than hiding it inside the high number, e.g. "the sandbox account may trigger a security review, which alone could add two weeks."
6. State the range with its confidence: "5 to 12 working days, 80% confident." The confidence comes from how many comparable tasks you have actually seen, not from nerves.
7. If one date is demanded, give the median (50th percentile) and label it: "median 8 days — as likely to slip as to land." Never quietly hand over the low end.
8. Recompute the range each time a part finishes. A range is a living object, not a one-time answer.

## Pitfalls

- Quoting the optimistic bound because it is the number the stakeholder wants; the later slip is then read as personal failure.
- Averaging the parts and then adding a margin, which hides correlated risk — all parts tend to slip in the same bad week.
- A range so wide ("2 to 20 weeks") that it carries no information and gets ignored entirely.
- Treating the midpoint as the plan; the plan must survive the pessimistic bound or the scope has to change.
- Dropping the confidence label, so "5 to 12 days" reaches the budget holder as "5 days."

## Verification

    python3 -c "low=[2,3,2,1,0.5]; high=[4,6,5,3,1]; print('range',sum(low),'-',sum(high),'ratio',round(sum(high)/sum(low),1))"
    range 8.5 - 19.0 ratio 2.2

Report the interval, the confidence behind it, and the largest single source of uncertainty, with the two bounds you summed.
