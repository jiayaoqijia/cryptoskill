---
name: compute-quorum-from-voting-supply
description: Use when checking whether a proposal will reach quorum or explaining a Defeated result that seemed to pass. Computes quorum from governor parameters and vote tallies, not from a guessed percentage.
---

# Compute quorum from voting supply

A proposal fails either because it did not reach quorum or because against outvoted for — two different failures with two different fixes. Compute both from the governor's own numbers.

## Procedure

1. Read the quorum formulation. OpenZeppelin governor exposes:
   `cast call $GOV "quorum(uint256)(uint256)" $BLOCK --rpc-url $RPC`
   and the numerator/denominator that produced it:
   `cast call $GOV "quorumNumerator()(uint256)" --rpc-url $RPC`
   `cast call $GOV "quorumDenominator()(uint256)" --rpc-url $RPC`
2. Note that OZ quorum is a fraction of total supply (or `getPastTotalSupply(block)` at the snapshot block), not of votes cast. A 4% numerator on a 1e9 supply is a 40,000,000 token floor.
3. Read the tally:
   `cast call $GOV "proposalVotes(uint256)(uint256,uint256,uint256)" $ID --rpc-url $RPC`
   which returns (againstVotes, forVotes, abstainVotes).
4. Apply the governor's own rules, which differ by version:
   - OZ `_quorumReached`: `forVotes + abstainVotes >= quorum`.
   - Compound Bravo: quorum counts `forVotes + abstainVotes` (abstain can carry quorum without a majority).
   - OZ `_voteSucceeded`: `forVotes > againstVotes` (strict).
5. Worked example: supply 1e9, numerator 4, so quorum = 40,000,000. Tally for=30,000,000, abstain=5,000,000, against=2,000,000. Quorum is NOT reached (35M < 40M), so the proposal is Defeated despite for>against.
6. Recompute at the snapshot block used by `quorum`, since supply moves:
   `cast call $TOKEN "getPastTotalSupply(uint256)(uint256)" $SNAPSHOT --rpc-url $RPC`

## Pitfalls

- Assuming quorum is a percentage of votes cast; in most governors it is a percentage of total supply, so low turnout fails even with unanimous support.
- Reading `totalSupply()` now instead of `getPastTotalSupply(snapshotBlock)`; a mint or burn between the vote and the check changes the answer.
- Counting abstain as support in sentiment summaries when the governor only counts it toward quorum, not toward `for > against`.
- Mixing Bravo and OpenZeppelin formulas — they agree on quorum but Bravo's `quorumVotes()` is a fixed value read once, while OZ recomputes per snapshot block.
- Treating Defeated as a rejection by voters when the cause was a quorum shortfall.

## Verification

    cast call $GOV "proposalVotes(uint256)(uint256,uint256,uint256)" $ID --rpc-url $RPC
    # for+abstain >= quorum AND for>against => the proposal should read Succeeded

Print the quorum number, the tally, and the two boolean tests; if a Defeated proposal passes both, the snapshot block used is the suspect.
