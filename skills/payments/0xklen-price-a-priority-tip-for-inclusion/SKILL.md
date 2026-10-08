---
name: price-a-priority-tip-for-inclusion
description: Use when choosing the priority fee for a transaction that must land in a given block: predicting base fee, reading recent blocks for the clearing tip, and setting a tip that wins without overpaying.
---

# Price a priority tip for inclusion

The tip is what actually buys inclusion — base fee is burned and only proves you are solvent — so the correct tip is the smallest value above the block's observed clearing tip for the share of gas you are willing to occupy.

## Procedure

1. Predict next-block base fee rather than reading the current one. EIP-1559 moves base fee by at most 12.5% per block, so a block that is running hot means the next base fee is higher:

   ```bash
   cast block latest --rpc-url $RPC --field baseFeePerGas
   cast block latest --rpc-url $RPC --field gasUsed
   ```

   If `gasUsed == gasLimit`, the next base fee is `base * 1.125`. Use that as the floor, not the current value.

2. Read the clearing tip from the last 10 blocks by looking at the effective priority fee of transactions that occupy similar gas:

   ```bash
   cast block <N> --rpc-url $RPC --field transactions --json | \
     jq '[.[] | .maxPriorityFeePerGas] | sort | .[length*0.5|floor]'
   ```

3. Target a percentile, not the mean. To reliably beat other bidders for the same block, price at roughly the 70th–80th percentile of observed tips; the mean is dragged down by many low-tip inclusions that are cheaper than yours cannot be.

4. Add an escalator only if latency is your real constraint: a generous `maxPriorityFeePerGas` with a tight `maxFeePerGas` lets you bid high without the base-fee risk of a runaway total.

5. Sanity-check the total cost against the value of the transaction. If the tip plus base fee approaches the profit, lower the tip and accept a later block rather than paying for the current one.

6. On L2s, replace this entirely: sequencers usually run first-come-first-served or a fixed priority, so a huge tip buys nothing and burns L2 gas. Check the chain's fee model before applying mainnet logic.

7. After inclusion, compare the paid effective tip to the block's clearing tip; a persistent gap above 30% means your estimator is stale.

## Pitfalls

- Using the mean tip. It is pulled down by many small, cheap inclusions and systematically underprices a competitive block.
- Setting `maxFeePerGas` equal to `base * 1.125` exactly. One hotter block and the transaction is stuck, because a growing base fee can exceed it.
- Ignoring gas share. A transaction that consumes 5M of a 30M block competes for a scarce resource and needs a higher tip than a 21k transfer.
- Treating a private relay bid as a tip. When routing through a bundle, the bid is the whole payment; the tip field is mostly a formatting detail.

## Verification

    cast block latest --rpc-url $RPC --field baseFeePerGas && cast block latest --rpc-url $RPC --field gasUsed

Compute the predicted next base fee and confirm the submitted `maxFeePerGas` clears it with margin, while `maxPriorityFeePerGas` sits above the recent median. Report predicted base fee, chosen tip, and inclusion block.
