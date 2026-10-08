---
name: verify-allowlist-merkle-proof
description: Use when an NFT allowlist is enforced by a Merkle root, before or after a mint. Recomputes the root, checks the leaf encoding, and proves unlisted addresses cannot claim.
---

# Verify allowlist Merkle proof

A Merkle allowlist is sound only if the root matches the leaf encoding the contract actually hashes and if every eligible address can still produce a valid proof.

## Procedure

1. Read the root and the leaf format:

   ```
   cast call $NFT "merkleRoot()(bytes32)" --rpc-url $RPC
   grep -nE 'keccak256|abi.encodePacked|abi.encode\(' src/*.sol
   ```

2. Reconstruct the leaf exactly. The common OpenZeppelin form is `keccak256(abi.encodePacked(address))`; a leaf built with `abi.encode` or that includes an amount will never verify against the contract's root.

3. Recompute the root from the published allowlist:

   ```
   node -e "const {StandardMerkleTree}=require('@openzeppelin/merkle-tree');\
   const t=StandardMerkleTree.of(require('./allowlist.json'),['address']);console.log(t.root)"
   ```

4. Compare the recomputed root with the on-chain value. A mismatch means the wrong list, wrong encoding, or a stale root.

5. Prove every address can actually mint:

   ```
   node -e "const t=StandardMerkleTree.load(t);for(const a of addresses) console.log(a,t.getProof([a]).length)"
   ```

6. Check the claim flag is set before minting (checks-effects-interactions), or a double-claim is possible:

   ```
   grep -nE 'claimed|isClaimed|usedNonce|_setClaimed' src/*.sol
   ```

7. Test a forged proof for an unlisted address — it must revert:

   ```
   cast call $NFT "mint(bytes32[],uint256)" "[0x00]" 1 --from $NOT_LISTED --rpc-url $RPC
   ```

8. Confirm the root is not owner-mutable after the allowlist is announced, or that any change emits an event.

## Pitfalls

- Hashing sorted pairs on the tool but unsorted pairs in the contract produces a root no standard library agrees with.
- A proof padded with zero hashes can collide and admit an unlisted address.
- Case-sensitive checksum mismatch (`0xAbC` vs `0xabc`) encodes to different leaves and silently skips a real user.
- Keying the claim flag by token id rather than by address lets one address claim many times.
- Reusing the same tree across seasons lets a proof from last season mint in the new phase.

## Verification

    node -e "const {StandardMerkleTree}=require('@openzeppelin/merkle-tree');console.log(StandardMerkleTree.load(t).root)"

Pass: the recomputed root equals `merkleRoot()` on-chain, and a proof for an unlisted address reverts. Report the root, the leaf encoding, and how double-claims are prevented.
