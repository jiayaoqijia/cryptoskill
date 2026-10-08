---
name: assess-sequencer-liveness-and-censorship
description: Use when an L2 transaction has not landed and you must decide whether the sequencer is down, lagging, or selectively censoring your transaction before retrying or escalating.
---

# Assess sequencer liveness and censorship

A stalled transaction means one of three different things — dead sequencer, degraded throughput, or
deliberate exclusion — and each demands a different response, so separate them with evidence before
resending blindly.

## Procedure

1. Establish liveness first: is the chain still producing blocks at all? Sample height twice, 30 s
   apart, against a fixed clock.

       H1=$(cast block-number --rpc-url $L2RPC); sleep 30
       H2=$(cast block-number --rpc-url $L2RPC); echo "$H1 -> $H2"

   Advancing height under a stable timestamp cadence means the chain is live.

2. Confirm block recency, not just count. Read the head block timestamp and compare it to wall clock;
   an L2 whose head is more than ~3 block times old is lagging even if height is nonzero.

       cast block latest --rpc-url $L2RPC --field timestamp

3. Distinguish "down" from "censoring". A halted sequencer produces no blocks and the mempool only
   grows. A censoring sequencer still fills blocks but omits your sender or your recipient. Test with
   a control transaction from a freshly funded throwaway key to the same contract: if the control
   lands in the next block and yours does not, localise the exclusion to your address or method.

4. Inspect what the block actually contains. Decode the last few blocks and look for a nontrivial
   count of transactions from diverse senders — an empty but advancing chain is a sequencer that
   accepts and drops.

       cast block latest --rpc-url $L2RPC --json | jq '.transactions | length'

5. Check the sequencer-feed and status endpoints. OP Stack exposes `ws://…/sequencer` and most chains
   publish a status page; an outage is usually announced there within minutes.

6. Measure L1 batch-posting freshness, the honest sign of health. If the batch poster has stopped
   writing to L1 much longer than its cadence, the L2 may be unable to settle even while producing
   blocks. Compare the latest L1 batch-inbox transaction timestamp to now.

7. Only after classifying do you act: retry with a higher tip for congestion, wait out an outage,
   or fall back to forced inclusion (see `force-include-a-transaction-through-l1-inbox`) for
   suspected censorship.

## Pitfalls

- Trusting `eth_getTransactionCount` (`pending`) as proof a tx reached the mempool; a censoring
  sequencer can accept into its pool and never include.
- Reading height from one RPC: a stale or load-balanced endpoint reports an old height that looks
  like an outage. Cross-check two independent providers.
- Calling it censorship when the sequencer is simply FCFS and under load; on OP Stack a high tip
  rarely reorders, so a "stuck" tx is usually just queued behind genuine traffic.
- Forgetting that a deposit-initiated transaction (L1 to L2) is processed in order and can lag
  behind a backlog independently of the sequencer's own health.
- Missing a chain-wide pause: some sequencers halt on upgrade or an L1 reorg of the inbox.

## Verification

    H1=$(cast block-number --rpc-url $L2RPC); sleep 30; H2=$(cast block-number --rpc-url $L2RPC)
    T=$(cast block latest --rpc-url $L2RPC --field timestamp); echo "height $H1->$H2 head_ts=$T now=$(date +%s)"
    # live if H2>H1 and now-T < ~3x block time

Report the classification (live / lagging / halted / censoring), the two heights sampled, the head
age in seconds, and the control-transaction result, each tied to the command that produced it.
