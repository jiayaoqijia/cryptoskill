---
name: account-for-mev-revenue-per-block
description: Use when computing what a searcher actually earned in a block, separating gross extractable value from gas, bid, and failed-bundle costs. Covers the line items that turn a headline number into net revenue.
---

# Account for MEV revenue per block

A searcher's gross extractable value is not revenue: gas paid by losing legs, the builder bid, and failed attempts all come off the top, and the honest number is net of every one of them.

## Procedure

1. Start with gross extracted value from the included legs. For a backrun, it is the token delta of the searcher address between the pre-block and post-block state:

   ```bash
   cast balance $SEARCHER --block $((N-1)) --rpc-url $RPC
   cast balance $SEARCHER --block $N --rpc-url $RPC
   ```

   Read the difference in the asset you actually gained, not ETH unless you ended in ETH.

2. Subtract the builder payment. In a Flashbots bundle the payment is the `coinbaseDiff` reported by `eth_callBundle`, or the coinbase transfer visible in the block. This is the dominant cost on competitive opportunities.

3. Subtract gas. Even in a bundle, the gas burned is separate from the tip on some relay paths; on a direct `eth_sendBundle` the payment usually *is* the gas, so do not double count.

4. Add back failed attempts. Reverting bundles usually cost nothing on-chain (they are never included), but simulations, RPC calls, and the opportunity cost of capital tied up in an unlanded arb are real. Track them per strategy, not per block.

5. Reconcile with the block's own accounting: list every transaction from your address in block N and sum transfers out and in. A discrepancy means a rebate, refund, or an unaccounted internal transfer.

6. For recurring strategies, keep a per-block ledger: `gross_extracted`, `builder_bid`, `gas_paid`, `net`. Net divided by gross over 100 blocks is the take-rate; a take-rate under 0.4 means the bid curve is eating the edge.

7. Attribute by classification, not by address hygiene: label each landed bundle as arbitrage, liquidation, sandwich, or backrun so the ledger can be compared across strategy families.

## Pitfalls

- Reading gross token deltas and calling it profit. On a competitive arb the builder bid typically captures 60–90% of the gross.
- Counting a bundle's gas twice because both a receipt and a coinbase transfer are visible.
- Mixing accounting currencies. Sum only after converting to a single unit at the block's price; doing it at the day's close makes per-block comparisons meaningless.
- Omitting failed attempts. A strategy with a 30% land rate shows far lower net than its winners imply.
- Ignoring inventory risk: an arb that ends holding a volatile token has unrealized loss not in any balance difference at block close.

## Verification

    cast balance $SEARCHER --block $((N-1)) --rpc-url $RPC && cast balance $SEARCHER --block $N --rpc-url $RPC

Then reconcile the summed line items against the observed balance delta; the residual should be zero after fees. Report gross, bid, gas, and net per block, plus the rolling take-rate.
