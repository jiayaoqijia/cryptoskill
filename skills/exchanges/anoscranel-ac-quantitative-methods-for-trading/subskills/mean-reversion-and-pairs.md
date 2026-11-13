---
name: mean-reversion-and-pairs
domain: crypto-trading/mean-reversion-and-pairs
trigger: "Building a mean-reversion or pairs trade on a spread."
anti_trigger: "Not for validating the backtest, and not for predicting convergence."
scope: "Spread construction, the stationarity assumption, and when mean reversion is wishful."
status: seedling
---

# Mean reversion and pairs

## Standard

A pairs trade buys one asset and sells a related one, holding the spread rather than either leg. The intuition is that the spread, unlike the assets, oscillates around a level, and a deviation from that level is a position with a natural exit. The entire method rests on one assumption: that the spread is stationary, meaning it reverts. If it is not, a deviation is not an opportunity but a break in the relationship, and the trade has no exit except the stop.

Construction is where the honesty lives. The ratio or the difference, the hedge ratio estimated from history, and the window over which the level is computed all embed assumptions about the relationship. A hedge ratio fitted on a calm period produces a spread that looks mean-reverting until the relationship shifts, and re-estimating the ratio mid-trade converts a losing position into a new trade with a hidden entry.

Primary sources: <https://quant.stackexchange.com/> and <https://www.quantconnect.com/docs/>.

## Decision rules

- Record the two legs and the economic reason they should co-move; no thesis, no trade.
- Record the spread definition: difference or ratio, and the hedge ratio method.
- Test the spread for stationarity before trading it, not after.
- Record the level and the band from a stated window, with the window's dates.
- Define the exit before entry: reversion to level, band breach, or time stop.
- State what a permanent divergence would look like, as the falsifier.

## Procedure

1. Write the economic link between the legs.
2. Construct the spread with an explicit hedge ratio method.
3. Test for stationarity and record the test, window, and result.
4. Set the level and bands from a stated window.
5. Define entries, exits, and the time stop.
6. Write the divergence falsifier into the record.

## Anti-patterns

- Trading correlation as if it were stationarity; correlated series can drift apart forever.
- Re-fitting the hedge ratio to make a losing spread look normal.
- A window chosen to make the bands look attractive.
- No time stop, so a broken relationship is held on hope.
- Treating a structural break as a larger-than-usual deviation.

## Done checklist

- [ ] Economic link stated.
- [ ] Spread and hedge method recorded.
- [ ] Stationarity tested with window and result.
- [ ] Level and bands dated.
- [ ] Exit rules defined before entry.
- [ ] Divergence falsifier written.

## Sources

- Quantitative finance discussion and references: <https://quant.stackexchange.com/>
- Algorithmic trading documentation and examples: <https://www.quantconnect.com/docs/>
- Risk management context: <https://www.investor.gov/introduction-investing>
