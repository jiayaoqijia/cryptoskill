---
name: index-inclusion-flows
domain: investing/index-inclusion-flows
trigger: "Anticipating the flows an index inclusion or exclusion creates."
anti_trigger: "Not for predicting index decisions, and not for the equity case."
scope: "Inclusion, exclusion, and the flow they create."
status: seedling
---

# Index inclusion flows

## Standard

When a market is added to a major index, or a security is added to an existing one, the funds that track the index must buy. The flow is disclosed in advance, it arrives in a narrow window around the effective date, and its size can be estimated from the index's assets and the security's weight. That predictability is what makes the event tradable and what makes it crowded.

The anticipation is the complication. A widely expected inclusion is partly priced before the announcement, and the flow at the effective date can be smaller than the estimate because funds pre-position or because the rebalancing is executed over several days. A study of the event that starts at the announcement misses the part that already happened.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the index, the announcement date, and the effective date.
- Record the estimated flow from index assets and the security's weight.
- Record the market's history with comparable inclusions and their price behaviour.
- Record how much of the flow is likely pre-positioned.
- Record the methodology's buffer or ranking rule that determined inclusion.
- Record the reverse event: what an exclusion would force.

## Procedure

1. Record the index and the event dates.
2. Estimate the flow from index size and weight.
3. Record comparable inclusion behaviour.
4. Assess pre-positioning.
5. Record the methodology's rule.
6. Write the flow analysis with the estimate and its uncertainty.

## Anti-patterns

- Estimating the flow without the index's asset base.
- Measuring the effect from the announcement date only.
- Assuming all tracking funds trade at the effective date.
- Ignoring buffer rules that make inclusion predictable in advance.
- Treating the estimate as a forecast of the price.

## Done checklist

- [ ] Index and dates recorded.
- [ ] Flow estimated.
- [ ] Comparable behaviour recorded.
- [ ] Pre-positioning assessed.
- [ ] Methodology rule recorded.
- [ ] Analysis written with uncertainty.

The flow estimate also depends on which funds actually track the index: an index used mainly by active managers to define a benchmark has far less passive money behind it than one used by large passive funds, and the same announcement can produce a fraction of the flow the index's stated assets imply. Recording the composition of the tracking base is what separates a plausible estimate from a wishful one.


## Sources

- Index event disclosure: <https://www.sec.gov/investor>
- Index methodology standards: <https://www.cfainstitute.org/>
- Fund flow context: <https://www.imf.org/>
