---
name: yield-curve
domain: investing/yield-curve
trigger: "Reading a yield curve's shape and stating what it does and does not signal."
anti_trigger: "Not for rate forecasting, and not for bond selection."
scope: "Curve shapes, what they have historically signalled, and the limits of the signal."
status: seedling
---

# Yield curve

## Standard

The yield curve plots yield against maturity. Its shape carries information about expectations and about the premium investors demand for holding longer maturities, and those two components are entangled: a flat curve can mean expectations of falling rates, a small term premium, or both. Reading the curve means being explicit about which interpretation is being used.

The inversion signal deserves its reputation and its caveats. An inverted curve has preceded several recessions with long and variable lags, and it has also produced false positives. The honest statement is that inversion is a signal with a lead time measured in quarters and a non-trivial error rate, and that its mechanism is disputed.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- State the maturities used and the source of the yields.
- Decompose the shape into expectations and term premium where data permits, or say that it cannot be decomposed.
- Inversion is reported with its historical lead time and error rate, not as a prediction.
- Curve changes are compared over a stated window; day-to-day moves are noise.
- The shape is recorded alongside the level; a curve can be steep at low yields or flat at high ones.
- Any portfolio action attributed to the curve is recorded with its reasoning.

## Procedure

1. Pull yields at the standard maturities from a single dated source.
2. Compute the spreads that define the shape: short versus long, and the belly.
3. Classify the shape: steep, flat, inverted, humped.
4. Compare with the same spreads six and twelve months earlier.
5. State the interpretation and the alternative interpretation.
6. Record the shape, the spreads, and the interpretation with its limits.

## Anti-patterns

- Calling an inversion a recession call.
- Mixing yields from different dates or sources.
- Reading a single day's move as a shape change.
- Ignoring the term premium when interpreting a flat curve.
- Using the curve to justify a trade without recording the reasoning.

## Done checklist

- [ ] Yields pulled from one dated source at standard maturities.
- [ ] Shape spreads computed.
- [ ] Shape classified.
- [ ] Comparison with six and twelve months earlier.
- [ ] Interpretation and alternative both stated.
- [ ] Record kept with limits.

## Sources

- Treasury yield-curve data: <https://fred.stlouisfed.org/>
- Investor education on interest rates: <https://www.investor.gov/introduction-investing>
- Regulatory context for rate disclosures: <https://www.sec.gov/investor>
