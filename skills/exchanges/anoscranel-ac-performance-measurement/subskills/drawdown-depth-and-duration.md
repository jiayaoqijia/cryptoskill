---
name: drawdown-depth-and-duration
domain: investing/drawdown-depth-and-duration
trigger: "Describing a drawdown in both depth and time."
anti_trigger: "Not for predicting drawdowns, and not for risk budgeting."
scope: "Depth, duration, recovery, and why two drawdowns of equal size differ."
status: seedling
---

# Drawdown depth and duration

## Standard

A drawdown has two dimensions that are usually reported as one. Depth is the fall from peak to trough; duration is the time from peak to recovery. Two strategies with identical maximum drawdowns are not equivalent if one recovered in months and the other took years, and the second dimension is what the investor actually experiences, because it is the time during which the decision to continue is being tested.

Recovery arithmetic is the reason depth matters disproportionately. A fall of twenty percent requires a rise of twenty-five percent to recover; a fall of fifty percent requires a hundred. Reporting the depth without the required recovery obscures the asymmetry, and reporting the maximum without the duration hides how long a holder would have spent underwater.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the peak date, trough date, and recovery date where it occurred.
- Record the depth and the required recovery percentage.
- Record the duration underwater in days or months.
- Record whether the drawdown is still open, and if so its length so far.
- Record the number of distinct drawdowns beyond a stated threshold.
- Compare drawdowns at equal depth, not only at maximum.

## Procedure

1. Build the return series and identify peaks and troughs.
2. Compute depth for each drawdown and the recovery required.
3. Measure duration from peak to recovery, or to today if open.
4. Count drawdowns beyond a stated threshold.
5. Compare across strategies at equal depth.
6. Write the summary with both dimensions.

## Anti-patterns

- Reporting maximum drawdown without duration.
- Ignoring an open drawdown because it has not recovered yet.
- Comparing depths across strategies with different volatility.
- Forgetting the recovery percentage.
- Using a threshold that excludes all but one event.

## Done checklist

- [ ] Peaks, troughs, recoveries recorded.
- [ ] Depth and required recovery computed.
- [ ] Duration measured.
- [ ] Open drawdowns noted.
- [ ] Count beyond threshold recorded.
- [ ] Comparison at equal depth made.

The pairing also explains why investors abandon strategies at the wrong moment: a deep but short drawdown is easier to hold than a shallow but long one, and a strategy that has been underwater for two years will be judged harshly even with a modest depth, which is a fact about the holder rather than about the strategy.


## Sources

- Investment performance standards: <https://www.cfainstitute.org/>
- Investor education on risk: <https://www.investor.gov/introduction-investing>
- Market data for series construction: <https://fred.stlouisfed.org/>
