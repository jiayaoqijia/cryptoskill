---
name: rates-option-hedging
domain: investing/rates-option-hedging
trigger: "Hedging the DV01 and vega of a rates option position."
anti_trigger: "Not for predicting rates, and not for portfolio duration policy."
scope: "DV01 and vega hedging, gamma in a rates book, and rehedging cost."
status: seedling
---

# Rates option hedging

## Standard

A rates option book carries at least three exposures: delta, expressed as DV01; vega, the sensitivity to the volatility surface; and gamma, the rate of change of delta. The first can be hedged with swaps or futures, the second with other options, and the third cannot be hedged at all — it is the position's shape, and it determines how often the delta hedge must be adjusted.

The hedging instruments are the practical constraint. Vega can only be offset in instruments that trade, which for many currencies means a handful of expiries and at-the-money strikes; a book with vega in an illiquid corner is a book with unhedgeable risk. That is why the record states both the exposure and the instruments available to offset it, rather than only the exposure.

Primary sources: <https://www.bis.org/> and <https://www.cmegroup.com/>.

## Decision rules

- Record DV01 per instrument and for the book, with the curve point.
- Record vega per expiry bucket and the surface point.
- Record gamma and the expected rehedging frequency.
- Record the instruments available to hedge each bucket.
- Record the cost of the hedge: spreads, financing, and clearing.
- Record which exposures are deliberately left unhedged and why.

## Procedure

1. Compute DV01 by curve point and aggregate.
2. Compute vega by expiry bucket.
3. Compute gamma and the implied rehedge frequency.
4. List available hedging instruments per bucket.
5. Record hedge costs.
6. Write the hedging summary with the unhedged residuals named.

## Anti-patterns

- Hedging DV01 and calling the book neutral.
- Ignoring vega concentration in an illiquid expiry.
- Assuming gamma can be hedged continuously.
- Using a hedge instrument with a different curve point.
- Omitting the cost of rehedging from the economics.

## Done checklist

- [ ] DV01 by point recorded.
- [ ] Vega by bucket recorded.
- [ ] Gamma and rehedge frequency recorded.
- [ ] Hedge instruments listed.
- [ ] Costs recorded.
- [ ] Unhedged residuals named.

The cross-bucket exposure is the usual source of surprise: a book that is flat on at-the-money vega per expiry can still be short the skew, because the wings move independently of the centre, and a hedging report that aggregates by expiry alone will show neutral while the position is exposed to a repricing of the wings rather than of the level.

## Sources

- Market conventions and risk practice: <https://www.bis.org/>
- Exchange rate products and data: <https://www.cmegroup.com/>
- Yield and volatility series: <https://fred.stlouisfed.org/>
