# 03 — Allocation, Performance and Attribution

## Purpose

Distinguish **what the portfolio owns** from **what produced the return**. A weight table is not performance; a return number without cash-flow handling is not attribution.

## Inputs

- Position values and quantities at the same timestamp.
- Cost basis or transfer history, if available.
- Benchmark and currency.
- Fees and transaction costs.

## Method

1. Compute weights and cluster weights.
2. Compute top-N, HHI, and effective N.
3. Compute TWR from sub-period returns; compute MWR only with cash-flow data.
4. Attribute contribution by position and cluster.
5. Compare with the pre-stated benchmark; state fees and FX.
6. If cost basis is missing, stop at value change.

## Allocation

### Core measures

- Weight: `w_i = value_i / total_value`.
- Top-1, top-2, top-5 concentration.
- Herfindahl-Hirschman Index: `HHI = Σ w_i²` (0–1; higher is more concentrated).
- Effective number of positions: `1 / HHI`.
- Cluster weight: sum weights sharing a chain, stablecoin, bridge, oracle, curator, validator, or custody provider.

### Cluster map

| Cluster | Positions | Weight | Shared dependency | Why it matters |
|---|---|---:|---|---|
| Example | A, B | 42% | Same bridge | One pause can freeze both |

Do not call a portfolio diversified because it has many tickers. Count the shared failure path.

## Performance

### Time-weighted return (TWR)

Use for most portfolios, especially when external cash flows are outside the manager’s control. Chain sub-period returns:

`TWR = Π(1 + r_t) − 1`

Where `r_t` is the sub-period return, adjusted for external flows at the start/end of each sub-period. State the valuation dates.

### Money-weighted return (MWR)

Use when the investor controls contributions/withdrawals, or for illiquid/closed-end positions. MWR is the IRR of cash flows and ending value. It reflects the investor’s actual experience, not manager skill.

### Benchmark and attribution

- Compare with the benchmark stated in the IPS-lite; do not choose it after the fact.
- Contribution: `contribution_i = w_i × r_i`; sum approximates portfolio return before rebalancing and fees.
- For a Brinson-style view, separate allocation, selection, and interaction only when a benchmark and coherent sectors exist. Crypto “sectors” are unstable; label the classification.
- Report fees and transaction costs; if unavailable, state `gross-of-fee` and do not compare with net returns.
- FX: for a TRY-based investor, decompose USD return and FX change; do not present the USD return as the investor’s return.

### Rules

1. Never annualize a return period shorter than one year.
2. Do not compare TWR with MWR as if they were the same measure.
3. Separate price return, income, and new flows.
4. If cost basis is missing, state `P&L not assessable`; value change is not performance.
5. If the portfolio changed materially, do not attribute the whole change to “performance.”

## Output table

| Measure | Value | Window | Benchmark | Evidence |
|---|---:|---|---|---|
| TWR | X% | 2026-01-01 to 2026-10-30 | BTC or policy portfolio | VERIFIED/ESTIMATED |
| MWR | X% | Same | — | ESTIMATED |
| Volatility | X% | 90d/365d | Benchmark | VERIFIED |
| Top-1 weight | X% | As-of date | Policy limit | VERIFIED |
| HHI | X | As-of date | — | VERIFIED |

## Failure modes

- Using a price-only return as portfolio performance.
- Ignoring deposits/withdrawals.
- Comparing a gross return with a net benchmark.
- Annualizing three months.
- Calling a high-yield position “income” when it is token emissions.

## Sources

- CFA Institute, *Overview of the Global Investment Performance Standards* (2026).
- CFA Institute, *Asset Allocation with Real-World Constraints* (2026).
- MSCI, performance attribution overview (Brinson and factor approaches).
