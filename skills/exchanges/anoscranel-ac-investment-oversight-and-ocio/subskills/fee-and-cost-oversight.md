---
name: fee-and-cost-oversight
domain: investing/fee-and-cost-oversight
trigger: "Verifying what delegation actually costs, line by line."
anti_trigger: "Not for negotiating fees, and not for fund selection."
scope: "Verifying fees, offsets, and the total cost of delegation."
status: seedling
---

# Fee and cost oversight

## Standard

The fee a delegator pays is rarely the fee it agreed. Management fees are quoted, then offset by agreements that cap the total, then supplemented by fees earned at the underlying level, then adjusted by rebates and by performance terms. The total cost of delegation is the sum of those layers, and verifying it means reconciling the invoice against the agreement rather than reading the schedule.

The check that catches most errors is arithmetic: compute the fee from the agreed basis and the actual assets, then compare it with what was charged. Discrepancies tend to be small in percentage terms and consistent in direction, which is why they survive for years; a reconciliation performed annually with the calculation shown is the only reliable control.

Primary sources: <https://www.cfainstitute.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record each fee layer: management, performance, underlying fund fees, custody, and administration.
- Record the basis for each and the assets it applies to.
- Record offsets, caps, and rebates, and how they interact.
- Recompute the fee from the agreement and compare with the invoice.
- Record the underlying fund fees the provider earns or shares.
- Record any fee change and its effective date.

## Procedure

1. Record each fee layer and its basis.
2. Recompute the fee from the agreement.
3. Compare the calculation with the invoice.
4. Reconcile offsets and caps.
5. Record underlying fees and sharing arrangements.
6. Write the reconciliation with any variance noted.

## Anti-patterns

- Accepting an invoice because the percentage looks right.
- Ignoring fees earned at the underlying level.
- Overlooking how offsets and caps interact.
- Treating a rebate as a reduction in total cost when it is a timing adjustment.
- Reconciling once at inception and never again.

## Done checklist

- [ ] Fee layers recorded.
- [ ] Bases recorded.
- [ ] Offsets and caps recorded.
- [ ] Fee recomputed and compared.
- [ ] Underlying fees recorded.
- [ ] Variance noted with its direction.

The variance that is worth escalating is not the largest in currency but the one that is systematic: a small consistent overcharge indicates a basis error that will repeat every period, while a larger one-off usually indicates a timing difference that will reverse, and the two call for different responses.

Recording the reconciliation method itself, not only its outcome, is what allows a successor to repeat it: a file that says the fee was verified this year tells a reader nothing about how, while one that records the basis, the assets, and the arithmetic can be re-run when the agreement changes.

## Sources

- Investment management standards: <https://www.cfainstitute.org/>
- Fee disclosure requirements: <https://www.sec.gov/investor>
- Investor guidance on costs: <https://www.investor.gov/introduction-investing>
