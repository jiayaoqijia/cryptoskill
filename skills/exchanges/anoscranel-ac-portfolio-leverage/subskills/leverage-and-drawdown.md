---
name: leverage-and-drawdown
domain: investing/leverage-and-drawdown
trigger: "Working out how borrowing changes the arithmetic of a fall."
anti_trigger: "Not for predicting drawdowns, and not for perp liquidation geometry."
scope: "How leverage changes recovery arithmetic and why the path matters more than the average."
status: seedling
---

# Leverage and drawdown

## Standard

Leverage changes the recovery arithmetic. A portfolio that falls fifty percent must rise a hundred percent to recover; a leveraged portfolio that falls seventy percent must rise more than two hundred percent, and if the fall triggered a forced sale, the recovery must be earned from a smaller base. That asymmetry is the reason leverage is not a symmetric amplifier even when the borrowing cost is low.

The path matters more than the average return for the same reason. A leveraged position can have a positive expected return and still end at zero if the sequence includes a fall deep enough to cross the maintenance boundary. The record should therefore be built on the worst plausible path rather than on the mean, and the test is whether the position survives that path with its collateral intact.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.finra.org/>.

## Decision rules

- Compute the recovery required after a stated fall, at the actual leverage ratio.
- Compute the fall that would trigger a forced sale, and the recovery from the post-sale base.
- Record the worst drawdown the strategy's own evidence contains.
- Record whether the position survives that drawdown without a call.
- State the sequence risk explicitly: an early fall is the binding scenario.
- Where the evidence contains no drawdown of that size, record the extrapolation as an assumption.

## Procedure

1. Set the leverage ratio and compute exposure.
2. Compute the maintenance boundary in percentage terms.
3. Take the worst drawdown from the strategy's evidence.
4. Test the position against that drawdown and against a deeper one.
5. Compute the recovery required from each resulting base.
6. Record the arithmetic and the survival conclusion.

## Anti-patterns

- Testing leverage against average returns.
- Computing recovery from the pre-fall portfolio.
- Ignoring that a forced sale changes the base.
- Using a drawdown sample that excludes the last crisis.
- Treating a stress test that just survives as comfortable.

## Done checklist

- [ ] Leverage ratio and exposure computed.
- [ ] Maintenance boundary computed.
- [ ] Worst evidenced drawdown recorded.
- [ ] Deeper stress tested.
- [ ] Recovery arithmetic computed from each base.
- [ ] Survival conclusion recorded.

A useful rule of thumb is that the recovery required from a post-sale base is much larger than the fall that caused it, so a forced sale is not a pause in the strategy but a change in the geometry of the strategy; the record should state the new base and the new required return explicitly.

## Sources

- Investor education on leverage and risk: <https://www.investor.gov/introduction-investing>
- Margin and liquidation practice: <https://www.finra.org/>
- Market drawdown data: <https://fred.stlouisfed.org/>
