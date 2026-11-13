---
name: curve-shape
domain: investing/curve-shape
trigger: "Reading the shape of one issuer's credit curve."
anti_trigger: "Not for predicting defaults, and not for the risk-free curve."
scope: "Slope, curvature, and what each shape is saying."
status: seedling
---

# Curve shape

## Standard

The credit curve is quoted as spreads at standard maturities, and its shape is described by the slope between two points and the curvature across three. An upward slope is the normal state: longer maturities carry more uncertainty, less liquidity, and a larger liquidity premium, so spreads widen with tenor.

Deviations carry the information. A flat curve says the market prices the same risk at every horizon, which is unusual and usually reflects a strong view about near-term events. A steep front end with a flat back end suggests a specific near-term concern that resolves. Inversion says the opposite: near-term risk exceeds long-term risk, which happens when default or restructuring is considered plausible within a short window.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the quoted points and the maturities they represent.
- Record the slope between the standard pairs and its change over time.
- Record the curvature across three points where the curve is quoted.
- Record the shape's historical range for this issuer and for peers.
- Record whether a segment is interpolated rather than quoted.
- Record the shape in one sentence, without interpretation.

## Procedure

1. Collect the quoted spreads by maturity.
2. Compute slopes for the standard pairs.
3. Compute curvature across three points.
4. Compare with the issuer's own history.
5. Note interpolated segments.
6. Write the shape description.

## Anti-patterns

- Reading a shape from two points when a third contradicts it.
- Treating an interpolated segment as a quoted one.
- Comparing shapes across issuers with different quoting conventions.
- Interpreting the shape before describing it.
- Ignoring a stale quote at one maturity.

## Done checklist

- [ ] Points and maturities recorded.
- [ ] Slopes computed.
- [ ] Curvature computed.
- [ ] History compared.
- [ ] Interpolation noted.
- [ ] Shape described.

A further observation worth recording is the curve's stability rather than only its level: a shape that has been unchanged for months tells a different story from one that moved sharply last week even if both describe the same slope, because the first is a settled market view and the second is a repricing in progress.


The comparison across time is what turns a description into evidence: a slope that has widened while the issuer's rating is unchanged is a market view forming, while a slope that has widened alongside a downgrade is the market catching up.


## Sources

- Credit derivatives conventions: <https://www.isda.org/>
- Market and credit data: <https://www.federalreserve.gov/>
- Spread series: <https://fred.stlouisfed.org/>
