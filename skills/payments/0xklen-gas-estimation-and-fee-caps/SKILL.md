---
name: gas-estimation-and-fee-caps
description: Use when setting a gas limit and EIP-1559 fee caps for a transaction. Computes base fee, priority tip, and a multiplier, and handles L2 data fees and hard caps.
---

# Estimate gas and set fee caps

Underpriced transactions stall and overpriced ones burn a budget, but a gas limit below the real cost silently burns the whole fee on a revert. This skill derives a limit and a fee cap from live data and states the caps explicitly.

## Procedure

1. Read the current base fee for the next block:
   `cast base-fee --rpc-url $RPC`
2. Get a priority tip estimate rather than guessing:
   `cast rpc eth_maxPriorityFeePerGas --rpc-url $RPC`
3. Estimate the gas limit and add headroom, since state can differ from the estimate by a few percent:
   `cast estimate $TO "transfer(address,uint256)" $RECIPIENT 1000000 --from $SENDER --rpc-url $RPC`
   Multiply by 1.2 and round up. Never set the limit equal to the estimate.
4. Set `maxFeePerGas = 2 * baseFee + maxPriorityFeePerGas` so the tx survives a base-fee spike for several blocks.
5. Set `maxPriorityFeePerGas` to the tip from step 2; treat it as a hard cap, not a suggestion.
6. On Optimism, Arbitrum, Base, and other L2s, add the L1 data fee. The total cost is the L2 execution gas plus the cost to post the calldata to L1, which can dominate for calldata-heavy calls. Estimate the call; do not assume.
7. Impose a policy cap: refuse to broadcast if `maxFeePerGas` exceeds your stated ceiling (for example 200 gwei) without explicit re-approval.
8. After broadcast, verify the tx actually carries the caps you set.

## Pitfalls

- `eth_gasPrice` returns a single legacy price; using it on an EIP-1559 chain leaves the tip uncontrolled.
- A gas limit copied from a similar tx is wrong the moment the storage slots differ; always estimate the actual payload.
- Setting `maxPriorityFeePerGas` at the block's observed tip during congestion overpays; prefer a percentile estimate.
- Blob and calldata pricing changed with EIP-4844; a fee model that ignores blob gas misprices any tx that posts blobs.
- A gas limit below the estimate gives no headroom: the tx reverts and you still pay for the gas consumed.
- `block.baseFee` changes every block; a fee set from a value read twenty minutes ago is stale.

## Verification

    cast estimate $TO "transfer(address,uint256)" $RECIPIENT 1000000 --from $SENDER --rpc-url $RPC && cast base-fee --rpc-url $RPC && cast rpc eth_maxPriorityFeePerGas --rpc-url $RPC
    # expect a limit >= the estimate and a maxFeePerGas above the current base fee

Report the gas limit, the base fee, the tip, and the resulting `maxFeePerGas` cap, quoting the commands.
