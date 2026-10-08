---
name: verify-l2-state-root-against-l1-batch
description: Use when you must confirm an L2's claimed state root matches the data committed to L1, before trusting a balance, an indexer, or a withdrawal.
---

# Verify L2 state root against L1 batch

An L2 will happily serve you a state root from its own RPC; the question that matters is whether that
root is the one derivable from the batch data on L1, and answering it means re-deriving rather than
asking.

## Procedure

1. Get the root the L2 *claims*. Read it from an independent L2 node (not the sequencer's public RPC if
   the operator is under suspicion) and from the settlement contract on L1:

       cast block $L2_BLOCK --rpc-url $L2RPC --field stateRoot
       cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC

2. Compute the *expected* root from L1 data. Pull the batches that cover the block (see
   `decode-a-rollup-batch-from-l1-calldata`) and replay them through a derivation node — op-node for
   OP Stack, nitro/`arb-node` for Arbitrum — or a reth/op-geth execution against the parent state.
   Derivation produces the canonical block hash and state root.

3. Compare. For OP Stack the output root is
   `keccak256(version ++ stateRoot ++ withdrawalStorageRoot ++ blockHash)` — compare the *state root*
   and block hash inside the tuple, because comparing the output root to a bare state root is a
   category error:

       cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)" $INDEX --rpc-url $L1RPC
       # then split: bytes32(version) ++ stateRoot ++ storageRoot ++ blockHash

4. For zk rollups, verify the proof instead of replaying: read the last verified batch from the
   verifier/oracle and confirm your block index is covered, then optionally call the verifier contract's
   view to check the proof binds that root.

5. Interpret the result by mechanism. On an optimistic rollup the root is an *assertion* not a proof —
   a match with your derivation is strong evidence, but finality requires the challenge window to pass
   with no successful dispute. On a zk rollup a passing proof is final. Say which you are claiming.

6. If roots disagree, do not act on any downstream value (a withdrawal, a balance an indexer computed).
   Re-derive from an earlier known-good block to localise where the divergence begins.

## Pitfalls

- Comparing the OP *output root* against an L2 `stateRoot` hex string; they are different objects and
  will never match, which looks like a false failure.
- Re-deriving with the sequencer's own node; if the operator is the adversary, the derivation input is
  suspect — use L1 batch data and an unmodified node binary.
- Treating a matched assertion on an optimistic chain as final before the challenge window elapses.
- Missing that OP output roots currently hash the state root plus a withdrawal storage root; an old
  version without that field will mismatch on newer deployments.
- Deriving across a reorg on L1 without re-reading the batch from the canonical L1 block.

## Verification

    cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC
    cast block $L2_BLOCK --rpc-url $L2RPC --field stateRoot
    # split the output-root tuple and compare stateRoot + blockHash to the independent derivation

Report the claimed state root, the L1-committed output root, the result of the independent derivation,
and the mechanism (assertion vs proof) — with the commands behind each value.
