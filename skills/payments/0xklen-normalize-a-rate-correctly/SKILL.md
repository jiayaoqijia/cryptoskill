---
name: normalize-a-rate-correctly
description: Use when comparing counts across units of different size. Picks the right exposure denominator and checks that normalising has not created a fake ranking.
---

# Normalize a Rate Correctly

Raw counts reward size, so analysts normalise — but the wrong denominator produces a ranking that is an artefact of the divisor. Per-capita, per-user, and per-session answer different questions.

## Procedure

1. State the question: is the comparison about propensity per person, per opportunity, or per unit of exposure? The denominator follows.
2. Choose an exposure denominator that all units actually have: orders per session, revenue per active user, defects per 1,000 units shipped.
3. For geographic or population comparisons, use a standardised rate (age- or mix-adjusted) when the populations differ.
4. Beware small denominators: a city with 200 residents produces wild per-capita rates; require a minimum base and pool or suppress below it.
5. Check whether the normaliser is itself moved by what you are measuring — dividing revenue by a GMV the same change boosted creates a ratio that cancels the effect:
   ```python
   df['rpu'] = df['revenue'] / df['active_users']
   df['rps'] = df['revenue'] / df['sessions']   # choose the one matching the question
   print(df[['rpu','rps']].corr())
   ```
6. Never average per-unit rates to get a total — aggregate numerator and denominator, then divide.

## Pitfalls

- Per-capita rates on tiny populations top every leaderboard and mean nothing; base size matters.
- Normalising by a metric the intervention moves (the denominator is downstream) hides the effect.
- Rates are not additive: summing two regions' per-capita rates is meaningless.
- A rate whose denominator is "all users ever" is not over any real population.
- Changing the normaliser between periods makes a trend that is purely definitional.
- A ratio of two aggregates and the mean of the same ratio are different numbers; print both when they diverge.
- Guard the division: a rounded-to-zero denominator yields an infinity, so wrap it in `nullif(x, 0)`.

## Verification

    psql "$DSN" -c "SELECT region, revenue, active_users, round(revenue::numeric/active_users,2) rpu FROM marts.region_month ORDER BY rpu DESC;"
    # rows below the agreed base floor are suppressed, not ranked

Report: "Ranked by revenue per active user with a 1,000-user base floor; the two smallest markets dropped out and the top 3 by raw revenue re-order once normalised."
