---
name: venus-protocol-ops
description: Analyze Venus Protocol lending/borrowing positions on BNB Chain with risk-first guidance. Use when users ask about Venus markets, collateral/borrow decisions, health factor, liquidation risk, APY/utilization comparison, isolated pools, or "can I borrow X safely" style what-if checks.
---

# Venus Protocol Ops

## Overview
Use this skill to provide **read-only**, risk-aware analysis for Venus Protocol. Prioritize liquidation safety, clarity, and explicit uncertainty over aggressive yield-chasing.

## Workflow

### 1) Classify user intent
Map request into one of these modes:
- **Market scan**: compare assets/pools (supply APY, borrow APY, utilization, caps)
- **Position check**: assess a wallet's current collateral/borrow health
- **What-if simulation**: estimate risk after a proposed borrow/supply/repay
- **Execution planning**: prepare step-by-step actions without broadcasting tx

If user asks for onchain execution, pause and request explicit confirmation + exact parameters. Use simulation first, then broadcast only after user confirms.

### 2) Collect data
Use scripts first:
- `scripts/fetch_markets.py` for market snapshot (official API base: `https://api.venus.io`, default scope: Core Pool only via `references/pool-filter.json`)
- `scripts/wallet_onchain_exposure.py` for real wallet onchain exposure
- `scripts/check_wallet_exposure.py` for manual/API fallback wallet summary
- `scripts/simulate_borrow.py` for hypothetical borrow impact
- `scripts/venus_deposit.js` for deposit preview/broadcast flow (approve + mint)
- `scripts/venus_withdraw.js` for withdraw preview/broadcast flow (redeem / redeemUnderlying) with post-withdraw HF prediction and safety line checks (default 1.2, user customizable)
- `scripts/venus_borrow.js` for borrow preview/broadcast flow
- `scripts/venus_repay.js` for repay preview/broadcast flow (approve + repayBorrow)
- `scripts/venus_collateral.js` for collateral enable/disable (enterMarkets / exitMarket)
- `scripts/hf_monitor.py` for threshold-based HF monitoring and advisory actions (includes ACCOUNT_UNHEALTHY alert when HF < safety line, default 1.2)

Example market query:
- `python scripts/fetch_markets.py --chain-id 56 --limit 200` (Core Pool default)
- `python scripts/fetch_markets.py --chain-id 56 --limit 200 --pool-scope all` (all pools)

If API is unavailable, continue with transparent assumptions and mark output as estimate.

### 3) Run risk rules
Apply rules from `references/risk-rules.md`:
- Compute health and safety buffer
- Flag borrow-cap / liquidity constraints
- Detect concentration risk (single volatile collateral)
- Classify risk: Low / Medium / High

### 4) Produce actionable output
Always include:
1. **Current state** (key numbers)
2. **Risk status** (Low/Medium/High + why)
3. **Safe range** (max suggested extra borrow or required extra collateral)
4. **Next best actions** (2-4 concrete steps)

Prefer concise bullets and exact numbers.

## Output format
Use this structure:
- **Summary**: one-line verdict
- **Metrics**: collateral, debt, health, utilization, APYs
- **Risk findings**: top 2-4 risks
- **Recommended plan**: concrete steps and limits
- **Assumptions**: data freshness, missing fields, estimate flags

## Guardrails
- Never claim guaranteed safety or returns.
- Never hide data gaps; explicitly note stale/missing data.
- Default to conservative thresholds when uncertain.
- Treat this as educational/risk tooling, not financial advice.
- For real transactions: run simulate mode first; require explicit confirmation for broadcast.
- For withdrawals: always predict post-withdraw HF; warn/block when predicted HF falls below safety line (default 1.2 unless user customizes).

## Quick usage
- One-command market check: `python scripts/venus_check.py --symbol vUSDT`
- Market + auto wallet risk check: `python scripts/venus_check.py --symbol vUSDT --wallet 0x...`
- What-if borrow (auto wallet): `python scripts/venus_check.py --symbol vUSDT --wallet 0x... --extra-borrow 120`
- Manual fallback: `python scripts/venus_check.py --symbol vUSDT --wallet 0x... --weighted-collateral 1500 --debt 1000`
- English brief mode: `python scripts/venus_check.py --symbol vUSDT --wallet 0x... --output brief --lang en`

## Protocol separation
- Venus Core scripts: `scripts/` root (e.g. `venus_*.js`, `fetch_markets.py`, `wallet_onchain_exposure.py`).
- Flux (Power by Fluid) scripts: `scripts/flux/`.
- Choose protocol-specific scripts directly so other agents can route quickly without mixing workflows.

## References
- Protocol overview: `references/protocol-overview.md`
- Risk thresholds and formulas: `references/risk-rules.md`
- Contract/address notes: `references/bnbchain-contracts.md`
- Terminology: `references/glossary.md`
- Venus CLI cookbook: `references/quick-commands.md`
- Flux CLI cookbook: `references/flux-quick-commands.md`
- Flux BNB addresses: `references/flux-bnb-addresses.json`
