---
name: detect-indexer-stall-by-block-lag
description: Use when an indexer may have silently stopped advancing. Computes head-minus-cursor lag on a schedule and alerts when it grows, rather than trusting a process that is up but not progressing.
---

# Detect an indexer stall by block lag

A process that is running is not a process that is progressing. The alarm is the gap between the chain head and the last indexed block, sampled on a timer.

## Procedure

1. Emit two gauges every 15s: `head_block` from the provider and `cursor_block` from the indexer.
2. Alarm on the difference, not either value:
   ```promql
   (chain_head_block - indexer_cursor_block) > 50
   ```
3. Page when lag exceeds the reorg depth plus a margin (50 blocks on L1, less where blocks are fast) and has risen for 3 consecutive samples; one spike is a burst, not a stall.
4. Separate "behind" from "stuck": `rate(indexer_cursor_block[5m]) == 0` with a non-zero head means the worker died; a slow positive rate means it is merely throttled.
5. Alert on cursor staleness too: `time() - indexer_cursor_timestamp_seconds > 120`.
6. Chart the provider's head separately so a provider lag is not read as an indexer stall.
7. Emit the cursor height from the store, not from process memory, so a crash that loses in-flight progress is reflected immediately.
8. Compare lag against the same window a day earlier to separate a genuine stall from a slow-day at the chain level.

## Pitfalls

- Alerting on absolute lag fires during every network burst; gate on the trend, not the instant.
- A cursor advanced in memory but not committed shows progress that vanishes on restart; measure the persisted cursor.
- A lagging provider makes a current indexer look far behind; compare against a second provider.
- A stalled consumer of the indexer's output queue looks healthy at the indexer but starves downstream; watch queue depth too.
- Two workers sharing one cursor make the lag metric oscillate; run one writer per stream.
- Sampling lag faster than the block time produces aliased sawtooth alarms; sample at or below the block interval.

## Verification

    curl -s localhost:9090/api/v1/query --data-urlencode 'query=chain_head_block - indexer_cursor_block' | jq '.data.result[0].value[1]'
    # expect a lag that stays under the alert threshold during normal operation

Report current head, current cursor, the lag, and the cursor advance rate over the last five minutes.
