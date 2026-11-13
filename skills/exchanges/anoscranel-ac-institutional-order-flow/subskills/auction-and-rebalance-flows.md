---
name: auction-and-rebalance-flows
domain: investing/auction-and-rebalance-flows
trigger: "Anticipating the flows that arrive on a schedule."
anti_trigger: "Not for predicting the index decision, and not for deal advice."
scope: "Closing auctions, index events, and the flows that arrive on a schedule."
status: seedling
---

# Auction and rebalance flows

## Standard

Some of the largest flows in a name are scheduled: the closing auction, where index funds and passive vehicles execute to the official close, and index rebalance dates, when tracking funds must buy or sell to match a changed benchmark. These flows are announced in advance and they arrive in a defined window, which makes them the one category of institutional activity that can be anticipated rather than inferred.

The anticipation is partial. The size of the flow can be estimated from index weights and the assets tracking the index, but the estimate carries error, and the trade is widely known, which means part of it is priced before the effective date. The record should state the estimate, its error band, and the portion likely already reflected, rather than treating the scheduled flow as a free signal.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the event, its announcement date, and its effective date.
- Estimate the flow from published weights and assets tracking the index, with the method stated.
- Record the error band and the assumptions behind the estimate.
- Record how much of the flow is likely already reflected in the price.
- Record the auction's historical volume share for the name.
- Record the post-event behaviour observed, for calibration.

## Procedure

1. Identify scheduled events for the name over the horizon.
2. Estimate each flow with a stated method.
3. Record the error band.
4. Assess the anticipated portion.
5. Record the auction volume share.
6. Compare the observed outcome with the estimate afterwards.

## Anti-patterns

- Treating a scheduled flow as an unpriced signal.
- Quoting an estimate without its error band.
- Ignoring the announcement-to-effective window.
- Assuming the closing auction is the only scheduled flow.
- Skipping the after-the-fact comparison.

## Done checklist

- [ ] Event and dates recorded.
- [ ] Flow estimated with method.
- [ ] Error band recorded.
- [ ] Anticipated portion assessed.
- [ ] Auction share recorded.
- [ ] Outcome compared afterwards.

The auction's own mechanics are worth recording because they decide execution: orders placed into the closing auction are matched at a single clearing price, so a participant who needs to be done by the close accepts whatever price the imbalance produces, and the last minutes before the close are where that price is discovered. That is why volume concentrates there and why a closing print can be several times the intraday norm.


## Sources

- Market structure and closing auction context: <https://www.sec.gov/investor>
- Trading practice guidance: <https://www.finra.org/>
- Investor education on index events: <https://www.investor.gov/introduction-investing>
