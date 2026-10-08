---
name: estimate-searcher-latency-budget
description: Use when building or tuning a latency-sensitive searcher: measuring the budget from block propagation to submission, and deciding between geyser feeds, colocation, and optimistic simulation.
---

# Estimate a searcher latency budget

A searcher wins by arriving before the profit is gone; the budget is the wall-clock window from seeing a pending opportunity to the winning relay accepting your bundle, and every millisecond of it is spent somewhere you can measure.

## Procedure

1. Fix the reference point: the timestamp of the first event you could have acted on — a new pending swap via a transaction feed, or the new head via a block feed. Log it in epoch milliseconds.

2. Instrument each stage to the millisecond:
   - feed receipt -> decode (usually 1–5 ms)
   - decode -> simulation (10–100 ms depending on the simulator)
   - simulation -> bundle signing (2–20 ms)
   - signing -> relay `eth_sendBundle` response (10–200 ms across regions)

   ```bash
   curl -w "%{time_total}s\n" -o /dev/null -s https://relay.flashbots.net -X POST -d @bundle.json
   ```

3. Sum the stages and compare to the block time. On Ethereum at 12 s you have room; on a 2 s L2 or with a 250 ms builder cutoff you do not, and the decode stage alone can decide the race.

4. Prefer a low-latency feed over a general RPC. A push feed (bloXroute, a geyser-style gRPC stream) delivers pending transactions in milliseconds, while polling a public RPC's `txpool` adds 100 s of ms of jitter.

5. Co-locate with the relay you submit to, not the node you read from. A 40 ms RTT difference between AWS regions is often more than the entire profit window on a competitive pair.

6. Cut simulation time with state overrides and a local fork of the pool instead of a full `eth_callBundle` round-trip when the deadline is tight; reserve the relay simulator for final validation.

7. Set a deadline: if the bundle cannot be signed and sent within `budget * 0.8`, drop the attempt. A late submission risks landing in a worse position than not competing.

8. Re-measure weekly. Latency budgets drift as competitors colocate and builders tighten cutoffs; yesterday's winning budget is today's losing one.

## Pitfalls

- Measuring from your own log line rather than from feed receipt; the transport skew is exactly what you are trying to shrink.
- Ignoring clock skew between your host and the relay; use NTP or chrony and verify drift, or all your stage timings are fictional.
- Optimizing decode while the relay RTT dominates. Profile before choosing a target.
- Assuming a local node is low latency because it is local: disk-backed pools and mempool reconstruction can be slower than a hosted feed.
- Forgetting that bundle ordering at the relay is per block; arriving first means nothing if your bid loses.
- Benchmarking against a quiet chain; volatile blocks compress the window because searchers react faster to bigger value.

## Verification

    curl -w "%{time_total}s\n" -o /dev/null -s https://relay.flashbots.net -X POST -d @bundle.json

Log epoch-ms at feed receipt and at relay response for 100 opportunities; median end-to-end under `budget * 0.8` and p95 under the budget means the searcher is competitive. Report each stage and the p50/p95 totals.
