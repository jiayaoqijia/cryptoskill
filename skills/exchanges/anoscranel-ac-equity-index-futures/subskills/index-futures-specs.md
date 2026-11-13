---
name: index-futures-specs
domain: investing/index-futures-specs
trigger: "Reading an index future's specification before sizing a position."
anti_trigger: "Not for predicting the index, and not for hedging policy."
scope: "Multiplier, tick, expiry cycle, cash settlement, and margin."
status: seedling
---

# Index futures specs

## Standard

An index future is defined by its multiplier, its tick, its expiry cycle, and its settlement. The multiplier converts index points into currency, so a contract's notional is the index level times the multiplier, and a tick is the smallest permitted price movement multiplied by the same number. Those two facts determine position size and the value of a stop, and they differ between contracts by design.

Cash settlement means there is no delivery obligation, which removes the physical risk that commodity contracts carry; the position simply settles against the index at expiry. What remains is the expiry cycle: index futures typically expire quarterly, and the contract that is most liquid is the front one until the roll period, when liquidity migrates to the next. That migration is a scheduling fact the trader has to plan around.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## Decision rules

- Record the multiplier, tick size, and tick value in currency.
- Record the notional at the current index level.
- Record the expiry cycle and the last trading day for the contract held.
- Record whether settlement is cash or physical; for index futures it is cash.
- Record the exchange's margin requirement and the broker's additional requirement.
- Record which contract month is currently the most liquid.

## Procedure

1. Obtain the contract specification from the exchange.
2. Record multiplier, tick, and tick value.
3. Compute notional at the current index level.
4. Record expiry dates and the roll convention.
5. Record margin requirements and any broker add-on.
6. Write the specification summary for the trade.

## Anti-patterns

- Confusing the index level with the contract value.
- Assuming a tick is worth the same across contracts.
- Holding a contract into expiry without a roll decision.
- Ignoring the broker's margin add-on when sizing.
- Treating cash settlement as a reason to ignore expiry.

## Done checklist

- [ ] Multiplier, tick, and tick value recorded.
- [ ] Notional computed.
- [ ] Expiry and last trading day recorded.
- [ ] Settlement method recorded.
- [ ] Margin requirements recorded.
- [ ] Liquidity of contract months noted.

The specification also fixes the smallest increment a stop can be placed at and the minimum price movement a fill can improve by, which is why a strategy designed on a different contract's tick can appear to work in backtest and fail in execution.


## Sources

- Exchange index futures specifications: <https://www.cmegroup.com/>
- Regulatory background on futures: <https://www.cftc.gov/>
- Investor education on futures products: <https://www.investor.gov/introduction-investing>
