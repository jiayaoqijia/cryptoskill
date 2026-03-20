# Venus Protocol Ops — Skill Summary

## 1) Purpose
`venus-protocol-ops` is a risk-first operations skill for Venus Protocol (BNB Chain). It supports:
- market scanning (APY, liquidity, utilization)
- wallet exposure and health checks
- what-if borrow simulation
- deposit and withdraw execution flows with safety confirmations

Primary design goal: **safe, explainable yield operations** with conservative defaults.

---

## 2) Current Capabilities

### A. Market Intelligence
- Pulls live market data from Venus API (`https://api.venus.io`)
- Normalizes:
  - supply/borrow APY
  - utilization
  - liquidity
  - collateral factor / liquidation threshold
  - market listing/borrowability flags

Script:
- `scripts/fetch_markets.py`

### B. Wallet Risk Analysis
- Onchain wallet read via `getAccountSnapshot` (vToken-level)
- Computes:
  - total supplied USD
  - total borrowed USD
  - weighted collateral USD
  - health and risk tier

Scripts:
- `scripts/wallet_onchain_exposure.py` (onchain auto mode)
- `scripts/check_wallet_exposure.py` (manual/API fallback)

### C. Borrow What-if Simulation
- Simulates post-borrow health
- Returns risk tier and max additional borrow for a target health threshold

Script:
- `scripts/simulate_borrow.py`

### D. One-Command Operator Interface
- Consolidated command for market + wallet + simulation
- Supports JSON output and brief English output for messaging

Script:
- `scripts/venus_check.py`

### E. Deposit Execution
- ERC20 flow: `approve -> mint(uint256)`
- Native flow support for BNB-style market (`mint()` with value)
- Defaults to simulation mode; broadcast requires explicit confirmation

Script:
- `scripts/venus_deposit.js`

### F. Withdraw Execution
- Supports both:
  - `redeemUnderlying(amount)`
  - `redeem(vTokenAmount)`
- Defaults to simulation mode; broadcast requires explicit confirmation

Script:
- `scripts/venus_withdraw.js`

---

## 3) Safety Model
- Default execution mode is `simulate` (no broadcast)
- Broadcast requires explicit guard (`--confirm YES`)
- Risk language avoids guarantees
- Strategy guidance is conservative-first:
  - avoid leverage by default
  - focus on stablecoin/high-liquidity routes unless user overrides

---

## 4) Key Files

### Core
- `SKILL.md`

### Scripts
- `scripts/fetch_markets.py`
- `scripts/calc_health.py`
- `scripts/check_wallet_exposure.py`
- `scripts/wallet_onchain_exposure.py`
- `scripts/simulate_borrow.py`
- `scripts/venus_check.py`
- `scripts/venus_deposit.js`
- `scripts/venus_withdraw.js`

### References
- `references/protocol-overview.md`
- `references/risk-rules.md`
- `references/bnbchain-contracts.md`
- `references/glossary.md`
- `references/quick-commands.md`
- `references/skill-summary.md` (this file)

### Asset
- `assets/report-template.md`

---

## 5) Example Commands

### Market snapshot
```bash
python scripts/venus_check.py --symbol vUSDC --output brief --lang en
```

### Wallet + risk check (onchain)
```bash
python scripts/venus_check.py --symbol vUSDC --wallet 0xYourWallet --output brief --lang en
```

### Deposit (safe preview)
```bash
node scripts/venus_deposit.js --asset vUSDC --amount 10 --wallet 0xYourWallet --mode simulate
```

### Deposit (broadcast)
```bash
node scripts/venus_deposit.js --asset vUSDC --amount 10 --private-key 0x... --mode broadcast --confirm YES
```

### Withdraw (safe preview)
```bash
node scripts/venus_withdraw.js --asset vUSDC --amount 1 --wallet 0xYourWallet --mode simulate
```

### Withdraw (broadcast)
```bash
node scripts/venus_withdraw.js --asset vUSDC --amount 1 --private-key 0x... --by underlying --mode broadcast --confirm YES
```

---

## 6) What’s Included vs Not Included

Included:
- Read-only market/wallet analytics
- Position risk scoring
- Deposit and withdraw execution primitives

Not included (yet):
- Full autonomous rebalancing engine with scheduler/policy daemon
- Cross-protocol routing optimizer
- Comprehensive gas/slippage optimizer across DEX routes

---

## 7) Operational Status
The skill is implemented, validated, and packaged as:
- `dist/venus-protocol-ops.skill`
