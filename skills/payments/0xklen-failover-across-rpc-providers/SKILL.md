---
name: failover-across-rpc-providers
description: Use when a workflow depends on a single RPC endpoint and you need redundancy that does not silently serve stale or forked data.
---

# Fail over across RPC providers

Two endpoints are not redundancy if one is behind or forked. Rank providers by health, detect
divergence explicitly, and fall back on failure without hiding the fact that you did.

## Procedure

1. Keep an ordered list of endpoints across independent operators (Alchemy, Infura, QuickNode,
   Ankr, a public node, or your own Erigon/`reth`).

       RPCS="https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_KEY \
             https://mainnet.infura.io/v3/$INFURA_KEY \
             https://rpc.ankr.com/eth \
             https://ethereum-rpc.publicnode.com"

2. Health-check each before use: chain id, head height, and head age.

       for u in $RPCS; do
         printf '%s chainid=%s head=%s\n' "$u" \
           "$(cast chain-id --rpc-url $u)" \
           "$(cast block-number --rpc-url $u)"
       done

3. Validate that every endpoint reports the *same hash* at the same height. Divergence means a
   fork, a stale node, or a lying endpoint — drop the minority.

       H=$(cast block-number --rpc-url "$(echo $RPCS | awk '{print $1}')")
       for u in $RPCS; do echo "$u $(cast block $H --json --rpc-url $u | jq -r .hash)"; done

4. In application code, use viem's ranked fallback transport so a failing endpoint is demoted
   and the fastest healthy one is preferred:

       import { createPublicClient, fallback, http } from 'viem'
       const client = createPublicClient({
         transport: fallback(
           [http(a), http(b), http(c)],
           { rank: { interval: 30_000, sampleCount: 5 }, retryCount: 2 },
         ),
       })

5. In scripts, wrap the call in a loop that rotates the endpoint on error and logs which one
   answered, so a silent failover is visible in the output.

## Pitfalls

- A provider returning HTTP 200 with a JSON-RPC error, or worse a stale block, does not raise
  an exception; only an explicit hash comparison catches a lagging node.
- Quotas are per-provider and not shared: a fallback list multiplies your effective rate-limit
  headroom but also means rate-limit errors must be distinguished from outage errors.
- Load-balanced RPC DNS names (e.g. free public gateways) can route each request to a different
  backend, so two calls in one logical operation may hit different heights — pin a block number
  for multi-call reads.
- Different providers compute gas estimates and `eth_call` return data slightly differently on
  state-changing edge cases; never mix providers within one simulation.
- Silently switching to a second endpoint can mask a real outage; log the switch with a warning.

## Verification

    for u in $RPCS; do cast block $H --json --rpc-url $u | jq -r .hash; done
    # all lines identical, and head ages under ~30s

Report each endpoint, its head height, and whether hashes agree; state which endpoint answered
the final call.
