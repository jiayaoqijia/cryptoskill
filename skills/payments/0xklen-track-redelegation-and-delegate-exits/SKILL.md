---
name: track-redelegation-and-delegate-exits
description: Use when watching for voting-power flight before a vote, or when a delegate unexpectedly loses influence. Reconstructs DelegateVotesChanged movements across a window and flags large exits.
---

# Track redelegation and delegate exits

Voting power moves silently between blocks and only appears at the next snapshot. A wave of redelegation away from a delegate before a vote changes the quorum landscape with no public announcement.

## Procedure

1. Pull `DelegateVotesChanged` for the window; each event carries `(delegate, previousBalance, newBalance)`:
   `cast logs --from-block $START --to-block $END --address $TOKEN "DelegateVotesChanged(address,uint256,uint256)" --rpc-url $RPC`
2. Compute per-delegate net change as `newBalance - previousBalance`, summing across events in the window.
3. Identify the delegator behind `DelegateChanged(delegator, from, to)` when a large move appears, so you can report who left, not just that weight fell.
4. Flag any delegate whose weight changed by more than 10% of quorum in the window, and any delegate whose weight dropped to zero (a full exit).
5. Correlate with the proposal calendar: an exit within 48 hours before a snapshot is more consequential than one mid-quarter.
6. Track the destination: weight often moves to another large delegate, which redistributes rather than reduces participation.
7. Publish the movers each week, with block numbers, so delegators can see where weight is going.

8. Bucket the net changes by hour so a burst just before a snapshot is visible rather than averaged away.
9. Attribute the destination address to a known actor where possible, and label unknown large recipients for review.
10. Persist the movers to a weekly file so the trend across weeks is comparable.

## Pitfalls

- Reading `getVotes` now and comparing to a week-old note; `getVotes` moves in the same block and only `getPastVotes` gives the historical figure.
- Confusing a transfer with a delegation; tokens can move without votes moving, and votes move when a delegator redelegates or transfers.
- Reporting a delegate's weight as lost when it moved to their own second address; cluster addresses before calling an exit.
- Missing self-delegation churn: some contracts delegate to themselves in bulk at on-chain action time, producing large but benign events.
- Sampling `DelegateVotesChanged` on a non-archive node when the window is old; historical logs need an archive or an indexer.

- Summing `DelegateVotesChanged` without the pairing `DelegateChanged` gives a weight delta with no owner.
- A balance that fell because a delegator's tokens were sold (not redelegated) is not an exit of support.
- Reading logs only from `latest` misses the window entirely once a few hundred blocks have passed.

## Verification

    cast logs --from-block $START --to-block $END --address $TOKEN "DelegateVotesChanged(address,uint256,uint256)" --rpc-url $RPC
    # sum (new-previous) per delegate; a drop near a snapshot is the flight to report

Report the movers with net weight change, the delegators behind each, and the proposal they precede, with the log range cited.
