---
name: delegate-voting-power-without-losing-it
description: Use when delegating, redelegating, or recovering token voting power in a DAO. Verifies the delegatee, the snapshot timing, and that the vote actually moved before the proposal snapshot.
---

# Delegate voting power without losing it

Voting power in an ERC20Votes token only exists where it is delegated; a holder who never delegated has zero votes, and a delegation made after the proposal snapshot does not count for that proposal. Confirm both the target and the timing.

## Procedure

1. Check where your votes currently sit:
   `cast call $TOKEN "delegates(address)(address)" $ME --rpc-url $RPC`
   `cast call $TOKEN "getVotes(address)(uint256)" $ME --rpc-url $RPC`
   If `delegates` is the zero address, your balance is idle and counts for nothing.
2. Choose the delegatee deliberately: a self-delegation makes you able to vote; delegating to a third party hands them your weight for every proposal until you redelegate.
3. Confirm the delegatee address against an independent source (their ENS, a signed forum post). A typo'd address is an irreversible transfer of voting power to a stranger.
4. Delegate and confirm the event:
   `cast send $TOKEN "delegate(address)" $DELEGATEE --rpc-url $RPC --private-key $KEY`
   then watch `DelegateChanged(delegator, from, to)` on the next block.
5. Verify the move landed before the proposal's snapshot block. ERC20Votes checkpoints are historical:
   `cast call $TOKEN "getPastVotes(address,uint256)(uint256)" $DELEGATEE $SNAPSHOT --rpc-url $RPC`
6. If a vote already passed you by, delegation now only affects future proposals; there is no retroactive fix.

## Pitfalls

- Delegating to a contract that has no way to vote (e.g. a plain multisig without a `vote` method) burns the power for that proposal.
- Redelegating the day of the vote: checkpoints are per-block, and the snapshot was taken at `block.number - 1` when the proposal was created, so late delegation is invisible to it.
- Delegating to a known exchange or custodian whose internal accounting does not pass the vote through.
- Assuming `balanceOf` equals `getVotes`; undelegated balances are excluded from tallies entirely.
- Using a hot key to delegate a large balance when the same key also holds the tokens — one compromise takes both.

## Verification

    cast call $TOKEN "getPastVotes(address,uint256)(uint256)" $DELEGATEE $SNAPSHOT --rpc-url $RPC
    # expect the delegatee's snapshot weight to include your balance, and 0 for the old delegatee

Report the old and new delegatee, the snapshot block, and both `getPastVotes` readings; a non-zero reading at the snapshot is the only proof the delegation counted.
