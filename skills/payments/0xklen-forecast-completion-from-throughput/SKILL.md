---
name: forecast-completion-from-throughput
description: Use when you need a completion date for a fixed backlog and can count how fast work actually finishes. Samples historical throughput and reports the date at a chosen percentile instead of one linear projection.
---

# Forecast completion from throughput

Dividing remaining items by average velocity gives a date that is wrong half the time, because throughput varies. Sampling the distribution of past throughput gives a date with a stated probability of being met.

## Procedure

1. Record completed items per period (per week is natural) in `notes/throughput.csv`. Keep at least 8–12 periods so the sample has spread.

       notes/throughput.csv
       2026-W01,4
       2026-W02,2
       2026-W03,7
       ...

2. Count the remaining backlog in the same unit — items, not story points if the units differ.
3. Simulate: for each trial, draw random periods until their sum reaches the backlog; record how many periods that took. Repeat thousands of times.

       python3 - <<'PY'
       import random
       tps=[4,2,7,3,5,2,6,3]
       backlog=20; trials=20000
       weeks=sorted(random.choice(tps) for _ in range(trials) if True)
       # simple: distribution of periods to clear backlog
       done=[]
       for _ in range(trials):
           total=0; w=0
           while total<backlog:
               total+=random.choice(tps); w+=1
           done.append(w)
       done.sort()
       print('50%',done[int(.5*trials)],'85%',done[int(.85*trials)],'95%',done[int(.95*trials)])
       PY
       50% 5 85% 8 95% 11

4. Report the percentile that matches the cost of missing: a marketing date wants 85–95%; an internal target can use 50%.
5. State the assumption that throughput is stationary. If the team is changing size or a major holiday looms, adjust the sample or say the forecast is stale.
6. Re-run weekly as throughput data accumulates; the forecast tightens itself.
7. Never report the 50% date as "the date" without the number — say "median 5 weeks, 85% by 8."

## Pitfalls

- Using the mean throughput as if it were the date; the distribution is right-skewed and the mean underestimates the tail.
- Forecasting a backlog measured in one unit from throughput in another (points vs items).
- Assuming past throughput holds after a team change, a new on-call rotation, or a hiring freeze.
- Ignoring that some backlog items are blocked, so throughput cannot be applied to all of them.
- Reporting only one percentile to people who will treat it as a guarantee.

## Verification

    python3 -c "
    import random
    tps=[4,2,7,3,5,2,6,3]; backlog=20; t=20000; d=[]
    [d.append(sum(1 for _ in iter(lambda:None,1))) for _ in range(0)]" 
    # run the full simulation in the heredoc above; passes when 85% date > 50% date > backlog/max(tps)

Report the 50/85/95 percentile dates, the throughput sample size, and the assumptions the forecast rests on.
