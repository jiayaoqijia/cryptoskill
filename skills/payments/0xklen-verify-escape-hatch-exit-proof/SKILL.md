---
name: verify-escape-hatch-exit-proof
description: Use when validating that a withdrawal or exit proof against an L1 bridge contract is well-formed and matches the canonical L2 state before you trust or submit it.
---

# Verify an escape hatch exit proof

A proof is only worth the root it is checked against, so verify in this order: recompute the leaf from
the message, rebuild the root from the branch, and confirm that root is the one the L1 contract
actually recognises — a locally valid proof against a stale or disputed root is a trap.

## Procedure

1. Recompute the withdrawal leaf exactly as the bridge contract hashes it. Getting the field order or
   abi-encoding wrong makes a valid proof fail. For OP Stack:

       # leaf = keccak256(abi.encodeWithSignature("WithdrawalTransaction(...)", nonce,sender,target,value,gasLimit,data))
       cast keccak $(cast abi-encode "f(uint256,address,address,uint256,uint256,bytes)" \
         $NONCE $SENDER $TARGET $VALUE $GASLIMIT $DATA)

2. Rebuild the root from the sibling branch. Walk the merkle proof, hashing pairs with the ordering
   the contract expects (OP uses sorted-pair hashing). Compare against the claimed output root.

       # python: for h in proof: leaf = keccak(sorted(leaf,h))

3. Confirm the output root is the canonical, final one on L1 — not merely one you were handed.
   Read it from the output oracle or dispute game by index:

       cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC

   Arbitrum: read `Rollup.rollupBlockHash` / the committed assertion via `Outbox` after the rollup
   block is confirmed.

4. Check the proof has not already been used and is still valid. Read the portal's record:

       cast call $OPTIMISM_PORTAL "provenWithdrawals(bytes32)(bytes32,uint128,uint128)" $WITHDRAWAL_HASH --rpc-url $L1RPC

   A nonzero timestamp with a different root than the current oracle output means the proof is stale
   and must be re-proved against the newer root.

5. Confirm the challenge window state. An OP withdrawal cannot be finalised until the 7-day challenge
   period on the referenced output has elapsed; a disputed game makes the root unusable.

6. Only now hand the proof to `finalizeWithdrawalTransaction` (OP) or `Outbox.executeTransaction`
   (Arbitrum). If step 3 or 4 fails, do not submit — regenerate against a fresh root.

## Pitfalls

- Verifying the proof against a root fetched from the wrong oracle or a superseded index; the proof is
  internally consistent and still fails on-chain.
- Hashing the leaf with the wrong field order or a missing selector; bridge contracts are unforgiving
  and the error surfaces only as an opaque revert.
- Reusing a proof whose `provenWithdrawals` entry already exists against a now-superseded root.
- Trusting a proof supplied by a counterparty without re-deriving the leaf yourself.
- Ignoring that a game disputed during the window freezes finalisation even though the proof is valid.

## Verification

    cast call $OPTIMISM_PORTAL "provenWithdrawals(bytes32)(bytes32,uint128,uint128)" $WITHDRAWAL_HASH --rpc-url $L1RPC
    cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC
    # proof's root == oracle output root, and timestamp + 604800 <= now

Report the recomputed leaf, the root you derived, the canonical root from the oracle, and whether the
challenge period has elapsed.
