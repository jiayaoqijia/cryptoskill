---
name: rounding-modes
domain: software-engineering/rounding-modes
trigger: "Choosing and applying a rounding mode for a monetary operation."
anti_trigger: "Not for tax or accounting policy, and not for display formatting alone."
scope: "Half-up, half-even, and truncation, and where each belongs."
status: seedling
---

# Rounding modes

## Standard

Rounding a monetary amount is a policy choice, and the modes differ in a way that becomes visible only in aggregate. Half-up pushes every exact half away from zero, so a large number of such amounts drifts consistently upward. Half-even, sometimes called banker's rounding, alternates in the long run and is the conventional choice where an unbiased aggregate matters.

The second decision is where rounding happens. Rounding at every intermediate step accumulates a bias that rounding once at the end does not, and the reverse is also true for a chain of divisions. The record states the mode and the step at which it is applied, because the same mode applied at different points produces different totals.

Primary sources: <https://www.iso.org/> and <https://www.iso20022.org/>.

## Decision rules

- Record the rounding mode per operation, not globally, since the appropriate choice varies.
- Record the step at which rounding is applied in a multi-step calculation.
- Record whether the mode is half-up, half-even, toward zero, or another.
- Record the statutory basis where a regulation specifies the mode.
- Record the display rounding separately from the calculation rounding.
- Record the aggregate bias the chosen mode produces over a volume.

## Procedure

1. Identify each operation that requires rounding.
2. Choose a mode and record the reasoning or the statutory basis.
3. Record the step at which rounding is applied.
4. Separate display rounding from calculation rounding.
5. Estimate the aggregate bias over a representative volume.
6. Test the extremes: exact half values, negative values, and zero.

## Anti-patterns

- Applying one mode everywhere because it is the default.
- Rounding at every intermediate step without recording it.
- Using display formatting as the calculation's rounding.
- Assuming half-up and half-even agree in aggregate.
- Testing only positive, non-half values.

## Done checklist

- [ ] Mode recorded per operation.
- [ ] Rounding step recorded.
- [ ] Statutory basis recorded where applicable.
- [ ] Display and calculation separated.
- [ ] Aggregate bias estimated.
- [ ] Extremes tested.

The half-even choice deserves its explanation because it looks arbitrary to anyone who has not met it: the alternation is what keeps a large number of exact halves from drifting in one direction, and a team that switches to half-up for intuitive reasons reintroduces a bias that appears only in the aggregate and only after volume.


## Sources

- Currency and numeric representation standards: <https://www.iso.org/>
- Payment messaging standards: <https://www.iso20022.org/>
- Financial reporting standards: <https://www.ifrs.org/>
