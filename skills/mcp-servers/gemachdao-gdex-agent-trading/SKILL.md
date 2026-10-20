---
name: gdex-agent-trading
description: Default agent flow for trading on GDEX via MCP — status, connect, preview, execute within the user's authority, follow the operation, manage or exit
---

# GDEX: Agent Trading (Default Flow)

Use these tools first. They sit on top of the full tool set and handle units, account
resolution, re-quoting and recovery for you. Drop to the specialised skills only for things
this flow does not cover yet (outcomes: **gdex-hl-outcomes**; copy trading: **gdex-copy-trading**).

## When to Use

- "What can you do?" / "Am I set up?" → `gdex_status`
- "Buy $20 of this on Base", "Sell half", "Long BTC $100 at 2x", "Close my short"
- "What do I own and what's pending?" → `gdex_positions`

## 1. Check readiness

`gdex_status` reports API reachability, connected accounts (no secrets), the delegated policy
per account, pending operations, supported trade kinds and the next setup step. Research and
quotes work without an account.

## 2. Connect once, without secrets in chat

```
gdex_connect { keyFile: "~/my-gdex-wallet.json" }   // JSON with privateKey, kept on this machine
gdex_connect { create: true }                         // new local wallet, starts unfunded
```

Returns an `accountRef` and the managed wallet addresses. Never ask the user to paste a private
key or seed phrase. Fund the **managed** wallets, not the control wallet. Sessions expire:
`gdex_connect { accountRef }` refreshes one.

## 3. Preview

`gdex_preview_trade` turns explicit intent into exact terms and a `previewId` (valid 60 s):

| kind | Required | Notes |
|------|----------|-------|
| `spot` | `chain`, `tokenAddress`, `side` buy\|sell, `amount` | Buy amount is USDC to spend; sell amount is tokens. USDC wallet chains: Ethereum, Optimism, BSC, Sonic, Base, Arbitrum, Solana. `slippagePct` default 1 (max 5). Buys auto-fund USDC and gas from other chains within a signed cap shown in the preview; `autoFunding: false` opts out. |
| `perp_open` | `coin`, `side` long\|short, `leverage`, and **one of** `notionalUsd` or `marginUsd` | "$100 at 2x" is ambiguous: ask which. Size is floored to the market's precision; $11 minimum; max leverage per market. Margin mode is set by GDEX: cross on core perps (shares the perp balance), isolated on builder-DEX and isolated-only markets; the preview says which. Builder-DEX markets: `xyz:TSLA`. |
| `perp_close` | `coin` (optional `size`, `dex`) | Reads the live position; reduce-only, correct side for longs and shorts. |

Show the user the `summary`, `warnings` and key `terms` (min received / size / margin) before asking.

## 4. Execute within the user's authority

`gdex_execute_trade { previewId, userApproved: true }` only after the user approved **that
preview**. Without `userApproved`, the account's delegated policy must allow it. The policy is a
file the user edits, `~/.gdex/policies/<accountRef>.json`:

```json
{ "expiresAt": "2026-11-01T00:00:00Z", "maxTradeUsd": 25, "maxDailyUsd": 100,
  "allowedKinds": ["spot", "perp_close"], "allowedChainIds": [8453, 622112261],
  "maxLeverage": 3, "maxSlippagePct": 2, "allowBridging": true }
```

The daily cap counts pending operations. Never write this file yourself. Results:

- `denied`: show the reasons. Don't retry with different numbers to slip under a limit.
- `revised`: the quote moved or expired. Show the new preview and get approval again.
- `submitted`: returns an `operation` (`opId`).

## 5. Follow the operation

`gdex_operation { opId }` waits (default 60 s) and reports `filled`, `failed`, `funding`,
`needs_retry` or `submission_unknown`. Spot shows each funding step; perps check the live
position.

- **`submission_unknown`**: the request may have executed. `gdex_operation` looks for it. Never
  preview and execute the same intent again until it's resolved.
- **`needs_retry`**: a dropped sell; use `usdc_retry_sell` (in-place, same nonce).
- **`pending` after the wait**: it is still settling, not failed.

## 6. Manage and exit

- `gdex_positions { accountRef }`: USDC and gas per chain, Hyperliquid positions on every DEX,
  open orders, unfinished operations. A section marked `unavailable` is unknown, not empty.
- `gdex_manage_position { accountRef, action: "close" | "reduce" | "sell", ... }` returns an exit
  preview against live state; execute it with `gdex_execute_trade`.

## Related Skills

- **gdex-usdc-wallet** — the USDC wallet underneath spot trades
- **gdex-perp-trading** — low-level Hyperliquid tools
- **gdex-hl-outcomes** — HIP-4 outcome markets
- **gdex-authentication** — manual signing (advanced)
