---
name: rates-vol-surface
domain: investing/rates-vol-surface
trigger: "Reading the rates volatility cube and its skew."
anti_trigger: "Not for forecasting volatility, and not for model selection."
scope: "The strike and expiry cube, and the skew that rates options carry."
status: seedling
---

# Rates volatility surface

## Standard

Rates volatility is a cube: expiry, underlying tenor, and strike. Each point is a different option, and the market quotes a subset of them, with interpolation filling the rest. The shape along the expiry axis is the term structure; along the strike axis it is the skew; and along the tenor axis it reflects the different behaviour of short and long rates.

The skew in rates has a characteristic shape that differs from equities. Because rates are bounded below in practice by a central bank's tolerance for negative policy rates, and because the distribution of rate outcomes is not symmetric, the smile is often skewed towards the upside for payers in some currencies and towards the downside in others. Reading a single at-the-money number without the skew is reading one point of a three-dimensional object.

Primary sources: <https://www.bis.org/> and <https://www.cmegroup.com/>.

## Decision rules

- Record the expiry, tenor, and strike of every quote used.
- Record the interpolation method where quotes are not available.
- Record the skew as the difference between a wing and the at-the-money level, with the wing stated.
- Record the term structure across at least three expiries.
- Record the data source and time of the quotes.
- Where the market is thin at a strike, record it and cap the confidence.

## Procedure

1. Collect quotes across the expiries and strikes in scope.
2. Record each point with its tenor.
3. Compute skew at a stated wing and term structure across expiries.
4. Note interpolation and thin points.
5. Record the source and time.
6. Write the surface summary.

## Anti-patterns

- Using one at-the-money number as the surface.
- Comparing skew across currencies without the wing definition.
- Ignoring the tenor axis in a cube.
- Interpolating across a thin region silently.
- Mixing quotes from different times of day.

## Done checklist

- [ ] Quotes recorded with expiry, tenor, strike.
- [ ] Interpolation recorded.
- [ ] Skew computed with wing stated.
- [ ] Term structure across expiries recorded.
- [ ] Source and time recorded.
- [ ] Thin points noted.

The expiry axis also carries an effect that a single surface does not show: at short expiries the volatility is dominated by scheduled events and by the policy calendar, while at long expiries it reflects the distribution of the terminal rate, so the same currency can have a steeply inverted term structure in one month and a flat one in ten years.

## Sources

- Market conventions and volatility data: <https://www.bis.org/>
- Exchange rate option data: <https://www.cmegroup.com/>
- Rate series: <https://fred.stlouisfed.org/>
