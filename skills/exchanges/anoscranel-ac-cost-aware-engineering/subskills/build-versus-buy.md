---
name: build-versus-buy
domain: software-engineering/build-versus-buy
trigger: "Deciding whether to build a component or pay for a managed one."
anti_trigger: "Not for vendor selection, and not for procurement."
scope: "The volume at which building beats buying, and the costs both hide."
status: seedling
---

# Build versus buy

## Standard

A managed service has a price per unit that is high relative to the raw infrastructure it runs on, and that margin buys operational work the team does not do. Building replaces the margin with engineering time and operational burden, and the comparison is only meaningful when both sides are counted in the same units over the same horizon.

The crossover is a volume, and it is usually higher than intuition suggests. A component that costs a month of engineering to build and a fraction of a person to operate needs a sustained volume before its infrastructure saving exceeds the managed price plus the opportunity cost of the engineer. Below that volume, building is a way of spending an engineer to save money the business did not need to save.

Primary sources: <https://www.finops.org/> and <https://martinfowler.com/>.

## Decision rules

- Record the managed cost at current volume and at a projected volume.
- Record the build cost: engineering time, opportunity cost, and ongoing operations.
- Record the operational burden honestly, including on-call and upgrade cycles.
- Record the crossover volume and the time to reach it.
- Record what the team would not build if it built this.
- Record the exit cost: what migrating back would take if the build underdelivers.

## Procedure

1. Record the managed cost at two volumes.
2. Estimate build time and record the opportunity cost.
3. Estimate ongoing operational burden and record it.
4. Compute the crossover volume and the time to reach it.
5. Record what is displaced by the build.
6. Record the exit path and its cost.

## Anti-patterns

- Comparing the managed price with raw compute and ignoring operations.
- Counting engineering time at zero because the team is salaried.
- Assuming the build stops costing after launch.
- Ignoring what will not be built while the component is built.
- No exit path, so a failed build becomes permanent.

## Done checklist

- [ ] Managed cost at two volumes recorded.
- [ ] Build time and opportunity cost recorded.
- [ ] Operational burden recorded.
- [ ] Crossover volume and timeline recorded.
- [ ] Displaced work recorded.
- [ ] Exit path recorded.

The build's hidden cost is the upgrade: a managed service carries compatibility work that a built component inherits, and a component built once and never upgraded becomes a liability whose replacement cost is the build repeated. Recording who owns the upgrade cadence is part of costing the build honestly.


## Sources

- FinOps build versus buy guidance: <https://www.finops.org/>
- Architecture decision practice: <https://martinfowler.com/>
- Cloud native service guidance: <https://www.cncf.io/>
