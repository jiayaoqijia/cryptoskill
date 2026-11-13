---
name: trigger-design
domain: investing/trigger-design
trigger: "Comparing catastrophe bond triggers and the basis risk each carries."
anti_trigger: "Not for predicting events, and not for recommending a bond."
scope: "Indemnity, industry loss, parametric, and modelled loss triggers."
status: seedling
---

# Trigger design

## Standard

An indemnity trigger pays on the sponsor's actual losses, which means the investor bears the sponsor's loss experience rather than the market's, and the sponsor has an incentive to settle claims accurately. An industry loss trigger pays when an index of insured losses across the industry exceeds a threshold, which removes the sponsor-specific risk but introduces basis risk: the index can fall short of the threshold while the sponsor's own losses are large, and the reverse.

Parametric triggers pay on a physical measurement — wind speed at a location, ground acceleration, rainfall — and settle quickly and objectively, at the cost of basis risk against the actual damage. Modelled loss triggers use a model to estimate industry loss from an event's parameters, which sits between the two. The record should state which design is in use and what the investor is actually exposed to, because the peril may be identical while the risk is not.

Primary sources: <https://www.sec.gov/investor> and <https://www.artemis.bm/>.

## Decision rules

- Record the trigger type and the reference used: sponsor loss, index, or measurement.
- Record the threshold, the attachment and exhaustion points, and the payout formula.
- Record the basis risk in both directions: trigger without loss, and loss without trigger.
- Record who calculates the index or measurement and how disputes resolve.
- Record the reset or extension provisions.
- Record the historical instances where the trigger and the actual loss diverged.

## Procedure

1. Identify the trigger type and reference.
2. Record thresholds and payout formula.
3. Record the calculation agent and dispute mechanism.
4. Assess basis risk in both directions.
5. Record reset and extension terms.
6. Write the trigger summary with its basis risk named.

## Anti-patterns

- Treating all cat bonds on the same peril as equivalent.
- Ignoring the basis risk direction that disadvantages the investor.
- Assuming the index is independent of the sponsor's book.
- Overlooking reset provisions that extend exposure.
- Reading the trigger without the payout formula.

## Done checklist

- [ ] Trigger type and reference recorded.
- [ ] Thresholds and formula recorded.
- [ ] Calculation agent recorded.
- [ ] Basis risk both directions recorded.
- [ ] Reset terms recorded.
- [ ] Divergence history recorded.

The basis risk that matters for a holder is the direction that produces a loss without a payout: an indemnity trigger protects the sponsor precisely, while an index trigger can leave the investor paid in full on an event that devastated the sponsor's book, and the reverse case is a payout the investor makes for an event that caused no insured loss at all.

## Sources

- Catastrophe bond disclosure: <https://www.sec.gov/investor>
- Insurance-linked securities market data: <https://www.artemis.bm/>
- Investor education on complex instruments: <https://www.investor.gov/introduction-investing>
