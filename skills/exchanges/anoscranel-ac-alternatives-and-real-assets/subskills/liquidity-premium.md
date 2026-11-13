---
name: liquidity-premium
domain: investing/liquidity-premium
trigger: "Understanding what the liquidity premium pays and when it does not."
anti_trigger: "Not for pricing an asset, and not for choosing a lockup."
scope: "The premium paid for illiquidity, and the conditions under which it is not paid."
status: seedling
---

# Liquidity premium

## Standard

Illiquid assets should offer a higher expected return than liquid ones, because the holder gives up the option to sell. That option has value, and the premium is its price. The premium is real in long samples; the problem is that it is paid at the end, conditionally, and not always.

The conditions under which it fails are specific and worth writing down: when the investor is forced to sell into an illiquid market, when the illiquidity coincides with the need for cash, and when the mark hides the loss until it becomes a realised one. A premium that is only paid to those who never need the money is a premium for patience, not for risk-taking, and patience is not always available.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## Decision rules

- The premium is estimated from observed transaction evidence where any exists, not from a model.
- The holding period over which it accrues is stated.
- The conditions under which it is not paid are listed before the position is taken.
- Any capital that a goal needs inside the lockup is excluded from the calculation.
- The premium is compared with the cost of the lockup — fees, monitoring, and foregone flexibility.
- A premium that survives only in a calm market is recorded as conditional.

## Procedure

1. Estimate the premium from transaction-based evidence.
2. State the holding period over which it accrues.
3. List the failure conditions.
4. Exclude goal-linked capital from the eligible base.
5. Compare the premium with the lockup's costs.
6. Record the conditional nature of the estimate.

## Anti-patterns

- Assuming the premium because the asset is illiquid.
- Quoting the premium without the holding period.
- Using capital needed for a goal as if it could wait.
- Ignoring the fees that consume part of the premium.
- Treating a mark-based return as the premium.

## Done checklist

- [ ] Premium estimated from transaction evidence.
- [ ] Holding period stated.
- [ ] Failure conditions listed.
- [ ] Goal-linked capital excluded.
- [ ] Costs compared with the premium.
- [ ] Conditional status recorded.

## Sources

- Investor education on risk and return: <https://www.investor.gov/introduction-investing>
- Rate series for opportunity cost: <https://fred.stlouisfed.org/>
- Regulatory context for private-asset disclosure: <https://www.sec.gov/investor>

The arithmetic that makes the premium concrete is the comparison with the liquid alternative: same exposure, no lockup, and the difference in expected return is what the illiquidity pays. Where that comparison cannot be made because no liquid equivalent exists, the premium is an assumption, and the record should say so rather than presenting it as a measurement.

The premium also has an opportunity cost that is easy to miss: capital inside a lockup cannot be rebalanced, cannot be used to meet a margin call elsewhere, and cannot be moved when the policy changes. Those foregone options are part of the price paid for the premium, and in a year when other holdings need liquidity, they can exceed it.

