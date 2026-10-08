---
name: check-node-health
description: Use when you are about to trust an RPC endpoint (your own node or a provider) and need to know it is live, synced, on the right chain, and not serving stale or forked data.
---

# Check node health

An endpoint can answer every call correctly and still be wrong: lagging behind the head, on a
different chain, or serving a fork. Check chain id, sync state, head height, head age, and
agreement with a second provider before relying on it.

## Procedure

1. Confirm the chain identity. A mismatch means every address and block number you have is for
   a different network.

       cast chain-id --rpc-url $RPC            # 1 mainnet, 11155111 sepolia, 10 optimism, 8453 base
       cast rpc net_version --rpc-url $RPC

2. Check sync status. `eth_syncing` returns `false` when caught up; an object means it is
   still syncing and its head is unusable.

       cast rpc eth_syncing --rpc-url $RPC

3. Compare head height and head age against wall-clock. Mainnet targets 12s blocks; a head
   timestamp more than ~30s old means the node is behind.

       cast block-number --rpc-url $RPC
       TS=$(cast block latest --json --rpc-url $RPC | jq -r .timestamp)
       echo $(( $(date +%s) - TS ))        # seconds behind, want < 30

4. Identify the client and version (useful for known bugs and feature support):

       cast rpc web3_clientVersion --rpc-url $RPC

5. Cross-check the head hash with a second, independent endpoint at the same height. A
   mismatch is a fork or a lagging node.

       H=$(cast block-number --rpc-url $RPC)
       cast block $H --json --rpc-url $RPC       | jq -r .hash
       cast block $H --json --rpc-url $RPC2      | jq -r .hash

6. Confirm the node serves the data classes you need — state history (archive) or logs — not
   just the head.

       cast logs --from-block $((H-10)) --to-block $H --address $ANY_TOKEN \
         "$(cast keccak 'Transfer(address,address,uint256)')" --rpc-url $RPC | head

## Pitfalls

- Some clients return `eth_syncing: false` even while behind if they are in "snap sync" late
  stage; the timestamp check catches what the sync flag misses.
- A load-balanced provider URL can route each request to a different node, so two calls in one
  operation may observe different heights; pin a block number for multi-call reads.
- Correct `chainId` does not prove you are on the canonical chain — a node on a minority fork
  reports the right chain id with wrong blocks. Only the second-provider hash check catches it.
- `ws://` and `http://` endpoints of the same provider can be served by different backends with
  different heads.
- Public endpoints are frequently rate-limited, not down; a fast error may be a quota issue, not
  a health problem (see `handle-rpc-rate-limits`).

## Verification

    cast chain-id --rpc-url $RPC               # expected id
    echo $(( $(date +%s) - $(cast block latest --json --rpc-url $RPC | jq -r .timestamp) ))
    # head age under 60s

Report the chain id, client version, head height, head age in seconds, and whether the head
hash matches a second provider.
