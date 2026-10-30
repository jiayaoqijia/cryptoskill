# 01 — Mandate, IPS-lite and Intake

## Purpose

Establish what the portfolio is for before measuring it. A return number without a mandate is not a performance verdict; it is an observation.

## Inputs

Collect, or explicitly mark missing:

| Input | Why it matters | Acceptable form |
|---|---|---|
| Scope | Which wallets, accounts, chains, and assets are in scope | Addresses or exported CSV; never a seed phrase |
| Return objective | Growth, income, preservation, or benchmark-relative | Named objective and benchmark |
| Risk tolerance | Maximum tolerable drawdown and loss floor | Percentage and currency amount |
| Horizon | When the money is needed | Date or range; note known cash needs |
| Liquidity | Required cash and access restrictions | Amount, currency, notice period |
| Tax/legal | Net return and eligibility | Residency, account type, restrictions |
| Governance | Who decides, executes, monitors | Named roles; no assumption |
| Review cycle | When the policy is revisited | Scheduled date and trigger events |
| Constraints | Prohibited assets, leverage, custody, stablecoin buffer | Explicit list |

## Method

1. Confirm the scope and the decision maker.
2. Convert each objective and constraint into a measurable field.
3. Record what is missing and why it changes the conclusion.
4. Draft the IPS-lite; do not start valuation until the mandate is usable.
5. If the mandate is incomplete, produce a Data Request Memo instead of a verdict.

## IPS-lite

Write a one-page policy before the review:

1. **Purpose and scope.** What is included and excluded.
2. **Objective.** Return target or benchmark; income vs growth.
3. **Risk.** Maximum drawdown, loss floor, risk budget, position and scenario limits.
4. **Horizon and liquidity.** Time horizon; cash needs; liability currency.
5. **Tax and legal.** Residency, account type, reporting, transfer restrictions.
6. **Governance.** Decision rights, approval, monitoring, escalation.
7. **Rebalancing.** Target weights, bands, frequency, tax-aware rules.
8. **Review.** Scheduled review date and event triggers.
9. **Constraints.** Prohibited assets, leverage limits, custody rules, stablecoin floor.

## Benchmark selection

There is no universal crypto benchmark. Choose one and state why:

- **BTC** — reserve-asset comparison; simple, but ignores breadth.
- **Total crypto market** — broad beta; sensitive to survivorship and changing constituents.
- **User-defined policy portfolio** — strategic weights; best for mandate-relative review.
- **Stablecoin/cash** — liquidity-sleeve comparison; not a growth benchmark.
- **None** — acceptable for a first diagnostic, but then no “outperformance” claim.

Record the benchmark, currency, and rebalancing method. Do not switch benchmarks after seeing results.

## Missing-data policy

- Missing mandate or risk limit: `suitability not assessable`; no position-size recommendation.
- Missing price or balance for more than 20% of value: data-gap memo; no full verdict.
- Missing cost basis: no P&L; report value change only and label it as such.
- Missing liquidity data: no exit-days estimate; state `liquidity not assessable`.

## Data Request Memo

When inputs are missing, return:

1. What is known.
2. What is missing, by name.
3. Why each missing item changes the conclusion.
4. The minimum data needed for the next mode.
5. A safe interim observation, without a buy/sell instruction.

## Failure modes

- Treating a wallet snapshot as a mandate.
- Assuming a long horizon because the user is young.
- Assuming stablecoins are cash.
- Using a benchmark that was chosen after the fact.
- Recommending a position size without a loss floor.

## Sources

- CFA Institute, *Elements of an Investment Policy Statement for Individual Investors* (2010).
- CFA Institute, *Asset Allocation with Real-World Constraints* (2026 curriculum).
