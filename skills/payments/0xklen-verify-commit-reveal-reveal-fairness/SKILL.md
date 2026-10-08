---
name: verify-commit-reveal-reveal-fairness
description: Use when a generative collection promises a "fair reveal" and claims the shuffle is verifiable. Checks that the seed was committed before the mint and cannot be biased by the revealer.
---

# Verify commit-reveal reveal fairness

A "fair reveal" is fair only if the seed was committed before the mint and the shuffle cannot be steered by the party who triggers the reveal.

## Procedure

1. Locate the commit and reveal steps:

   ```
   grep -nE 'commit|reveal|seed|provenance|shuffle' src/*.sol
   ```

2. Confirm the commitment was recorded on-chain before the first mint:

   ```
   cast call $NFT "provenanceHash()(bytes32)" --rpc-url $RPC
   cast logs --address $NFT "Revealed(bytes32)" --from-block 0 --json
   ```

   The reveal event block must be later than the first `Transfer(0x0, ...)` block.

3. Inspect how the shuffle seed is built. An acceptable pattern commits a base seed first, then mixes it with a future on-chain value:

   ```
   seed = keccak256(abi.encodePacked(baseSeed, provenanceHash, blockhash(commitBlock + 1)))
   ```

4. Reject any pattern where the owner supplies the seed after seeing mints — that lets the owner choose the seed that gives the team the rare tokens.

5. Confirm the shuffle reorders token ids, not the order files are served by an API:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC
   ```

6. Check the null reveal: before reveal `tokenURI` returns a placeholder; after, a fixed on-chain mapping. A server-side swap is not a commit-reveal.

7. Recompute the id-to-trait mapping yourself and compare for several ids:

   ```
   python3 -c "import hashlib;print(int(hashlib.sha256(bytes.fromhex('01')).hexdigest(),16)%10000)"
   ```

8. Confirm `reveal()` cannot be called twice and cannot be skipped forever (a timeout path or a forced reveal).

## Pitfalls

- `blockhash` alone is predictable one block ahead; a minter whose transaction lands in the same block can grind token ids.
- Committing file hashes (provenance) but shuffling with an uncommitted seed is the classic fake reveal.
- A placeholder `tokenURI` served by the project's own API is mutable — only an on-chain mapping is commit-reveal.
- Revealing each token as it mints leaks rarity early and enables sniping.
- Re-hashing an already-hashed value inside the contract yields a seed different from your off-chain check.

## Verification

    cast call $NFT "provenanceHash()(bytes32)" --rpc-url $RPC
    cast logs --address $NFT "Revealed(bytes32)" --from-block 0 --to-block latest --json

Pass: the on-chain mapping matches an independently recomputed shuffle for at least 5 ids, and the reveal block is after the first mint block. Report the commit tx, the seed composition, and the shuffle check.
