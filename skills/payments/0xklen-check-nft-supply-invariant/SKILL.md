---
name: check-nft-supply-invariant
description: Use when an NFT collection's reported supply, token ids, or burn count must be trusted. Reconstructs supply from events and checks it matches totalSupply and the cap.
---

# Check NFT supply invariants

`totalSupply`, the highest token id, and the count of live owners drift apart in collections with burns, gaps, or enumeration tricks; assert the invariants before trusting any number.

## Procedure

1. Read the reported supply and the cap:

   ```
   cast call $NFT "totalSupply()(uint256)" --rpc-url $RPC
   cast call $NFT "maxSupply()(uint256)" --rpc-url $RPC
   ```

2. Check whether ids are contiguous:

   ```
   for i in $(seq 1 $N); do cast call $NFT "ownerOf(uint256)(address)" $i --rpc-url $RPC \
     || echo "missing $i"; done
   ```

3. Reconstruct supply from mint and burn events and compare with `totalSupply()`:

   ```
   mints=$(cast logs --address $NFT "Transfer(address,address,uint256)" --from-block $START --json \
     | jq '[.[]|select(.topics[1]==ZERO)]|length')
   burns=$(... select(.topics[2]==ZERO) ... )
   echo $((mints - burns))
   ```

4. Check the invariant `totalSupply() <= maxSupply`, or `totalSupply() + burned == maxSupply` if the collection burns toward a fixed cap.

5. Verify owner enumeration is not relied upon for correctness; `balanceOf` summed over live holders should equal `totalSupply` when owners are tracked.

6. For ERC-721A-style lazy ownership, confirm `totalSupply` reflects the batch, not the number of `Transfer` events.

## Pitfalls

- ERC-721A emits one `Transfer` per batch mint, so naive event counting undercounts unless you account for batches.
- `totalSupply` often starts at 0 while ids start at 1; the cap-versus-supply off-by-one either oversells a slot or wastes one.
- Burned ids that are re-mintable break the "supply never grows after the cap" invariant.
- A proxy upgrade that resets `_totalMinted` reports a supply contradicting the events.
- Marketplace item counts include un-minted reservations, so their number differs from `totalSupply`.

## Verification

    echo $((mints - burns)); cast call $NFT "totalSupply()(uint256)" --rpc-url $RPC

Pass: the event-derived count equals `totalSupply()`, ids are contiguous or the gaps are explained, and `totalSupply() <= maxSupply`. Report both numbers, the gap list, and the burn count.
