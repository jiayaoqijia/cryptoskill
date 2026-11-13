---
name: currency-access-and-cost
domain: investing/currency-access-and-cost
trigger: "Working out how to obtain an emerging market currency and what it costs."
anti_trigger: "Not for forecasting the currency, and not for hedging policy."
scope: "Onshore versus offshore currency, and what access costs."
status: seedling
---

# Currency access and cost

## Standard

An emerging market currency may trade in two forms. The onshore market is subject to local rules and is available to registered participants; the offshore market, usually a deliverable or non-deliverable forward market, is available to others at a different price. The gap between the two is a measure of the cost of access, and it widens when capital is leaving.

The cost of converting is more than the spot rate. The bid-offer in the currency pair, the forward points reflecting the interest differential, and any regulatory cost of using the onshore market all add. For an investor whose return is denominated in a hard currency, the forward points are often the largest component and the one most often left out of a return comparison.

Primary sources: <https://www.imf.org/> and <https://www.bis.org/>.

## Decision rules

- Record whether the exposure uses onshore or offshore currency.
- Record the spot bid-offer and its typical range.
- Record the forward points and the interest differential they imply.
- Record the gap between onshore and offshore prices where both exist.
- Record the regulatory cost or restriction attached to onshore access.
- Record the total conversion cost for a round trip.

## Procedure

1. Record the market used and its accessibility.
2. Record the spot spread.
3. Record forward points and the implied differential.
4. Record the onshore-offshore gap.
5. Compute the round-trip cost.
6. Write the currency access summary.

## Anti-patterns

- Comparing returns without the forward points.
- Assuming the offshore rate is available at size.
- Ignoring the regulatory cost of onshore access.
- Using a spot rate sampled at an illiquid hour.
- Treating a non-deliverable forward as equivalent to a deliverable one.

## Done checklist

- [ ] Market and access recorded.
- [ ] Spot spread recorded.
- [ ] Forward points recorded.
- [ ] Onshore-offshore gap recorded.
- [ ] Round-trip cost computed.
- [ ] Summary written.

The non-deliverable forward deserves separate attention: it settles in a hard currency against a fixing rather than delivering the local currency, so it provides the exposure without the ability to hold the currency, and its price embeds the market's view of the convertibility risk. A position hedged with an NDF has not removed the convertibility risk; it has priced it.


The comparison that makes the cost legible is against the exposure's expected return: a round-trip conversion cost of two percent on an allocation held for a year consumes a substantial share of a plausible equity return, while the same cost on a multi-year holding is trivial. Recording the cost against the intended holding period is what turns an operational charge into an allocation decision.


## Sources

- Currency market structure: <https://www.bis.org/>
- Cross-border flow data: <https://www.imf.org/>
- Rate and exchange data: <https://fred.stlouisfed.org/>
