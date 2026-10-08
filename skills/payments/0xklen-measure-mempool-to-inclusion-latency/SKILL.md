---
name: measure-mempool-to-inclusion-latency
description: Use when tuning maxBlockNumber or judging whether a route lands fast enough: measuring broadcast-to-inclusion time in blocks and seconds for public and private submission paths.
---

# Measure mempool-to-inclusion latency

The number that decides your `maxBlockNumber` and your route is how many blocks a submission takes to land, measured rather than assumed, and it differs by an order of magnitude between the public mempool and a private relay.

## Procedure

1. Stamp the broadcast: record the wall-clock epoch ms at the moment the signed transaction or bundle hits the endpoint, from the client, not from a log line elsewhere.

2. Record the inclusion: poll for the receipt and read its block number and the block's timestamp.

   ```bash
   H=$TXHASH; while true; do cast receipt $H --rpc-url $RPC 2>/dev/null | grep -q blockNumber && break; sleep 2; done
   cast block $(cast receipt $H --rpc-url $RPC --field blockNumber) --rpc-url $RPC --field timestamp
   ```

3. Compute two figures: blocks-to-inclusion (`receipt_block - head_at_broadcast`) and seconds (`receipt_ts - broadcast_ts`). Blocks is what matters for `maxBlockNumber`; seconds tells you about the route's latency.

4. Run 100 samples per route and keep the distribution, not the mean. Public mempool inclusion is bimodal — most land in block N+1, the rest stall for a fee spike — so a median of 1 block hides a p95 of 15.

5. Set `maxBlockNumber = head + ceil(p95_blocks)`. A private tx that outlives its relevance is worse than one that expires, because it can land hours later at a stale price.

6. Compare routes on the same trade size. A private RPC adds latency by design (it waits for a builder) but removes reordering; a public send is faster but exposed. Measure both before choosing.

7. Watch for the reverting-throughput case: when the chain is busy, inclusion latency for low-tip transactions jumps because blocks are full. Re-measure during a spike, not only on a quiet day.

## Pitfalls

- Measuring seconds only and ignoring blocks; a 4 s route that skips three blocks is more dangerous than a 12 s route that lands in the next one.
- Starting the clock when the client logs instead of when bytes leave the host; the transport skew is a real part of route latency.
- Assuming private equals slow. Some protected RPCs land in the next block more reliably than the public mempool.
- Polling the receipt against a lagging node, which reports a stale head and makes inclusion look later than it was.
- Taking p50 only. The tail is where stuck transactions and stale fills come from.

## Verification

    cast receipt $TXHASH --rpc-url $RPC --field blockNumber

Subtract the head at broadcast from the receipt block across 100 samples; a p95 of one or two blocks justifies a tight `maxBlockNumber`. Report p50/p95 blocks-to-inclusion and seconds per route.
