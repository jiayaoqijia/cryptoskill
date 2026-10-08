---
name: plan-a-sequencer-outage-failover
description: Use when a production service depends on an L2 and must keep serving reads, and fail over writes safely, while the sequencer is down.
---

# Plan a sequencer outage failover

When the sequencer stops, every L2 read still works against the frozen head but no new L2 transaction
confirms, so the plan is not "retry harder" — it is degrade reads to last-known-good with an explicit
staleness bound and route critical writes through the L1 paths that still function.

## Procedure

1. Enumerate what actually breaks. On a sequencer outage: new L2 writes stop, the mempool grows,
   L2 balances and contract state are frozen at the head, L1 to L2 deposits queue but are not
   executed, and L2 to L1 withdrawals cannot be proven until an output root is posted. L1 reads,
   L1 to L2 deposit submission, and calldata/log data all still work.

2. Put a hard staleness gate on cached reads. Record `head_ts` and serve cached values only while
   `now - head_ts < STALE_MAX`, otherwise return an explicit `stale` flag rather than silently
   showing frozen data.

       H=$(cast block-number --rpc-url $L2RPC)
       TS=$(cast block $H --rpc-url $L2RPC --field timestamp)
       age=$(( $(date +%s) - TS )); [ $age -gt 30 ] && echo "DEGRADED age=${age}s"

3. Graceful-degrade writes: reject user-initiated L2 writes with a clear message and a retry window
   instead of queueing unbounded pending transactions that will all fire on recovery.

4. Protect the recovery thundering herd. On sequencer resume, a backlog of transactions lands in
   whatever order the sequencer chooses; cap your own backlog and use idempotency keys so replays
   do not double-spend.

5. For funds that must move during an outage, use the L1 side: deposits can be submitted to the
   portal/inbox now and will execute on recovery; withdrawals escalate to forced inclusion if the
   outage exceeds the inclusion window (e.g. Arbitrum delayed-inbox forceInclusion at 24 h).

6. Never fail a read to a different chain silently. If you fall back to L1 archival state, label the
   response with its source block and chain id so downstream consumers know it is not the live L2.

7. Set an alarm on head age and on pending-pool depth so the degraded state is entered automatically,
   not discovered by a user.

## Pitfalls

- Retrying writes into a stalled mempool; the transactions pile up and all execute at once on resume,
  often at a bad price.
- Serving frozen balances as if current — an outage during a liquidation or settlement window can
  turn a stale read into a real loss.
- Assuming deposits execute during the outage; they are queued and only processed once the sequencer
  runs again.
- Hard-coding a single RPC; the outage detection must survive that endpoint also failing.
- Treating a paused/upgrading sequencer as censorship and escalating to forced inclusion too early.

## Verification

    for i in 1 2 3; do cast block-number --rpc-url $L2RPC; sleep 5; done
    # flat heights across samples => outage confirmed; service should already report status=degraded

Report the last healthy height, the head age at degrade time, whether writes were rejected or queued,
and the fallback path taken, with the sampled heights behind the claim.
