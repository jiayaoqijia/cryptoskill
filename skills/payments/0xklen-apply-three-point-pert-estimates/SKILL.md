---
name: apply-three-point-pert-estimates
description: Use when you have optimistic, most-likely and pessimistic values for a task and need a defensible single number plus a variance. Uses the PERT weighted average and combines variances across a chain.
---

# Apply three-point PERT estimates

Three numbers per task beat one, because they carry the shape of the risk. PERT weights the most likely value four times and folds the spread into a standard deviation you can sum across a chain.

## Procedure

1. For each task collect: optimistic `o` (everything goes well), most likely `m`, pessimistic `p` (realistic worst case, not catastrophe).
2. Weighted mean: `te = (o + 4m + p) / 6`.

       python3 -c "o,m,p=3,6,15; print('te', round((o+4*m+p)/6,2))"
       te 7.0

3. Standard deviation for a task: `sd = (p - o) / 6`, and variance is `sd**2`.
4. For a chain, sum the expected times and sum the *variances* (not the standard deviations), then take the square root:

       python3 -c "
       t=[(3,6,15),(2,3,8),(1,2,4)]
       te=[(o+4*m+p)/6 for o,m,p in t]
       var=[((p-o)/6)**2 for o,m,p in t]
       import math; print('total', round(sum(te),2), 'sigma', round(math.sqrt(sum(var)),2))"
       total 11.17 sigma 2.54

5. A one-sigma band covers ~68%; for an 80% commitment use roughly `total + 0.84*sigma`.
6. Do not sum standard deviations — adding the sigmas directly assumes perfect correlation and badly overstates the chain's spread.
7. Round `te` to the unit you can defend; do not report 7.03 days.

## Pitfalls

- Letting `p` become an unbounded catastrophe so `sigma` explodes and every range is useless.
- Adding standard deviations across a chain instead of adding variances first.
- Using `m` alone (the "most likely") as the commitment, which ignores that the pessimistic tail is where deadlines break.
- Forcing a symmetric range when the task is clearly skewed; PERT assumes a shape that may not hold.
- Reusing one task's three points for another in the same chain, which hides that the chain's risk is concentrated.

## Verification

    python3 -c "
    o,m,p=3,6,15; print((o+4*m+p)/6, (p-o)/6)"
    # 7.0 2.0  — the weighted mean and per-task sigma; combined sigma uses summed variances

Report each task's o/m/p, the weighted mean, and the chain total with its combined sigma and the confidence band.
