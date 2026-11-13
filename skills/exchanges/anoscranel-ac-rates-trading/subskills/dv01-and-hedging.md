---
name: dv01-and-hedging
domain: investing/dv01-and-hedging
trigger: "Computing DV01 and the hedge ratio between a bond position and a future."
anti_trigger: "Not for predicting rate moves, and not for portfolio duration policy."
scope: "DV01, hedge ratios, and duration-weighted hedging across the curve."
status: seedling
---

# DV01 and hedging

## Standard

DV01 is the change in value for a one-basis-point move in yield, and it is the unit that makes positions across the curve comparable. A cash bond and a future have different DV01s, and hedging means matching them: the number of futures contracts equals the position's DV01 divided by the future's DV01, adjusted for the cheapest-to-deliver bond, whose DV01 is what the contract actually tracks.

The subtlety is that the hedge ratio is not constant. As yields move, the CTD can switch, and the future's DV01 changes with it; convexity means the cash bond's DV01 changes faster than the future's. A hedge computed once is a hedge for today's yields, and a position held through a large move will drift away from neutrality without any trade having been made.

Primary sources: <https://www.cmegroup.com/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record DV01 for the cash position and for the CTD bond, with the yield used.
- Compute the hedge ratio as position DV01 divided by future DV01.
- Record the future's DV01 per contract, which depends on the CTD.
- Record the assumed yield move over which the hedge is expected to hold.
- Record the convexity difference between the cash bond and the CTD.
- Recompute the ratio whenever the CTD changes or yields move materially.

## Procedure

1. Compute the cash position's DV01 at the current yield.
2. Compute the CTD's DV01 per contract notional.
3. Divide to get the number of contracts.
4. Record the yield range over which the ratio is valid.
5. Note the convexity mismatch and its direction.
6. Recompute at the stated review triggers.

## Anti-patterns

- Using the notional value to compute a hedge ratio.
- Assuming the hedge ratio is stable across a large yield move.
- Ignoring the CTD when computing the future's DV01.
- Hedging with a contract of the wrong maturity bucket.
- Treating a duration hedge as a credit hedge.

## Done checklist

- [ ] Cash DV01 computed with its yield.
- [ ] CTD DV01 computed per contract.
- [ ] Hedge ratio computed and recorded.
- [ ] Validity range stated.
- [ ] Convexity mismatch noted.
- [ ] Recalculation triggers set.

The hedge's quality is also visible in its residual: after hedging, the position should still have a small DV01 and a larger exposure to the shape of the curve, and a record that shows only one number cannot distinguish a good hedge from a position that has quietly become a different trade.

## Sources

- Bond futures and conversion factor data: <https://www.cmegroup.com/>
- Treasury yield data: <https://www.federalreserve.gov/>
- Rate series for scenario analysis: <https://fred.stlouisfed.org/>
