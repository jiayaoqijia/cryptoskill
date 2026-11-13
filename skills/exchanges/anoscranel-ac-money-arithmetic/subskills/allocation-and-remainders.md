---
name: allocation-and-remainders
domain: software-engineering/allocation-and-remainders
trigger: "Splitting an amount so that the parts sum to the whole."
anti_trigger: "Not for tax apportionment rules, and not for accounting policy."
scope: "Splitting an amount so the parts sum to the whole."
status: seedling
---

# Allocation and remainders

## Standard

Dividing an amount into equal parts produces a remainder, and how that remainder is distributed determines whether the parts sum to the whole. Rounding each part independently loses or creates units; allocating the remainder to specific parts and reconciling the total preserves it. The second approach is the only one that survives an audit.

The distribution rule is a policy. Giving every remainder unit to the first part biases toward it; distributing them to the largest parts reduces proportional distortion; rotating the recipient across runs distributes the bias over time. Whichever rule is chosen, the invariant is the same: the sum of the allocated parts equals the original amount exactly.

Primary sources: <https://www.iso20022.org/> and <https://www.ifrs.org/>.

## Decision rules

- Record the allocation rule and the reason for choosing it.
- Record the invariant that the parts sum to the whole, and how it is asserted.
- Record the remainder distribution: first parts, largest parts, or rotating.
- Record the behaviour for negative amounts, which reverses the direction of the bias.
- Record the precision of the parts relative to the whole, since more parts mean more remainder.
- Record the test that verifies the invariant across many divisors.

## Procedure

1. Record the allocation rule and the remainder handling.
2. Implement allocation so that the sum is computed and any difference assigned.
3. Assert the invariant in code rather than in a comment.
4. Handle negative amounts and record the direction.
5. Test across divisors including primes and values larger than the amount.
6. Record the maximum remainder observed.

## Anti-patterns

- Rounding each part independently.
- Distributing the remainder to the first part without recording the bias.
- An allocation that fails when the divisor exceeds the amount.
- Ignoring the sign of the amount in the distribution.
- No assertion, so a regression is discovered by a customer.

## Done checklist

- [ ] Allocation rule recorded.
- [ ] Remainder distribution recorded.
- [ ] Invariant asserted in code.
- [ ] Negative handling recorded.
- [ ] Tested across many divisors.
- [ ] Maximum remainder recorded.

The rotation rule is worth considering where the same allocation recurs many times: giving the remainder to the first part every period means the same recipient is advantaged every period, and the bias, though tiny per allocation, becomes a systematic transfer that a counterparty can eventually notice.


## Sources

- Payment and settlement messaging standards: <https://www.iso20022.org/>
- Financial reporting standards: <https://www.ifrs.org/>
- Currency representation standards: <https://www.iso.org/>
