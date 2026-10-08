---
name: design-nft-airdrop-claim
description: Use when an NFT airdrop or claim lets eligible addresses mint for free. Verifies the snapshot is frozen, the root is committed, and each address can claim exactly once.
---

# Design an NFT airdrop claim

A claim contract must let exactly the eligible addresses claim once, within a bounded window, and must not let the owner redirect the allocation after the snapshot.

## Procedure

1. Freeze the snapshot before claims open: record the block number and commit the eligibility set's root:

   ```
   cast call $AIRDROP "merkleRoot()(bytes32)" --rpc-url $RPC
   cast call $AIRDROP "snapshotBlock()(uint256)" --rpc-url $RPC
   ```

   Eligibility derived from `block.number` at claim time is gameable.

2. Verify the claim flag is set before the transfer (checks-effects-interactions):

   ```
   grep -nE 'claimed\[|_setClaimed|hasClaimed' src/Airdrop.sol
   ```

3. Check the deadline and any post-deadline sweep:

   ```
   cast call $AIRDROP "claimEnd()(uint256)" --rpc-url $RPC
   ```

   A sweep to the owner is acceptable only if pre-announced; an unannounced sweep rug-pulls unclaimed tokens.

4. Confirm the token quantity per leaf is committed in the root, not fetched from a mutable API.

5. Test double-claim and forged-proof:

   ```
   cast call $AIRDROP "claim(bytes32[],uint256)" "$PROOF" 1 --from $ELIGIBLE --rpc-url $RPC
   cast call $AIRDROP "claim(bytes32[],uint256)" "[0x00]" 1 --from $NOT_LISTED --rpc-url $RPC
   ```

6. Check the per-proof gas cost scales acceptably with tree depth for large allowlists.

## Pitfalls

- Setting the root after the announcement lets the owner add or remove addresses at will.
- A leaf that includes an amount served by an API rather than committed in the root lets the amount change.
- A claim window with no end lets a griefer hold tokens out of circulation forever.
- Reusing a Merkle tree across seasons lets last season's proof claim this season's allocation.
- Claiming transfers by index, so if the supply was not fully minted the last claimants revert.

## Verification

    cast send $AIRDROP "claim(bytes32[],uint256)" "$PROOF" 1 --rpc-url $RPC --private-key $KEY

Pass: the first claim succeeds, a second from the same address reverts, and a proof for an ineligible address reverts. Report the root, the snapshot block, the window, and the double-claim result.
