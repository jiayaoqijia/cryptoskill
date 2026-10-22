---
name: nirium-agentic-payments
description: >-
  Scaffold and run an x402 paid API server on Stellar with open-source
  client libraries: charge AI agents per API call with x402Serve(), a
  function from the nirium SDK that runs entirely on your own server,
  scaffold that server with nirium-cli in one command, and separately
  read live protocol data through the nirium-mcp server. Use when the
  user wants to charge AI agents for API access on Stellar, needs a
  working x402 seller in minutes without hand-rolling the facilitator
  client, or wants an MCP-connected agent to read market state / control
  an autonomous loop on a running Stellar agent.
license: Apache-2.0
metadata:
  homepage: https://nirium.xyz
  repository: https://github.com/nirium-protocol/nirium-sdk
---

# Nirium: charge AI agents and read live signals on Stellar

Nirium publishes open-source client libraries for x402 agentic payments
on Stellar — a TypeScript/Python SDK, a scaffolding CLI, and an MCP
server. `x402Serve()`, the function these scaffold around, runs on
**your own server**: Nirium doesn't operate, host, or route through
anything in that path, and never sees your end users' requests. It's
not a demo — Nirium's own mainnet endpoint, running the identical
function, has been billing real USDC over x402 since 9 July 2026. A
mainnet settlement from that day, verifiable on Stellar Expert:
[`3134a51c…7558bc`](https://stellar.expert/explorer/public/tx/3134a51c66091fd7fbd85b38a4a6ec6cd432bb92c2450eac84ea7855cb7558bc).

**You're responsible for your own compliance.** `x402Serve()` is a
general-purpose library, not a service Nirium provides to your end
users — you choose what to charge for, who `payTo` is, and which
jurisdiction you operate in. You remain solely responsible for
complying with the financial, tax, and consumer-protection laws that
apply to your own use of it.

## Do this

### 1. Scaffold a paid API in one command

```bash
npm install -g nirium-cli
nirium create x402 --name my-paid-api
cd my-paid-api && npm install
```

Fill two values in the generated `.env`:

| Variable | Where it comes from |
|---|---|
| `STELLAR_PAY_TO` | the Stellar account that receives payments (`G...`) |
| `X402_FACILITATOR_API_KEY` | free — keys are per network, and the scaffold defaults `STELLAR_NETWORK` to `testnet`: [channels.openzeppelin.com/testnet/gen](https://channels.openzeppelin.com/testnet/gen) for testnet, [channels.openzeppelin.com/gen](https://channels.openzeppelin.com/gen) for mainnet |

The API key is not optional — the facilitator rejects unauthenticated
servers on both testnet and mainnet, so without it your routes never
get as far as offering a 402.

```bash
npm run dev
```

### 2. Charge per request with `x402Serve()`

The scaffolded server is about ten lines because `x402Serve()`, from the
[`nirium`](https://www.npmjs.com/package/nirium) SDK, carries the
facilitator client, the scheme registration, and the route table:

```ts
import { x402Serve } from 'nirium';

app.use('/premium', x402Serve({
    payTo: 'G...',
    routes: { 'GET /signals': '$0.02' },
}));
```

A caller without payment gets a 402 carrying the terms; one that pays
gets the data, and the USDC transfer settles on Stellar before your
handler returns. No subscription, no card, no invoice, no human in the
middle. This is the exact pattern Nirium's own mainnet endpoint runs in
production against real callers — see the devlog for a real incident
(and its fix) from operating it at scale: [docs/devlog.md](https://github.com/nirium-protocol/nirium-sdk/blob/main/docs/devlog.md).

Optional, off by default: set `NIRIUM_X402SERVE_TELEMETRY=true` if you
want to send Nirium a non-blocking usage ping (your `payTo`, a
SHA-256 hash of your `facilitatorApiKey` — never the key itself,
network, route/request counts, SDK version). It never affects a
payment either way, on or off.

### 3. Read live protocol data with `nirium-mcp`

```bash
npx nirium-mcp
```

Claude Desktop / Cursor MCP config:

```json
{
  "mcpServers": {
    "nirium": {
      "command": "npx",
      "args": ["-y", "nirium-mcp"],
      "env": { "AGENT_API_URL": "https://nirium-agent-mainnet.fly.dev" }
    }
  }
}
```

No key needed for the read-only tools below — they work against the
live mainnet agent right now:

- `get_market_state` — XLM/USDC price, SDEX spread, base fee, Blend rate, CETES rate
- `get_loop_status` — autonomous loop status, scan count, last decision
- `get_nodes` — execution nodes with live status, custody model, network
- `get_wallet_info` — the configured x402/MPP wallet and which tools are enabled

Paid tools (`get_premium_signals` $0.02, `get_premium_market` $0.05,
`execute_paid_strategy` $0.25, over x402; `get_mpp_signals` $0.02,
`get_mpp_market` $0.05, over MPP) need a funded `STELLAR_SECRET_KEY` and
are **testnet only today** — the mainnet box holds no signing key by
design, so it returns `501` rather than charging for an endpoint it
cannot serve. Don't tell a user these settle on mainnet; they do not yet.

### Alternative: scaffold a standalone signal listener (no MCP client needed)

```bash
nirium create bot --name my-agent          # TypeScript
nirium create bot --name my-agent -t py    # Python
```

Connects directly to a Nirium agent and prints incoming signals from
its autonomous loop. Defaults to the testnet agent; set `NIRIUM_API_URL`
and `NIRIUM_API_KEY` in `.env` to point elsewhere.

## Reference

- SDK + CLI + MCP source, examples: [github.com/nirium-protocol/nirium-sdk](https://github.com/nirium-protocol/nirium-sdk)
- CLI: [npmjs.com/package/nirium-cli](https://www.npmjs.com/package/nirium-cli)
- MCP server: [npmjs.com/package/nirium-mcp](https://www.npmjs.com/package/nirium-mcp)
- TypeScript SDK: [npmjs.com/package/nirium](https://www.npmjs.com/package/nirium) · Python: [pypi.org/project/nirium](https://pypi.org/project/nirium/)
- Facilitator API key (required for `x402Serve()`): [channels.openzeppelin.com/gen](https://channels.openzeppelin.com/gen)
