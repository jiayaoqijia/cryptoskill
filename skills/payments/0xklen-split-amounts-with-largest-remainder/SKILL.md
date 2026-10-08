---
name: split-amounts-with-largest-remainder
description: Use when one amount must be divided among N parties (splitting a bill, allocating a discount, distributing a payout). Distributes the indivisible remainder so the parts sum exactly to the total.
---

# Split amounts with the largest remainder

Dividing $10 three ways as `10/3` and rounding each part gives `3.33 * 3 = 9.99` — a cent vanishes. The largest-remainder (Hamilton) method allocates whole minor units so the parts sum exactly to the total.

## Procedure

1. Work in integer minor units. Target `T`, weights `w_i` (equal split means all weights 1).
2. Compute each exact share `s_i = T * w_i / W` where `W = sum(w_i)`, and keep the integer remainder `r_i = (T * w_i) % W`.
3. Give every party `floor(s_i)`.
4. The shortfall is `T - sum(floor(s_i))`, at most `N-1` minor units. Hand one extra unit each to the parties with the largest `r_i`.
5. Break ties deterministically — by party id, not by set/dict iteration order — or the same inputs produce different splits and reconciliations flap.
6. A party with zero weight receives 0 and is excluded from the remainder allocation.
7. Negative totals (refunds) work the same with signs preserved; integer division that truncates toward zero vs toward minus infinity differs, so handle the sign explicitly.
8. Assert the invariant: `assert sum(parts) == T`.
9. Round the weights only if they are fractional; if a weight has sub-unit precision, scale all weights by a common factor first.
10. Expose the remainder-assignment policy (largest-remainder, first-party-takes, round-robin) so the business owns the choice.
11. Persist the split so a later re-sum reproduces the same per-party amounts; recomputing with a different weight order can differ.
12. For a payout, log each party's share and the total so an auditor sees the sum equals the source.
13. Guard the zero total: `T = 0` yields all-zero parts, not a division by zero.

## Pitfalls

- Rounding each part independently with half-up sums to `T ± N/2` cents; the imbalance lands somewhere and someone silently eats it.
- Using float `T / N` and rounding gives an arbitrary residual that differs across languages.
- Tie-breaking by hash or set order makes the split non-reproducible.
- Dumping the whole remainder on the first party concentrates all rounding on one account — fine only if the spec says so.
- Splitting in dollars and converting to cents afterwards loses precision; start and stay in the smallest unit.
- Using a float weight (0.1 for a 10% share) as the multiplier pulls the split back into floating point; store weights as integers.

## Verification

    python3 -c "T=1000; w=[1,1,1]; base=[T*x//sum(w) for x in w]; print(base, T-sum(base))"   # [333,333,333], remainder 1 -> one party takes the extra unit

Pass when a property test asserts `sum(split(T, w)) == T` for random `T` and weights. Report the method, the tie-break key and a sample split.
