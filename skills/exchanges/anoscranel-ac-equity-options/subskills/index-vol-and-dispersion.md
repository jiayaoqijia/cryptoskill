---
name: index-vol-and-dispersion
domain: investing/index-vol-and-dispersion
trigger: "Understanding why index volatility differs from its components' volatility."
anti_trigger: "Not for forecasting volatility, and not for portfolio policy."
scope: "Index volatility as a function of correlation, and what dispersion trades."
status: seedling
---

# Index volatility and dispersion

## Standard

An index's volatility is not the average of its components' volatilities; it is lower, because the components do not move together. The gap is correlation. When correlation is low, individual moves offset and the index is calm even if single names are volatile; when correlation rises towards one, the index inherits the components' volatility and diversification disappears.

That relationship is what a dispersion trade exploits: selling index volatility while buying the volatility of the components expresses a view that correlation will fall. The trade's risk is concentrated in exactly the states where correlation rises — a market-wide shock — which is why the position typically earns small amounts and loses heavily in a crisis, and why the record must state the correlation assumption rather than the implied volatilities alone.

Primary sources: <https://www.cboe.com/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the index implied volatility and the weighted component implied volatility.
- Record the implied correlation implied by the two.
- Record the historical correlation and its range.
- Record the dispersion structure's legs and the vega weights.
- Record the loss under a correlation spike, in currency.
- Record the liquidity of the component options, which decides whether the trade can be sized.

## Procedure

1. Collect index and component implied volatilities.
2. Compute implied correlation from them.
3. Record historical correlation over comparable windows.
4. Construct the dispersion legs with vega weights.
5. Compute the loss under a correlation rise.
6. Record the trade and its correlation assumption.

## Anti-patterns

- Treating index volatility as an average of components.
- Trading dispersion without the component liquidity to support it.
- Ignoring the correlation spike scenario.
- Comparing implied correlation across indices with different compositions.
- Assuming the historical correlation range is a bound.

## Done checklist

- [ ] Index and component vol recorded.
- [ ] Implied correlation computed.
- [ ] Historical correlation recorded.
- [ ] Legs and weights recorded.
- [ ] Spike loss computed.
- [ ] Assumption recorded.

The practical consequence is that an index option position is a position on correlation as well as on level: a trader who buys index options expecting a volatile market can lose if the volatility arrives in a few names while the index stays calm, and the record should state which of the two exposures the position is meant to carry.


## Sources

- Index and option volatility data: <https://www.cboe.com/>
- Market and volatility series: <https://fred.stlouisfed.org/>
- Regulatory product information: <https://www.sec.gov/investor>
