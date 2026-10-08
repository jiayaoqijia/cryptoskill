---
name: initiate-a-canonical-l2-withdrawal
description: Use when moving assets from an L2 back to L1 through the canonical bridge, following the initiate-prove-wait-finalise sequence rather than a third-party bridge.
---

# Initiate a canonical L2 withdrawal

A canonical withdrawal is a three-phase protocol — initiate on L2, prove against a posted root on L1,
then finalise after the challenge window — and skipping or mis-ordering a phase means the funds sit
unclaimed on L1 until you redo it.

## Procedure

1. Initiate on the L2. For OP Stack plus ETH or an ERC-20, call the L2 standard bridge; the money is
   burned/escrowed on L2 and a message is appended to the L2-to-L1 message passer:

       cast send $L2_STANDARD_BRIDGE "withdraw(address,uint256,uint32,bytes)" \
         $TOKEN $AMOUNT 200000 0x --rpc-url $L2RPC --private-key $KEY

   Native ETH on OP Stack: send to `L2ToL1MessagePasser` (0x4200000000000000000000000000000000000016)
   via `initiateWithdrawal`.

2. Capture the withdrawal identity: the `MessagePassed` event on L2 gives the nonce, sender, target,
   value, gasLimit, data, and the `withdrawalHash`. This hash keys everything downstream.

3. Wait for an L2 output root covering your L2 block to be posted on L1. On OP Stack this is the
   `L2OutputOracle` (or the `DisputeGameFactory` under fault proofs); on Arbitrum, the rollup must
   confirm the block. No root, no proof.

4. Prove on L1 with the withdrawal and its merkle proof against that output root:

       cast send $OPTIMISM_PORTAL "proveWithdrawalTransaction((uint256,address,address,uint256,uint256,bytes),uint256,bytes32,bytes32[])" \
         "($NONCE,$SENDER,$TARGET,$VALUE,$GASLIMIT,$DATA)" $OUTPUT_INDEX $ROOT $PROOF --rpc-url $L1RPC

   Arbitrum: nothing to prove manually; the `Outbox` executes against the confirmed rollup block.

5. Wait the challenge window. OP mainnet: 604800 s (7 days). Arbitrum One: ~6.4 days (45818 L1 blocks).
   Track `provenWithdrawals[hash].timestamp`.

6. Finalise on L1:

       cast send $OPTIMISM_PORTAL "finalizeWithdrawalTransaction((uint256,address,address,uint256,uint256,bytes))" \
         "($NONCE,$SENDER,$TARGET,$VALUE,$GASLIMIT,$DATA)" --rpc-url $L1RPC

   Or `Outbox.executeTransaction` on Arbitrum. Confirm the target received the funds.

7. Record each transaction hash and the phase timestamps so the withdrawal is auditable end to end.

## Pitfalls

- Using a third-party bridge when the user asked for the canonical one (or vice versa); they have
  different trust and fee profiles. Confirm which is meant.
- Proving against an output root that is later disputed, invalidating finalisation; re-prove against
  the winning root.
- Under-estimating the L2-to-L1 message gas on the finalise call, which can revert and strand the
  proof (though it stays re-finalisable).
- Forgetting that Arbitrum withdrawals need no manual prove step but do need the rollup block to
  confirm — assuming it is instant leads to failed `Outbox` calls.
- Sending the L2 `withdraw` to the wrong bridge address (a lookalike); verify the canonical address
  from the chain's docs, not a token list.

## Verification

    cast call $OPTIMISM_PORTAL "provenWithdrawals(bytes32)(bytes32,uint128,uint128)" $WITHDRAWAL_HASH --rpc-url $L1RPC
    cast receipt $FINALIZE_TXHASH --rpc-url $L1RPC --field status   # 1 == funds released

Report the withdrawal hash, the output index and root used, the challenge-period end time, and the
finalise transaction status.
