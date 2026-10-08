---
name: draft-a-proposal-through-governance-stages
description: Use when shepherding a DAO proposal from discussion to execution. Names each stage, the artifact that gates it, and the on-chain state to read before advancing.
---

# Draft a proposal through its governance stages

A proposal that skips a stage fails at the next one: a forum idea with no temperature check gets no quorum, and an on-chain proposal whose calldata was never reviewed executes something nobody agreed to. Each stage has a gate and a readable on-chain state.

## Procedure

1. Fix the stage ladder and the artifact each stage produces: forum post -> temperature-check poll -> Snapshot vote -> on-chain `propose()` -> voting delay -> voting period -> timelock queue -> `execute()`.
2. Read the governor's timing and threshold parameters before promising any date:
   `cast call $GOV "votingDelay()(uint256)" --rpc-url $RPC`
   `cast call $GOV "votingPeriod()(uint256)" --rpc-url $RPC`
   `cast call $GOV "proposalThreshold()(uint256)" --rpc-url $RPC`
   Multiply delays by the chain's block time (12s on mainnet) to get wall-clock.
3. Post the proposal text plus the exact calldata in the forum; the calldata is the contract, the prose is commentary.
4. Run the Snapshot poll for at least the forum-announced window (commonly 5-7 days) and record the snapshot block number.
5. Submit on-chain only after the poll passes; capture the `proposalId` from the `ProposalCreated` event.
6. Watch the state machine rather than the clock:
   `cast call $GOV "state(uint256)(uint8)" $ID --rpc-url $RPC`
   0 Pending, 1 Active, 2 Canceled, 3 Defeated, 4 Succeeded, 5 Queued, 6 Expired, 7 Executed.
7. Advance only when the state reads Succeeded (4); queue, then execute after `proposalEta`.

## Pitfalls

- Announcing a vote date from a forum post without reading `votingDelay` and `votingPeriod`; the real window is set on-chain and can differ per proposal.
- Treating a Snapshot pass as binding when the governor reads a different token snapshot block; the on-chain snapshot is `block.number - 1` at propose time.
- Losing the `proposalId`: it is a hash of targets, values, calldatas and description, so a whitespace edit to the description changes it.
- Skipping the timelock because the vote passed; the delay is the exit window for token holders and cannot be waved through.

## Verification

    cast call $GOV "state(uint256)(uint8)" $ID --rpc-url $RPC
    # 4 = Succeeded means ready to queue; 7 = Executed means done

Report the current state enum, the parameter values read, and the next gate to clear, each with its command.
