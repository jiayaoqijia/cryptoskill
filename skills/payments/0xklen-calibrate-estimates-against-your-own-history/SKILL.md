---
name: calibrate-estimates-against-your-own-history
description: Use when your estimates keep missing low and you suspect a personal bias. Measures the ratio of actual to estimated across your own finished tasks and applies that factor to new estimates.
---

# Calibrate estimates against your own history

Everybody has a personal multiplier — the amount their estimates run low by. Measuring yours turns "I always underestimate" into a number you can apply in advance, so long as you keep the log honest by including the misses.

## Procedure

1. Keep a log of every estimate you make, its estimate, and its actual. One line each in `notes/estimates.csv`, from now on and backfilled if you have data:

       notes/estimates.csv
       date,task,est_days,act_days
       2026-01-05,endpoint-a,3,5
       2026-01-12,endpoint-b,2,2
       2026-01-20,migration-c,4,11
       2026-01-28,bugfix-d,1,1

2. Compute the ratio actual/estimate for each row and take the median. Median, not mean — one overrun would otherwise dictate the factor.

       python3 -c "
       import statistics as s
       rows=[(3,5),(2,2),(4,11),(1,1)]
       r=[a/e for e,a in rows]; print('median ratio', round(s.median(r),2))"
       median ratio 1.5

3. Apply the factor to new estimates only when you have at least ~10 samples; below that, widen the range instead of trusting a factor.
4. Do not adjust for tasks you believe are different until you have data; the whole point is that the bias is invisible from inside.
5. Recompute the factor quarterly. It shrinks as you learn and can drift back up under new kinds of work.
6. Log tasks that came in *under* estimate too — a log that only records overruns is a gripe list, not a calibration.

## Pitfalls

- Excluding the tasks that blew up "because they were unusual" — those are exactly the data.
- Using the mean, which one 3x task dominates.
- Applying a factor from noisy work to a genuinely different task shape without checking the class.
- Trusting a factor built on five samples.
- Recording only the estimate, never the actual, so the log can never be calibrated.

## Verification

    python3 -c "
    import csv,statistics as s
    r=[float(a)/float(e) for e,a in csv.reader(open('notes/estimates.csv'))][0:]"
    # passes when the median actual/estimate ratio is computed over >= 10 logged rows

Report your median overrun factor, the sample size behind it, and the adjusted estimate for the current task.
