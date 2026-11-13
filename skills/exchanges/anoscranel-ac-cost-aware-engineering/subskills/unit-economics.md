---
name: unit-economics
domain: software-engineering/unit-economics
trigger: "Computing what one request, one tenant, or one action costs."
anti_trigger: "Not for pricing decisions, and not for contract negotiation."
scope: "Cost per request, per tenant, and per unit of business value."
status: seedling
---

# Unit economics

## Standard

A total bill is not an engineering metric: it mixes volume, price, and waste, and it moves for reasons no team controls. The unit cost is the engineering metric — cost per request, per active user, per tenant, per gigabyte stored — because it can be compared across time and across designs while volume changes.

Computing it requires attributing shared costs, which is the hard part. A database serving many services, a cluster running many workloads, and a network path shared by every tenant all have costs that no single unit owns. The allocation rule is a policy, and the record should state it, because two teams using different rules will reach different conclusions about the same system.

Primary sources: <https://www.finops.org/> and <https://www.cncf.io/>.

## Decision rules

- Record the unit chosen and why it reflects the business rather than the infrastructure.
- Record which costs are direct and which are allocated, and the allocation rule.
- Record the unit cost at a stated volume, since fixed costs distort it at low volume.
- Record the trend across periods rather than a single measurement.
- Record the cost of the largest single tenant, which is often disproportionate.
- Record the unit cost of the slowest-growing and fastest-growing segment separately.

## Procedure

1. Choose the unit and record the reasoning.
2. Classify costs as direct or shared, and record the allocation rule.
3. Compute the unit cost at the current volume.
4. Record the trend over several periods.
5. Compute the top tenant's cost and compare it with the average.
6. Record the segments where unit cost is rising.

## Anti-patterns

- Reporting total spend and calling it a cost metric.
- Allocating shared costs by headcount, which bears no relation to consumption.
- Computing unit cost at a volume where fixed costs dominate.
- Comparing unit costs across periods with different allocation rules.
- Ignoring that one tenant can consume a large share of a shared resource.

## Done checklist

- [ ] Unit chosen and justified.
- [ ] Direct and allocated costs separated.
- [ ] Unit cost computed at stated volume.
- [ ] Trend recorded.
- [ ] Top tenant cost recorded.
- [ ] Rising segments identified.

The unit should be chosen so that it cannot be gamed by the team being measured: a cost per deployment rewards deploying less, while a cost per active user measures the thing the business actually pays for, and the difference decides whether the metric improves the system or the reporting.


## Sources

- FinOps practice guidance: <https://www.finops.org/>
- Cloud native cost management: <https://www.cncf.io/>
- Performance and efficiency standards: <https://www.w3.org/>
