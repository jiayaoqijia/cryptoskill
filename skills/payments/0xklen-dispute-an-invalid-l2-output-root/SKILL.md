---
name: dispute-an-invalid-l2-output-root
description: Use when an optimistic rollup posts an output root you can prove wrong and you must challenge it within the dispute window before it becomes final.
---

# Dispute an invalid L2 output root

An optimistic rollup asserts output roots rather than proving them, so correctness rests on someone
actually disputing a bad root inside the window — and the dispute must reference the exact block and
the exact game contract, or it is ignored.

## Procedure

1. Establish that the root really is wrong before spending gas. Re-derive the L2 state independently:
   run a node (op-node/reth or nitro) against L1, or fetch the raw batch data and replay it, then
   compute the state root at the claimed L2 block number and compare to the asserted root.

       cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC
       cast block $L2_BLOCK_NUMBER --rpc-url $L2RPC --field stateRoot   # independent node, not the sequencer's RPC

   A mismatch between the asserted `outputRoot` and your independently derived root is the case.

2. Confirm you are inside the window. Compare the assertion timestamp and the configured challenge
   period; once elapsed the root is final and a dispute is impossible.

3. Locate the dispute game for that root (OP fault proofs) via the factory and read its status and
   the disputed index; on Arbitrum read the assertion and its `confirmPeriodBlocks`.

       cast call $DISPUTE_GAME_FACTORY "findLatestGames(uint32,uint256,uint256)" 0 0 20 --rpc-url $L1RPC

4. Submit the challenge with the correct bonds. Disputing requires posting the bond the game defines
   (in ETH) and, in a fault-proof game, eventually providing the counter-proof or the disputed state
   transition. Underfunding reverts; overpaying wastes capital.

       cast send $DISPUTE_GAME_FACTORY "create(GameType,bytes)" ... --value $BOND --rpc-url $L1RPC

   Arbitrum: call `Rollup.challengeAssertion` / the configured challenge manager with the assertion
   hash and staker address.

5. Follow the game to resolution. If the game is interactive (bisection / one-step proof), you must
   respond within each move's timeout or forfeit; monitor the game clock, not just the L1 clock.

6. If the challenge succeeds, the invalid root is rejected and the correct one can be posted; record
   the game address, the disputed block, your evidence, and the resolution for the incident log.

## Pitfalls

- Disputing from the sequencer's own RPC — if the operator is the one lying, re-derive from an
  independent node or from L1 data, not the endpoint under suspicion.
- Missing the interactive-game timeouts; a default in a bisection game loses the bond and lets the bad
  root through.
- Posting the wrong bond size or the wrong game type, causing a revert or opening the wrong game.
- Chasing an already-final root; check the challenge period before doing expensive re-derivation.
- Forgetting that a valid dispute still costs L1 gas during exactly the congestion you may be
  investigating, and that losing a dispute burns the bond.

## Verification

    cast call $ROLLUP "getAssertion(bytes32)" $ASSERTION_HASH --rpc-url $L1RPC   # status/firstChildBlock
    cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC
    # independently derived root != asserted root, and index still inside the challenge window

Report the disputed index, your independently derived root versus the asserted one, the evidence
source (what re-derived it), the bond posted, and the game resolution status.
