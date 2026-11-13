---
name: commodity-option-hedging
domain: investing/commodity-option-hedging
trigger: "Hedging a physical commodity exposure with options."
anti_trigger: "Not for predicting prices, and not for hedge accounting."
scope: "Hedging a physical exposure with options, and what the hedge does not cover."
status: seedling
---

# Commodity option hedging

## Standard

A physical exposure has three dimensions: volume, timing, and basis. An option hedge can address the price dimension and, with an average structure, part of the timing, but it does not address volume, which is uncertain for a producer, nor basis, which is the difference between the local physical price and the futures price the option settles against.

That is why a hedged physical position can still lose money. If the local basis moves against the hedger, the hedge offsets the futures move and leaves the basis loss exposed. The record should quantify the basis risk separately and state what part of the exposure remains unhedged, rather than reporting the position as hedged on the strength of the option's notional.

Primary sources: <https://www.cftc.gov/> and <https://www.eia.gov/>.

## Decision rules

- Record the physical exposure: volume, timing, location, and quality.
- Record the option hedge: strike, expiry, and the future it settles against.
- Record the basis between the local physical price and the futures price.
- Record the volume uncertainty and how the hedge handles it.
- Record the cost of the hedge against the value of the protection.
- Record the residual exposure explicitly, including basis and volume.

## Procedure

1. Record the physical exposure in its three dimensions.
2. Select the hedge instrument and record its terms.
3. Compute the hedge ratio against volume and timing.
4. Quantify the historical basis range.
5. Compute the hedge cost per unit protected.
6. Write the hedge summary with residuals named.

## Anti-patterns

- Calling a position hedged when basis is unhedged.
- Hedging a volume that does not materialise.
- Using a futures contract for a different delivery point without the basis.
- Ignoring the cost of the option relative to the protection.
- Assuming the hedge covers quality differences.

## Done checklist

- [ ] Physical exposure recorded in three dimensions.
- [ ] Hedge instrument recorded.
- [ ] Hedge ratio computed.
- [ ] Basis range quantified.
- [ ] Cost per unit computed.
- [ ] Residuals named.

The hedge ratio also drifts with the hedge itself: as the option moves in or out of the money, its delta changes, and a physical position hedged once at inception becomes under- or over-hedged as the market moves, which is why the record carries a rehedging rule rather than a single ratio.


## Sources

- Regulatory guidance on hedging: <https://www.cftc.gov/>
- Energy and physical market data: <https://www.eia.gov/>
- Agricultural data: <https://www.usda.gov/>
