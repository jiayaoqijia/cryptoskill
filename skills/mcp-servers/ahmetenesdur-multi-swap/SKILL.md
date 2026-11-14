---
name: multi-swap
description: Execute multiple token swaps in a single Starknet transaction via Fibrous (default). Supports per-provider selection (avnu, ekubo, or auto to race all). Supports 2-3 swap pairs bundled into one multicall. Use this skill when the user wants to swap multiple token pairs at once, do batch swaps, execute several trades simultaneously, perform parallel swaps, or do bulk trading in one transaction. Also trigger when the user mentions "two swaps", "three swaps", "swap X and Y at the same time", or wants to convert multiple tokens in a single call.
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx starkfi@latest multi-swap *)
    - Bash(npx starkfi@latest status)
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest tx-status *)
---

# Multi-Swap

Execute 2-3 independent token swaps in a single Starknet transaction via Fibrous (default). Other providers can be selected with `--provider`, or use `--provider auto` to race all providers per pair. All swaps are bundled into one multicall, saving gas compared to executing them individually.

## Prerequisites

- Active session required.
- Sufficient balance for ALL source tokens + gas fees.

## Rules

1. BEFORE any multi-swap, you MUST run `npx starkfi@latest status` and `npx starkfi@latest balance` to verify connectivity and source token balances for ALL pairs.
2. Minimum **2** and maximum **3** swap pairs per multi-swap. Single swaps should use the `trade` skill instead.
3. The pairs string MUST be wrapped in **double quotes** and each pair separated by a **comma**.
4. Each pair follows the format: `<amount> <FROM>><TO>` (no spaces around `>`).
5. Default slippage is **1%**. To change, use `--slippage <percent>`.
6. Suggest using `--simulate` first so the user can confirm gas cost.
7. AFTER a successful multi-swap, you MUST verify using `npx starkfi@latest tx-status <hash>`.

## Commands

```bash
npx starkfi@latest multi-swap "<pairs>" [--provider <fibrous|avnu|ekubo|auto>] [--slippage <percent>] [--simulate] [--json]
```

## Parameters

| Parameter    | Type   | Description                                            | Required |
| ------------ | ------ | ------------------------------------------------------ | -------- |
| `pairs`      | string | Swap pairs: `"100 USDC>ETH, 50 USDT>STRK"` (2-3 pairs) | Yes      |
| `--provider` | string | Provider: `fibrous` (default), `avnu`, `ekubo`, `auto` (race all) | No       |
| `--slippage` | number | Slippage tolerance in % (default: `1`)                 | No       |
| `--simulate` | flag   | Estimate fees without broadcasting                     | No       |
| `--json`     | flag   | Output as JSON                                         | No       |

## Pair Format

```
"<amount> <FROM>><TO>, <amount> <FROM>><TO>"
```

Examples:

- `"100 USDC>ETH, 200 USDT>STRK"` — two pairs
- `"50 DAI>ETH, 100 USDC>STRK, 0.1 ETH>USDT"` — three pairs (maximum)

## Examples

**User:** "Swap 100 USDC to ETH and 200 USDT to STRK in one transaction"

```bash
npx starkfi@latest status
npx starkfi@latest balance
npx starkfi@latest multi-swap "100 USDC>ETH, 200 USDT>STRK"
npx starkfi@latest tx-status <hash>
```

**User:** "Simulate swapping 50 DAI, 100 USDC, and 0.1 ETH"

```bash
npx starkfi@latest multi-swap "50 DAI>ETH, 100 USDC>STRK, 0.1 ETH>USDT" --simulate
```

## Error Handling

| Error                     | Action                                                         |
| ------------------------- | -------------------------------------------------------------- |
| `Too few pairs`           | Multi-swap requires at least 2 pairs. Use `trade` for singles. |
| `Too many pairs`          | Maximum 3 pairs. Split into multiple calls.                    |
| `No route found`          | One or more pairs lack liquidity.                              |
| `Insufficient balance`    | Check `balance` — user may lack one of the source tokens.      |
| `Provider unavailable`    | Specified provider is invalid. Valid: fibrous, avnu, ekubo.    |
| `All providers failed`    | All providers timed out or errored. Retry later.               |
| `Simulation failed`       | One of the routes is invalid or would revert.                  |
| `Not authenticated`       | Run `authenticate-wallet` skill first.                         |

## Related Skills

- Use `trade` for a single swap (simpler syntax).
- Use `batch` for combining swaps with other operations (stake, supply, send).
- Use `balance` to verify you have enough of all source tokens.
