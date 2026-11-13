---
name: implied-volatility
domain: crypto-trading/implied-volatility
trigger: "Reading implied volatility, skew, and term structure as prices."
anti_trigger: "Not for forecasting realised volatility, and not for trade selection."
scope: "Implied volatility, skew, and term structure, and what the surface does and does not say."
status: seedling
---

# Implied volatility

## Standard

Implied volatility is the volatility input that makes a pricing model reproduce the market price. It is therefore a price, quoted in volatility units, not a forecast of what will happen. When someone says implied volatility is high, they mean options are expensive relative to the model's other inputs; they do not mean the market will be volatile, though often it will be.

The surface adds structure. Skew is the difference in implied volatility between strikes: equity indices typically show higher implied volatility for downside strikes because protection there is in demand. Term structure is the difference across expiries: near-dated options can carry a premium into an event and collapse after it. Both are prices for risk transfer, and both move before the news does.

Primary sources: <https://www.cboe.com/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Quote implied volatility with the expiry, the strike, and the model used.
- Read skew as a price for protection, not as a prediction of direction.
- Read term structure with the event calendar: a kink usually marks a scheduled event.
- Compare current implied volatility with its own history, not with a universal threshold.
- Where the surface is illiquid at a strike, record the interpolation and its uncertainty.
- Never present implied volatility as a probability.

## Procedure

1. Record the implied volatility for the strikes and expiries in scope.
2. Compute skew and term-structure spreads.
3. Compare with the same measures over the prior year.
4. Check the event calendar for kinks.
5. Note where the surface is thin or interpolated.
6. Record the reading with its date and model.

## Anti-patterns

- Treating implied volatility as a forecast.
- Comparing implied volatility across assets with different histories.
- Ignoring skew and reading only at-the-money levels.
- Missing an event kink in the term structure.
- Quoting a single number without strike and expiry.

## Done checklist

- [ ] Implied volatility recorded with strike, expiry, model.
- [ ] Skew computed.
- [ ] Term-structure spreads computed.
- [ ] Historical comparison made.
- [ ] Event kinks checked.
- [ ] Thin strikes noted.

## Sources

- Options market data and education: <https://www.cboe.com/>
- Investor education on options volatility: <https://www.investor.gov/introduction-investing>
- Regulatory context for options products: <https://www.sec.gov/investor>

The most reliable reading of a volatility surface is comparative: today against its own history, this strike against its neighbours, this expiry against the next. A level quoted alone carries almost no information, which is why the record always pairs it with the comparison it is being judged against.
