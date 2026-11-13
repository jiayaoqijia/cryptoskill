---
name: futures-versus-etf
domain: investing/futures-versus-etf
trigger: "Choosing between an index future and an ETF for the same exposure."
anti_trigger: "Not for fund selection in general, and not for predicting the index."
scope: "Financing, dividends, tax, leverage, and the trade-offs between the two vehicles."
status: seedling
---

# Futures versus ETF

## Standard

The same index exposure can be obtained through a future or through an ETF, and the choice changes the economics rather than the exposure. A future embeds financing explicitly in its basis and requires margin; an ETF embeds its costs in a fee and tracks the index with a small difference. Over a day the two are close; over a year the differences in financing, dividends, tax treatment, and roll cost dominate.

The decision also depends on the holder's constraints. A future can be sized precisely and hedged quickly, but it requires margin management and a roll discipline; an ETF is simpler to hold but carries a fee, a tracking difference, and a secondary-market spread. The record states which vehicle was chosen, the reason, and the cost estimate for both, because the choice is reversible and should be revisited when rates or fees change.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.sec.gov/investor>.

## Decision rules

- Record the exposure required and the two candidate vehicles.
- Estimate the future's annual cost: roll cost plus financing embedded in the basis plus commissions.
- Estimate the ETF's annual cost: expense ratio plus tracking difference plus spread amortised.
- Record the tax treatment of each in the relevant jurisdiction, as a question for a professional if unclear.
- Record the operational burden: margin, roll discipline, and collateral for the future.
- Record the size at which each vehicle becomes preferable, if that is the deciding factor.

## Procedure

1. State the exposure and the holding period.
2. Compute the future's all-in annual cost.
3. Compute the ETF's all-in annual cost.
4. Record tax treatment and any jurisdiction question.
5. Record operational requirements for each.
6. Write the comparison and the choice with its conditions.

## Anti-patterns

- Comparing the future's margin with the ETF's full price as if they were costs.
- Ignoring roll cost in the future's annual cost.
- Comparing gross returns without dividends.
- Assuming the ETF's tracking difference is zero.
- Choosing the vehicle on cost alone when margin management is the binding constraint.

## Done checklist

- [ ] Exposure and horizon stated.
- [ ] Future's annual cost estimated.
- [ ] ETF's annual cost estimated.
- [ ] Tax treatment recorded or flagged.
- [ ] Operational requirements recorded.
- [ ] Choice and conditions written.

## Sources

- Investor education on funds and costs: <https://www.investor.gov/introduction-investing>
- Fund disclosure requirements: <https://www.sec.gov/investor>
- Rate data for financing estimates: <https://fred.stlouisfed.org/>
