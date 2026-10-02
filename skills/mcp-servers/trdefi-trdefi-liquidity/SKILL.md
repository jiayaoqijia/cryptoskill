---
name: trdefi-liquidity
description: Live non-custodial stablecoin liquidity for AI agents. Use when an agent needs to find real USDC/USDT maker positions to trade against, quote a stablecoin swap on-chain at the current block, or earn swap fees on idle stablecoins without moving custody. Covers listing positions, quoting a swap, and reading settled volume across 20 networks (Ethereum, Base, Arbitrum, Optimism, Polygon, BNB Chain and 14 more). Read-only tools are free and need no key.
license: MIT
---

# TRDEFI Liquidity

Live, non-custodial stablecoin liquidity, exposed as a remote MCP server at
`https://yield.trdefi.com/mcp`.

## When to use this

Use it when an agent needs to:

- Find a **real on-chain counterparty** for a stablecoin swap, instead of a custodial venue.
- **Quote** a USDC/USDT swap against a maker position at the current block, before committing to anything.
- See where **stablecoin liquidity** actually sits across chains, with settled volume.
- Understand how a treasury can **earn swap fees on idle stablecoins without depositing them anywhere**:
  the funds stay in the holder's own wallet, backed by a bounded, revocable allowance.

## When not to use this

- It is not a price oracle for arbitrary tokens. Positions are stablecoin pairs.
- It does not sign or broadcast anything. Nothing here can move a wallet's funds.
- It is not a yield aggregator. It reports positions that exist; it does not rank or recommend them.

## Tools

| Tool | Use it for |
|---|---|
| `trdefi_stats` | Aggregate counts and settled volume over 1, 7 and 30 days. Start here to check the venue is alive. |
| `trdefi_chains` | Which networks are live, their settlement engine address, and the tokens a position can be built from. Use this instead of hardcoding chain or token identifiers. |
| `trdefi_positions` | List open maker positions. Filter by network and pair. Each row carries the strategy hash, network, pair, tokens and settled volume. |
| `trdefi_position_detail` | One position in full, by its 32-byte strategy hash. |
| `trdefi_quote` | Price a swap against one position, on-chain, at the current block. |
| `trdefi_badge` | A shields.io payload for the catalogue metrics, for a README. |

All six are **read-only** and require **no API key**.

## Working with quotes

A maker may gate a position on the caller holding an access licence token, and roughly four in five do.
Those positions answer with a clear reason instead of a price. **That is a property of the maker's
strategy, not an error** — treat it as a signal to try a different position rather than a failure to
retry.

Each position carries a `quote_eligible` flag (USDC/USDT and router-attached). `GET
/api/strategies?quote_ready=true` returns only the positions the router can price, so a quote attempt
starts from a candidate that can actually answer.

## Prepare endpoints

Outside the MCP surface, two HTTPS endpoints prepare unsigned transactions:

- `POST /v1/positions` — the transactions that create a maker position.
- `POST /v1/swaps` — the transaction that executes a swap.

Both answer **HTTP 402** with their payment terms when unpaid, and settle USDC on Base
(`eip155:8453`) at **$0.02 per request**, so an agent needs no account and no API key. An API key is
accepted as an alternative. **The transactions are unsigned**: the caller signs and broadcasts with its
own wallet, and TRDEFI cannot sign on the caller's behalf.

The service is x402-native — discovery is free, execution is metered — and is listed in the **x402
Bazaar** (the CDP catalogue), so agents that discover services through the Bazaar find it with no
registration.

## What TRDEFI does not do

It never takes custody, never holds funds, and never signs. A position is backed by a bounded,
revocable on-chain allowance (a plain ERC-20 `approve` — no deposit, no permit required), so exit is
one transaction: dock and revoke.
