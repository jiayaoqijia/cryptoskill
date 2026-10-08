---
name: simulate-vote-outcome-before-committing
description: Use when a large voter is about to commit, or when deciding whether to spend influence on a proposal. Projects the tally from current votes and unvoted delegate weight against quorum and majority.
---

# Simulate a vote outcome before committing

Casting a large vote late, or not at all, can flip a proposal that looked safe on day one. Project the tally from what is already on the board plus the delegates who have not voted, then decide.

## Procedure

1. Pull the current tally and the snapshot:
   `cast call $GOV "proposalVotes(uint256)(uint256,uint256,uint256)" $ID --rpc-url $RPC`
   `cast call $GOV "proposalSnapshot(uint256)(uint256)" $ID --rpc-url $RPC`
2. Enumerate the top delegated addresses and their snapshot weights:
   `cast call $TOKEN "getPastVotes(address,uint256)(uint256)" $DELEGATE $SNAPSHOT --rpc-url $RPC`
   Loop this over the delegate set from your subgraph or Tally export; do not sample only the ones you recognise.
3. Reconstruct who has already voted from `VoteCast(proposalId, voter, support, weight, reason)` logs, then compute the uncommitted weight as delegate weight minus cast weight.
4. Model three scenarios — all uncommitted sit out, all vote for, all vote against — and compare each to quorum and to `for > against`.
5. If your own weight can change the outcome, compute the exact threshold: how many more for votes are needed for `for + abstain >= quorum` and for `for > against`.
6. Re-simulate near the end of the voting period; whales vote late and a day-one projection is routinely wrong.

7. Fetch each unvoted delegate's public stance and split the projection into committed and undecided weight.
8. Re-run the model after every large `VoteCast`; a single whale changes the scenarios, not just the totals.
9. Record the projection's block and assumptions so a post-mortem can compare forecast to outcome.

## Pitfalls

- Projecting from token holdings instead of `getPastVotes`; only delegated weight counts, and it is fixed at the snapshot block.
- Ignoring abstain: a wall of abstain can satisfy quorum while for still loses to against.
- Assuming a delegate votes the way their public statement says; check `VoteCast` logs for their actual support value.
- Treating the sum of for across multiple proposals as additive influence when delegations changed between snapshots.
- Forgetting that a late redelegation does not change snapshot weight, so last-minute lobbying is a no-op.

- Treating the delegate set as static; new delegations after the snapshot do not change this proposal's weight.
- Assuming a delegate's abstain counts toward majority; in most governors it counts toward quorum only.
- Running the projection once at the start and relying on it; the tally moves and the decision window is short.

## Verification

    cast call $GOV "proposalVotes(uint256)(uint256,uint256,uint256)" $ID --rpc-url $RPC
    # compare live for/against/abstain against the projected totals for each scenario

Report the three scenario tallies, the majority and quorum booleans for each, and the weight needed to flip, with the votes you read behind them.
