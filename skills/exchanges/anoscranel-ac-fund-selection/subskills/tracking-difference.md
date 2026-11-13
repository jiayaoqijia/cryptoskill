---
name: tracking-difference
domain: investing/tracking-difference
trigger: "Comparing a fund's delivered return with its index over time."
anti_trigger: "Not for predicting future tracking, and not for fund recommendations."
scope: "Tracking difference versus tracking error, and what each reveals about implementation quality."
status: seedling
---

# Tracking difference

## Standard

Two measures describe how well a fund follows its index, and they answer different questions. Tracking difference is the cumulative gap between the fund's return and the index's return over a period — it tells you what the fund actually cost you relative to the benchmark. Tracking error is the volatility of that gap — it tells you how reliably the fund follows.

A fund can have a small tracking error and a persistently negative tracking difference: it follows the index faithfully, just below it, usually because of fees. A fund with a large tracking error is doing something the index does not describe, whether sampling, holding cash, or using derivatives, and that something needs explaining before the fund does.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.sec.gov/investor>.

## Decision rules

- Compute tracking difference over one, three, and five years where data exists, net of fees.
- Compute tracking error over the same windows and report both.
- Compare the difference with the expense ratio; a gap much larger than the fee needs an explanation.
- Record any structural reason for the gap: sampling, cash drag, securities lending, tax.
- Use the same index and the same currency basis for both series.
- Where the fund changed methodology, split the history at the change.

## Procedure

1. Pull fund and index total returns over the chosen windows.
2. Compute the difference for each window.
3. Compute the volatility of the daily or monthly differences.
4. Compare the difference with the expense ratio.
5. Identify structural causes from the fund's disclosure.
6. Record the findings with the windows and the data source.

## Anti-patterns

- Comparing price returns with total returns.
- Using one year as the evidence.
- Ignoring a methodology change mid-history.
- Assuming a large gap is always a defect before checking the cause.
- Mixing currency bases.

## Done checklist

- [ ] Difference computed over three windows.
- [ ] Tracking error computed over the same windows.
- [ ] Difference compared with the expense ratio.
- [ ] Structural causes identified.
- [ ] Methodology changes respected.
- [ ] Findings recorded with sources and dates.

## Sources

- Investor education on index funds: <https://www.investor.gov/introduction-investing>
- Fund and index disclosure context: <https://www.sec.gov/investor>
- Market return data: <https://fred.stlouisfed.org/>

The most useful comparison is against the fund's own fee: a fund that tracks within a few basis points of its expense ratio is doing what it promised, while a fund whose gap is several times the fee is telling you something about implementation that the marketing page does not. That ratio belongs in the record.
