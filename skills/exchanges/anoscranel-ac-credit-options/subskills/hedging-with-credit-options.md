---
name: hedging-with-credit-options
domain: investing/hedging-with-credit-options
trigger: "Hedging credit exposure with options rather than with CDS."
anti_trigger: "Not for predicting defaults, and not for credit analysis."
scope: "Vega and spread DV01, and what a delta hedge in credit does not cover."
status: seedling
---

# Hedging with credit options

## Standard

A credit option hedge differs from a CDS hedge in what it leaves exposed. Buying protection with a CDS removes spread risk linearly; buying a payer option removes it below the strike and leaves the position exposed to the premium paid and to the passage of time. The choice between them is a choice about which risk to keep, not about which is cheaper.

The greeks are the same in name and different in behaviour. Delta in credit is spread DV01, vega is sensitivity to spread volatility, and the two interact through the recovery assumption. A hedge that matches DV01 at inception drifts as spreads move, and a hedge that matches vega in one expiry leaves the term structure exposed in the others.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the exposure being hedged and its spread DV01.
- Record the hedge instrument: CDS, option, or index.
- Record the hedge ratio in spread DV01 and the residual after the hedge.
- Record the vega left exposed and the expiries it sits in.
- Record the cost of the hedge against the protection it provides.
- Record the scenario in which the hedge fails, such as a jump to default.

## Procedure

1. Compute the exposure's spread DV01.
2. Choose the hedge instrument and record why.
3. Compute the ratio and the residual.
4. Record vega and its expiry distribution.
5. Compute cost per unit of protection.
6. Write the hedge summary with its failure scenario.

## Anti-patterns

- Assuming an option hedge removes the same risk as a CDS.
- Matching DV01 and ignoring vega.
- Ignoring the premium's cost in the hedge's economics.
- Assuming a hedge covers a jump to default.
- Leaving the residual unrecorded.

## Done checklist

- [ ] Exposure and DV01 recorded.
- [ ] Instrument chosen and justified.
- [ ] Ratio and residual recorded.
- [ ] Vega recorded by expiry.
- [ ] Cost computed.
- [ ] Failure scenario written.

The hedge also changes the position's behaviour in a default: a CDS hedge pays out on the event, while an option hedge pays only if the option is in the money and only up to its notional, so a jump to default can leave the hedged position with a loss the hedge was never designed to cover. That difference is not a detail of sizing; it is a difference in what the hedge is for, and the record should state which risk it is meant to remove.

## Sources

- Credit derivatives standards: <https://www.isda.org/>
- Market and credit data: <https://www.federalreserve.gov/>
- Spread series: <https://fred.stlouisfed.org/>
