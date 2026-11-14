---
name: dca
description: Create, preview, list, and cancel recurring Dollar-Cost Averaging (DCA) buy orders on Starknet via AVNU or Ekubo. Use this skill when the user wants to set up automatic recurring purchases, dollar-cost average into a token, create a DCA order, schedule periodic buys, invest regularly, buy every day/week/month, or manage existing DCA orders. Also trigger when the user says "recurring buy", "scheduled purchase", "buy X of Y every day", or any variation about automated periodic investing — even if they don't use the term "DCA" explicitly.
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest dca-create *)
    - Bash(npx starkfi@latest dca-list)
    - Bash(npx starkfi@latest dca-list *)
    - Bash(npx starkfi@latest dca-cancel *)
    - Bash(npx starkfi@latest dca-preview *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Dollar-Cost Averaging (DCA)

Create recurring buy orders that automatically swap a fixed amount of one token into another at regular intervals. Supports AVNU and Ekubo DCA providers.

## Prerequisites

- Active session required.
- Sufficient balance of the sell token for the total DCA amount.
- Account must be deployed on-chain.

## Rules

1. BEFORE any DCA operation, you MUST run `npx starkfi@latest status` and `npx starkfi@latest balance` to verify connectivity and funds.
2. ALWAYS run `dca-preview` before `dca-create` to verify the expected output per cycle.
3. The `--per-cycle` flag is **required** for `dca-create`. It sets the amount sold each execution cycle.
4. Frequency uses ISO 8601 duration format: `P1D` (daily), `PT12H` (12 hours), `P1W` (weekly).
5. Suggest using `--simulate` first to verify the DCA order would succeed.
6. AFTER a successful creation, verify with `npx starkfi@latest tx-status <hash>`.

## Commands

### Preview a Cycle

```bash
npx starkfi@latest dca-preview <amount> <sell_token> <buy_token> [--provider <avnu|ekubo>] [--json]
```

### Create a DCA Order

```bash
npx starkfi@latest dca-create <total_amount> <sell_token> <buy_token> \
  --per-cycle <amount> \
  [--frequency <duration>] \
  [--provider <avnu|ekubo>] \
  [--simulate] [--json]
```

### List DCA Orders

```bash
npx starkfi@latest dca-list [--status <ACTIVE|CLOSED|INDEXING>] [--provider <avnu|ekubo>] [--page <n>] [--json]
```

### Cancel a DCA Order

```bash
npx starkfi@latest dca-cancel <order_id_or_address> [--provider <avnu|ekubo>] [--json]
```

## Parameters

| Parameter     | Type   | Description                                  | Required |
| ------------- | ------ | -------------------------------------------- | -------- |
| `amount`      | string | Total sell amount (create) or per-cycle amount (preview) | **Yes** |
| `sell_token`  | string | Token to sell (e.g. `STRK`, `ETH`)           | **Yes**  |
| `buy_token`   | string | Token to buy (e.g. `USDC`, `ETH`)            | **Yes**  |
| `order_id_or_address` | string | The UUID OR on-chain contract address (`0x...`) from `dca-list` | **Yes** (cancel) |
| `--per-cycle` | string | Amount to sell per cycle                      | **Yes** (create) |
| `--frequency` | string | ISO 8601 duration (default: `P1D`=daily)     | No       |
| `--provider`  | string | DCA provider: `avnu` (default) or `ekubo`    | No       |
| `--status`    | string | Filter orders: `ACTIVE`, `CLOSED`, `INDEXING` | No (list) |
| `--simulate`  | flag   | Estimate fees without broadcasting           | No       |
| `--json`      | flag   | Output as JSON                               | No       |

## Examples

**User:** "Buy 10 USDC worth of ETH every day for 100 days"

```bash
npx starkfi@latest status
npx starkfi@latest balance
npx starkfi@latest dca-preview 10 USDC ETH
npx starkfi@latest dca-create 1000 USDC ETH --per-cycle 10 --frequency P1D --simulate
npx starkfi@latest dca-create 1000 USDC ETH --per-cycle 10 --frequency P1D
npx starkfi@latest tx-status <hash>
```

**User:** "DCA into STRK weekly with 50 USDC per week, total 200 USDC"

```bash
npx starkfi@latest status
npx starkfi@latest balance
npx starkfi@latest dca-preview 50 USDC STRK
npx starkfi@latest dca-create 200 USDC STRK --per-cycle 50 --frequency P1W
```

**User:** "Show my active DCA orders"

```bash
npx starkfi@latest dca-list --status ACTIVE --json
```

**User:** "Cancel my DCA order"

```bash
npx starkfi@latest dca-list --status ACTIVE
npx starkfi@latest dca-cancel <order_id_or_address>
npx starkfi@latest tx-status <hash>
```

## Error Handling

| Error                  | Action                                                     |
| ---------------------- | ---------------------------------------------------------- |
| `DCA_FAILED`           | Check the error message for details (balance, provider).   |
| `Insufficient balance` | Check `balance` for the sell token.                        |
| `Not authenticated`    | Run `authenticate-wallet` skill first.                     |
| `Invalid frequency`    | Use ISO 8601 format: `P1D`, `PT12H`, `P1W`, `P1M`.        |

## Related Skills

- Use `trade` for a one-time swap instead of recurring.
- Use `batch` to combine a DCA creation with other operations.
- Use `portfolio` to check your overall positions and balances.
