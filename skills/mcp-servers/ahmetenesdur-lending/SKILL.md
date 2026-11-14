---
name: lending
description: Manage Vesu V2 lending positions on Starknet — supply assets, borrow against collateral, repay debt, withdraw, close positions, monitor health factors, and auto-rebalance risky positions. Use this skill when the user mentions lending, borrowing, supplying collateral, Vesu, earn interest, health factor, liquidation risk, monitoring positions, auto-rebalancing, protecting against liquidation, "my position is risky", "health factor low", or DeFi yield from lending protocols — even if they don't say "lending" explicitly.
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.2.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest lend-pools)
    - Bash(npx starkfi@latest lend-pools *)
    - Bash(npx starkfi@latest lend-status *)
    - Bash(npx starkfi@latest lend-supply *)
    - Bash(npx starkfi@latest lend-withdraw *)
    - Bash(npx starkfi@latest lend-borrow *)
    - Bash(npx starkfi@latest lend-repay *)
    - Bash(npx starkfi@latest lend-close *)
    - Bash(npx starkfi@latest lend-monitor)
    - Bash(npx starkfi@latest lend-monitor *)
    - Bash(npx starkfi@latest lend-auto *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Lending (Vesu V2)

Manage lending and borrowing positions on Vesu V2 protocol on Starknet. Supply assets to earn yield, borrow against collateral, repay debt, monitor health factors, auto-rebalance risky positions, and close positions.

## Prerequisites

- Active session required.
- Sufficient token balance for supply/repay operations + gas fees.

## Rules

1. BEFORE any lending action, run `npx starkfi@latest lend-pools` to discover available pools and tokens. Use `lend-pools <name>` for detailed pool info including APY rates.
2. Pool can be specified by **name** (e.g. `Prime`, `Genesis`) or by **contract address** (`0x...`).
3. BEFORE borrowing, run `npx starkfi@latest lend-status` to check existing positions, or with `--pool` and `--collateral-token` for Health Factor:
    - Health Factor **> 2.0** → Safe to borrow.
    - Health Factor **1.5 – 2.0** → WARN the user about increasing risk.
    - Health Factor **< 1.5** → STRONGLY advise against borrowing. Suggest repaying instead.
    - Health Factor **< 1.1** → DO NOT proceed without explicit double-confirmation from the user.
4. AFTER any transactional operation, verify with `tx-status`.
5. When using `--use-supplied`, the borrow is backed by the user's existing earn positions (supplied positions) rather than transferring from wallet.
6. When the user asks about health, risk, or liquidation — use `lend-monitor` first for a comprehensive overview with 4-level risk classification (SAFE/WARNING/DANGER/CRITICAL).
7. When a position's health factor is low, suggest `lend-auto` to automatically rebalance. Always use `--simulate` first to preview the action before executing.

## Commands

### Discovery

```bash
# List all pools (overview table)
npx starkfi@latest lend-pools [--json]

# Detailed pool info with APY rates
npx starkfi@latest lend-pools <name> [--json]

# View all lending positions (auto-scan)
npx starkfi@latest lend-status

# View specific position status
npx starkfi@latest lend-status --pool <name|address> --collateral-token <symbol> [--borrow-token <symbol>]
```

### Supply & Withdraw

```bash
# Supply (deposit assets to earn yield)
npx starkfi@latest lend-supply <amount> --pool <name|address> --token <symbol> [--simulate]

# Withdraw (remove supplied assets)
npx starkfi@latest lend-withdraw <amount> --pool <name|address> --token <symbol> [--simulate]
```

### Borrow & Repay

```bash
# Borrow (provide collateral and take loan)
npx starkfi@latest lend-borrow \
  --pool <name|address> \
  --collateral-amount <n> --collateral-token <symbol> \
  --borrow-amount <n> --borrow-token <symbol> \
  [--use-supplied] [--simulate]

# Repay (pay back borrowed amount)
npx starkfi@latest lend-repay <amount> --pool <name|address> --token <symbol> --collateral-token <symbol> [--simulate]
```

### Close Position

```bash
# Atomically repay all debt and withdraw all collateral
npx starkfi@latest lend-close --pool <name|address> --collateral-token <symbol> --borrow-token <symbol> [--simulate]
```

### Health Monitoring

```bash
# Scan all positions across all pools
npx starkfi@latest lend-monitor [--json]

# Monitor specific position
npx starkfi@latest lend-monitor --pool <name|address> --collateral-token <symbol> --borrow-token <symbol>

# Custom warning threshold
npx starkfi@latest lend-monitor --warning-threshold 1.5
```

### Auto-Rebalance

```bash
# Auto-rebalance (picks best strategy — repay or add collateral)
npx starkfi@latest lend-auto --pool <name|address> --collateral-token <symbol> --borrow-token <symbol>

# With specific strategy
npx starkfi@latest lend-auto --pool <name|address> --collateral-token <symbol> --borrow-token <symbol> --strategy repay
npx starkfi@latest lend-auto --pool <name|address> --collateral-token <symbol> --borrow-token <symbol> --strategy add-collateral

# Simulate first (always recommended)
npx starkfi@latest lend-auto --pool <name|address> --collateral-token <symbol> --borrow-token <symbol> --simulate
```

## Parameters

### lend-supply / lend-withdraw

| Parameter | Type   | Description                                | Required |
| --------- | ------ | ------------------------------------------ | -------- |
| `amount`     | number | Amount (positional)                        | Yes      |
| `--pool`     | string | Pool name or address                       | Yes      |
| `--token`    | string | Token symbol (`USDC`, `ETH`, `STRK`, etc.) | Yes      |
| `--simulate` | flag   | Estimate fees and validate without executing | No     |

### lend-borrow

| Parameter             | Type   | Description                           | Required |
| --------------------- | ------ | ------------------------------------- | -------- |
| `--pool`              | string | Pool name or address                  | Yes      |
| `--collateral-amount` | number | Collateral amount to supply           | Yes      |
| `--collateral-token`  | string | Collateral token (e.g. `ETH`, `STRK`) | Yes      |
| `--borrow-amount`     | number | Amount to borrow                      | Yes      |
| `--borrow-token`      | string | Token to borrow (e.g. `USDC`, `USDT`) | Yes      |
| `--use-supplied`      | flag   | Use existing earn positions as collateral    | No       |
| `--simulate`          | flag   | Estimate fees and validate without executing | No       |

### lend-repay

| Parameter            | Type   | Description                      | Required |
| -------------------- | ------ | -------------------------------- | -------- |
| `amount`             | number | Amount to repay (positional)     | Yes      |
| `--pool`             | string | Pool name or address             | Yes      |
| `--token`            | string | Token to repay (e.g. `USDC`)     | Yes      |
| `--collateral-token` | string | Collateral token of the position | Yes      |
| `--simulate`         | flag   | Estimate fees and validate without executing | No |

### lend-close

| Parameter            | Type   | Description             | Required |
| -------------------- | ------ | ----------------------- | -------- |
| `--pool`             | string | Pool name or address    | Yes      |
| `--collateral-token` | string | Collateral token symbol | Yes      |
| `--borrow-token`     | string | Borrow token symbol     | Yes      |
| `--simulate`         | flag   | Estimate fees and validate without executing | No |

### lend-status

Run without arguments to **auto-scan all pools**. Or specify `--pool` + `--collateral-token` for a detailed position view.

| Parameter            | Type   | Description                            | Required              |
| -------------------- | ------ | -------------------------------------- | --------------------- |
| `--pool`             | string | Pool name or address                   | No (auto-scan if omitted) |
| `--collateral-token` | string | Token supplied/used as collateral      | No*                   |
| `--borrow-token`     | string | Borrow token (needed to see debt + HF) | No                    |

> \* Required when `--pool` is specified.

### lend-monitor

Run without arguments to **scan all pools**. Or specify `--pool` + `--collateral-token` + `--borrow-token` for a single position.

| Parameter              | Type   | Description                          | Required                  |
| ---------------------- | ------ | ------------------------------------ | ------------------------- |
| `--pool`               | string | Pool name or address                 | No (scans all if omitted) |
| `--collateral-token`   | string | Collateral token symbol              | No*                       |
| `--borrow-token`       | string | Debt token symbol                    | No*                       |
| `--warning-threshold`  | number | Custom warning threshold (default: 1.3) | No                     |

> \* Required when `--pool` is specified.

**Risk Levels:**

| Level        | Health Factor | Meaning                               |
| ------------ | ------------- | ------------------------------------- |
| **SAFE**     | > 1.3         | No action needed                      |
| **WARNING**  | 1.1 – 1.3    | Monitor closely                       |
| **DANGER**   | 1.05 – 1.1   | Repay debt or add collateral          |
| **CRITICAL** | ≤ 1.05        | Imminent liquidation risk             |

### lend-auto

| Parameter              | Type   | Description                                    | Required |
| ---------------------- | ------ | ---------------------------------------------- | -------- |
| `--pool`               | string | Pool name or address                           | Yes      |
| `--collateral-token`   | string | Collateral token symbol                        | Yes      |
| `--borrow-token`       | string | Debt token symbol                              | Yes      |
| `--strategy`           | string | `repay`, `add-collateral`, or `auto` (default) | No       |
| `--target-hf`          | number | Target health factor (default: 1.3)            | No       |
| `--simulate`           | flag   | Estimate fees and validate without executing | No       |

## Examples

**User:** "What lending pools are available?"

```bash
npx starkfi@latest lend-pools
```

**User:** "Show me details for the Prime pool"

```bash
npx starkfi@latest lend-pools Prime
```

**User:** "Supply 500 USDC to Prime"

```bash
npx starkfi@latest status
npx starkfi@latest balance --token USDC
npx starkfi@latest lend-supply 500 --pool Prime --token USDC --simulate  # Preview first
npx starkfi@latest lend-supply 500 --pool Prime --token USDC             # Execute
npx starkfi@latest tx-status <hash>
```

**User:** "Borrow 100 USDC with ETH collateral from Prime"

```bash
npx starkfi@latest lend-status
# Check Health Factor before proceeding
npx starkfi@latest lend-borrow \
  --pool Prime \
  --collateral-amount 0.1 --collateral-token ETH \
  --borrow-amount 100 --borrow-token USDC
npx starkfi@latest tx-status <hash>
```

**User:** "Repay my 100 USDC loan from Prime"

```bash
npx starkfi@latest lend-repay 100 --pool Prime --token USDC --collateral-token ETH
npx starkfi@latest tx-status <hash>
```

**User:** "Close my ETH/USDC position in Prime"

```bash
npx starkfi@latest lend-close --pool Prime --collateral-token ETH --borrow-token USDC
npx starkfi@latest tx-status <hash>
```

**User:** "How healthy is my position?"

```bash
# Comprehensive health monitoring with risk levels
npx starkfi@latest lend-monitor

# Detailed health factor for specific position
npx starkfi@latest lend-monitor --pool Prime --collateral-token ETH --borrow-token USDC
```

**User:** "My position is at risk, fix it"

```bash
# First, check current state
npx starkfi@latest lend-monitor --pool Prime --collateral-token ETH --borrow-token USDC

# Simulate the auto-rebalance action
npx starkfi@latest lend-auto --pool Prime --collateral-token ETH --borrow-token USDC --simulate

# Execute after user confirms
npx starkfi@latest lend-auto --pool Prime --collateral-token ETH --borrow-token USDC
npx starkfi@latest tx-status <hash>
```

**User:** "Protect my ETH/USDC position from liquidation"

```bash
# Choose a specific strategy — repay debt
npx starkfi@latest lend-auto --pool Prime --collateral-token ETH --borrow-token USDC --strategy repay --simulate
```

## Error Handling

| Error                     | Action                                                        |
| ------------------------- | ------------------------------------------------------------- |
| `Pool not found`          | Run `lend-pools` to list valid pool names.                    |
| `Health Factor too low`   | Warn of liquidation risk. Suggest repaying or supplying more. |
| `Insufficient collateral` | Cannot borrow without supplying first.                        |
| `Dust limit`              | Borrow amount is below the pool's minimum dollar value (~$10). Increase it. |
| `Insufficient balance`    | Check `balance` — user may need to swap for the token.        |
| `Not authenticated`       | Run `authenticate-wallet` skill first.                        |
| `Monitor failed`          | Check pool/token params and retry.                            |
| `Rebalance failed`        | Check balances, health factor, and retry.                     |

## Related Skills

- Use `balance` to verify available assets before supplying.
- Use `trade` to swap tokens if the user doesn't have the right asset.
- Use `portfolio` for a full overview including lending positions with USD values.
- Use `batch` to combine supply operations with swaps, staking, or vault deposits.
- Use `troves` for vault-based yield strategies (different from lending).
- Use `lst` for liquid staking yield (xSTRK can also be supplied to lending pools).
- Use `portfolio-rebalance` (within `portfolio` skill) to optimize overall portfolio allocation.
