---
name: data-cost-and-build
domain: investing/data-cost-and-build
trigger: "Deciding whether to buy a dataset or build it."
anti_trigger: "Not for pipeline engineering, and not for procurement."
scope: "Buy versus build, total cost, and the maintenance burden."
status: seedling
---

# Data cost and build

## Standard

Buying a dataset costs a subscription; building one costs engineering, maintenance, and the ongoing attention that keeps a scraper working when a source changes its structure. The comparison is rarely made fairly, because the subscription is a visible line item while the build cost is spread across salaries and incidents.

The maintenance burden is the part most often underestimated. A scraped dataset is a dependency on someone else's website, and every change to that site is an interruption that must be detected and repaired. A licensed dataset moves that burden to the vendor but introduces a dependency on their continued operation and pricing. Either way the record should state the total cost including maintenance, and the failure mode when the source changes.

Primary sources: <https://www.nber.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the subscription cost and its escalation terms.
- Record the build cost: engineering time, infrastructure, and maintenance per year.
- Record the failure modes of each option and their frequency.
- Record the dependency created: a vendor's continuity or a source's stability.
- Record the cost of the alternative if the data becomes unavailable.
- Record the decision and the threshold at which it would be revisited.

## Procedure

1. Estimate the subscription cost over the horizon.
2. Estimate build cost including maintenance.
3. List failure modes for each.
4. Assess the dependency each creates.
5. Compare on total cost over the horizon.
6. Record the decision and its revisit threshold.

## Anti-patterns

- Comparing a subscription with engineering time at zero.
- Ignoring maintenance in the build cost.
- Assuming a source will keep its structure.
- Assuming a vendor will keep its pricing.
- Deciding once and never revisiting.

## Done checklist

- [ ] Subscription cost recorded.
- [ ] Build cost with maintenance recorded.
- [ ] Failure modes listed.
- [ ] Dependencies assessed.
- [ ] Total cost compared.
- [ ] Revisit threshold recorded.

The comparison also depends on the horizon: a build that takes a year to produce a usable dataset is expensive for a short research question and cheap for an indefinitely maintained process, and the same engineering cost is a different decision depending on how long the data will be used.


A third option is often missed: using a public or regulatory dataset that is neither purchased nor built, at the cost of lower resolution, and the record should compare it against the two paid routes rather than leaving it out of the options set.


## Sources

- Research practice on data infrastructure: <https://www.nber.org/>
- Market data context: <https://www.sec.gov/investor>
- Investor education on research costs: <https://www.investor.gov/introduction-investing>
