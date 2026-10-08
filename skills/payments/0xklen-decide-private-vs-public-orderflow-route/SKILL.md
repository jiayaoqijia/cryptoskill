---
name: decide-private-vs-public-orderflow-route
description: Use when choosing where to send a transaction or order: public mempool, private relay, or an orderflow auction. Scores sandwich exposure, inclusion certainty, and refunds to pick the route for a given trade.
---

# Decide private vs public orderflow routing

The route is a trade-off between certainty and leakage: public flow lands fast but is visible to searchers; private flow hides you but can sit unlanded for blocks, and losing inclusion is itself a cost on a time-sensitive trade.

## Procedure

1. Classify the transaction. A time-critical liquidation or a price-moving swap needs inclusion certainty more than it needs privacy; a slow treasury rebalance has the opposite preference.

2. Estimate sandwich exposure with the impact rule: `notional / pool_depth > 0.001` and slippage tolerance above 0.5% means public routing is a leak. Below both, public is fine and simpler.

3. If exposed and time-critical, route through a relay that guarantees inclusion for a fee (e.g. a private RPC with revert protection) rather than one that only hides you. Verify the endpoint's fallback policy — some forward to the public mempool when you set no expiry, which defeats the purpose.

4. If exposed and not time-critical, use an orderflow auction. You lose latency but gain a refund; run the same trade through the auction for a week and compare realized rates to your public baseline before committing.

5. If not exposed and time-critical, just use the public mempool with a competitive tip. Privacy has no value here and adds a failure mode (stale inclusion at a moved price).

6. Quantify the inclusion risk of each private path: submit a 1 wei self-transfer through the endpoint three times and record blocks-to-inclusion. Anything above three blocks is too unreliable for a deadline trade.

7. Decide in writing: route, expected inclusion time, expected leakage, and the cost of the worst case. If the worst case (unlanded) exceeds the benefit of the route, send publicly.

## Pitfalls

- Treating "private" as a single property. Hiding a tx and guaranteeing its inclusion are different relay features, often on different endpoints.
- Routing a liquidation through a lossy private path and missing the block; the penalty is far larger than any sandwich saved.
- Using an auction for latency-sensitive flow. Bundling delays can exceed the block time, so the order misses its window entirely.
- Assuming a public RPC without a private relay is equivalent to a protected one. Plain public submission broadcasts to every searcher within milliseconds.
- Forgetting L2s: sequencer flow is already ordered, so the mainnet private/public split mostly does not apply, but priority-order auctions can still leak.

## Verification

    for i in 1 2 3; do cast send $SELF --value 0 --rpc-url $PRIVATE_RPC --private-key $PK; done; sleep 60; cast block-number --rpc-url $RPC

Compare the block at submission with the receipt block for the private sends: a spread above three blocks is unreliable for deadline work. Report route, blocks-to-inclusion, and expected leakage.
