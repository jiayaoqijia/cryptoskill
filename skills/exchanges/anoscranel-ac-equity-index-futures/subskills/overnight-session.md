---
name: overnight-session
domain: investing/overnight-session
trigger: "Trading an index future outside the cash equity session."
anti_trigger: "Not for predicting the overnight move, and not for market-structure theory."
scope: "Nearly continuous trading, session liquidity, and the gap when cash opens."
status: seedling
---

# Overnight session

## Standard

Index futures trade nearly around the clock on the exchange's electronic platform, while the underlying cash market trades a much shorter session. That mismatch is the reason the future carries most of the price discovery for overnight news: an earnings release or a policy announcement after the cash close moves the future, and the cash index simply does not trade until the next morning.

Liquidity is not evenly distributed across that extended session. Depth is greatest when the cash market is open and the futures contract's own cash-equity arbitrage is active; it thins in the overnight hours, when spreads widen and the same order moves the price further. Trading the overnight session therefore means accepting a different cost structure, and a stop placed there is more likely to be triggered by noise.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## Decision rules

- Record the trading hours of the contract and of the underlying cash market.
- Record the liquidity profile by hour, with spread and depth sampled.
- Record the position's exposure to overnight news, in notional and in margin terms.
- Record the stop policy for the overnight session, which may differ from the day.
- Record the gap between the future's last price and the cash open, and its history.
- Record whether the strategy requires holding through the cash open.

## Procedure

1. Map the futures session and the cash session.
2. Sample spreads and depth in each hour band.
3. Compute the position's notional and margin exposure overnight.
4. Set the overnight stop policy and record its rationale.
5. Collect the history of gap sizes at the cash open.
6. Review overnight behaviour against the policy.

## Anti-patterns

- Assuming overnight liquidity equals day liquidity.
- Using a day-session stop distance in a thin overnight market.
- Ignoring the gap between the future and the cash open.
- Holding a leveraged position through an event without a funding check.
- Treating the future's overnight price as the cash market's price.

## Done checklist

- [ ] Sessions mapped.
- [ ] Liquidity sampled by hour.
- [ ] Overnight exposure computed.
- [ ] Stop policy recorded.
- [ ] Gap history collected.
- [ ] Behaviour reviewed against policy.

The practical rule is to size overnight positions by the overnight book rather than by the day's, and to record the difference explicitly: a position that is comfortable at midday can be several times the depth available at three in the morning.


## Sources

- Exchange trading hours and contract data: <https://www.cmegroup.com/>
- Regulatory market information: <https://www.cftc.gov/>
- Market volatility data: <https://fred.stlouisfed.org/>
