---
name: budget-the-l1-withdrawal-challenge-delay
description: Use when planning cash flow, an SLA, or a treasury decision and you must price in the full L2-to-L1 withdrawal delay stack, not a single quoted number.
---

# Budget the L1 withdrawal challenge delay

The headline "7-day withdrawal" hides four stacked delays, and a plan that budgets one number will
miss its date whenever the submitting cadence or the proof step drifts.

## Procedure

1. Decompose the delay into its components for the specific chain:
   - L2 inclusion of the initiate transaction (one to a few L2 block times).
   - Output-root / assertion cadence: OP Stack posts an output roughly every ~30 min to 1 h depending
     on the config; Arbitrum confirms an assertion per rollup block.
   - Challenge / withdrawal delay: OP mainnet 604800 s; Arbitrum One 45818 L1 blocks (~6.4 days).
   - Prove + finalise transactions: one L1 inclusion each (~12 s, more under congestion).

2. Read the on-chain parameters instead of trusting docs, because they vary by deployment:

       cast call $L2_OUTPUT_ORACLE "CHALLENGE_PERIOD()(uint256)" --rpc-url $L1RPC
       cast call $L2_OUTPUT_ORACLE "L2_BLOCK_TIME()(uint256)" --rpc-url $L1RPC
       cast call $ROLLUP "confirmPeriodBlocks()(uint64)" --rpc-url $L1RPC   # Arbitrum

3. Compute the target date as `t_initiate + cadence + challenge + margin`. For Arbitrum convert
   blocks to time at ~12 s per L1 block and add a cadence margin.

       python3 -c "t=__import__('time').time(); print(t+604800)"   # OP: target unix ts

4. Add an explicit safety margin for the two stochastic segments: when the output root lands, and the
   L1 gas market at finalisation. A 24-hour buffer is reasonable for a treasury; a same-day need is
   not compatible with a canonical withdrawal.

5. If the deadline is tighter than the delay, the only ways to close the gap are a third-party bridge
   (different trust model), a CEX, or a pre-positioned L1 liquidity buffer — state the tradeoff rather
   than pretending the canonical delay can be shortened.

6. Track the live withdrawal against the plan: record `provenWithdrawals[hash].timestamp`, then
   compute remaining = `timestamp + CHALLENGE_PERIOD - now` and alert if the finalisation window is
   about to expire.

## Pitfalls

- Quoting 7 days flat and forgetting the output-root cadence that pushes the real date out by up to a
  day on OP Stack.
- Treating the challenge period as synchronised to your initiate timestamp; it starts when the output
  root is posted, which can be later.
- Using a single L1 block time for Arbitrum's block-counted window when L1 block times drift.
- Assuming finalisation is free: it is an L1 transaction whose gas spikes exactly when L1 is busy.
- Planning a settlement date that needs the funds "within the day" from a canonical withdrawal.

## Verification

    P=$(cast call $OPTIMISM_PORTAL "provenWithdrawals(bytes32)(bytes32,uint128,uint128)" $WITHDRAWAL_HASH --rpc-url $L1RPC | awk '{print $2}')
    C=$(cast call $L2_OUTPUT_ORACLE "CHALLENGE_PERIOD()(uint256)" --rpc-url $L1RPC)
    python3 -c "print('finalisable in', $P + $C - __import__('time').time(), 'seconds')"

Report the per-component delay, the computed finalisable timestamp, the margin added, and the on-chain
parameter sources.
