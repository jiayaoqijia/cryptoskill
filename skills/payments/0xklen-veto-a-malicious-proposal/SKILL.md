---
name: veto-a-malicious-proposal
description: Use when a proposal with hidden or harmful calldata has been queued and must be stopped before execution. Detects the payload, cancels before the timelock fires, and records the reason transparently.
---

# Veto a malicious proposal

The window between voting and execution exists so a harmful payload can be stopped. Cancel it from the governance path, not by front-running, and publish the reason so the veto is not itself an act of censorship.

## Procedure

1. Decode every calldata in the queued proposal and compare to the stated intent:
   `cast calldata-decode "<sig>" <data>` for each entry.
   Look for transfers to an unknown address, `upgradeTo` on the treasury proxy, `grantRole` to a fresh key, or an unlimited `approve`.
2. Confirm the proposal is still queued and not executed:
   `cast call $GOV "state(uint256)(uint8)" $ID --rpc-url $RPC` (5 = Queued is the last cancellable state).
3. Cancel through the governor if you are the proposer:
   `cast send $GOV "cancel(address[],uint256[],bytes[],bytes32)" $TARGETS $VALUES $CALLDATAS $DESC_HASH --rpc-url $RPC --private-key $KEY`
4. If you are not the proposer, use the guardian veto if the governor exposes one, or `cancel` the timelock operation with `CANCELLER_ROLE`:
   `cast send $TIMELOCK "cancel(bytes32)" $OP_ID --rpc-url $RPC --private-key $KEY`
5. Verify the operation can no longer execute: `isOperationPending(id)` returns false and the id is marked done/cancelled.
6. Publish the veto with the decoded payload diff and the deployment-wide impact, then file a postmortem.

## Pitfalls

- Waiting for the vote to conclude before reviewing calldata; the review must happen before the snapshot, and again at queue time.
- Cancelling without decoding: a veto based on a social-media rumour erodes the emergency power's legitimacy.
- Assuming `cancel` is available to anyone; on many governors only the proposer or guardian can cancel, and the wrong caller reverts.
- Front-running an execute with a cancel transaction and hoping to win the block; route through the guardian path instead of racing.
- Missing a second proposal carrying the same payload; compare the calldata hash across all pending ids, not just the flagged one.
- Cancelling a benign proposal and calling it malicious; verify the diff against the intent before acting.

## Verification

    cast call $GOV "state(uint256)(uint8)" $ID --rpc-url $RPC && cast call $TIMELOCK "isOperationPending(bytes32)(bool)" $OP_ID --rpc-url $RPC
    # state 2 (Canceled) and isOperationPending false prove the payload cannot run

Report the decoded malicious calldata, the cancel transaction hash, and the post-cancel state, with the commands behind them.
