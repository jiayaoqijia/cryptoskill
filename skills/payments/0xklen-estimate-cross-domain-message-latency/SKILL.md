---
name: estimate-cross-domain-message-latency
description: Use when an SLA or retry budget depends on how long an L1-to-L2 or L2-to-L1 message takes, which differs by orders of magnitude by direction.
---

# Estimate cross-domain message latency

L1 to L2 is fast — minutes — while L2 to L1 waits out the rollup's settlement and challenge window,
so a single "cross-chain latency" number is always wrong in one direction.

## Procedure

1. Split by direction before estimating anything.
   - L1 to L2 (deposits, retryables): bounded by L2 block times once the sequencer is healthy —
     roughly a minute to minutes on OP Stack, and ~10 minutes to create-and-execute on Arbitrum.
   - L2 to L1 (withdrawals, `sendTxToL1`): must wait for the output/assertion to post on L1 and then
     the challenge window before a claim — 7 days (OP) or ~6.4 days (Arbitrum).

2. Read the settlement cadence, which governs the L2-to-L1 leg more than any fixed constant:

       cast call $L2_OUTPUT_ORACLE "L2_BLOCK_TIME()(uint256)" --rpc-url $L1RPC
       cast logs --address $L2_OUTPUT_ORACLE "OutputProposed(bytes32,uint256,uint256,uint256)" --rpc-url $L1RPC --from-block $RECENT

3. For a live message, measure rather than model: take the source `SentMessage` (or deposit) event
   timestamp and the destination execution timestamp, and subtract.

       case: src_ts=$(cast receipt $SRC_TX --rpc-url $SRC_RPC --field blockNumber) -> block timestamp
             dst_ts=$(cast receipt $DST_TX --rpc-url $DST_RPC --field blockNumber) -> block timestamp
       latency = dst_ts - src_ts

4. For a budget, use the pessimistic branch. L1 to L2 under a healthy sequencer is minutes, but under
   an outage it is the forced-inclusion window (Arbitrum delayed inbox 24 h). L2 to L1 is always at
   least the challenge period unless you use a third-party bridge with its own liquidity model.

5. Convert block-counted windows to time with the live L1 block time, not the nominal 12 s, and fold
   in the source-chain confirmation requirement (an L1 message is not actionable until it is final
   enough for the bridge's config).

6. Present a table: direction, mechanism, best-case, expected, worst-case, and the on-chain parameter
   backing the window. Mark any figure you pulled from docs rather than chain.

## Pitfalls

- Reusing the L1-to-L2 number for L2-to-L1; the challenge window dominates and the estimate is off by
  a week.
- Assuming L1-to-L2 is instant because deposits "always work" — during a sequencer outage they queue.
- Measuring a warm sample that happened to post right before an output root landed and reading that as
  typical; the challenge window still applies to L2-to-L1.
- Ignoring that a fast third-party bridge quotes minutes precisely because it is not the canonical
  path and carries its own trust cost.
- Forgetting source-chain finality before the destination processes the message.

## Verification

    SRC_TS=$(cast block $(cast receipt $SRC_TX --rpc-url $SRC_RPC --field blockNumber) --rpc-url $SRC_RPC --field timestamp)
    DST_TS=$(cast block $(cast receipt $DST_TX --rpc-url $DST_RPC --field blockNumber) --rpc-url $DST_RPC --field timestamp)
    echo "latency_seconds=$((DST_TS - SRC_TS))"

Report the direction, the best/expected/worst case with the on-chain window source, and the measured
latency for any live message — labelled measured versus modelled.
