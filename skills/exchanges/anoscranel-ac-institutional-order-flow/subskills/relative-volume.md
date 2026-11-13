---
name: relative-volume
domain: investing/relative-volume
trigger: "Judging whether volume is genuinely unusual for this name and hour."
anti_trigger: "Not for predicting price, and not for identifying participants."
scope: "Volume against a time-of-day baseline rather than against yesterday."
status: seedling
---

# Relative volume

## Standard

Unusual volume is only meaningful against a baseline, and the right baseline is the same name at the same time of day on comparable days. Raw volume compared with the previous session's total is misleading for most of the day, because the intraday distribution is not flat: the open and the close carry a disproportionate share, and a mid-morning figure that looks small against a full day may be large against the same hour historically.

The standard construction is relative volume: current cumulative volume divided by the average cumulative volume at the same elapsed time over a lookback window. Expressed that way, a reading of two means the name has traded twice its normal pace for that hour, which is a statement that can be compared across names and across the session.

Primary sources: <https://www.finra.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the elapsed session time and the cumulative volume.
- Record the lookback window and its median cumulative volume at the same elapsed time.
- Compute relative volume and record it as a ratio.
- Record the name's typical dispersion around that ratio.
- Record any scheduled event that explains a high reading.
- Compare relative volume across names only when the baseline windows match.

## Procedure

1. Record cumulative volume and elapsed time.
2. Build the baseline from the same elapsed times over the lookback.
3. Compute the ratio and its distribution.
4. Check the event calendar for an explanation.
5. Record the reading with its percentile.
6. Write the observation.

## Anti-patterns

- Comparing today's partial volume with yesterday's full-day total.
- Using a flat-volume baseline across the session.
- Reading a high ratio without checking for a scheduled event.
- Comparing ratios computed over different windows.
- Treating volume as directional.

## Done checklist

- [ ] Elapsed time and cumulative volume recorded.
- [ ] Baseline window recorded.
- [ ] Ratio computed.
- [ ] Dispersion recorded.
- [ ] Events checked.
- [ ] Percentile recorded.

The lookback window is the choice that decides the answer: twenty sessions captures the name's recent character, sixty captures a fuller range of conditions, and a window that includes an unusual event will raise the baseline and understate today's reading. The record should state the window and whether any session in it was excluded, because an unstated window makes the ratio uninterpretable.


## Sources

- Trading data and reporting guidance: <https://www.finra.org/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on volume analysis: <https://www.investor.gov/introduction-investing>
