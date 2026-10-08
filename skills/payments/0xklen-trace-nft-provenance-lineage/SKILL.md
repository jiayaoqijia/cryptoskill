---
name: trace-nft-provenance-lineage
description: Use when you must establish the chain of ownership of a specific NFT from mint to now. Walks every transfer in order and flags burns, re-mints, and wraps that break the story.
---

# Trace NFT provenance lineage

Provenance is the ordered list of addresses a token has passed through since mint; a gap, a burn, or a contract that never minted it breaks the story and can hide a stolen or re-minted token.

## Procedure

1. Find the mint transaction — the first `Transfer(0x0, owner, id)`:

   ```
   cast logs --address $NFT "Transfer(address,address,uint256)" \
     0x0000000000000000000000000000000000000000000000000000000000000000 $OWNER --from-block 0 --json
   ```

2. Walk every transfer of that id in order:

   ```
   cast logs --address $NFT "Transfer(address,address,uint256)" --from-block 0 --to-block latest --json \
     | jq -r '.[] | select(.topics[3]==TOKENID_HEX) | [.blockNumber,.transactionHash,.topics[1],.topics[2]] | @tsv'
   ```

3. Confirm the first hop is a mint (`from == 0x0`) and the last `to` equals the current owner:

   ```
   cast call $NFT "ownerOf(uint256)(address)" $ID --rpc-url $RPC
   ```

4. Check for a burn (`to == 0x0`) followed by a re-mint of the same id — that reuses a token id and breaks provenance.

5. Cross-reference each hop with the marketplace sale. A sale event on a different contract between two transfers means the token was wrapped or bridged; note the originating chain.

6. For bridged collections, verify the canonical origin: `ownerOf(id)` on the source chain must match the mint there.

7. Record the lineage as ordered `(block, tx, from, to)` and flag any hop with no matching transaction context.

## Pitfalls

- A log query whose block range predates deployment returns nothing — an empty result is not proof of "no transfers".
- A transfer executed by an operator still shows the true sender in the event after `_transfer`; the approval holder is not the sender.
- ERC-1155 uses `TransferSingle`/`TransferBatch`, not `Transfer`; querying the wrong event yields an empty lineage.
- Lazy-minted (voucher) tokens first hit chain at redeem, so the on-chain mint date is not the claimed mint date.
- RPC log limits can silently truncate a long history; paginate and assert the hop count against an indexer.

## Verification

    cast call $NFT "ownerOf(uint256)(address)" $ID --rpc-url $RPC

Pass: the last event's `to` equals `ownerOf(id)`, the first event is a mint, and no id is minted twice. Report the hop count, the mint tx, and any burn/re-mint found.
