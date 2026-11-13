---
name: fund-liquidity
domain: investing/fund-liquidity
trigger: "Assessing how a fund's liquidity behaves, including in stress."
anti_trigger: "Not for predicting fund closures, and not for recommendations."
scope: "Premiums and discounts, creation and redemption, and what happens to spreads in stress."
status: seedling
---

# Fund liquidity

## Standard

A fund's liquidity has two layers: the liquidity of the underlying assets and the liquidity of the fund's own shares. For an ETF they are connected by the creation and redemption mechanism, which lets authorised participants arbitrage the difference — in normal conditions. In stress the connection can stretch: the underlying bonds may not trade, the arbitrage may become uneconomic, and the ETF trades at a discount to the value of assets nobody can sell.

For a mutual fund the layer is different: shares are bought and sold at the fund's valuation, not on an exchange, so the risk is a gate or a suspension rather than a discount. Both structures have documented stress behaviour, and both should be recorded before they are needed.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the underlying assets' liquidity separately from the fund's.
- For ETFs, record the historical premium and discount range.
- For mutual funds, record redemption terms, gates, and fees.
- Note the size and concentration of the fund relative to the underlying market.
- Record what happened to the vehicle in the last stress episode where data exists.
- Where the fund is a large holder of an illiquid asset, record the exit risk.

## Procedure

1. Assess the underlying market's liquidity.
2. Pull the fund's premium or discount history.
3. Record redemption terms for mutual funds; creation and redemption details for ETFs.
4. Compare fund size with the underlying market's daily turnover.
5. Check stress-period behaviour where available.
6. Record the liquidity assessment with its limits.

## Anti-patterns

- Treating daily trading as evidence of underlying liquidity.
- Ignoring the premium and discount history.
- Assuming gates and fees will not be invoked.
- Overlooking the fund's size relative to the market.
- Using calm-period spreads for a stress assessment.

## Done checklist

- [ ] Underlying liquidity assessed.
- [ ] Premium or discount history recorded.
- [ ] Redemption and creation terms recorded.
- [ ] Fund size versus market turnover compared.
- [ ] Stress behaviour checked where data exists.
- [ ] Assessment written with limits.

## Sources

- Fund liquidity and redemption disclosure: <https://www.sec.gov/investor>
- Investor education on fund trading: <https://www.investor.gov/introduction-investing>
- Market liquidity data: <https://fred.stlouisfed.org/>

The practical test is to ask what would happen to this vehicle if the underlying market closed for a week. An ETF would trade on its own supply and demand, a mutual fund would price at stale values, and both would face redemptions into a market that cannot absorb them. The record should state which of those applies.
