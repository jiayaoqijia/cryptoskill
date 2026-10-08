---
name: audit-delegatee-power-concentration
description: Use when checking whether a DAO's voting power is centralised, or before trusting a single delegate. Measures top-delegate share and Gini against quorum, using snapshot weights.
---

# Audit delegatee power concentration

A DAO where three addresses control quorum is not governed by its token holders; it is governed by three people. Measure the distribution of delegated weight at a snapshot and flag when one holder can carry or block a vote alone.

## Procedure

1. Export delegated weights at a fixed snapshot block from the token's `DelegateChanged` history or a delegation subgraph:
   `graphql { delegates(first:1000, orderBy:"delegatedVotes", orderDirection:"desc", block:{number:$SNAPSHOT}) { id delegatedVotes } }`
2. Cross-check the top addresses with on-chain checkpoints:
   `cast call $TOKEN "getPastVotes(address,uint256)(uint256)" $DELEGATE $SNAPSHOT --rpc-url $RPC`
3. Compute three numbers: top-1 share, top-5 share, and the Gini coefficient, each as a fraction of total delegated weight.
   Gini on a sorted weight vector `x`: `sum((2*i - n - 1) * x[i]) / (n * sum(x))`.
4. Compare against the quorum threshold:
   `cast call $GOV "quorum(uint256)(uint256)" $SNAPSHOT --rpc-url $RPC`
   If top-1 >= quorum, one delegate decides alone.
5. Flag any delegate above 33% of total delegated weight as a de-facto veto.
6. Re-measure quarterly; concentration drifts as delegators rotate.

7. Separate the top decile from the tail: report the share held by the smallest 90% to show how thin the base is.
8. Recompute after clustering known actors; a foundation, its multisig, and its cold wallet are one delegate, not three.
9. Track the trend across the last four snapshots to see whether concentration is rising, not merely high.

## Pitfalls

- Counting raw token balance instead of delegated weight; a large holder who never delegated has no votes and should not raise the concentration figure.
- Using `latest` weights for a snapshot audit; delegations change and the historical figure is the one that governed the vote.
- Ignoring addresses that are the same actor (multisig, cold wallet, DAO treasury) — cluster first, then compute, or the concentration is understated.
- Reporting the Gini without the top-N share; a Gini hides whether the concentration is one whale or a long tail.
- Assuming high concentration is a bug; a foundation that delegates to itself may be intentional, but it must be disclosed.

- Summing delegated weight and calling it distributed ignores the long tail of zero-vote holders.
- A falling top-1 share with a rising top-5 share means power moved between insiders, not out to holders.
- Excluding the treasury's own delegated votes understates concentration when the same few control it.

## Verification

    python3 -c "x=sorted(W); n=len(x); print(sum((2*i-n-1)*v for i,v in enumerate(x))/(n*sum(x)))"
    # Gini near 1 means near-total control; near 0 means broad distribution

Report top-1 and top-5 share, the Gini, and the quorum, all at the same snapshot block, with the export cited.
