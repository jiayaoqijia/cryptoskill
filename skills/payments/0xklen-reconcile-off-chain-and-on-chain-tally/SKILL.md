---
name: reconcile-off-chain-and-on-chain-tally
description: Use when a Snapshot signal and the on-chain execution disagree, or to prove an off-chain vote was counted faithfully. Recomputes signed-vote weight against past delegated balances.
---

# Reconcile off-chain and on-chain tally

Off-chain votes are signatures weighted by delegated balance at a block; the execution is separate. When a signal and an execution diverge, or when one is challenged, recompute the off-chain tally from the raw signed messages.

## Procedure

1. Fetch the off-chain proposal and its votes:
   `graphql { proposal(id:"$PID") { snapshot choices scores } votes(first:1000, where:{proposal:"$PID"}) { voter choice vp } }` from the Snapshot hub (`https://hub.snapshot.org/graphql`).
2. For each voter, recompute weight at the poll's `snapshot` block:
   `cast call $TOKEN "getPastVotes(address,uint256)(uint256)" $VOTER $SNAPSHOT --rpc-url $RPC`
   Sum per choice and compare to the hub's published `scores`. A gap means the hub weighted differently or a vote was spoofed.
3. Verify the signature. A Snapshot `Vote` is EIP-712 over the poll's domain; recover the signer and confirm it matches the voter:
   `cast wallet verify --address $VOTER <digest> <signature>`
4. Check for a strategy gap: some Snapshot strategies weight custom tokens or LP balances, so `vp` may not equal `getPastVotes`. Read the strategy, not just the token.
5. Compare the off-chain winner to the on-chain execution; record any proposal where a Snapshot pass did not lead to the promised on-chain action.
6. Keep the raw signature and block number per vote so the reconciliation is reproducible.

7. Export the raw signed messages and recovered addresses to a file so a third party can rerun the check.
8. Recompute the poll's quorum using the same `getPastTotalSupply` at the snapshot block.
9. Report the delta per choice, not just a pass/fail, so a small weighting bug is visible.

## Pitfalls

- Assuming Snapshot weight equals ERC20Votes `getPastVotes`; custom strategies weight LP tokens, staked balances, and NFTs.
- Missing a "disapprove" option or a hidden second choice in multi-choice polls; handling only yes/no misreports the tally.
- Counting a deleted or edited vote; Snapshot lets a voter re-sign, and only the latest message per voter counts.
- Trusting the hub's `scores` without recomputation; the whole point is an independent replay.
- Comparing an off-chain signal to an on-chain override that intentionally ignored it; note the declared rationale instead of calling it fraud.

- A Snapshot space with delegated voting disabled weights the signer's own balance, not delegatees' — read the space settings.
- Multi-strategy spaces sum several token weights; recomputing with only the primary token gives a wrong total.
- A voter who signed twice and edited the choice leaves two messages; counting both double-counts the weight.

## Verification

    graphql { votes(where:{proposal:"$PID"}) { voter choice vp } }
    # recompute sum(vp) per choice from getPastVotes at the snapshot block; it must equal the hub scores

Report the recomputed per-choice totals, the hub totals, and any differing voters, each with the block number and signature basis.
