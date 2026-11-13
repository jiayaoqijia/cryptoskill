---
name: price-and-volume-adjustment
domain: investing/price-and-volume-adjustment
trigger: "Adjusting historical data so a series is comparable across corporate actions."
anti_trigger: "Not for building a backtest, and not for forecasting."
scope: "Adjusting history so a chart is comparable, and the difference between adjusted and total-return series."
status: seedling
---

# Price and volume adjustment

## Standard

A historical price series is only comparable if every corporate action since the first observation has been applied to it consistently. Splits scale prices and volumes inversely; dividends reduce the price on the ex-date; spin-offs redistribute value. A series adjusted for one action and not another is worse than an unadjusted one, because the gaps are invisible.

Two series types matter. A split-adjusted price series answers "what did the price do" in today's share terms. A total-return series adds reinvested dividends and answers "what did an investor earn". Neither is correct for every question, and the record must state which is being used and what it does and does not include.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the series type: raw, split-adjusted, or total return.
- Record which actions have been applied and which have not.
- Volume is adjusted by the same ratio as price for splits, in the opposite direction.
- Dividend adjustments are applied on the ex-date, not the payment date.
- Never mix series types within one comparison or chart.
- Where a series' adjustment history is unknown, record it as unknown and find another source.

## Procedure

1. Identify the series type and the adjustments applied.
2. List the corporate actions in the period and check each is applied or explicitly excluded.
3. Adjust volume consistently with price.
4. Label the series and its coverage in the record.
5. Re-derive one known data point as a test.
6. Record the source and retrieval date.

## Anti-patterns

- Charting an unadjusted series across a split.
- Mixing total-return and price series in one table.
- Applying a dividend adjustment on the payment date.
- Assuming a vendor's series is adjusted for everything.
- Leaving the series type unstated.

## Done checklist

- [ ] Series type recorded.
- [ ] Actions applied or excluded listed.
- [ ] Volume adjusted consistently.
- [ ] Series labelled with coverage.
- [ ] One data point re-derived as a test.
- [ ] Source and retrieval date recorded.

## Sources

- Regulatory context for price and volume reporting: <https://www.sec.gov/investor>
- Investor education on total return: <https://www.investor.gov/introduction-investing>
- Rule context for corporate-action processing: <https://www.finra.org/rules-guidance>

The test that catches most errors is arithmetic: re-derive one known data point from the raw series and the stated adjustments, and see whether it matches the vendor's value. When it does not, the series is mislabelled, and every analysis built on it inherits the error.
