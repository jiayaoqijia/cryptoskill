---
name: troves
description: Deposit and withdraw from Troves DeFi yield vault strategies on Starknet. View available strategies, check positions, and manage vault deposits. Use this skill when the user mentions Troves, vault, yield vault, DeFi vault, strategy, yield farming, vault deposit, vault withdraw, earning yield through vaults, passive yield strategies, or wants to deposit into or withdraw from a yield strategy — even if they don't say "Troves" explicitly.
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.3.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest troves-list)
    - Bash(npx starkfi@latest troves-list *)
    - Bash(npx starkfi@latest troves-position)
    - Bash(npx starkfi@latest troves-position *)
    - Bash(npx starkfi@latest troves-deposit *)
    - Bash(npx starkfi@latest troves-withdraw *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Troves DeFi Vaults

Manage Troves yield vault strategies on Starknet: browse curated vault strategies, deposit tokens to earn yield, and withdraw from positions. Strategies range from single-asset vaults to dual-asset LP positions (e.g. Ekubo CL pools).

## Prerequisites

- Active session required.
- Sufficient token balance for deposits + gas fees.

## Rules

1. BEFORE any deposit, you MUST run `npx starkfi@latest troves-list` to discover available strategies and their current APY, TVL, and risk factors.
2. BEFORE depositing, check `balance` to confirm the user has enough of the required deposit token(s).
3. Use `troves-position` to check the user's current vault positions before withdrawing.
4. **Risk awareness:** Always inform the user of the strategy's `riskFactor` (1.0 = low, 5.0 = high) and `isAudited` status before depositing.
5. Suggest using `--simulate` first for large deposits to verify the transaction would succeed.
6. AFTER any transactional operation (deposit, withdraw), verify with `tx-status`.
7. Only deposit into strategies with status `Active`. Warn if a strategy is `Paused` or `Deprecated`.
8. **Dual-asset strategies:** When a strategy has 2 deposit tokens (e.g. `STRK, ETH`), you MUST provide `--amount2` and `--token2` flags in addition to the primary amount and token. Omitting these will produce a descriptive validation error explaining exactly which parameters are missing.

## Commands

```bash
# List all available strategies
npx starkfi@latest troves-list [--json]

# Check current vault positions
npx starkfi@latest troves-position <strategy-id> [--json]

# Deposit into a strategy (single-asset)
npx starkfi@latest troves-deposit <amount> <strategy-id> [--token <symbol>] [--simulate] [--json]

# Deposit into a strategy (dual-asset)
npx starkfi@latest troves-deposit <amount> <strategy-id> -t <symbol> --amount2 <value> --token2 <symbol2> [--simulate] [--json]

# Withdraw from a strategy
npx starkfi@latest troves-withdraw <amount> <strategy-id> [--token <symbol>] [--amount2 <value>] [--token2 <symbol2>] [--simulate] [--json]
```

## Parameters

### troves-deposit / troves-withdraw

| Parameter    | Type   | Description                                             | Required |
| ------------ | ------ | ------------------------------------------------------- | -------- |
| `amount`     | number | Amount to deposit or withdraw (positional)              | Yes      |
| `strategy-id`| string | Strategy ID (positional, e.g. `evergreen_strk`)         | Yes      |
| `--token`    | string | Token symbol (default: STRK)                            | No       |
| `--amount2`  | string | Second token amount for dual-asset strategies           | Dual-asset only |
| `--token2`   | string | Second token symbol for dual-asset strategies           | Dual-asset only |
| `--simulate` | flag   | Estimate fees without broadcasting                      | No       |
| `--json`     | flag   | Output as JSON                                          | No       |

## Strategy Types

### Single-Asset Strategies
Strategies with one deposit token (e.g. `evergreen_strk`, `hyper_xstrk`). Only `--token` and `amount` are needed.

### Dual-Asset Strategies
Strategies with two deposit tokens (e.g. `ekubo_cl_strketh`, `ekubo_cl_strkusdc_v2`). Both token amounts are required via `--amount2` and `--token2` flags. Check `depositTokens` in `troves-list` output to identify these.

## Strategy Properties

Each strategy has the following properties:

| Property        | Description                        |
| --------------- | ---------------------------------- |
| `id`            | Unique strategy identifier         |
| `name`          | Human-readable strategy name       |
| `apy`           | Current annual percentage yield    |
| `tvlUsd`        | Total value locked in USD          |
| `depositTokens` | Accepted deposit tokens            |
| `riskFactor`    | Risk rating (1.0 = low, 5.0 = high) |
| `isAudited`     | Whether the strategy is audited    |
| `status`        | `Active`, `Paused`, or `Deprecated` |

## Examples

**User:** "What yield vault strategies are available?"

```bash
npx starkfi@latest troves-list
```

**User:** "Deposit 500 STRK into Evergreen vault"

```bash
npx starkfi@latest status
npx starkfi@latest balance --token STRK
npx starkfi@latest troves-list  # Verify strategy exists and is Active
npx starkfi@latest troves-deposit 500 evergreen_strk --simulate
npx starkfi@latest troves-deposit 500 evergreen_strk
npx starkfi@latest tx-status <hash>
```

**User:** "Deposit into Ekubo STRK/ETH pool" (dual-asset)

```bash
npx starkfi@latest troves-list --json  # Check depositTokens for ekubo_cl_strketh
npx starkfi@latest balance --token STRK
npx starkfi@latest balance --token ETH
npx starkfi@latest troves-deposit 100 ekubo_cl_strketh -t STRK --amount2 0.005 --token2 ETH --simulate
npx starkfi@latest troves-deposit 100 ekubo_cl_strketh -t STRK --amount2 0.005 --token2 ETH
npx starkfi@latest tx-status <hash>
```

**User:** "Show me my vault positions"

```bash
npx starkfi@latest troves-position evergreen_strk
```

**User:** "Withdraw 200 STRK from Evergreen"

```bash
npx starkfi@latest troves-position evergreen_strk  # Check available balance
npx starkfi@latest troves-withdraw 200 evergreen_strk --simulate
npx starkfi@latest troves-withdraw 200 evergreen_strk
npx starkfi@latest tx-status <hash>
```

**User:** "Find the highest APY vault for STRK"

```bash
npx starkfi@latest troves-list --json
# Parse and present strategies sorted by APY, filtered by STRK deposit token
```

## Error Handling

| Error                               | Action                                                         |
| ----------------------------------- | -------------------------------------------------------------- |
| `Strategy not found`                | Run `troves-list` to find valid strategy IDs.                  |
| `Strategy paused`                   | Strategy is not accepting deposits. Choose another one.        |
| `Insufficient balance`              | Check `balance` for the required deposit token(s).             |
| `Simulation failed`                 | Transaction would revert. Check amount, strategy, and gas.     |
| `Not authenticated`                 | Run `authenticate-wallet` skill first.                         |
| `dual-asset strategy ... must provide` | Strategy requires two token amounts. Add `--amount2` and `--token2`. |
| `does not accept <token>`           | Use a token from the strategy's `depositTokens` list.          |

## Related Skills

- Use `balance` to verify available tokens before depositing.
- Use `portfolio` for a full overview including vault positions with USD values.
- Use `batch` to combine vault deposits with swaps or staking in one transaction.
- Use `lst` for liquid staking (different yield mechanism — share price appreciation).
- Use `staking` for delegation staking (validator-based yield).
