---
name: balance
description: Check Starknet wallet token balances — STRK, ETH, and all ERC-20 tokens. Use this skill when the user asks about their balance, holdings, funds, tokens, wallet contents, or wants to know how much of something they have. Also use before any transaction to verify sufficient funds. Trigger whenever the user says "check my balance", "how much ETH do I have", "what's in my wallet", "do I have enough", "show my tokens", or any variation about checking available assets — even if they don't use the word "balance".
license: MIT
compatibility: Requires Node.js 22+ and npx.
metadata:
    version: 0.1.0
    author: ahmetenesdur
    category: wallet-data
allowed-tools:
    - Bash(npx starkfi@latest balance)
    - Bash(npx starkfi@latest balance *)
    - Bash(npx starkfi@latest status)
---

# Check Balance

Fetch wallet holdings on Starknet: STRK, ETH, and all ERC-20 tokens with non-zero balances.

## Prerequisites

- Active session required. If not authenticated, run `authenticate-wallet` skill first.

## Rules

1. If the user asks to check a specific token, use `--token <symbol>`.
2. If no token is specified, run `balance` without flags to show all balances.
3. Use `--json` when the output will be consumed by another skill or pipeline.
4. Run this BEFORE `send`, `trade`, `multi-swap`, or any transactional skill to verify sufficient funds.

## Commands

```bash
# All token balances
npx starkfi@latest balance [--json]

# Specific token balance
npx starkfi@latest balance --token <symbol> [--json]
```

## Parameters

| Parameter | Type   | Description                               | Required |
| --------- | ------ | ----------------------------------------- | -------- |
| `--token` | string | Token symbol (e.g. `STRK`, `ETH`, `USDC`) | No       |
| `--json`  | flag   | Output as JSON                            | No       |

## Examples

**User:** "Check my balance"

```bash
npx starkfi@latest balance
```

**User:** "How much STRK do I have?"

```bash
npx starkfi@latest balance --token STRK
```

**User:** "Get my balances as JSON"

```bash
npx starkfi@latest balance --json
```

## Error Handling

| Error               | Action                                                           |
| ------------------- | ---------------------------------------------------------------- |
| `Not authenticated` | Run `authenticate-wallet` skill first.                           |
| `Network error`     | Retry once. If persistent, use `config` skill to set custom RPC. |

## Related Skills

- Run this BEFORE `send` or `trade` to verify sufficient funds.
- Run this BEFORE `staking` to confirm available STRK/BTC tokens.
- Run this BEFORE `lending` supply operations to confirm available assets.
- Run this BEFORE `dca` to verify sufficient sell token balance for the total DCA amount.
- Run this BEFORE `confidential` `conf-fund` to verify sufficient tokens for funding the confidential account.
- Run this BEFORE `troves` deposits to verify sufficient tokens for the vault strategy.
- Run this BEFORE `lst` liquid staking to confirm available STRK.
- Use `portfolio` for a complete view including staking, lending, vault, and LST positions with USD values.
