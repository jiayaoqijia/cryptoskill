---
name: screen-airdrop-recipients-for-sybil-clusters
description: Use when reviewing an airdrop list or designing sybil resistance: clusters wallets by funding source, timing, and behaviour, and sets thresholds to exclude farmed clusters.
---

# Screen airdrop recipients for sybil clusters

Sybil farmers are cheap to mint but expensive to make look unlinked; the giveaways are shared funding sources, near-identical amounts, and burst timing, and a cluster that shows all three (`funding_link + timing_link + behaviour_link = 3`) is almost certainly one operator.

## Procedure

1. Export the recipient set with first-funding info. For each address find who first sent it gas and when:

   cast logs --from-block 0 --address $TOKEN "Transfer(address,address,uint256)" --rpc-url $RPC

2. Build a funding graph: edges from funder -> recipient. A single funder whose out-degree exceeds 20 with small equal amounts is a faucet cluster.

3. Cluster by (funder, amount-range, day). Threshold: same funder + same amount bucket + same 24h window for >= 5 wallets is a cluster; drop it.

4. Behavioural signals: identical tx ordering, same DEX router, identical swap sizes, funding within seconds. Score = funding_link + timing_link + behaviour_link; >= 2 of 3 is sybil.

5. Weight positive signals: distinct funding paths, varying amounts, timing spread over months, real gas spend, bridge usage. Reward these rather than raw activity counts.

6. Publish the criteria and a self-report window (e.g. 48h) so false positives can appeal; keep an exclusion log keyed by cluster id.

   python3 -c "
   import collections
   funders=collections.Counter(['0xa']*6+['0xb']+['0xc']*5)
   print([f for f,c in funders.items() if c>=5])"
   ['0xa', '0xc']

## Pitfalls

- A funding-link-only filter drops legitimate users who withdraw from the same exchange hot wallet in a batch.
- Counting raw transaction counts rewards bots; a wallet with 1,000 dust txs is more farmed than one with 5 meaningful ones.
- Retroactive threshold leakage: if criteria are known before the snapshot, farmers optimise to them. Hold thresholds until after the snapshot.

## Verification

    python3 -c "
    import collections
    funders=collections.Counter(['0xa']*6+['0xb'])
    print([f for f,c in funders.items() if c>=5])"

Any funder with >= 5 recipients in the same window is flagged before manual review.

Report cluster count, excluded wallets, and the rule triggered for each.
