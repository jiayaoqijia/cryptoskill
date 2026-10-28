# Portfolio Fit, Suitability and Macro

Purpose: connect the asset to the investor's constraints and to the broader regime. A good asset can be a bad fit; a bad fit is a real risk.

## Suitability inputs

- Horizon and liquidity needs inside that horizon.
- Maximum tolerable drawdown and loss floor.
- Liability currency; USD/TRY exposure; need for income versus growth.
- Jurisdiction, eligibility, accreditation, KYC/AML, transfer restrictions.
- Existing concentration and correlation with current holdings.
- Leverage tolerance and margin/liquidation constraints.

If these are absent: `suitability not assessable — requires <named inputs>`. Never assume them and never prescribe an allocation.

## Portfolio fit

- Correlation/beta versus the existing portfolio, the benchmark, BTC/TAO, equities, gold and cash; state the window and regime.
- Volatility, maximum drawdown, recovery time, tail risk and liquidity under stress.
- Concentration: single asset, sector, factor, counterparty, venue, custody.
- Currency: nominal versus real return; decompose USD return and FX change for a TRY-based investor.
- Horizon match: lock-ups, vesting, redemption gates, unstake queues.

## Behavioral biases

- Anchoring to purchase price or a prior target; sunk-cost; confirmation; recency; loss aversion; overconfidence; home bias.
- If the user owns the asset or has a prior view, separate the asset case from the ownership case; never infer position size.

## Positioning and consensus

- Analyst estimates and revisions, short interest/borrow, options skew, fund/ETF flows; label as positioning, not evidence.
- For crypto: funding/OI/basis, exchange flows and holder cohorts; see `crypto-technical.md` and `crypto-onchain-flows.md`.

## Risk budget and sizing (only with explicit constraints)

- Define the maximum loss the investor can tolerate; position size is a function of that budget and the loss floor, not a universal percentage.
- Stress test: −50%, −80%, liquidity −50%, correlation → 1, funding/withdrawal freeze.
- Kelly or fractional Kelly only with explicit assumptions and a clear warning; not a default.
- Do not present a position size as a recommendation without the user's constraints.

## Macro and cycle

- Rates, inflation, FX, liquidity, credit and policy affect an asset only through a named channel: cash flow, discount rate, funding, demand, or cost.
- Identify the cycle/life-cycle stage; normalize margins and multiples across the cycle; do not extrapolate a peak or trough as steady state.
- Regime shifts: risk-on/risk-off, regulatory change, liquidity crunch, sector rotation.
- For crypto: TAO/BTC beta, stablecoin liquidity, exchange access, on-chain settlement conditions.

## ESG and materiality

- Use ESG only where material to cash flow, licence to operate, cost of capital, litigation or stakeholder risk. Avoid box-ticking and unsupported scores.

## Sources

- Portfolio holdings/constraints, benchmark and FX data, central-bank/IMF/FRED, correlation APIs.
- Record the window, regime and currency for every correlation statement.

## Report

- Standard: one paragraph or a compact table. Deep: a portfolio-fit page with correlation, drawdown, liquidity and stress tests.
- State `not assessable` when constraints are absent; state the inputs required.
- The report may say the asset is not a core holding, but not how much to buy.
