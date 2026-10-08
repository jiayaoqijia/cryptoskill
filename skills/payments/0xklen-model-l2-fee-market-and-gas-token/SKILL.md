---
name: model-l2-fee-market-and-gas-token
description: Use when estimating an L2 transaction fee or explaining an L2 fee, by decomposing it into the L2 execution component and the L1 data-availability component.
---

# Model L2 fee market and gas token

An L2 transaction pays two different markets at once — the L2's own EIP-1559 execution fee and a
pass-through of the cost of publishing the data to L1 — and quoting a single number hides which one
moved.

## Procedure

1. Identify the fee model. OP Stack charges `L2 gas × L2 base fee` plus an L1 data fee computed by the
   `GasPriceOracle` from the L1 base fee (or blob base fee), two scalars, and the signed transaction's
   RLP size. Arbitrum uses an L2 base fee plus an L1 calldata cost read from its own precompile/
   `GasPriceOracle`. zkSync and others differ again.

2. Read the oracle inputs on OP Stack:

       cast call 0x420000000000000000000000000000000000000F "l1BaseFee()(uint256)" --rpc-url $L2RPC
       cast call 0x420000000000000000000000000000000000000F "blobBaseFee()(uint256)" --rpc-url $L2RPC
       cast call 0x420000000000000000000000000000000000000F "baseFeeScalar()(uint32)" --rpc-url $L2RPC
       cast call 0x420000000000000000000000000000000000000F "decimals()(uint256)" --rpc-url $L2RPC

3. Get the L1 data fee for a specific transaction directly rather than re-deriving the formula:

       cast call 0x420000000000000000000000000000000000000F "getL1Fee(bytes)(uint256)" $SIGNED_TX_RLP --rpc-url $L2RPC

4. Compute the L2 execution fee: `gasUsed × effectiveGasPrice`, where the base fee adjusts per block
   toward a target gas usage like any EIP-1559 chain. Read the current base fee:

       cast block latest --rpc-url $L2RPC --field baseFeePerGas

5. Sum: `total = l2_execution_gas × base_fee + getL1Fee(signed_rlp)`. Note the L1 data fee is charged
   in the L2 gas token, so a rising L1 reveals itself as a rising L2 fee even with idle L2 blocks.

6. For estimation, use the node's `eth_estimateGas` and the oracle's fee, and inflate the L1 component
   for a safety margin because the RLP size is fixed but the L1 base fee at inclusion is not:

       cast estimate $TO --rpc-url $L2RPC --value $V

7. Report the decomposition explicitly (L2 portion in gwei, L1 portion in the gas token and its USD
   equivalent), never a single blended figure.

## Pitfalls

- Assuming L2 gas is cheap so the fee is cheap; on OP Stack the L1 data fee can dominate for
  calldata-heavy transactions.
- Reading `l1BaseFee` after an L1 spike but estimating against a cached value, under-quoting by a lot.
- Mixing the L1 blob base fee and the L1 execution base fee — post-Dencun chains scale by the blob
  fee, not the execution fee, and using the wrong one is off by orders of magnitude.
- Forgetting the `decimals()`/scalar scaling when hand-deriving; use `getL1Fee` instead.
- Treating the L2 gas token as always ETH; some chains use their own token, and the fee is then
  denominated in that token.

## Verification

    cast call 0x420000000000000000000000000000000000000F "getL1Fee(bytes)(uint256)" $RLP --rpc-url $L2RPC
    cast block latest --rpc-url $L2RPC --field baseFeePerGas
    # then compare against the receipt's effectiveGasPrice × gasUsed on a landed tx

Report the L2 execution fee, the L1 data fee, their ratio, and the oracle values used, each traced to
the call that produced it.
