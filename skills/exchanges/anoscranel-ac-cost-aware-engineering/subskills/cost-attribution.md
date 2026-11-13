---
name: cost-attribution
domain: software-engineering/cost-attribution
trigger: "Making a cost visible to the team that causes it."
anti_trigger: "Not for budget approval, and not for charging internal customers."
scope: "Tagging, shared-cost allocation, and making a cost visible to its owner."
status: seedling
---

# Cost attribution

## Standard

A cost that nobody sees is a cost that nobody optimises. Attribution is the mechanism that connects a line on the invoice to the person who can change it, and it works only if the mapping is complete: an untagged resource is a cost that belongs to no one, and shared resources are where attribution usually fails.

The engineering is in the tagging discipline and the allocation rule. Tags must be applied by the deployment mechanism rather than by convention, because a convention is followed until someone forgets. Shared costs must be allocated by a rule that reflects consumption, because a rule that reflects headcount or revenue makes the cost invisible to the team that could reduce it.

Primary sources: <https://www.finops.org/> and <https://www.cncf.io/>.

## Decision rules

- Record the tag schema and which tags are mandatory.
- Record where tags are enforced: the deployment template, not the documentation.
- Record the untagged cost and its trend, since that number measures the discipline.
- Record the shared-cost pool and the allocation rule, with its rationale.
- Record the frequency of reporting and to whom it goes.
- Record the resources that cannot be tagged and how they are handled.

## Procedure

1. Define the tag schema and the mandatory keys.
2. Enforce tags in the deployment path and record the rejection behaviour.
3. Measure untagged cost each period and record the trend.
4. Identify shared pools and record the allocation rule.
5. Report per owner on a schedule.
6. Review the rule when the pool's composition changes.

## Anti-patterns

- Tags applied by convention and hoped for.
- Allocating shared cost by headcount or revenue.
- Reporting totals to a central team rather than to the owners.
- Ignoring untagged cost because it is small this month.
- Changing the allocation rule without recording the change, which breaks period comparison.

## Done checklist

- [ ] Tag schema and mandatory keys recorded.
- [ ] Enforcement point recorded.
- [ ] Untagged cost measured with trend.
- [ ] Shared pool and rule recorded.
- [ ] Reporting cadence and recipients recorded.
- [ ] Rule changes recorded.

The untagged number is the most useful figure in the whole exercise precisely because it is uncomfortable: a persistent ten percent untagged is a statement about how the deployment path works, not about one team's carelessness, and it usually points at a resource type that cannot carry tags at all.


## Sources

- FinOps attribution guidance: <https://www.finops.org/>
- Cloud native cost governance: <https://www.cncf.io/>
- Metadata and tagging standards: <https://www.w3.org/>
