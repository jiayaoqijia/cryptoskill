---
name: check-funnel-conversion-integrity
description: Use when building or reading a conversion funnel. Enforces monotonic step counts, time-ordered steps, and one attribution window before trusting the rates.
---

# Check Funnel Conversion Integrity

A funnel is a sequence in time, not a set of filtered counts. If step 3 is not a subset of step 2, or the steps are joined without order, the "conversion" measures your SQL rather than user behaviour.

## Procedure

1. Define each step as an event and require the steps to happen in order within a bounded window (commonly 1 or 7 days).
2. Compute with a window-function funnel so each step joins to the prior step's timestamp, not to a session id you assume is shared:
   ```sql
   WITH s AS (
     SELECT user_id, step, ts,
            row_number() OVER (PARTITION BY user_id, step ORDER BY ts) rn
     FROM events WHERE step IN ('view','add','checkout','purchase')
   )
   SELECT step, count(DISTINCT user_id) FROM (
     SELECT user_id, 'view' step, ts FROM s WHERE step='view' AND rn=1
     UNION ALL
     SELECT user_id, 'add', ts FROM s WHERE step='add'
   ) t GROUP BY step;
   ```
3. Assert monotonicity: each step's count must be at most the previous. A breach is a join or definition bug, not a funnel.
4. Apply one attribution window to every step and state it; widening the window lifts completion for all steps.
5. De-duplicate: a user who views ten products is one funnel entry, not ten.
6. Check device and session boundaries: a purchase on a phone after a cart built on web breaks a session-scoped join.
7. Report both step counts and step-to-step rates, plus the overall view-to-purchase rate.

## Pitfalls

- Counting events instead of users makes later steps look larger than earlier ones.
- A session-keyed funnel drops users who cross devices, usually on the highest-value path.
- "Complete a purchase" counted by order rows can exceed "start checkout" if orders come from another source.
- Different lookback windows per step quietly inflate the conversion rate.
- Bot and test-account traffic concentrates in early steps and deflates every downstream rate.

## Verification

    psql "$DSN" -c "WITH f AS (...) SELECT step, n, n <= lag(n) OVER (ORDER BY ord) AS monotonic FROM f;"
    # every row must show monotonic = true

Report: "Funnel view->add->checkout->purchase = 100,000 -> 22,400 -> 9,100 -> 3,050 (3.05%), monotonic, 7-day window, users de-duplicated."
