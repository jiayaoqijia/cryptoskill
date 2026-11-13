---
name: volume-profile-and-vwap
domain: investing/volume-profile-and-vwap
trigger: "Reading where volume traded and the footprint of a benchmarked order."
anti_trigger: "Not for predicting direction, and not for identifying the participant."
scope: "Where volume traded, VWAP bands, and the footprint of a benchmarked order."
status: seedling
---

# Volume profile and VWAP

## Standard

A volume profile plots how much traded at each price, which shows where the market accepted value and where it moved through quickly. A large concentration at a level that later holds on retest is evidence that a substantial participant transacted there; a thin band that the price crossed in minutes is evidence that nobody did. The profile is a description of acceptance rather than a forecast.

VWAP is the average price at which the day's volume traded, and orders benchmarked to it leave a footprint: volume arriving steadily through the session rather than clustered at the open and close, and a tendency for the price to revert toward the running average. A scheduled order that must finish by the close produces a pattern, and the pattern is visible in the intraday volume distribution.

Primary sources: <https://www.finra.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the profile's resolution and the session used.
- Record the high-volume levels and whether they held on retest.
- Record the intraday volume distribution against the name's baseline shape.
- Record the deviation of the price from the running VWAP through the session.
- Record whether the pattern is consistent with a scheduled order or with opportunistic flow.
- Record the alternative explanation: an event, an expiry, or a rebalance.

## Procedure

1. Build the profile at a stated resolution.
2. Identify high-volume levels and their retest behaviour.
3. Compare the intraday volume shape with the baseline.
4. Compute the price's deviation from running VWAP.
5. Assess consistency with a benchmarked order.
6. Write the observation with alternatives.

## Anti-patterns

- Reading a volume profile as support and resistance without the retest evidence.
- Treating VWAP as a prediction of the close.
- Ignoring the name's normal intraday shape.
- Assuming scheduled execution from steady volume alone.
- Missing an event that explains the distribution.

## Done checklist

- [ ] Resolution and session recorded.
- [ ] High-volume levels recorded.
- [ ] Retest behaviour recorded.
- [ ] Volume shape against baseline recorded.
- [ ] VWAP deviation recorded.
- [ ] Alternatives recorded.

The profile's other use is comparative: the same name's profile from a month earlier shows whether value has migrated to a new level, which is a slower and more reliable observation than anything a single session can provide. Migration of the high-volume node is evidence that the market's accepted price has changed, and it survives the noise that a single day's prints contain.


## Sources

- Trading and execution guidance: <https://www.finra.org/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on trading volume: <https://www.investor.gov/introduction-investing>
