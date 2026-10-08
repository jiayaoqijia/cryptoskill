---
name: build-cohort-retention-curves
description: Use when plotting or reading retention. Builds curves on complete cohorts only, with an explicit qualifying event and week-0 base.
---

# Build Cohort Retention Curves

Retention is only meaningful against a fixed cohort and a fixed qualifying event. A curve that mixes acquisition months, rebases week 0, or includes half-finished cohorts is decoration.

## Procedure

1. Define the qualifying event that starts the clock (first login, first purchase, first key action) and the return event (any session, or the same key action).
2. Assign each user to exactly one cohort: `date_trunc('week', first_event_at)` in the product's reporting timezone.
3. Index time as whole weeks between first event and activity, and count distinct users active at each index over the cohort base:
   ```sql
   SELECT cohort_week, weeks_since, count(DISTINCT user_id) AS active
   FROM activity a JOIN first_seen f USING (user_id)
   WHERE a.day >= f.first_day
   GROUP BY 1, 2;
   ```
4. Divide by the cohort's week-0 size, not by the previous week's active count — rolling and classic retention are different products; label which you use.
5. Drop or grey out incomplete cohorts: the newest has fewer observed weeks than the oldest, so its tail is censored and must not be compared.
6. Plot all cohorts with week number on x and cohort as the line colour; a flattening tail is the signal, not the height of week 1.
7. Compare cohorts at equal age (week 4 vs week 4), never a young cohort's week-1 against an old cohort's week-8.

## Pitfalls

- Rebased curves that renormalise each week hide absolute loss; week 0 must be the acquisition count.
- If the return event is weaker than the qualifying event, retention is understated and looks like churn.
- A cohort defined by first-event date shifts whenever historical data is backfilled.
- Weekly cohorts in a timezone without DST handling gain or lose an hour and a few boundary users each spring.
- New-product cohorts often dip before they rise; do not read the first three points as a trend.

## Verification

    # newest cohort must have fewer observed weeks; flag any complete-looking censored cohort
    python3 - <<'PY'
import pandas as pd
d = pd.read_csv('retention.csv')
mx = d.groupby('cohort')['weeks_since'].max()
assert mx.iloc[-1] < mx.iloc[0], "latest cohort is censored, do not compare tails"
print(mx.tail())
PY

Report: "Cohort curves on complete weeks only; 2026-09 cohort is censored at week 2 and excluded. Week-4 retention slid from 31% to 24% across the last four cohorts at equal age."
