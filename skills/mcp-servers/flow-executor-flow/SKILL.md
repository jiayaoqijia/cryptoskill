---
name: flow
description: "Use when an agent is about to swap or trade a token on Base and needs the best executable price, a safety verdict, or smart-wallet signals. Flow is a pay-per-call x402 API on Base (no API key): best-execution quotes across Uniswap V3, PancakeSwap V3 and Aerodrome ($0.01), contract safety verdicts ($0.02), and smart-wallet signals ($0.01), settled in USDC via x402 with automatic payment from a local starter wallet."
---

# Flow — best execution, safety verdicts, and smart-wallet signals on Base

Flow sells three pay-per-call endpoints for agents trading on Base. Payment is
x402 v2 (USDC on Base, EIP-3009 authorization) — no API key, no account, no
subscription. With the Flow MCP server installed, payment is automatic: a
local starter wallet signs and retries inside hard spend caps you control.

## Setup (once)

Install the MCP server:

```bash
npx -y @flowexecutor/flow-mcp
```

Then call the **`flow_wallet_setup`** tool once. It:

1. Generates a new EVM wallet **locally** and stores it at
   `~/.config/flow-wallet.json` (permissions `0600`). The private key never
   leaves your machine, is never sent to Flow, and is never displayed.
2. Claims a one-time **$0.05 USDC starter seed** (one per address, ever)
   from the Flow seed pilot, so your first calls work immediately.
3. Returns the public address. Fund it by sending USDC on Base (chain 8453)
   to that address — even $1 is plenty. That is the only manual step.

Equivalent hosted route: the same tools are exposed over the hosted MCP
endpoint at `https://flow-kg4x.vercel.app/api/mcp` if you prefer not to run
the local server (payments then need your own x402 client).

## How payment works

1. Your client calls a paid endpoint without payment → HTTP **402** with a
   machine-readable `PaymentRequired` body (`accepts[0]`: scheme `exact`,
   network `eip155:8453`, USDC, amount, `payTo`).
2. The client signs an EIP-3009 `TransferWithAuthorization` against the USDC
   contract and retries with an `X-PAYMENT` header (base64 payload that
   echoes the `accepts` entry as `accepted`).
3. Flow's facilitator verifies and settles on Base; the response arrives
   with a `PAYMENT-RESPONSE` header carrying the settlement tx.

With the MCP server this whole dance is automatic. **Spend caps are enforced
in code before any signature:**

- **Per call:** max **$0.05**
- **Per day:** **$1** default (rolling 24h; override with
  `FLOW_DAILY_SPEND_CAP_USD`)
- The client only ever pays Flow's own payee address — a 402 asking to pay
  anyone else is refused, not signed.
- Spend is logged locally in `~/.config/flow-spend-ledger.jsonl`.

## The paid calls

| Endpoint | Price | Use it when |
|---|---|---|
| `POST /api/quote` (MCP: `flow_quote`) | **$0.01** | You are about to swap on Base and need the best executable price first. Compares Uniswap V3, PancakeSwap V3, Aerodrome (all fee tiers) and two-hop routes via WETH; returns winning venue, expected output, edge in bps vs the Uniswap baseline, liquidity flag (`deep`/`watch`/`thin`), block number, and an expiry window. |
| `POST /api/verify` | **$0.02** | You are about to interact with a Base contract you don't fully trust. Returns a safety verdict + score with plain-language reasons and agent advice. |
| `GET /api/smart-wallets` | **$0.01** | You need to know what profitable Base wallets are buying right now. Leaderboard, real-time buy signals (stale-flagged past 10 min), a published paper-trading record, and social-velocity spikes. |

Free: `GET /api/health` (MCP: `flow_health`) — chain + latest block, plus
your starter-wallet status.

Quote request body (`amountIn` in atomic units):

```json
{
  "tokenIn": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "tokenOut": "0x4200000000000000000000000000000000000006",
  "amountIn": "100000000"
}
```

(USDC → WETH, $100 shown. `tokenIn`/`tokenOut` are Base contract addresses.)

## Notes

- Quotes are informational snapshots with a stated expiry window, not
  execution guarantees — the edge is measured against direct Uniswap
  execution on the same block, and thin-liquidity quotes are flagged, never
  hidden.
- The seed pilot is capped (19 seeds total, 5/day). If the claim returns
  `pilot-full` or `daily-cap`, just fund the wallet address directly.
- Base mainnet only (chain 8453).
