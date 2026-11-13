---
name: fx-vol-quotes
domain: investing/fx-vol-quotes
trigger: "Reading an ATM straddle, risk reversal, and butterfly quote."
anti_trigger: "Not for predicting volatility, and not for option pricing theory."
scope: "ATM straddle, 25-delta risk reversal, and butterfly as the market's volatility quote."
status: seedling
---

# FX volatility quotes

## Standard

FX volatility is quoted as a triplet rather than a surface. The at-the-money level is quoted as the implied volatility of a straddle at the forward, the risk reversal is the difference in implied volatility between the call and the put at a given delta, and the butterfly is the average of the two wings less the at-the-money level. Together they describe the level, the skew, and the curvature of the smile with three numbers instead of a full surface.

Reading them is a matter of knowing what each measures. A negative risk reversal means the market pays more for the downside currency than the upside, which is the normal state when one currency is the funding currency of the pair. A high butterfly means the wings are expensive relative to the centre, which typically signals demand for protection against large moves rather than for direction.

Primary source: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the ATM level, the risk reversal, and the butterfly, with the delta point used.
- Record the expiry and the cut for each quote.
- Reconstruct the call and put implied volatilities from the triplet.
- Record the historical range of the triplet, not just its level.
- Record the direction of the skew and the currency it favours.
- Where a quote is for a different delta point, record it rather than interpolating silently.

## Procedure

1. Collect the three quotes at a stated delta and expiry.
2. Reconstruct the wing volatilities.
3. Record the historical range of each component.
4. Interpret the skew in terms of the currencies involved.
5. Note any event that explains an unusual butterfly.
6. Record the triplet with its date and source.

## Anti-patterns

- Quoting a single implied volatility for an FX pair and calling it the market.
- Comparing risk reversals across pairs with different delta points.
- Ignoring the butterfly, which carries the tail demand.
- Reading a negative risk reversal as a directional forecast.
- Using a quote from a different expiry to price a trade.

## Done checklist

- [ ] Triplet recorded with delta and expiry.
- [ ] Wing volatilities reconstructed.
- [ ] Historical ranges recorded.
- [ ] Skew interpreted by currency.
- [ ] Event explanation noted.
- [ ] Quote dated and sourced.

## Sources

- Foreign exchange market structure and turnover: <https://www.bis.org/>
- Market rates and data: <https://www.federalreserve.gov/>
- Volatility and rate series: <https://fred.stlouisfed.org/>
