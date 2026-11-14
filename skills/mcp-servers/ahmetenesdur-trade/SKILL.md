---
name: trade
description: Swap tokens on Starknet via Fibrous DEX aggregator. Supports per-provider selection (avnu, ekubo, or auto to race all). Use this skill when the user wants to swap, exchange, trade, convert, buy, or sell one token for another on Starknet. Also use when the user asks about token prices, exchange rates, DEX routing, best swap route, or wants to check how much they would receive for a given amount — even if they don't explicitly say "swap".
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest trade *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Trade / Swap Tokens

Exchange one token for another on Starknet via Fibrous (default). Other providers (AVNU, Ekubo) can be selected with `--provider`, or use `--provider auto` to race all providers for the best price. All transactions are routed through the Paymaster by default (gas paid in STRK or configured token).

## Prerequisites

- Active session required.
- Sufficient balance of the source token + gas fees.

## Rules

1. BEFORE any trade, you MUST run `npx starkfi@latest status` and `npx starkfi@latest balance` to verify connectivity and source token balance.
2. Default slippage is **1%**. To change, use `--slippage <percent>`.
3. Suggest using `--simulate` first for large trades so the user can review the estimated fee and expected output before committing.
4. AFTER a successful trade, you MUST verify the transaction using `npx starkfi@latest tx-status <hash>`.
5. For **multiple swaps in one transaction**, use the `multi-swap` skill instead.

## Commands

```bash
npx starkfi@latest trade <amount> <from> <to> [--provider <fibrous|avnu|ekubo|auto>] [--slippage <percent>] [--simulate] [--json]
```

## Parameters

| Parameter    | Type   | Description                                       | Required |
| ------------ | ------ | ------------------------------------------------- | -------- |
| `amount`     | number | Amount of source token to swap                    | Yes      |
| `from`       | string | Source token symbol (e.g. `ETH`, `USDC`)          | Yes      |
| `to`         | string | Target token symbol (e.g. `STRK`, `DAI`)          | Yes      |
| `--provider` | string | Provider: `fibrous` (default), `avnu`, `ekubo`, `auto` (race all) | No |
| `--slippage` | number | Slippage tolerance in % (default: `1`)            | No       |
| `--simulate` | flag   | Estimate fees without broadcasting                | No       |
| `--json`     | flag   | Output as JSON                                    | No       |

## Examples

**User:** "Swap 100 USDC for ETH"

```bash
npx starkfi@latest status
npx starkfi@latest balance --token USDC
npx starkfi@latest trade 100 USDC ETH
npx starkfi@latest tx-status <hash>
```

**User:** "How much ETH would I get for 500 USDC?"

```bash
npx starkfi@latest trade 500 USDC ETH --simulate
```

**User:** "Convert 0.5 ETH to STRK with 2% slippage"

```bash
npx starkfi@latest status
npx starkfi@latest balance --token ETH
npx starkfi@latest trade 0.5 ETH STRK --slippage 2
npx starkfi@latest tx-status <hash>
```

## Error Handling

| Error                     | Action                                                  |
| ------------------------- | ------------------------------------------------------- |
| `No route found`          | Liquidity may be too low or pair doesn't exist.         |
| `Insufficient balance`    | Check `balance` and suggest a smaller amount.           |
| `Provider unavailable`    | Specified provider is invalid. Valid: fibrous, avnu, ekubo. |
| `All providers failed`    | All providers timed out or errored. Retry later.        |
| `Simulation failed`       | Route is invalid or would revert. Do not retry blindly. |
| `Not authenticated`       | Run `authenticate-wallet` skill first.                  |

## Related Skills

- Use `balance` to check available tokens before trading.
- Use `multi-swap` for executing 2-3 swaps in a single transaction.
- Use `batch` for combining a swap with other operations (stake, supply, send, dca, troves).
- Use `dca` for recurring buy orders instead of a one-time swap.
- Use `troves` to deposit swap proceeds into yield vaults.
- Use `lst` for liquid staking after swapping to STRK.
- Use `config` to set a custom RPC if experiencing rate limits.
