---
name: snapshot-voting-power-at-a-past-block
description: Use when auditing a past vote, resolving a snapshot dispute, or verifying delegated weight at a historical block. Queries ERC20Votes checkpoints and the off-chain snapshot block, not current balances.
---

# Snapshot voting power at a past block

A vote is decided at a fixed block, not at the moment you read the chain. Reproducing that block's delegated totals is the only way to audit a tally or settle a dispute about who was eligible.

## Procedure

1. Establish the snapshot block for the vote: for on-chain proposals read `proposalSnapshot(id)`; for Snapshot.org polls read the `snapshot` field from the proposal JSON.
   `cast call $GOV "proposalSnapshot(uint256)(uint256)" $ID --rpc-url $RPC`
2. Read delegated weight at that block, not now:
   `cast call $TOKEN "getPastVotes(address,uint256)(uint256)" $WHO $SNAPSHOT --rpc-url $RPC --block $SNAPSHOT`
   Binary-search the checkpoint with `getPastVotes` if you need the exact block a delegation took effect.
3. Read the total supply that quorum is measured against:
   `cast call $TOKEN "getPastTotalSupply(uint256)(uint256)" $SNAPSHOT --rpc-url $RPC`
4. For each voter, sum `getPastVotes(voter, SNAPSHOT)` and compare against the weight recorded in their `VoteCast` log; a mismatch means the log was tampered with or you read the wrong block.
5. Reconstruct balances by replaying `Transfer` logs from the token's deployment if checkpoints are unavailable (older or non-standard tokens).
6. Cache the block number in the report; "at snapshot" without a number is unverifiable.

7. Persist the snapshot block and per-voter readings to a file so a challenge can be answered from evidence.
8. If `getPastVotes` reverts, confirm the node is archival; a pruned node cannot serve historical state.
9. Cross-check the total delegated weight against the sum of per-delegate `getPastVotes` at the same block.

## Pitfalls

- Reading `balanceOf` or `getVotes` at `latest` and calling it the snapshot; both move, and the difference is exactly the dispute.
- Using an archival node's `latest` when the snapshot is a past block — without a full archive node the historical `getPastVotes` call fails.
- Assuming the Snapshot.org block equals the on-chain `proposalSnapshot`; they are chosen by two different systems.
- Forgetting that an ERC20Votes delegation takes effect at the next checkpoint, so a delegation in the snapshot block itself may not be counted.
- Reading `getPastTotalSupply` at the snapshot for a token that mints continuously and then quoting it as today's supply.

- Reading at a block before the token's deployment returns a zero that looks like 'no votes' rather than an error.
- Assuming every checkpointed transfer creates a vote checkpoint; only delegation changes do.
- Quoting a weight at a block with no explicit number; 'around the vote' is not auditable.

## Verification

    cast call $TOKEN "getPastVotes(address,uint256)(uint256)" $VOTER $SNAPSHOT --rpc-url $RPC
    # must equal the weight in that voter's VoteCast log for proposal $ID

Report the snapshot block, each voter's past votes, and the past total supply; a per-voter match against the logs is the audit pass.
