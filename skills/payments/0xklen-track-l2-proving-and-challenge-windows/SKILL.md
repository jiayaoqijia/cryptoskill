---
name: track-l2-proving-and-challenge-windows
description: Use when you need to know whether a given L2 batch or state root is still challengeable, and when it becomes final, before acting on its outputs.
---

# Track L2 proving and challenge windows

Every L2 output is in one of a few states — proposed and challengeable, disputed, or final — and an
action keyed to the wrong state (releasing funds, trusting a withdrawal) is the failure this skill
prevents.

## Procedure

1. Identify the mechanism: optimistic rollups have a time-based challenge window (fraud proofs); zk
   rollups have a proof-verification step with little or no challenge window. The clock you track
   differs between them.

2. For optimistic chains, read the proposal record and its timestamp. OP Stack output oracle:

       cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC

   The tuple is (outputRoot, l2BlockNumber, timestamp). Arbitrum: read the assertion and the
   `confirmPeriodBlocks` setting to know the window in blocks.

3. Compute the remaining challengeable time and the finalisable time:

       python3 -c "t=$TS; print('finalisable_at', t+604800, 'remaining', t+604800-__import__('time').time(), 's')"

4. Check whether a dispute game exists and its status. Under OP fault proofs, list recent games and
   inspect the one covering your output; a game in progress or one that resolved against the root
   freezes finality:

       cast call $DISPUTE_GAME_FACTORY "findLatestGames(uint32,uint256,uint256)((uint256,uint256,bytes32,address,uint64,uint64,uint8)[])" 0 0 10 --rpc-url $L1RPC

5. For zk rollups, verify the proof is current rather than scanning for a window: read the last
   verified batch from the verifier/oracle and confirm your batch index is at or below it.

6. Drive alerts off state transitions, not just expiry: alert when remaining time drops below a
   threshold if you intend to dispute, and block any settlement code path until the root is final.

7. Log (index, root, proposed_at, window_end, state) each poll so a dispute or a missed window is
   reconstructible after the fact.

## Pitfalls

- Reading the window from docs when the deployment exposes different constants via `CHALLENGE_PERIOD()`
  or `confirmPeriodBlocks()`.
- Comparing timestamps across clocks — the proposal timestamp is an L1 block timestamp, so compare it
  to `date +%s` on a synced host (L1 timestamps are close to wall clock but not identical).
- Assuming a final-looking 1-hour zk escrow delay is the whole story; some zk bridges add a separate
  exit delay on top of proof time.
- Treating a game in progress as a settled finalisation, or vice versa.
- Polling the oracle by a stale index after a reorg that changed the latest index.

## Verification

    cast call $L2_OUTPUT_ORACLE "getL2Output(uint256)(bytes32,uint128,uint128)" $INDEX --rpc-url $L1RPC
    date +%s    # compare: proposed timestamp + challenge period vs now
    # final iff (proposed_ts + CHALLENGE_PERIOD) <= now AND no live dispute game

Report the output index, its root, the window end time, remaining seconds, and the game state — with
the call that produced each field.
