---
name: review-marketplace-listing-signature
description: Use when accepting an NFT listing signature from a marketplace order. Decodes price, fees, expiry and domain chain, and confirms the signer actually owns the token.
---

# Review a marketplace listing signature

A listed NFT is moved by a signed order, not by an on-chain approval alone — read the order's price, fees, expiry, and domain chain before accepting it.

## Procedure

1. Identify the order format: Seaport (`OrderComponents`), Wyvern (`Order`), or a custom listing.

2. Decode the core fields — `offerer`, `offer` (the token), `consideration` (what the seller receives), `startTime`, `endTime`, `salt`. Use the marketplace's decoder or an SDK rather than hand-crafting a Seaport ABI:

   ```
   node -e "const {OrderComponents}=require('@opensea/seaport-js');console.log(...)"
   ```

3. Read the consideration array. Every entry must be a fee to a known marketplace or royalty address, and the seller's own entry must be the majority. An unknown `recipient` taking a large share is the attack.

4. Check `endTime` is in the future and bounded. A listing with a far-future `endTime` and a stale price is a standing liability.

5. Confirm the signature's domain matches this chain and the canonical contract:

   ```
   cast call $SEAPORT "information()(string,bytes32)" --rpc-url $RPC
   ```

   Recompute the domain separator with `keccak256(abi.encode(domainTypehash, ...))` and compare.

6. Verify the signer owns or is approved for the token:

   ```
   cast call $NFT "ownerOf(uint256)(address)" $ID --rpc-url $RPC
   cast call $NFT "getApproved(uint256)(address)" $ID --rpc-url $RPC
   ```

7. Check the order has not been cancelled or filled via `getOrderStatus(orderHash)` returning a bitmap.

## Pitfalls

- A listing signature without `chainId` in the domain can be replayed from a testnet onto mainnet.
- Seaport counter-based cancellation is per-sender and global; one counter increment cancels many listings at once.
- A `NATIVE` consideration entry with a large amount is usually the price, not a fee — do not misread it as one.
- Wyvern permits a "private" listing with a fixed taker; accepting a public listing at a private-only price is a common trick.
- The order hash shown by the marketplace UI differs from the contract's hash if the fee recipient list differs.

## Verification

    cast call $NFT "ownerOf(uint256)(address)" $ID --rpc-url $RPC
    # plus getOrderStatus for the computed order hash

Pass: the signer owns or is approved for the token, the consideration recipients are all expected, and `endTime` is bounded. Report the price, the fee split, the expiry, and the domain chain.
