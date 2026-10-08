---
name: attribute-l2-fee-spikes-to-l1-costs
description: Use when an L2's transaction fees spike and you must attribute the increase to L1 data costs, L2 congestion, or the gas-token price, rather than guessing a cause.
---

# Attribute L2 fee spikes to L1 costs

An L2 fee is a sum of an execution charge and a pass-through of L1 data cost, so a spike with idle L2
blocks and flat execution gas is almost certainly the L1 side — and the way to say so is to decompose
and correlate, not to eyeball one number.

## Procedure

1. Decompose a sample of real transactions into the two components. Use the oracle for the L1 portion
   and the receipt for the execution portion:

       cast call 0x420000000000000000000000000000000000000F "getL1Fee(bytes)(uint256)" $RLP --rpc-url $L2RPC
       cast receipt $TXHASH --rpc-url $L2RPC --json | jq '{gasUsed, effectiveGasPrice}'

2. Build a short time series. Poll the L2 base fee and the oracle's `l1BaseFee` (or `blobBaseFee`)
   every block or every minute for the window under investigation, and store (ts, l2_base_fee,
   l1_base_fee, blob_base_fee, pending_txs):

       for i in $(seq 1 60); do
         printf '%s %s %s %s\n' "$(date +%s)" \
           "$(cast block latest --rpc-url $L2RPC --field baseFeePerGas)" \
           "$(cast call 0x42...0F 'l1BaseFee()(uint256)' --rpc-url $L2RPC)" \
           "$(cast call 0x42...0F 'blobBaseFee()(uint256)' --rpc-url $L2RPC)"
         sleep 60
       done
   (resolve the `0x42...0F` placeholder to the real GasPriceOracle address for the chain).

3. Test the L2-congestion hypothesis: if the L2 base fee rose because the chain was busy, L2 block gas
   usage or the pending count should be elevated in the same window.

       cast block latest --rpc-url $L2RPC --json | jq '{gasUsed, gasLimit}'

4. Test the L1 pass-through hypothesis: correlate the L2 L1-data-fee component with the L1 base fee
   (or blob base fee). A rising L1 fee with a flat L2 execution component confirms the pass-through.

5. Check the gas-token price separately. L2 fees are denominated in the gas token; a fiat-denominated
   spike with a flat gas-denominated fee is a price move, not a fee move.

6. State the finding as a decomposition with a confidence level and the evidence series, and explicitly
   say when two causes are indistinguishable (e.g. L1 and L2 both rising) rather than picking one.

## Pitfalls

- Asserting "the L2 is congested" from a high fiat fee; convert to gas and to the L1/L2 split first.
- Correlating on a handful of points and calling it causation; use a window long enough to include a
  non-spike period.
- Reading `l1BaseFee` after Dencun without checking whether the chain now scales by `blobBaseFee`; the
  wrong input gives a nonsensical split.
- Ignoring the fixed per-transaction L1 cost that dominates small transactions, which can make a whole
  cohort look expensive for reasons unrelated to the spike.
- Assuming the fee oracle updates instantly; there is a lag between an L1 change and the L2 fee
  reflecting it, so align the series with that lag.

## Verification

    # two-point decomposition around the spike, both components
    cast call 0x420000000000000000000000000000000000000F "getL1Fee(bytes)(uint256)" $RLP --rpc-url $L2RPC
    cast block latest --rpc-url $L2RPC --field baseFeePerGas
    # correlate the L1-fee series against the L1 base-fee series over the window

Report the decomposed fee before/after the spike, which component moved, the correlation basis, and
the confidence — with the series length and sources noted.
