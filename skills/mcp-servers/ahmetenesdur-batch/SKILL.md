---
name: batch
description: Execute multiple different DeFi operations in a single Starknet transaction — combine swaps, staking, lending supply/borrow/repay/withdraw, token sends, DCA orders, and Troves vault deposits/withdrawals into one multicall. Use this skill when the user wants to batch, combine, bundle, or chain multiple diverse operations together in one atomic transaction, such as "swap ETH and then stake STRK" or "withdraw from lending and swap" or "repay debt and stake" or "swap and send in one go" or "create a DCA order and stake" or "deposit into vault and swap". Also trigger when the user mentions multicall, combining operations, doing multiple things at once, or wants to save gas by bundling actions — even if they don't use the word "batch".
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest batch *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Batch Execute

Bundle multiple diverse DeFi operations into a single Starknet multicall transaction. Supports combining **swaps**, **staking**, **lending supply/borrow/repay/withdraw**, **token sends**, **DCA orders**, and **Troves vault deposits/withdrawals** — all executed atomically in one on-chain call.

## Prerequisites

- Active session required.
- Sufficient balance for all operations + gas fees.
- Minimum **2 operations** required per batch.

## Rules

1. BEFORE any batch, you MUST run `npx starkfi@latest status` and `npx starkfi@latest balance` to verify connectivity and funds.
2. A batch MUST include at least **2 operations**. For single operations, use the dedicated skill (`trade`, `send`, `staking`, `lending`, or `dca`).
3. Each `--swap`, `--stake`, `--supply`, `--send`, `--dca-create`, and `--dca-cancel` flag can appear **multiple times** (repeatable).
4. If the batch includes a `--send` operation, you MUST confirm the recipient address with the user before executing.
5. Suggest using `--simulate` first to verify the entire batch would succeed.
6. AFTER a successful batch, verify with `npx starkfi@latest tx-status <hash>`.
7. All operations in a batch are **atomic** — if any one fails, the entire transaction reverts.

## Commands

```bash
npx starkfi@latest batch [--simulate] [--json] \
  --swap "<amount> <from> <to>" \
  --stake "<amount> <token> <validator_or_pool>" \
  --supply "<amount> <token> <pool>" \
  --send "<amount> <token> <recipient>" \
  --borrow "<col_amt> <col_token> <bor_amt> <bor_token> <pool>" \
  --repay "<amount> <token> <col_token> <pool>" \
  --withdraw "<amount> <token> <pool>" \
  --dca-create "<amount> <sell> <buy> <perCycle> [frequency]" \
  --dca-cancel "<orderId>" \
  --troves-deposit "<amount> <token> <strategyId> [amount2 token2]" \
  --troves-withdraw "<amount> <token> <strategyId> [amount2 token2]"
```

## Operation Formats

| Flag       | Format                                     | Example                         |
| ---------- | ------------------------------------------ | ------------------------------- |
| `--swap`   | `"<amount> <from> <to>"`                   | `--swap "100 USDC ETH"`         |
| `--stake`  | `"<amount> <token> <validator_or_0xPool>"` | `--stake "500 STRK Karnot"`     |
| `--supply` | `"<amount> <token> <pool>"`                | `--supply "100 USDC Prime"`     |
| `--send`       | `"<amount> <token> <0xRecipient>"`         | `--send "10 STRK 0x07b2..."`    |
| `--borrow`     | `"<col_amt> <col_token> <bor_amt> <bor_token> <pool>"` | `--borrow "0.5 ETH 500 USDC Prime"` |
| `--repay`      | `"<amount> <token> <col_token> <pool>"`    | `--repay "100 USDC ETH Prime"`  |
| `--withdraw`   | `"<amount> <token> <pool>"`                | `--withdraw "200 USDC Prime"`   |
| `--dca-create` | `"<amount> <sell> <buy> <perCycle> [freq]"` | `--dca-create "1000 USDC ETH 10 P1D"` |
| `--dca-cancel` | `"<orderId>"`                              | `--dca-cancel "abc123"`         |
| `--troves-deposit`  | `"<amount> <token> <strategyId> [amount2 token2]"` | `--troves-deposit "100 STRK evergreen_strk"` or `"100 STRK ekubo_cl_strketh 0.005 ETH"` |
| `--troves-withdraw` | `"<amount> <token> <strategyId> [amount2 token2]"` | `--troves-withdraw "50 STRK evergreen_strk"` or `"50 STRK ekubo_cl_strketh 0.005 ETH"` |

> **Note:** `--stake` accepts either a validator name (e.g. `Karnot`) or a pool contract address (starting with `0x`). The CLI auto-detects the format.

## Parameters

| Parameter    | Type   | Description                           | Required |
| ------------ | ------ | ------------------------------------- | -------- |
| `--swap`     | string | Swap operation (repeatable)           | No\*     |
| `--stake`    | string | Stake operation (repeatable)          | No\*     |
| `--supply`   | string | Lending supply operation (repeatable) | No\*     |
| `--send`       | string | Token transfer operation (repeatable) | No\*     |
| `--borrow`     | string | Borrow from lending pool (repeatable) | No\*     |
| `--repay`      | string | Repay lending debt (repeatable)       | No\*     |
| `--withdraw`   | string | Withdraw from lending pool (repeatable) | No\*   |
| `--dca-create` | string | Create DCA order (repeatable)         | No\*     |
| `--dca-cancel` | string | Cancel DCA order (repeatable)         | No\*     |
| `--troves-deposit`  | string | Troves vault deposit (repeatable) | No\*     |
| `--troves-withdraw` | string | Troves vault withdraw (repeatable) | No\*    |
| `--simulate` | flag   | Estimate fees without broadcasting    | No       |
| `--json`     | flag   | Output as JSON                        | No       |

\*At least 2 operations (of any type) are required.

## Examples

**User:** "Swap 100 USDC to ETH and stake 500 STRK with Karnot in one transaction"

```bash
npx starkfi@latest status
npx starkfi@latest balance
npx starkfi@latest batch --swap "100 USDC ETH" --stake "500 STRK Karnot"
npx starkfi@latest tx-status <hash>
```

**User:** "Withdraw my USDC from Prime lending and swap it to ETH"

```bash
npx starkfi@latest status
npx starkfi@latest balance
npx starkfi@latest batch --withdraw "200 USDC Prime" --swap "200 USDC ETH"
npx starkfi@latest tx-status <hash>
```

**User:** "Repay my USDC debt on Prime and stake STRK"

```bash
npx starkfi@latest status
npx starkfi@latest balance
npx starkfi@latest batch --repay "100 USDC ETH Prime" --stake "50 STRK karnot"
npx starkfi@latest tx-status <hash>
```

**User:** "Borrow USDC using ETH as collateral and swap half to STRK"

```bash
npx starkfi@latest status
npx starkfi@latest balance
npx starkfi@latest batch \
  --borrow "0.5 ETH 500 USDC Prime" \
  --swap "250 USDC STRK"
npx starkfi@latest tx-status <hash>
```

**User:** "Simulate a batch of two swaps and a stake"

```bash
npx starkfi@latest batch --simulate \
  --swap "100 USDC ETH" \
  --swap "200 USDT STRK" \
  --stake "500 STRK Karnot"
```

## Error Handling

| Error                    | Action                                                        |
| ------------------------ | ------------------------------------------------------------- |
| `Too few operations`     | At least 2 operations required. Use dedicated skills instead. |
| `Insufficient balance`   | Check `balance` for all required tokens.                      |
| `Invalid validator/pool` | Run `validators`/`pools` to find valid names/addresses.       |
| `Simulation failed`      | One of the operations would revert. Check each individually.  |
| `Not authenticated`      | Run `authenticate-wallet` skill first.                        |

## Related Skills

- Use `trade` for a single swap.
- Use `staking` for standalone staking operations.
- Use `lending` for standalone lending operations.
- Use `send` for standalone token transfers.
- Use `dca` for standalone DCA order management.
- Use `troves` for standalone vault deposit/withdraw operations.
- Use `lst` for liquid staking operations (not supported in batch).
