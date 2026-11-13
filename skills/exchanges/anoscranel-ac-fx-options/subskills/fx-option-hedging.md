---
name: fx-option-hedging
domain: investing/fx-option-hedging
trigger: "Hedging the delta and vega of an FX option position."
anti_trigger: "Not for pricing models, and not for portfolio currency hedging."
scope: "Delta hedging in spot, vega management, and the cost of rehedging."
status: seedling
---

# FX option hedging

## Standard

Hedging an FX option means trading spot against the option's delta, and the frequency of that trading determines the realised cost. Continuous hedging is an idealisation: in practice the hedger rehedges at intervals or at thresholds, and the difference between the option's implied volatility and the volatility realised over the hedge path is what the position earns or loses.

Vega is the second exposure, and it is not hedgeable in the same way. A position's vega can be offset by trading other options, which requires a market in the right expiry and strike, and in quiet periods that market may not exist at a reasonable spread. A book that is delta-neutral and short vega is therefore exposed to a repricing of the whole surface, and the record should say so.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the delta, the rehedging rule, and the threshold that triggers a trade.
- Record the implied volatility at entry and the realised volatility over the hedge period.
- Record the vega position and the instruments available to offset it.
- Record the cost of the hedge: spread, financing, and the number of rehedges.
- Record the gamma profile, since it determines how often the delta moves.
- Record the underline assumption about jumps, which no delta hedge covers.

## Procedure

1. Record delta and the rehedging rule.
2. Estimate the number of rehedges implied by the gamma.
3. Compute the hedge cost at the observed spread.
4. Record vega and the offsetting instruments.
5. Compare implied with realised volatility over the period.
6. Write the hedging summary with its assumptions.

## Anti-patterns

- Assuming continuous hedging is achievable.
- Ignoring the cost of the rehedges in the position's economics.
- Reporting delta-neutral without the vega.
- Estimating hedge cost at the tightest observed spread.
- Assuming a delta hedge protects against a gap.

## Done checklist

- [ ] Delta and rehedge rule recorded.
- [ ] Rehedge count estimated.
- [ ] Hedge cost computed.
- [ ] Vega and offsets recorded.
- [ ] Implied versus realised compared.
- [ ] Gap assumption recorded.

The practical consequence is that the hedging regime, not the model, determines the result: two traders with the same option and the same view can earn different amounts depending on when they rehedge, and the record should state the regime so the outcome can be attributed to it rather than to the market alone.


## Sources

- Foreign exchange market structure: <https://www.bis.org/>
- Market rates and volatility data: <https://www.federalreserve.gov/>
- Volatility series: <https://fred.stlouisfed.org/>
