---
name: credit-spread-volatility
domain: investing/credit-spread-volatility
trigger: "Interpreting a quoted credit spread volatility and its assumptions."
anti_trigger: "Not for forecasting spreads, and not for option theory."
scope: "Spread volatility, quoting conventions, and the role of assumed recovery."
status: seedling
---

# Credit spread volatility

## Standard

Credit options are quoted in spread volatility: the volatility of the spread, expressed either as a percentage of the spread or in basis points. The conversion between the two follows the same logic as in rates, and the choice matters most when spreads are wide or narrow, because a percentage quote on a wide spread implies a large absolute move.

Recovery is the second input, and it changes the relationship between spread and default probability. A lower assumed recovery raises the loss given default, so a given spread implies a higher default probability; the option's value depends on that mapping, and two quotes built on different recovery assumptions are not directly comparable. The record states the recovery assumption beside the volatility.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record whether the volatility is quoted in percentage or basis-point terms.
- Record the spread level at which any conversion was made.
- Record the assumed recovery and its source.
- Record the model used to convert spread volatility into a price.
- Record the effect of a change in the recovery assumption on the price.
- Where the convention is unstated, record it as ambiguous.

## Procedure

1. Identify the quoting convention from the confirmation.
2. Record the spread level used for conversion.
3. Record the recovery assumption.
4. Convert the quote into the alternative convention for comparison.
5. Record the model and its inputs.
6. Write the volatility summary with assumptions named.

## Anti-patterns

- Comparing percentage and basis-point quotes directly.
- Ignoring recovery when converting spread into probability.
- Using a recovery assumption from a different seniority.
- Reporting vega without the convention.
- Assuming a quote's convention from its magnitude.

## Done checklist

- [ ] Volatility convention recorded.
- [ ] Spread level recorded.
- [ ] Recovery recorded.
- [ ] Conversion done and shown.
- [ ] Model recorded.
- [ ] Ambiguity flagged.

A further subtlety is that spread volatility is not a single number across the curve: short-dated options on a name often carry higher annualised volatility than long-dated ones when a specific event is expected, and the term structure of spread volatility is the place where event risk is priced. A comparison that uses one expiry's volatility for a trade in another is a comparison of two different expectations, and the record should state which expiry the number belongs to.

## Sources

- Credit derivatives market standards: <https://www.isda.org/>
- Market and credit data: <https://www.federalreserve.gov/>
- Spread series: <https://fred.stlouisfed.org/>
