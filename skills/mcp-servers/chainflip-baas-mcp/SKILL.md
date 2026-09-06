---
name: chainflip-swap
description: >
  Execute native cross-chain cryptocurrency swaps via Chainflip Broker as a Service.
  Trigger whenever the user wants to swap, exchange, trade, convert, move, or bridge
  crypto across chains: BTC, ETH, SOL, DOT, TRX (Tron), USDC, USDT, FLIP. These are
  real Layer-1 assets, no wrapped tokens and no bridges. Patterns: "swap BTC for ETH",
  "convert my SOL to USDC", "move DOT to Tron", "get a quote for 1 BTC to ETH",
  "DCA 5000 USDC into BTC", "what's the rate", "start a swap", "check my swap status",
  "where do I send my Bitcoin". Also triggers for status checks: "is my swap done",
  "track swap <id>", "swap stuck". If the user names any of these assets with intent
  to move or trade them, use this skill.
license: MIT
metadata:
  author: Chainflip Broker as a Service
  homepage: https://chainflip-broker.io
  version: "0.1.0"
---

# Chainflip BaaS, native cross-chain swap

Swap real Layer-1 assets across chains through a Chainflip broker. No wrapped tokens,
no bridge contracts, no smart-contract approvals, no gas wiring on the agent side. The
flow is: quote, start a swap to get a deposit address, send the source asset to that
address, monitor to completion.

## Why this is simpler than a bridge or DEX skill

Chainflip uses a deposit-address model. `start_swap` returns an address on the source
chain. The user (or their wallet) sends the source asset there and the swap settles
natively to the destination address. The agent never builds, approves, or signs an
on-chain transaction. There is nothing to wire to a wallet or a signer.

## MCP availability check

This skill drives the Chainflip BaaS MCP server.

1. Call `list_assets` (no parameters).
2. If it returns asset data, the MCP server is connected. Continue.
3. If the tool is not found, connect the remote server, then restart the session:
   - Claude Code (CLI): `claude mcp add --transport http chainflip-baas https://chainflip-broker.io/mcp`
   - Config file (Claude Desktop, Cursor, OpenClaw mcporter, Hermes):
     ```json
     {
       "mcpServers": {
         "chainflip-baas": {
           "type": "url",
           "url": "https://chainflip-broker.io/mcp"
         }
       }
     }
     ```

No API key is required to swap. Provide one only to earn broker commission (see below).

Tool names below assume the server is registered as `chainflip-baas`. In some clients the
tools appear namespaced, for example `mcp__chainflip-baas__start_swap`.

## Supported assets

Native L1 assets only: BTC, ETH, SOL, DOT, TRX (Tron), USDC, USDT, FLIP. USDC and USDT
exist on multiple chains, so asset identifiers use the form `<ticker>.<network>`, for
example `btc.btc`, `eth.eth`, `sol.sol`, `dot.dot`, `usdc.eth`, `usdt.tron`. Always call
`list_assets` first to get the exact identifiers and which chains are enabled.

## Swap workflow

### Step 1, discover assets
Call `list_assets`. Record the exact source and destination identifiers and confirm both
are enabled.

### Step 2, quote
- Human-readable amounts: `get_quotes` with e.g. `1.5` for 1.5 BTC.
- Native units: `get_native_quotes` with e.g. `150000000` for 1.5 BTC in satoshis.

Present the estimated output, rate, and fees to the user before starting.

### Step 3, start the swap
Call `start_swap` with:
- `sourceAsset`: e.g. `btc.btc`
- `destinationAsset`: e.g. `eth.eth`
- `destinationAddress`: recipient on the destination chain (validated server-side)
- `refundAddress`: address on the source chain, used if the minimum price cannot be met
- `minimumPrice` (optional): destination-per-source ratio. For `btc.btc` to `eth.eth`, `28.5`
  means 1 BTC gets at least 28.5 ETH. Omit to auto-calculate from pool prices with 2%
  slippage. `0` accepts any price.
- `apiKey` (optional): partner key to attribute the swap and earn commission.

The response contains the deposit address on the source chain and a swap ID.

For a chunked, Dollar-Cost-Averaging swap, call `start_dca_swap` instead. It takes the same
inputs plus chunking parameters, inspect the tool schema for the exact fields.

### Step 4, send funds
Instruct the user to send the source asset to the returned deposit address. This is a plain
native send, no approval or contract interaction. If the swap cannot meet the minimum price,
funds are returned to `refundAddress`.

### Step 5, monitor
Call `check_status` with the swap ID. Report progress through its stages (Waiting, Receiving,
Swapping, Sending, Sent, Completed) until the destination-chain egress completes.
`check_status` needs no API key and can be called by anyone holding the ID.

## Earning commission (optional)

Chainflip BaaS lets the integrator keep the broker commission on every swap. If the agent
operator has a partner key (register at https://chainflip-broker.io), pass it as `apiKey` on
`start_swap` or `start_dca_swap` to attribute the swap and earn. Omitting the key routes
through the anonymous house broker. A wrong key fails loudly rather than silently degrading.

## Guidance prompt

The server exposes a `swap-assistant` prompt with detailed workflow guidance. Load it if the
client supports MCP prompts and you need the full decision tree.

## Support

Start with the docs, then reach a human if needed:

- Documentation (self-serve, start here): https://chainflip-broker.io/ai
- Website (register for an optional partner key): https://chainflip-broker.io
- Report a bug or ask a question: https://github.com/CumpsD/broker-as-a-service/issues
- X: https://x.com/ChainflipBaaS

## Common issues

| Symptom | Cause | Fix |
| --- | --- | --- |
| "Unknown Source/Destination Asset" | wrong identifier | call `list_assets`, use the exact `<ticker>.<network>` id |
| "Invalid Destination Address" | address not valid for the destination chain | re-check the recipient address |
| "Source/Destination Asset not enabled" | asset temporarily disabled | pick another route or retry later |
| swap not progressing | funds not yet sent or still confirming | verify the send to the deposit address, keep polling `check_status` |
| "Invalid API key" | wrong partner key | omit the key or supply a valid one |

---

Verified against the live server (`https://chainflip-broker.io/mcp`, serverInfo "Broker as a
Service" v1) on 2026-07-23. Real funds move on `start_swap` and `start_dca_swap`, treat every
call as irreversible.
