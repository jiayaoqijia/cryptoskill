---
name: cost-of-leverage
domain: investing/cost-of-leverage
trigger: "Working out what borrowed money costs and what return it must earn."
anti_trigger: "Not for predicting returns, and not for comparing brokers' service."
scope: "The borrowing rate, the break-even return it implies, and the drag it adds."
status: seedling
---

# Cost of leverage

## Standard

Borrowing costs a rate, and that rate sets a hurdle: the leveraged portion of the portfolio must earn more than the borrowing cost to add anything, and it must earn it after tax where interest is not deductible. The hurdle is not the only consideration, but it is the arithmetic that has to be done first, because a portfolio leveraged at a rate above its expected return is a plan to lose money slowly.

The comparison set matters. A margin loan, a securities-backed line, a personal loan, and a mortgage refinance carry different rates, different callability, and different tax treatment, and the cheapest rate is not always the safest structure. The record states the rate, the day-count basis, the reset behaviour for floating rates, and the collateral consequences attached to each option.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the borrowing rate, its basis, and whether it floats or resets.
- Compute the break-even return: rate divided by one minus the tax rate, where interest is not deductible.
- Compare the break-even with the portfolio's own long-run evidence, not with an optimistic forecast.
- Record the total annual interest at the intended loan size.
- Record the opportunity cost of assets pledged as collateral.
- Where the rate resets, record the sensitivity to a stated increase.

## Procedure

1. Collect the rate, basis, and reset terms for each borrowing option.
2. Compute the after-tax break-even return.
3. Compute annual interest at the planned loan size.
4. Compare the break-even with the portfolio's historical return range.
5. Test a rate rise and record the change in annual cost.
6. Write the cost summary with its assumptions.

## Anti-patterns

- Comparing the rate with a hoped-for return rather than an evidenced one.
- Ignoring the tax treatment of interest.
- Assuming a floating rate stays at today's level.
- Ignoring the cost of the collateral pledged.
- Treating a promotional rate as permanent.

## Done checklist

- [ ] Rate, basis, and reset recorded.
- [ ] After-tax break-even computed.
- [ ] Annual interest at planned size computed.
- [ ] Break-even compared with evidenced returns.
- [ ] Rate-rise sensitivity recorded.
- [ ] Cost summary written.

The comparison should also include the return on the assets that would otherwise be sold: borrowing to avoid selling a position is only rational if the position's expected return exceeds the borrowing cost, which is the same test applied from the other direction and is often forgotten when the loan is framed as flexibility.

## Sources

- Investor education on borrowing to invest: <https://www.investor.gov/introduction-investing>
- Interest-rate and margin data: <https://www.federalreserve.gov/>
- Market rate series: <https://fred.stlouisfed.org/>
