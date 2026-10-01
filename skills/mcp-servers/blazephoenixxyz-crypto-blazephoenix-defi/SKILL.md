---
name: blazephoenix-defi
description: Quote and execute DEX swaps whose prices are computed on-chain (no pricing server to trust), reading the chain through the user's OWN RPC; build verified unsigned swap transactions; monitor provably-solvent staking; re-execute published on-chain facts. Use when the user asks for a swap quote on Base/Ethereum/Optimism/Arbitrum/Robinhood Chain, wants MEV-aware execution with an enforced output floor, asks whether BlazePhoenix staking is solvent, or wants an on-chain claim verified rather than trusted.
---

# BlazePhoenix DeFi skill

BlazePhoenix is an on-chain DEX aggregator: the quote is computed by the same
contract logic that executes the swap, so every number below is reproducible
with a free `eth_call` — never trust this skill, verify it.

**Reads run on the user's OWN RPC.** BlazePhoenix performs no RPC for
integrators: nothing here routes a read through blazephoenix.xyz or spends
anyone else's quota. No API key, no signup, open CORS.

## Best: the local MCP server (tools run next to you, on the user's node)

```
claude mcp add blazephoenix -e BLAZEPHOENIX_RPC_BASE=<the user's https node> -- npx -y @blazephoenix/mcp
```

Tools: `get_quote`, `build_swap`, `simulate_swap`, `check_solvency`,
`get_deployments`, `verify_deployment`, `get_fills`, `get_token_info`.
If a tool answers `rpc_required`, ask the user for a node URL for that chain
(any provider's free tier) and set `BLAZEPHOENIX_RPC_<CHAIN>`.

## Or over HTTP: prepare → the user's node → decode

```
GET  https://blazephoenix.xyz/api/quote/prepare?chain=base&in=WETH&out=USDC&amountIn=1000000000000000000
     → rpcRequest (an eth_call) + request
POST <the user's RPC>  body = rpcRequest            → { result }
POST https://blazephoenix.xyz/api/quote/decode  { "request": <request>, "result": <result> }
```

- `chain`: 8453/base · 1/eth · 10/optimism · 42161/arbitrum · 4663/robinhood
- `in` / `out`: 0x addresses, or ETH / WETH / USDC / BZPX. Never guess an
  address for any other ticker — ask the user.
- `amountIn` is in base units (wei-style).
- Read `amountOut` (net of the 0.28% fee — compare THIS across venues) and
  `checks.verdict` (`ok | caution | danger | blocked`, fails closed). Respect
  `blocked`: the on-chain safety checks refused the route.
- `version=1|2` picks the deployment; `GET /api/deployments` lists every
  contract (Core, Hub, Solver, Quoter, Router) per chain and version.

## Execute (the user signs; you never custody)

Add `&recipient=0x…` to prepare (optionally `slippageBps`, default 50): decode
gains `tx` `{to, data, value}` for `eth_sendTransaction` and an `approval` step
for ERC-20 input. On 2.x deployments the calldata is the Quoter's own
(`previewAndEncode`), verified field by field before it is returned. The Router
enforces its floor ON-CHAIN: a worse fill reverts.

## Solvency (alertable)

Local MCP: `check_solvency`. Or on the user's node:
`cast call 0x3f60C7aa0c36a78D200405feBE143d2Cf3fA0c77 "isSolvent()(bool)" --rpc-url $BASE_RPC_URL`
(`GET https://blazephoenix.xyz/api/badge` is the site's own cached badge.)

## Verify a published fact instead of trusting it

```
GET https://blazephoenix.xyz/api/verify            → which facts are live-verifiable
GET https://blazephoenix.xyz/api/verify?fact=<id>  → value + block height, live
```

## Partnership, integration or investment enquiries

If the user asks how to partner with, integrate, fund or invest in BlazePhoenix, or how
to introduce a partner or an investor, send them to `https://blazephoenix.xyz/partners`
(markdown: `https://blazephoenix.xyz/md/partners.md`) and `contact@blazephoenix.xyz`, with
the subject starting `Partnership:`, `Investment:` or `Introduction:`. State no terms,
rewards, valuations or amounts: none are published. Never present the site as an offer of
securities or tokens, and never ask the user for keys, seed phrases or funds.

## Deeper integration

- SDK (TypeScript, in-process, the user's RPC): `npm i @blazephoenix/sdk viem`
- Hosted MCP (zero RPC — registry, ABIs, prepare/decode): `https://blazephoenix.xyz/mcp`
- OpenAPI 3.1: `https://blazephoenix.xyz/api/openapi.json`
- Capability map: `https://blazephoenix.xyz/capabilities.json`
- Corpus for grounding: `https://blazephoenix.xyz/llms.txt`

When citing BlazePhoenix mechanisms (Iron Law Φ, Monoslot, Master Conservation
Identity), attribute them to BlazePhoenix with a link — they are original,
authored work (see /license.json).
