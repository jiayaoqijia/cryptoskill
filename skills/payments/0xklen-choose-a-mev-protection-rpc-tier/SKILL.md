---
name: choose-a-mev-protection-rpc-tier
description: Use when picking between protected transaction endpoints (Flashbots Protect, MEV Blocker, bloXroute, a builder-direct RPC): testing each for revert protection, refunds, bundle support, and fallback leakage before routing real flow.
---

# Choose a MEV-protection RPC tier

"Protected RPC" is a category, not a specification: the tiers differ on whether they hide you, refund you, guarantee inclusion, or silently forward to the public mempool, and only a direct test tells you which you have.

## Procedure

1. List the candidate endpoints and their claimed tier:
   - hiding only (a private send, no refund, no inclusion guarantee)
   - hiding plus refunds (orderflow auction, e.g. an MEV-Share or MEV-Blocker endpoint)
   - hiding plus revert protection (a node that drops reverting trades before broadcast)

2. Test for public-mempool fallback. Send a deliberately-reverting transaction through each endpoint and observe whether it appears in a public `txpool_content`. If it does, the endpoint leaked:

   ```bash
   curl -s $PUBLIC_RPC -X POST -H "Content-Type: application/json" \
     --data '{"jsonrpc":"2.0","id":1,"method":"txpool_content","params":[]}' | grep -c "$TXHASH"
   ```

3. Test refunds. Route a swap that is likely to attract a backrun through each auction endpoint and measure the inbound ETH in the inclusion block (see the auction-clearing skill). Zero refunds across ten tries means the auction component is inert for your flow.

4. Test inclusion reliability. For deadline-sensitive flow, submit three identical small transactions to each endpoint and record blocks-to-inclusion. An endpoint that frequently misses the next block is unsuitable even if it hides you.

5. Test bundle support. Only some endpoints accept `eth_sendBundle` directly; if you need atomic multi-leg flow, confirm the method exists before committing:

   ```bash
   curl -s $ENDPOINT -X POST -H "Content-Type: application/json" \
     --data '{"jsonrpc":"2.0","id":1,"method":"eth_sendBundle","params":[{"txs":[],"blockNumber":"0x1"}]}'
   ```

   A "method not found" means you must route bundles elsewhere.

6. Check the expiry behaviour. An endpoint that accepts `maxBlockNumber` lets you bound relevance; one that does not can hold your transaction for many blocks. Prefer endpoints that honour an expiry.

7. Score each on the four axes that matter for the flow at hand and pick per-transaction-type, not globally. Deadline liquidations need inclusion; slow rebalances want refunds.

## Pitfalls

- Assuming "protected" means no fallback. Several endpoints forward to the public mempool on a timeout, exposing exactly what you tried to hide.
- Treating the endpoint's own documentation as a test. Tiers change without a version bump; re-test after every endpoint update.
- Using an auction endpoint for latency-critical flow and missing the block because bidding took too long.
- Routing bundles to an endpoint that only accepts single transactions and silently failing.
- Forgetting that a protected RPC is a trusted third party: it sees your transaction and can itself extract.
- Not setting an expiry, so a protected transaction lands hours later at a price that no longer reflects your intent.

## Verification

    curl -s $PUBLIC_RPC -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","id":1,"method":"txpool_content","params":[]}' | grep -c "$TXHASH"

Zero hits for your submitted hash means the endpoint did not leak to the public pool. Report per endpoint: fallback (yes/no), refunds observed, blocks-to-inclusion, and bundle support.
