---
name: inclusion-arbitrage
domain: investing/inclusion-arbitrage
trigger: "Assessing the trade created by known inclusion or deletion rules."
anti_trigger: "Not for predicting index decisions, and not for deal advice."
scope: "The trade created by rules that are known in advance."
status: seedling
---

# Inclusion arbitrage

## Standard

Index rules are published, so a security's likely inclusion or deletion can be anticipated from the rules and the data. Tracking funds must then transact on the effective date, which creates a flow whose size can be estimated from the index weight and the assets following it. That combination — a predictable flow at a known date — is the basis of index arbitrage.

The opportunity is limited by its own visibility. The estimate carries error, the market anticipates the flow, and the effect on the price is largest in the announcement window rather than the effective date. The record should state the estimated flow, the anticipated portion, and the cost of being wrong about the decision itself, since a rule-based prediction can fail when the committee exercises discretion.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the rule and the data point that would trigger inclusion or deletion.
- Record the announcement date and the effective date.
- Estimate the flow from the index weight and the tracked assets.
- Record the error band and the assumptions behind the estimate.
- Record how much of the flow is likely already priced.
- Record the discretion the decision-making body retains.

## Procedure

1. Test the security against the published rules.
2. Record the announcement and effective dates.
3. Estimate the flow and its error band.
4. Assess the anticipated portion.
5. Record the discretion risk.
6. Write the estimate with its limits.

## Anti-patterns

- Treating a rule-based prediction as a decision.
- Quoting a flow without an error band.
- Ignoring the announcement window in favour of the effective date.
- Assuming the tracked assets are known precisely.
- Sizing for the flow as if the decision were certain.

## Done checklist

- [ ] Rule and trigger recorded.
- [ ] Dates recorded.
- [ ] Flow estimated with error band.
- [ ] Anticipation assessed.
- [ ] Discretion recorded.
- [ ] Limits stated.

Recording the discretion is the field that keeps the estimate honest: an index committee that has deviated from its rules in the past makes a rule-based prediction weaker, and the same flow estimate carries very different confidence depending on that history.


The cost of being wrong about the decision is asymmetric in a way worth recording: a security that is not added returns to its pre-anticipation price, so a position built on the expectation carries a loss that the flow estimate never sized.


## Sources

- Index methodology and announcements: <https://www.investor.gov/introduction-investing>
- Market structure context: <https://www.sec.gov/investor>
- Fund and index data: <https://fred.stlouisfed.org/>
