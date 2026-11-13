---
name: fx-operational-costs
domain: investing/fx-operational-costs
trigger: "Measuring what converting between currencies actually costs."
anti_trigger: "Not for choosing a bank, and not for predicting rates."
scope: "Spreads, conversion timing, and the cost stack of moving money between currencies."
status: seedling
---

# FX operational costs

## Standard

Converting currency has a cost stack: the spread between the quoted bid and offer, any commission or margin the provider adds, the value date, and the opportunity cost of the timing. Individually these are small; on repeated conversions across a portfolio they are a visible drag, and on small amounts the fixed components dominate.

The honest measurement is against a reference rate — the mid-market rate at the moment of conversion — with the difference recorded in both currency terms and basis points. A provider that quotes "no commission" and marks up the rate is charging the same money under a different label.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## Decision rules

- Record the reference mid-rate at the timestamp of conversion, with its source.
- Record the effective rate achieved and the difference in basis points.
- Record any commission separately from the spread.
- Record the value date and the funding cost of the interval.
- Compare providers on the same reference and the same amount.
- Aggregate the total conversion cost over a period, not per trade.

## Procedure

1. Capture the reference mid-rate at the conversion timestamp.
2. Record the effective rate and compute the spread in basis points.
3. Record commissions separately.
4. Record value date and any funding cost.
5. Compare two providers on the same basis.
6. Aggregate the period's total cost.

## Anti-patterns

- Comparing providers on quoted "zero commission" alone.
- Using a stale reference rate.
- Ignoring the value-date funding cost.
- Measuring per trade and missing the aggregate drag.
- Comparing different amounts as if the spread were constant.

## Done checklist

- [ ] Reference mid-rate captured with source and timestamp.
- [ ] Effective rate and spread in basis points recorded.
- [ ] Commission recorded separately.
- [ ] Value date and funding cost recorded.
- [ ] Providers compared on the same basis.
- [ ] Period aggregate computed.

## Sources

- Reference exchange-rate data: <https://fred.stlouisfed.org/>
- Investor education on transaction costs: <https://www.investor.gov/introduction-investing>
- Regulatory context for cost disclosure: <https://www.sec.gov/investor>

The aggregate is what matters: a portfolio that converts monthly at a twenty-basis-point spread is paying a quarter of a percent a year for the privilege of holding foreign assets, and that cost belongs in the same table as the management fee rather than in a footnote about execution.

Timing is the component most easily forgotten: a conversion executed at a month-end or a market open pays a wider spread than the same conversion mid-session, and a recurring conversion schedule can be moved to a cheaper window without changing anything else about the position.
