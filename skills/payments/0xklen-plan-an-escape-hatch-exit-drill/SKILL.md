---
name: plan-an-escape-hatch-exit-drill
description: Use when you need a rehearsed, timed procedure to move funds off an L2 through L1 when the sequencer or prover is malicious or permanently down.
---

# Plan an escape hatch exit drill

An escape hatch nobody has executed is a hypothesis, not a safety property: rehearse the full exit on
a fork with real contract addresses and record the wall-clock cost, so a real incident is a checklist
run rather than a first attempt.

## Procedure

1. Name the exact escape for each asset. Not all assets share a path:
   - Native gas token: withdraw via the canonical bridge on L2, prove on L1, finalise after the
     challenge window (OP Stack `OptimismPortal`), or `ArbSys.sendTxToL1` / token bridge (Arbitrum).
   - ERC-20s: the chain's L2 standard bridge `withdraw` / `withdrawTo`, which burns on L2 and mints or
     releases on L1.
   - Contract-controlled funds in a protocol on the L2: often there is no escape at all without a
     forced call, so record that limitation as a finding.

2. Determine what must come *from L2* versus what can be computed from L1 data. A withdrawal message
   must be proven against a posted output/state root; if the prover is down and no root has been
   posted for your block, the exit is blocked until a root appears. Note the dependency explicitly.

3. Rehearse on a fork of L1 with the L2 endpoint live, using the real bridge contracts:

       anvil --fork-url $L1RPC --block-time 2 &
       cast send $L2_STANDARD_BRIDGE "withdraw(address,uint256,uint32,bytes)" \
         $TOKEN $AMOUNT 200000 0x --rpc-url $L2RPC --private-key $L2KEY

4. Time each phase: L2 initiation, waiting for the output root, proving, the challenge window
   (OP mainnet 7 days = 604800 s; Arbitrum ~6.4 days = 45818 L1 blocks), and finalisation. Sum them
   into a single "time to liquid L1 funds" figure.

5. Pre-fund and pre-authorise the L1 side. Finalisation is an L1 transaction that needs ETH for gas
   and the correct signer; if the exit is triggered during a crisis, L1 gas may be high. Keep a funded
   L1 key and, for custody, a threshold signer set ready.

6. Walk the *adversarial* variant: what changes if the sequencer is censoring the L2 withdrawal
   transaction itself? Then the exit must begin from forced inclusion on L1 (see
   `force-include-a-transaction-through-l1-inbox`), which adds the grace period on top.

7. Write the runbook with copy-pasteable commands, the exact contract addresses per chain, the signer
   thresholds, and the expected total duration; store it with the treasury key documentation.

## Pitfalls

- Assuming the L2 standard bridge is the escape when the funds sit in a third-party bridge or a
  protocol contract; those have their own, often weaker, exit paths.
- Forgetting the proving step needs a valid output root; a halted proposer can block a withdrawal
  even with a working sequencer.
- Rehearsing only the happy path and never the forced-inclusion branch, so the drill does not test the
  scenario it exists for.
- Missing that some assets can only be exited after the L2 resumes and a batch is posted — no exit
  exists for a chain that has permanently stopped and posted no root.
- Timing the drill from memory instead of from receipts; the challenge window is measured in block
  timestamps, which drift under low block production.

## Verification

    cast call $L2_STANDARD_BRIDGE "withdraw(address,uint256,uint32,bytes)" ... --rpc-url http://127.0.0.1:8545
    cast logs --from-block $WITHDRAW_BLOCK --address $L2_BRIDGE "MessagePassed(uint256,address,address,uint256,uint256,bytes,bytes32)" --rpc-url $L2RPC

Report the assets covered, the exit path per asset, the measured time-to-liquid for each phase, and
the adversarial-branch time — each figure traced to a receipt timestamp.
