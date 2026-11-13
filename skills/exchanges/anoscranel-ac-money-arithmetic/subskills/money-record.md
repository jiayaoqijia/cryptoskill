---
name: money-record
domain: software-engineering/money-record
trigger: "Writing the policy that governs monetary representation and rounding."
anti_trigger: "Not for accounting policy, and not for tax advice."
scope: "The written policy: representation, rounding, and tolerance."
status: seedling
---

# Money record

## Standard

The money record states the representation, the rounding mode per operation, the allocation rule, the conversion sequence, and the reconciliation tolerance. It is written before the first ambiguous operation, because a money policy inferred from a codebase after the fact describes what the code does rather than what it should do.

Its second function is to make a discrepancy attributable. When two systems disagree, the record says which rounding points lie between them, which mode each applies, and what bound the arithmetic permits — so the question becomes whether the implementation matches the policy rather than what the policy is.

Primary sources: <https://www.iso.org/> and <https://www.iso20022.org/>.

## Decision rules

- The record states the representation and the minor unit exponent per currency.
- The rounding mode is recorded per operation, with the step at which it applies.
- The allocation rule is recorded with its remainder distribution.
- The conversion sequence and intermediate precision are recorded.
- The reconciliation tolerance is recorded with its derivation.
- The record is append-only; policy changes are dated amendments with the affected systems named.

## Procedure

1. Record the representation and currency exponents.
2. Record the rounding mode and position per operation.
3. Record the allocation and remainders.
4. Record conversion and precision.
5. Record the tolerance and its derivation.
6. Amend on any policy change and name the systems affected.

## Anti-patterns

- A policy written after the discrepancies.
- Recording the mode globally rather than per operation.
- Leaving the allocation rule implicit.
- A tolerance without derivation.
- Changing the policy without naming the systems that must be updated.

## Done checklist

- [ ] Representation and exponents recorded.
- [ ] Rounding per operation recorded.
- [ ] Allocation and remainders recorded.
- [ ] Conversion and precision recorded.
- [ ] Tolerance with derivation recorded.
- [ ] Amendments dated with affected systems.

The record is most useful as a checklist for a new service: a team adding a payment path can read it and discover which rounding mode the platform expects, rather than choosing one and producing the first discrepancy that the reconciliation team then has to attribute.


The amendment discipline matters more here than in most records, because a change in rounding or representation makes prior calculations incomparable rather than wrong: an amount recorded before the change and one after it may both be correct on their own policy and cannot be summed without a conversion that the record should describe.


## Sources

- Currency and numeric standards: <https://www.iso.org/>
- Payment messaging standards: <https://www.iso20022.org/>
- Financial reporting standards: <https://www.ifrs.org/>
