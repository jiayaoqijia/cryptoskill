---
name: reconcile-mev-pnl-across-blocks
description: Use when an off-chain MEV ledger and on-chain balances disagree over a range of blocks: tracing residuals back to missed bundles, relay refunds, and internal transfers, and closing the period.
---

# Reconcile MEV PnL across blocks

An internal ledger of "what we extracted" drifts from the chain over any period because bundles you logged as wins never landed, refunds arrived silently, and internal transfers moved value you did not record, so the two must be tied out block by block.

## Procedure

1. Fix the range and the identity. List every address the strategy controls, including the hot wallet, the funder, and any throwaway searchers, because value moves between them and a single-address view misses the net.

2. Take the on-chain net: sum balance changes across the range for every controlled address, per asset:

   ```bash
   cast balance $ADDR --block $START --rpc-url $RPC
   cast balance $ADDR --block $END --rpc-url $RPC
   ```

3. Sum the ledger: gross extracted minus builder bids minus gas, matching the line items used in per-block accounting. Convert both sides to one unit at each block's price before comparing.

4. Compute the residual: `on_chain_net - ledger_net`. A nonzero residual is not noise; it has a cause, and each block where it moved should be identified.

5. Attribute residuals in this order:
   - a bundle logged as sent but never included (ledger too high)
   - a relay or auction refund (on-chain too high, often a small ETH transfer from a contract)
   - an unrecorded internal transfer between controlled addresses (net cancels, so only a single-address view shows a gap)
   - a gas rebate or a subsidised transaction

6. Walk the blocks that carry a residual and match each to a transaction with `cast run` traces. Do not accept "rounding" — token amounts are integers, so the residual is a discrete event, not a precision artefact.

7. Close the period: adjust the ledger for the identified items, re-run the sum, and confirm the residual falls below a threshold set by base fees alone (a few dollars per address). Anything larger is an unexplained event you must name.

8. Keep the reconciliation as a saved artefact per period with the block range, addresses, both sides, and the residual. The next period's opening balance is this period's close.

## Pitfalls

- Reconciling one address. Internal transfers move value without touching the outside world, so a per-address sum shows phantom gains and losses.
- Treating a missed bundle as a cost. It is zero on-chain; if your ledger counted the expected profit, that is the residual.
- Forgetting refunds from orderflow auctions, which arrive as separate small transfers and look like unexplained income.
- Mixing assets without converting at the right block, so a price move looks like an accounting error.
- Calling a leftover amount dust. Token integers mean the residual is exact; the discrepancy is a real event.
- Ignoring gas paid from a different funder address than the one you are reconciling, which shifts the residual to the wrong side.

## Verification

    echo "on-chain net vs ledger net"; cast balance $ADDR --block $END --rpc-url $RPC

After adjusting for identified items, the residual should be within base-fee noise per address. Report the block range, addresses, on-chain net, ledger net, each attributed residual, and the final residual.
