---
name: mandate-design
domain: investing/mandate-design
trigger: "Writing the constraints that define what a manager may and may not do."
anti_trigger: "Not for selecting the manager, and not for the policy itself."
scope: "Guidelines, discretion, and the constraints that define a mandate."
status: seedling
---

# Mandate design

## Standard

A mandate is the contract that converts a policy into operating instructions. It states the benchmark, the permitted instruments, the concentration limits, the tracking-error budget, and the constraints on leverage, liquidity, and currency. Each of those is a choice, and the choices decide what kind of portfolio the manager can build: a wide tracking-error budget is an instruction to take risk, and a narrow one is an instruction to hug the benchmark.

The design failure that recurs is a mandate that constrains the visible and not the consequential. Limits on a single holding are common; limits on the aggregate exposure to a factor, a counterparty, or a liquidity profile are less common, and it is the aggregate that produces the surprise. A mandate should state what the portfolio must be able to do — sell a stated share within a stated period — as well as what it may hold.

Primary sources: <https://www.cfainstitute.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the benchmark and the tracking-error budget.
- Record the permitted and excluded instruments.
- Record concentration limits at holding, sector, factor, and counterparty level.
- Record liquidity requirements expressed as an ability to sell.
- Record leverage and currency constraints.
- Record the reporting obligations and the breach-notification requirement.

## Procedure

1. Record the benchmark and risk budget.
2. Record permitted and excluded instruments.
3. Record limits at each level of aggregation.
4. Record the liquidity requirement as an operational test.
5. Record leverage, currency, and derivative constraints.
6. Write the mandate summary with its consequential limits.

## Anti-patterns

- Constraining holdings but not factor or counterparty exposure.
- Setting a tracking-error budget that contradicts the return objective.
- Expressing liquidity limits as a permitted asset list rather than as an ability to sell.
- Leaving breach notification undefined.
- Writing a mandate the manager cannot comply with and monitoring it anyway.

## Done checklist

- [ ] Benchmark and budget recorded.
- [ ] Instruments recorded.
- [ ] Limits at each level recorded.
- [ ] Liquidity requirement operationalised.
- [ ] Leverage and currency recorded.
- [ ] Reporting obligations recorded.

The clause that is most often missing and most often needed is the one describing what happens when a limit is breached by market movement rather than by a trade: whether the manager must restore compliance immediately, within a stated period, or only report it determines whether the mandate is a hard constraint or an intention, and the difference is only discovered at the moment it matters.

## Sources

- Investment management standards: <https://www.cfainstitute.org/>
- Regulatory context for managed accounts: <https://www.sec.gov/investor>
- Investor guidance on mandates: <https://www.investor.gov/introduction-investing>
