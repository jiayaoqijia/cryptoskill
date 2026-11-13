---
name: cost-drivers-at-scale
domain: software-engineering/cost-drivers-at-scale
trigger: "Working out which cost will dominate as volume grows."
anti_trigger: "Not for pricing negotiation, and not for capacity measurement."
scope: "What dominates as volume grows, and what does not."
status: seedling
---

# Cost drivers at scale

## Standard

Cost components scale differently, and the one that dominates at a thousand requests is rarely the one that dominates at a million. Compute is roughly linear in requests; storage is linear in retained data and grows monotonically unless something deletes it; egress is linear in bytes transferred and is often the largest line for data-heavy systems; and per-request managed services are linear in calls but with a fixed price floor that makes them expensive at low volume and cheap at high.

The engineering decision follows from which term dominates. A system whose cost is dominated by storage should delete and tier; one dominated by egress should cache at the edge and reduce payloads; one dominated by per-request charges should batch. Optimising the term that is not dominant produces effort without effect, which is why the breakdown precedes the intervention.

Primary sources: <https://www.finops.org/> and <https://www.cncf.io/>.

## Decision rules

- Record the cost breakdown by component at the current volume.
- Record the scaling exponent assumed for each component: linear, sublinear, or superlinear.
- Record which component dominates at ten times the current volume, extrapolated.
- Record the fixed-cost floors that make a component disproportionately expensive at low volume.
- Record the components that grow monotonically without a deletion policy.
- Record the intervention and the component it targets, so effort matches the dominant term.

## Procedure

1. Break the bill down by component.
2. Record each component's current cost and its volume driver.
3. Extrapolate to a higher volume and record which dominates.
4. Identify components with no deletion policy and their growth.
5. Choose the intervention that targets the dominant term.
6. Record the expected effect and measure it after.

## Anti-patterns

- Optimising compute when storage dominates.
- Assuming all components scale linearly.
- Ignoring egress because it is not on the compute invoice.
- Leaving a component with no retention policy and expecting its cost to be stable.
- Intervening before the breakdown is known.

## Done checklist

- [ ] Breakdown by component recorded.
- [ ] Scaling behaviour recorded per component.
- [ ] Dominant term at higher volume extrapolated.
- [ ] Fixed-cost floors recorded.
- [ ] Monotonic growth identified.
- [ ] Intervention targeted and effect measured.

The extrapolation should be stated with its assumption, because the exponent is a guess: a component assumed linear that is actually superlinear will dominate sooner than the model says, and recording the assumption lets the estimate be corrected when the first data point at higher volume arrives.


## Sources

- FinOps cost optimisation guidance: <https://www.finops.org/>
- Cloud native efficiency practice: <https://www.cncf.io/>
- Data transfer and peering reference: <https://www.ietf.org/>
