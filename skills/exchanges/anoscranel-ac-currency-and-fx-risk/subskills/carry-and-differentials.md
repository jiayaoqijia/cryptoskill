---
name: carry-and-differentials
domain: investing/carry-and-differentials
trigger: "Understanding FX carry and the interest-rate differential behind it."
anti_trigger: "Not for recommending a carry trade, and not for predicting rates."
scope: "Interest-rate differentials, carry, and the parity conditions that describe the trade-off."
status: seedling
---

# Carry and differentials

## Standard

FX carry is the return from holding a higher-yielding currency funded in a lower-yielding one. The return has two parts: the interest differential, which accrues steadily, and the exchange-rate change, which can erase it in a day. That asymmetry is the whole risk: the carry is small and frequent, the loss is large and rare.

Covered interest parity says the forward differential should equal the interest differential, so a hedged carry earns approximately the domestic rate. Uncovered parity says the expected exchange change should offset the differential — a condition that holds in the long run at best and is violated for years at a time. Both are descriptions of a trade-off, not trading rules.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the two policy or market rates, their tenors, and the dates.
- Compute the differential in annualised terms and show the arithmetic.
- Distinguish hedged carry (forward-covered) from unhedged carry (exchange-exposed).
- Record the historical drawdown of the currency pair, not just its yield.
- Treat a large differential as a warning about expected depreciation as well as an opportunity.
- Record the funding currency's own risks, including funding availability.

## Procedure

1. Record the two rates with tenors and dates.
2. Compute the annualised differential.
3. State whether the position is hedged or unhedged.
4. Record the pair's drawdown history.
5. Note the implied depreciation in the forward if hedged.
6. Record the finding with its asymmetry.

## Anti-patterns

- Quoting the carry without the drawdown.
- Assuming the differential is free money.
- Ignoring funding-currency risk.
- Comparing rates at different tenors.
- Treating uncovered parity as a timing rule.

## Done checklist

- [ ] Rates recorded with tenor and date.
- [ ] Annualised differential computed.
- [ ] Hedged or unhedged stated.
- [ ] Drawdown history recorded.
- [ ] Forward-implied depreciation noted where hedged.
- [ ] Asymmetry recorded.

## Sources

- Policy and market rate series: <https://fred.stlouisfed.org/>
- Investor education on currency risk: <https://www.investor.gov/introduction-investing>
- Regulatory context for rate disclosures: <https://www.sec.gov/investor>

The asymmetry is the point: carry accrues in small positive increments and is given back in occasional large moves, so a strategy's average return can look attractive while its worst month is catastrophic. Recording the drawdown alongside the yield is what keeps the two visible at the same time.

The funding leg is half the position and gets a fraction of the attention. Its availability can be withdrawn, its cost can change with policy, and in a stress episode the currency that was cheap to borrow becomes expensive at exactly the moment the position needs rolling.
