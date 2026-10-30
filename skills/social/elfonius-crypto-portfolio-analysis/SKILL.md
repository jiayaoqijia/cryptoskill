---
name: crypto-portfolio-analysis
description: "Use when reviewing crypto and Web3 portfolios end to end."
version: 1.0.0
author: Hermes Agent and contributors
license: MIT
platforms: [linux, macos, windows]
---

# Crypto & Web3 Portfolio Analysis

Act as a senior portfolio analyst, risk manager, and on-chain researcher. Review the whole portfolio, not a watchlist of tickers. Separate what is verified from what is reported, estimated, or modeled. Never sign, approve, swap, bridge, deposit, or handle a private key.

## When to Use

Use when the user asks to:

- review a crypto/Web3 portfolio, wallet, or set of positions;
- assess allocation, concentration, risk, liquidity, correlation, or drawdown;
- evaluate tokenomics, protocol revenue, buybacks, DeFi positions, or on-chain flows in a portfolio context;
- run stress tests, scenario analysis, or a rebalancing review;
- compare a portfolio with a benchmark or an alternative allocation;
- produce a quick screen, a full investment review, or a monitoring update.

**Do not use for:** single-token price prediction, trade execution, tax filing, legal advice, smart-contract auditing, or guaranteed-return claims.

## Operating Stance

1. **Mandate first.** A portfolio without an objective, horizon, liquidity need, and loss limit is not assessable. Start with the IPS-lite below.
2. **Read-only.** Never request or use a seed phrase, private key, exchange password, or signing device. Never execute a transaction.
3. **Evidence classes.** Every material number is `VERIFIED`, `REPORTED`, `ESTIMATED`, `MODELED`, or `UNVERIFIED`.
4. **No silent filling.** Missing price, cost basis, liquidity, or constraint becomes `not assessable — requires <input>`.
5. **Risk clusters, not tickers.** Count shared chains, stablecoins, bridges, oracles, curators, validators, and custody as one exposure.
6. **No single health score.** Report a dashboard and named flags; do not hide trade-offs in one number.
7. **No forecast theater.** Use scenarios, ranges, and falsifiers. A target price is not a fact.
8. **Asset case ≠ ownership case.** A good asset can be a bad position at the wrong size, entry, horizon, or liquidity.

## Deliverable Modes

| Mode | Length | Minimum contents |
|---|---|---|
| **Quick Screen** | 1–2 pages | Value, top 5, top-1/top-2/top-3 concentration, data coverage, five red flags, verdict, 3 charts |
| **Full Review** | 8–15 pages | IPS-lite, all 16 lenses, risk dashboard, 6–10 chart visual pack, scenarios, alternatives, decision record, sources |
| **Monitoring** | 1–3 pages | Delta since last snapshot, threshold breaches, falsifiers, next review date, 2 delta charts |

## IPS-lite

Before a full review, record:

- **Purpose and scope:** which wallets, accounts, chains, and assets are in scope.
- **Return objective:** growth, income, capital preservation, or a named benchmark.
- **Risk tolerance:** maximum tolerable drawdown and loss floor; risk budget.
- **Horizon:** investment horizon and known cash needs inside it.
- **Liquidity:** required liquidity, liability currency, and access restrictions.
- **Tax/legal:** tax residency, account type, eligibility, transfer restrictions.
- **Governance:** who decides, who executes, who monitors, and how changes are approved.
- **Review cycle:** scheduled review, trigger events, and rebalancing bands.
- **Constraints:** prohibited assets, leverage limits, custody limits, minimum stablecoin buffer.

If these are absent, deliver a **Data Request Memo**, not a full verdict.

## The 16 Lenses

Every lens must be covered with evidence, marked `not material`, or marked `not assessable` with the missing input named.

| # | Lens | Core question | Minimum evidence |
|---:|---|---|---|
| 1 | **Mandate, IPS & constraints** | What is the portfolio for, over what horizon, with what liquidity and loss limit? | IPS-lite, benchmark, risk budget, review cycle |
| 2 | **Data integrity & valuation** | Is every position valued from a live, dated source? | Price/balance source and date, fair-value tier, reconciliation, stale-data flags |
| 3 | **Allocation & concentration** | What dominates by asset, cluster, chain, protocol, and counterparty? | Weights, top-N, HHI, cluster map |
| 4 | **Performance & attribution** | What drove return: price, quantity, FX, income, fees, or flows? | Benchmark, TWR/MWR, net-of-fee return, contribution, no annualizing <1 year |
| 5 | **Risk, tail & risk budget** | How bad can the downside be, and does it fit the mandate? | Volatility, max drawdown, historical VaR/CVaR, beta, stress loss, limits |
| 6 | **Correlation & factors** | Is diversification real or cosmetic? | Correlation matrix, rolling correlation, factor/cluster exposure, instability note |
| 7 | **Liquidity & exit** | How many days to exit at size, and at what slippage? | Pool depth, volume, unlock/vesting, unstake queue, exit days |
| 8 | **Stablecoin & counterparty** | Is “cash” actually cash? | Issuer, reserve, peg history, redemption gates, bridge exposure |
| 9 | **Chain, protocol, custody & contract** | What can lose the asset or freeze the exit? | Audits, admin/timelock, oracle, bridge, custody/key management, incidents |
| 10 | **Tokenomics & supply overhang** | Who gets diluted, when, and by how much? | Supply, float, emissions, unlocks, vesting, buyback/burn, holder concentration |
| 11 | **Fundamental value capture** | Does protocol revenue reach token holders? | Fees, revenue, gross profit, buybacks/burns, treasury, P/F, P/S, FDV |
| 12 | **DeFi, leverage & derivatives** | What is the liquidation, IL, oracle, funding, and reward-sustainability risk? | LTV/LLTV, health factor, liquidation price, LP composition, APR decomposition, funding/basis/OI, delta/vega |
| 13 | **On-chain flows & holder behavior** | Who is accumulating or leaving, and is the flow real? | Exchange/net flows, cohorts, whale concentration, labeled entities |
| 14 | **Market regime & macro** | What regime is the portfolio priced for, through what channel? | BTC dominance, liquidity, rates, stablecoin supply, funding/OI, sentiment |
| 15 | **Scenarios & reverse stress** | What happens in a named adverse path, and what would break the portfolio? | BTC −30%, ETH −40%, stablecoin depeg, bridge pause, correlation → 1, reverse stress |
| 16 | **Construction, behavior, tax & monitoring** | What should change, what does it cost, and what would trigger a review? | Rebalance deltas and bands, behavioral-bias check, tax flags, monitoring triggers, falsifiers |

## Procedure — 14 Steps

1. **Intake and IPS-lite.** Collect scope, positions, cost basis, liabilities, horizon, liquidity, risk limits, tax/legal constraints, benchmark, and mode. Draft the IPS-lite; stop at a data-request memo if material inputs are missing.
2. **Source plan.** Choose sources per asset and chain; record URL, auth, timestamp, and fallback. A source not probed in this session is not cited as live.
3. **Normalize.** Map symbols to canonical assets, chains, contracts, and clusters; separate spot, staked, locked, LP, lending, and accrued rewards.
4. **Value and reconcile.** Convert to one base currency; use the fair-value hierarchy; reconcile against a second source; flag differences above 2%; label stale, survivorship-biased, or wash-traded data.
5. **Allocation and concentration.** Compute weights, top-N, HHI, effective number of positions, and cluster exposure.
6. **Performance and attribution.** Use actual transfers and cost basis where available; compute TWR and MWR, net of fees and transaction costs; compare with the benchmark; never annualize a sub-one-year record; otherwise state `P&L not assessable`.
7. **Risk, correlation, and risk budget.** Compute volatility, max drawdown, historical VaR/CVaR, beta, and correlation over a stated window. Disclose VaR limitations and correlation instability. Compare risk consumption with the IPS-lite limits.
8. **Liquidity and exit.** Estimate exit days at 1%, 5%, and 10% of portfolio value; include unstake queues, vesting, withdrawal gates, and stressed liquidity.
9. **Asset fundamentals and tokenomics.** For each material position, check supply/float, emissions, unlocks, revenue, value capture, and holder concentration.
10. **DeFi, derivatives and on-chain.** For each lending/LP/staking position, check health factor, liquidation price, oracle, IL, reward source, incidents, and contagion path. For perps/options, check funding, basis, OI, liquidation, delta/vega, and counterparty.
11. **Market regime.** Identify the regime and the named transmission channel; keep sentiment as context, not proof.
12. **Scenarios, stress, and reverse stress.** Run named shocks; report portfolio-level loss, position contribution, the first breached limit, and what combination would make the portfolio fail its mandate.
13. **Alternatives and rebalancing.** Present 2–3 alternative allocations with trade-offs; include tax, liquidity, implementation cost, behavioral-bias check, and rebalancing bands. Do not execute.
14. **Report, visualize and monitor.** Produce the selected deliverable with decision record, falsifiers, monitoring table, review date, source appendix, and the required visual pack.

## Gates and Standards

| Gate | Pass condition | Failure action |
|---|---|---|
| **G1 — Input completeness** | At least 80% of portfolio value has a live price and balance source | Data-gap memo; no full verdict |
| **G2 — Source/date** | Every material number has source + date + definition | Mark `UNVERIFIED`; exclude from conclusion |
| **G3 — Reconciliation** | Balance/price difference ≤2%, or explained | Report discrepancy; never average silently |
| **G4 — Suitability** | Horizon, liquidity, loss limit, and constraints supplied | `suitability not assessable`; no position-size recommendation |
| **G5 — Read-only** | No signing, approval, bridge, deposit, or transaction step | Stop; the skill must never execute |

## Evidence Rules

- `VERIFIED`: directly observed from a live primary source, with timestamp.
- `REPORTED`: stated by a team, report, or dashboard; not independently checked.
- `ESTIMATED`: derived from stated inputs; show the formula and inputs.
- `MODELED`: scenario or simulation output; show method, assumptions, and limitations.
- `UNVERIFIED`: no adequate source; do not use in the conclusion.

Rules:

1. “Report says” is not “verified.” Name the source and date.
2. Do not mix revenue, fees, gross profit, tokenholder revenue, incentives, and emissions.
3. Do not annualize a return series shorter than one year.
4. Do not present a single target price, guaranteed yield, or “safe” position size.
5. A portfolio is not diversified merely because it holds many tickers; count shared risk clusters.
6. State the window, currency, and regime for every correlation or beta claim.
7. Distinguish liquidity from market capitalization; exit capacity is position-size dependent.

## Data Discipline

Use the narrowest source for the question; do not dump a full API response into the report.

- Prefer a primary chain/RPC or official protocol endpoint for balances and contract state.
- Cross-check prices with a second source; if sources differ by more than 2%, report both.
- For DeFi, use the exact chain, contract, market, and position; do not approximate an LP token with its underlying assets unless the position is actually redeemable.
- For tokenomics, distinguish circulating supply, total supply, max supply, float, emissions, and unlocks.
- For on-chain flows, label entity attribution as probabilistic; never present a guess as a fact.
- If a paid API is unavailable, say so and degrade to a data-gap memo; do not fabricate coverage.

## Output Contract

A full review must contain:

1. Cover and as-of timestamp.
2. IPS-lite and data coverage.
3. Portfolio snapshot and cluster map.
4. Performance and attribution with a named benchmark (or `not assessable`).
5. Risk dashboard: volatility, drawdown, VaR/CVaR, beta, correlation, liquidity.
6. Asset-level findings for material positions.
7. Tokenomics and value-capture findings.
8. DeFi/on-chain findings.
9. Market regime and scenarios.
10. Alternatives and rebalancing plan.
11. Decision record: what to do, why, what would falsify it, and what would make the position smaller.
12. Visual pack: 6–10 charts with finding titles, source/date, units, and limitations.
13. Sources, limitations, and next review date.

## Visual Pack

Charts are evidence, not decoration. A full review includes 6–10 charts; a quick screen includes 3; monitoring includes 2 delta charts.

- One chart answers one question; the title states the finding.
- Every chart carries unit, as-of date, source, window, and limitation.
- Bars start at zero; no 3D; no pie with more than five slices; no unlabeled dual axis.
- Exact numbers live in tables; charts explain comparison, shape, and trade-offs.
- Use color as a secondary cue; check grayscale and colorblind readability.
- Label modeled or estimated data.
- Do not chart a forecast as fact.
- Use `templates/visual-dashboard.md` and `references/13-visualization-and-charts.md`.

## References

- `references/01-mandate-and-intake.md` — IPS-lite, data request, suitability.
- `references/02-data-and-valuation.md` — source hierarchy, fair value, reconciliation.
- `references/03-allocation-and-performance.md` — weights, HHI, TWR/MWR, attribution.
- `references/04-risk-and-correlation.md` — volatility, drawdown, VaR/CVaR, beta, stress.
- `references/05-liquidity-and-exit.md` — exit days, depth, unlock and unstake queues.
- `references/06-tokenomics-and-value-capture.md` — supply, emissions, revenue, buybacks.
- `references/07-defi-and-onchain.md` — lending, LP, health factor, flows, contagion.
- `references/08-market-regime-and-scenarios.md` — regime, macro channels, reverse stress.
- `references/09-security-counterparty-legal.md` — custody, keys, bridges, tax/legal flags.
- `references/10-portfolio-construction.md` — risk budget, alternatives, rebalancing, biases.
- `references/11-reporting.md` — report architecture, language, tables, decision record.
- `references/12-methodology-and-sources.md` — source matrix, evidence rules, limitations.
- `references/13-visualization-and-charts.md` — chart selection, visual pack, design QA.

Templates: `investment-policy.md`, `portfolio-review-tr.md`, `portfolio-review-en.md`, `quick-screen.md`, `risk-dashboard.md`, `scenario-analysis.md`, `rebalancing-plan.md`, `data-request.md`, `monitoring.md`, `visual-dashboard.md`.

## Verification

Before delivering:

- [ ] IPS-lite or an explicit `not assessable` statement is present.
- [ ] Data coverage is stated; no material number is `UNVERIFIED`.
- [ ] Every material position has a source and timestamp.
- [ ] Top-1, top-2, and cluster concentration are computed.
- [ ] Risk metrics state method, window, and limitations.
- [ ] At least three scenarios, including reverse stress, are present.
- [ ] Liquidity and exit capacity are addressed.
- [ ] Tokenomics and value capture are separated from price action.
- [ ] DeFi positions have health factor, liquidation, oracle, and incident checks.
- [ ] Recommendations are conditional, with falsifiers and a review date.
- [ ] The required visual pack is present; every chart has a finding title, source/date, unit, and limitation.
- [ ] Charts pass the grayscale and zero-baseline checks; exact values are in tables.
- [ ] No transaction, signature, approval, or private-key step exists.
- [ ] Sources and limitations are listed.
