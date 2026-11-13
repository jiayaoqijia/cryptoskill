---
name: asset-allocation-policy
domain: investing/asset-allocation-policy
trigger: "Setting target weights and permitted ranges for the policy portfolio."
anti_trigger: "Not for security selection, and not for market timing."
scope: "Target weights and permitted ranges, and the separation of policy from market view."
status: seedling
---

# Asset allocation policy

## Standard

Allocation is the policy decision with the largest effect on outcomes, and the one most easily contaminated by a view about next year. The discipline is to set target weights from the goals and constraints, express them as ranges rather than points, and separate the strategic target from any tactical view by making tactical deviations explicit, bounded, and time-limited.

Ranges exist because rebalancing needs room, and because a range is an honest statement that the right weight is not knowable to the percentage point. A policy with point targets and no bands will be breached constantly, and each breach becomes an ad hoc decision.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.cfainstitute.org/>.

## Decision rules

- Targets derive from the goals, horizon, and binding risk constraint; the derivation is written down.
- Each target carries a range; the range width reflects the tolerance for drift and the cost of rebalancing.
- Tactical views are permitted only within the range, with a stated expiry.
- A view that requires leaving the range is a proposal to change policy, which requires the policy process.
- No target is set to a number that implies a return the plausibility test rejected.
- Ranges are consistent with the constraints register; an instrument class prohibited by constraints gets no target.

## Procedure

1. Derive target weights from the goals and the binding constraint.
2. Set a range per target and explain the width.
3. Check each range against the constraints register.
4. Write the tactical allowance: maximum deviation, expiry, and who may take it.
5. Record the derivation and the assumptions behind the targets.
6. Add the allocation table to the policy statement.

## Anti-patterns

- Setting targets from a forecast of next year's returns.
- Using point targets with no bands.
- Allowing an open-ended tactical view.
- Setting a target in an instrument class the constraints prohibit.
- Changing targets after a market move without a policy review.

## Done checklist

- [ ] Targets derived from goals and constraint, derivation written.
- [ ] Range per target with explained width.
- [ ] Ranges checked against constraints.
- [ ] Tactical allowance bounded and time-limited.
- [ ] Derivation assumptions recorded.
- [ ] Allocation table added to the statement.

## Sources

- Investor education on asset allocation: <https://www.investor.gov/introduction-investing>
- Investment-policy reference material: <https://www.cfainstitute.org/>
- Disclosure context for portfolio policy: <https://www.sec.gov/investor>

The allocation table is the part of the policy most likely to be revised for the wrong reason, because it is the part a market move makes visible. A target should change when the goals or constraints change, and the record should make that distinction explicit by dating the derivation rather than the decision.

