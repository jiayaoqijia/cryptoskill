---
name: decompose-trend-from-seasonality
description: Use when a metric moved and someone calls it a trend. Separates the underlying trend from weekly and yearly seasonality before interpreting the change.
---

# Decompose Trend from Seasonality

Most week-over-week "changes" are the calendar. Before attributing a move to a cause, strip the day-of-week and annual cycles and see what survives.

## Procedure

1. Plot the raw series at daily grain first; aggregation to weeks or months hides the cycle generating the move.
2. Compare against the same period last year (year over year) and the same weekday (week over week), not against the immediately preceding bucket.
3. Decompose with STL and inspect the three components:
   ```python
   from statsmodels.tsa.seasonal import STL
   import pandas as pd
   s = pd.read_csv('daily.csv', index_col='date', parse_dates=True)['value']
   r = STL(s, period=7, robust=True).fit()
   print(r.trend.tail(), r.seasonal.tail(), r.resid.abs().max())
   ```
4. Check the residual for a spike at the launch date; a spike is the effect, a smooth trend is not.
5. Fit a changepoint on the trend component (e.g. `ruptures` PELT) to date the shift rather than eyeballing it.
6. Use a 7-day or 28-day trailing window for noisy funnels, and state the window.
7. For a year-over-year claim, confirm the two periods have the same number of business days and no holiday shift.

## Pitfalls

- Monthly reporting can hide a strong weekly cycle; the same metric at daily grain swings plus or minus 15%.
- Calendar effects (Easter, Ramadan, Black Friday) move between months and fake a trend break.
- 4-4-5 retail calendars exist so October has the same selling days each year — check which calendar the source uses.
- Re-indexing a series to 100 at a chosen date makes an arbitrary baseline look like growth.
- A holiday week compared to a normal week can show a 30% "drop" that is entirely calendar.

## Verification

    python3 -c "import pandas as pd; d=pd.read_csv('daily.csv',parse_dates=['date']); print(d.groupby(d.date.dt.day_name())['value'].mean().round(1))"
    # weekday profile should explain the move before any causal claim

Report: "Week-over-week -8% is weekday mix — Saturday volume is 40% below weekday and this week had five full weekdays after the holiday shift. Trend component is flat (+0.2%)."
