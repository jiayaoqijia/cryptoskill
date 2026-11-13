---
name: environment-cost
domain: software-engineering/environment-cost
trigger: "Keeping the number and size of test environments finite."
anti_trigger: "Not for production capacity planning, and not for cost attribution of features."
scope: "What environments cost and how to keep them finite."
status: seedling
---

# Environment cost

## Standard

Test environments are usually the majority of a non-production infrastructure bill, and the reason is structural: production is one system with a load pattern, while the test estate is many systems with a concurrency pattern — every open change may want its own, every long-lived branch keeps one, and each one left running costs the same per hour whether anyone is using it. The bill is not a property of the application's size but of the estate's width, and the width is what needs managing.

The finite-estate designs follow from that. Preview environments get automatic teardown at merge, and idle previews get the same fate after a stated period, so the estate's size tracks the number of changes in flight. Shared staging gets sized for its actual concurrent users, not for the release-day fantasy of the whole company on it at once, and it gets scaled down out of hours where the work allows. Nothing leaks; and the leaked resource is found by inventory, not by the invoice.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Inventory every environment class with its size, count ceiling, and per-day cost estimate.
- Tie preview lifetime to the merge event, with automatic destruction on merge or abandonment.
- Set an idle-destroy policy for any environment class that can be recreated from definition.
- Size shared staging for measured concurrent use, and record the ceiling that justifies the size.
- Review the environment inventory monthly; unknowns are leaks by definition.
- Compute and report the estate's cost as a per-change figure the team can feel.

## Procedure

1. Inventory environments with size and per-day cost per class.
2. Set count ceilings and idle-destroy policies per class.
3. Wire teardown to merge events for previews.
4. Measure concurrent staging use and resize to it.
5. Sweep the inventory monthly and reconcile against the bill.
6. Publish the per-change environment cost.

## Anti-patterns

- Environments for branches abandoned last year.
- Staging sized by an imagined release-day stampede.
- A bill reviewed quarterly with no inventory to compare it against.
- Teardown wired to success only.
- No per-change cost, so the estate grows without anyone deciding.

## Done checklist

- [ ] Inventory with sizes and ceilings.
- [ ] Teardown automatic and complete.
- [ ] Idle-destroy policies set.
- [ ] Staging resized to measured use.
- [ ] Monthly inventory review.
- [ ] Per-change cost published.

## Sources

- Deployment pipeline environments: <https://martinfowler.com/bliki/DeploymentPipeline.html>
- Immutable and disposable environments: <https://docs.docker.com/>
- Continuous delivery cost practice: <https://martinfowler.com/articles/continuousIntegration.html>
