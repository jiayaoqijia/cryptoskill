---
name: normal-vs-lognormal-vol
domain: investing/normal-vs-lognormal-vol
trigger: "Comparing a basis-point volatility quote with a percentage one."
anti_trigger: "Not for predicting volatility, and not for model selection theory."
scope: "Basis-point versus percentage volatility, and what negative rates did to the convention."
status: seedling
---

# Normal and lognormal volatility

## Standard

Rates can be quoted with two kinds of volatility. Lognormal volatility is a percentage of the rate, familiar from equity options; normal volatility is an absolute number of basis points per annum. The two produce the same option value only when the conversion is done at the rate prevailing, and the conversion is approximately normal volatility equals lognormal volatility times the rate.

The distinction became unavoidable when rates went negative, because a lognormal model cannot represent a negative rate. Normal volatility, also called basis-point volatility, handles negative rates naturally, and it became the default for many short-dated instruments in currencies that experienced them. A quote that does not state the convention is ambiguous, and the difference between the two interpretations is large when rates are near zero.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the volatility type: normal or lognormal, or "shifted" with the shift stated.
- Record the rate at which any conversion was made.
- Convert between conventions explicitly and record the conversion.
- Record the currency's recent history of negative or near-zero rates.
- Record which convention the venue and the counterparty use.
- Where a quote does not state the type, record it as ambiguous rather than assuming.

## Procedure

1. Identify the convention from the confirmation or the venue.
2. Record the rate used for any conversion.
3. Convert the quote into the other convention for comparison.
4. Record the effect of the conversion at current rates.
5. Note the currency's rate history.
6. Write the volatility summary with its type named.

## Anti-patterns

- Mixing quotes from two conventions in one comparison.
- Converting at a rate that has since moved without saying so.
- Assuming lognormal when the currency has had negative rates.
- Reporting vega without the volatility convention.
- Treating a "shifted" model's volatility as normal.

## Done checklist

- [ ] Volatility type recorded.
- [ ] Conversion rate recorded.
- [ ] Conversion performed and shown.
- [ ] Rate history noted.
- [ ] Venue convention recorded.
- [ ] Ambiguity flagged where present.

The practical consequence is that a vega number is meaningless without its convention: a one-basis-point move in a normal-vol quote and a one-percentage-point move in a lognormal quote are different events, and a book that aggregates vega across both without converting is adding quantities that do not share a unit. The record should convert everything into one convention before any exposure is summed or hedged.

## Sources

- Market conventions and standards: <https://www.bis.org/>
- Policy rates and yield data: <https://www.federalreserve.gov/>
- Rate series including negative periods: <https://fred.stlouisfed.org/>
