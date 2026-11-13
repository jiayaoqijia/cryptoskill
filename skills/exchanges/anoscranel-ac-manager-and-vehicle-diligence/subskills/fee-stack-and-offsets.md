---
name: fee-stack-and-offsets
domain: investing/fee-stack-and-offsets
trigger: "Computing what a manager actually costs after offsets and expenses."
anti_trigger: "Not for comparing fund vehicles, and not for predicting returns."
scope: "Management fees, performance fees, and the offsets that reduce them."
status: seedling
---

# Fee stack and offsets

## Standard

The management fee is the visible cost; the performance fee is the conditional one; and the expenses charged to the vehicle are the ones that are neither. Together they form a stack that compounds against the allocator, and the offsets — provisions that reduce the management fee by some portion of fees the manager earns elsewhere, such as monitoring or transaction fees — determine how much of that stack is actually paid.

Reading the stack means modelling it at a stated return rather than quoting its components. A two and twenty structure at a ten percent gross return costs a very different fraction of the net return than the same structure at a five percent return, because the performance fee is calculated on a smaller base while the management fee is not. The record states the all-in cost at two or three return levels.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the management fee, its base, and whether it is charged on committed or invested capital.
- Record the performance fee, the hurdle, the high-water mark, and the crystallisation frequency.
- Record the expenses charged to the vehicle, with the caps where they exist.
- Record every offset and its basis: monitoring fees, transaction fees, and any rebate.
- Compute the all-in cost at two or three gross return levels.
- Record the fee terms relative to comparable vehicles.

## Procedure

1. Record the fee and expense terms.
2. Record offsets and their calculation.
3. Model the all-in cost at low, mid, and high returns.
4. Compute the net return at each level.
5. Compare the terms with comparable vehicles.
6. Write the cost analysis with the assumptions.

## Anti-patterns

- Quoting a management fee as the cost of the vehicle.
- Ignoring expenses that sit outside the management fee.
- Assuming an offset is 100 percent when it is partial.
- Comparing fee levels without the return assumption.
- Overlooking a high-water mark that resets on a schedule.

## Done checklist

- [ ] Fee terms recorded.
- [ ] Expense terms recorded.
- [ ] Offsets recorded.
- [ ] All-in cost modelled at three returns.
- [ ] Net returns computed.
- [ ] Comparison made.

The compounding matters more than the level: a two percent management fee and a twenty percent performance fee at a seven percent gross return leaves the allocator with roughly five and a half percent, so the fee has consumed over a fifth of the gross return before any consideration of risk. Computing that fraction at the allocator's own return expectation is what turns a fee schedule into a decision.

## Sources

- Fund fee disclosure: <https://www.sec.gov/investor>
- Investment management standards: <https://www.cfainstitute.org/>
- Fund governance research: <https://www.nber.org/>
