---
name: uniswap-v4-hooks
description: Find a Uniswap v4 hook for a problem, read its parameters and limitations, and decode what any hook address will do, using the HookForge MCP server or TypeScript SDK. Use when designing or reviewing a v4 pool with hooks.
---

# HookForge

HookForge is a catalogue of Uniswap v4 hooks (Solidity + Foundry) with a TypeScript SDK and an MCP server. The packages `@hookforge/mcp` and `@hookforge/sdk` are not on npm, so run them from a clone of https://github.com/nirholas/hookforge. Node 20 or newer.

## Build the MCP server

```bash
git clone https://github.com/nirholas/hookforge && cd hookforge
npm install
npm run build -w @hookforge/registry
npm run build -w @hookforge/mcp
claude mcp add hookforge -- node "$PWD/packages/mcp/dist/server.js"
```

No API key and no network access are needed. The catalogue ships inside the package.

## MCP tools

| Tool | Use |
|---|---|
| `search_hooks` | Describe the problem in plain language, get ranked hooks with the matched terms. Start here. |
| `list_hooks` | The whole catalogue, filterable by tag, family or chain. |
| `get_hook` | One hook in full: mechanism, prior art, `limitation`, parameters, permissions, errors, addresses. |
| `decode_hook_address` | Which callbacks Uniswap will invoke for any hook address, decoded offline from the address bits. |
| `get_deployment` | A hook's address on a chain plus that chain's PoolManager. |
| `list_chains` | Chains with a known v4 PoolManager and their ids. |

Always read the `limitation` field from `get_hook` before recommending a hook. Absence from the catalogue only means HookForge did not publish that hook, not that it is unsafe.

## SDK (`packages/sdk`, built on viem)

```ts
import { describePool, findHooks, hookAddress, loadManifest, dynamicFeePoolKey, poolId, permissionsFromAddress } from "@hookforge/sdk";

findHooks({ tag: "mev", chainId: 8453 });           // MEV hooks deployed on Base
hookAddress("depeg-shield", 42161);                  // address on Arbitrum One
const manifest = await loadManifest("depeg-shield"); // manifest.configure.fields, manifest.limitation
const key = dynamicFeePoolKey(tokenA, tokenB, 60, hookAddress("arb-tax-decay", 8453));
const id = poolId(key);                              // matches PoolIdLibrary.toId
```

`describePool(client, poolKey)` takes a viem public client and returns pool id, hook identity and catalogue entry for any v4 pool. `identifyHook(client, address)` reads `IHookMetadata` (`hookName`, `hookVersion`, `specURI`, `hookTags`). `permissionsFromAddress(address)` works offline. `formatFee(pips)` turns `3000` into `"0.30%"`.

## Contracts

```bash
npm run contracts:build   # forge build --root contracts
npm run contracts:test    # forge test --root contracts
```

## Worked example

Ask the agent: "my pool gets drained during a stablecoin depeg". Call `search_hooks` with that sentence, then `get_hook` on the top slug, read `limitation` and `configure.fields`, then `get_deployment` for the target chain.
