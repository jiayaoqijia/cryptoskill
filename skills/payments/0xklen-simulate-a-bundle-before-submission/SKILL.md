---
name: simulate-a-bundle-before-submission
description: Use when a multi-leg bundle is about to go to a builder relay and any one leg could revert and drop the whole bundle. Covers eth_callBundle, signature headers, per-leg gas, and the coinbaseDiff check against your bid.
---

# Simulate a bundle before submission

A bundle is all-or-nothing at execution, but at simulation time each leg still has to pass on the post-state the earlier legs create; if you bid without simulating, a single reverting leg silently burns the opportunity and the relay drops you.

## Procedure

1. Assemble the bundle as ordered, already-signed raw transactions. Ordering is the strategy; do not let a script re-sort across accounts.

2. Simulate against the exact target block using the relay's own simulator — a local node lacks the pending state of the pool you intend to hit:

   ```bash
   curl -s https://relay.flashbots.net -X POST -H "Content-Type: application/json" \
     -H "X-Flashbots-Signature: $FB_ADDR:$FB_SIG" \
     --data '{"jsonrpc":"2.0","id":1,"method":"eth_callBundle","params":[{"txs":["0x..","0x.."],"blockNumber":"0x'$NEXT'","stateBlockNumber":"latest"}]}'
   ```

3. Read three fields per response: `success` per leg, `gasUsed` per leg, and the top-level `coinbaseDiff` — that is the maximum tip the bundle can pay.

4. If leg B depends on state leg A writes, confirm the sim reports the sequential result. Independent `eth_call`s against `latest` do not chain state and will under-report or falsely revert.

5. Pin `blockNumber` to the block you are targeting. A simulation run at `latest` for a bundle aimed at `N+1` can succeed against reserves that the pending block has already moved.

6. Compare `coinbaseDiff` to your intended bid. If `coinbaseDiff < bid`, the bundle physically cannot pay and the relay rejects it with an opaque error rather than a partial fill.

7. Only after `success: true` for every leg and `coinbaseDiff >= bid` do you submit. Store the sim output keyed by bundle hash for the post-mortem if inclusion fails.

## Pitfalls

- Simulating on a public node. Gas and state diverge from the builder's view; a sim that passes there may revert in the real block.
- Treating `eth_estimateGas` as a revert check. It returns a number for a transaction that would succeed, but does not chain state across a multi-leg bundle.
- Ignoring the signature header. `eth_callBundle` on Flashbots returns 401 without a valid `X-Flashbots-Signature` from the searcher EOA; an unsigned call looks like an empty result.
- Bidding the full `coinbaseDiff`. Leaving zero margin means any gas-price tick in the target block turns a marginal bundle into a losing one.

## Verification

    curl -s https://relay.flashbots.net -X POST -H "Content-Type: application/json" -H "X-Flashbots-Signature: $FB_ADDR:$FB_SIG" --data '{"jsonrpc":"2.0","id":1,"method":"eth_callBundle","params":[{"txs":["0x.."],"blockNumber":"0x'$NEXT'","stateBlockNumber":"latest"}]}'

Every leg shows `success: true`, `gasUsed` is under the per-tx limit you submitted, and `coinbaseDiff` exceeds the bid. Report the bundle hash, target block, and both numbers.
