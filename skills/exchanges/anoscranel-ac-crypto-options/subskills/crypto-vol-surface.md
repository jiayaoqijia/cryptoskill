---
name: crypto-vol-surface
domain: crypto-trading/crypto-vol-surface
trigger: "Reading the crypto volatility surface and its skew."
anti_trigger: "Not for forecasting volatility, and not for generic surfaces."
scope: "DVOL, skew, term structure, and the weekend effect."
status: seedling
---

# Crypto volatility surface

## Standard

Crypto volatility surfaces carry a persistent structure that differs from equities. The skew usually favours upside calls in bull phases and downside puts in stress, and it can flip faster than in listed markets because the participant base is smaller and more leveraged. Index-level volatility measures exist, but they are computed from a limited set of expiries and strikes, so they describe the surface rather than summarise it.

Term structure reflects the event calendar: expiries around protocol upgrades, regulatory dates, or large token unlocks trade at a premium, and the front of the curve can be far above the back. The weekend adds a further effect, since liquidity thins while the market keeps trading, and implied volatility often carries a premium into it.

Primary sources: <https://www.cftc.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the expiry, strike, and venue for every volatility used.
- Record the index measure and its methodology where one is quoted.
- Record the skew direction and the level at a stated delta.
- Record the term-structure slope across at least three expiries.
- Record the events inside each expiry's life.
- Record the weekend effect if the position spans one.

## Procedure

1. Collect quotes across expiries and strikes.
2. Record the index measure and its limits.
3. Compute skew at a stated delta and term-structure spreads.
4. Map events onto expiries.
5. Note the weekend effect.
6. Write the surface summary with dates.

## Anti-patterns

- Treating a published volatility index as the whole surface.
- Comparing skew across venues with different strike grids.
- Ignoring an unlock or upgrade inside the expiry.
- Assuming weekend liquidity matches weekday.
- Using one expiry's volatility for a position in another.

## Done checklist

- [ ] Quotes recorded with expiry, strike, venue.
- [ ] Index measure recorded.
- [ ] Skew computed at a stated delta.
- [ ] Term structure recorded.
- [ ] Events mapped.
- [ ] Weekend effect noted.

The skew's persistence is also a risk to any position that treats it as fixed: a shift from call-skew to put-skew can happen within days, and a structure that was priced against one shape loses when the shape changes even if the underlying stands still, so the record should state the skew it was priced against.


Because the surface is thinner than its listed equivalents, a single large trade can move a wing and make the skew look informative when it is only reflecting one participant's hedging, which is a reason to record the size behind a quote before treating the shape as a market signal.

## Sources

- Regulatory market information: <https://www.cftc.gov/>
- Investor guidance on volatility products: <https://www.investor.gov/introduction-investing>
- Market structure context: <https://www.sec.gov/investor>
