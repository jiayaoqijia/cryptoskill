---
name: account-for-l2-sequencer-mev
description: Use when reasoning about MEV on a rollup: the sequencer is the sole orderer, so extraction happens through priority queues, time-boost auctions, or outright reordering, and none of the mainnet builder economics apply.
---

# Account for L2 sequencer MEV

On a rollup the sequencer is the builder and the mempool at once, so MEV shows up as priority-fee discrimination or a time-boost auction rather than as competitive builder bids, and a mainnet searcher's mental model is wrong here.

## Procedure

1. Identify the ordering mechanism before modelling revenue. Optimism-style chains are first-come-first-served with a small priority-fee tiebreak; Arbitrum runs a first-come-first-served sequencer with a time-boost auction on some deployments; zk stacks vary. Read the chain's docs, do not assume.

2. Measure the priority fee actually needed. On FCFS chains, tipping above the minimum rarely changes order, so a large tip is pure burn:

   ```bash
   cast block latest --rpc-url $L2RPC --field baseFeePerGas
   cast receipt $TXHASH --rpc-url $L2RPC --field effectiveGasPrice
   ```

3. Test whether priority affects order: send two identical transactions from different funded accounts with different tips and see which lands first. If tip does not matter, you are on FCFS.

4. For time-boost chains, price the auction. TimeBoost-style privileges grant a small execution advantage; model it as buying the next-order slot for a window, and compare the cost against the edge it enables.

5. Check forced-inclusion latency. On an L2, a transaction the sequencer delays can be forced through the L1 inbox, but that takes the sequencer-failure window (tens of minutes to days). MEV you cannot reorder around is still extractable if you are willing to wait.

6. Separate fee revenue from ordering revenue for the sequencer. Base fee on an L2 is cheap; the sequencer's profit is mostly the ordering advantage and any auction, not the tip.

7. Never mix L1 and L2 PnL in one ledger. Gas and tip magnitudes differ by orders of magnitude, and the same strategy has completely different economics on each.

## Pitfalls

- Applying Flashbots bundle logic on an L2; there is no builder relay with `eth_sendBundle` and no bidding market in the mainnet sense.
- Tipping heavily hoping to jump the queue on an FCFS sequencer, which just burns the tip.
- Assuming the L2 mempool is private. It is operated by the sequencer, which sees everything, so MEV-Shield-style protection usually means trusting the operator rather than hiding from a public pool.
- Ignoring that some L2s post a batch to L1 with its own ordering, so an L1 reorg or reordering can disturb your L2 inclusion.
- Forgetting that cross-domain messages have their own latency, which dominates any intra-block MEV you were modelling.
- Treating a 2 s block time as more competitive; fewer searchers and lower values often make L2 opportunities less contested, not more.

## Verification

    cast block latest --rpc-url $L2RPC --field baseFeePerGas && cast receipt $TXHASH --rpc-url $L2RPC --field effectiveGasPrice

Compare the tip paid against the minimum that still lands; a persistent large gap on an FCFS chain confirms wasted tip. Report the ordering mechanism, tip paid, inclusion position, and whether an auction applies.
