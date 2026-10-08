---
name: pin-nft-assets-with-content-hashes
description: Use when an NFT points at off-chain images or JSON on IPFS/Arweave and the collection claims permanence. Verifies the CID resolves, is pinned, and matches the on-chain metadata hash.
---

# Pin NFT assets by content hash

A `tokenURI` that returns `ipfs://Qm.../1.json` is permanent only if that CID is actually pinned and its `image` field resolves to a second pinned CID. Check both before believing the permanence claim.

## Procedure

1. Read the token URI and any on-chain metadata commitment:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC
   cast call $NFT "metadataHash(uint256)(bytes32)" 1 --rpc-url $RPC
   ```

2. Fetch the JSON through a gateway and hash the exact bytes:

   ```
   curl -sL "https://ipfs.io/ipfs/$CID/1.json" -o meta.json
   python3 -c "import hashlib;print(hashlib.sha256(open('meta.json','rb').read()).hexdigest())"
   ```

   Compare with the on-chain hash. A mismatch means the metadata can change server-side.

3. Confirm the `image` target is itself a content address, not `https://cdn.../1.png`:

   ```
   jq -r '.image, .animation_url // empty' meta.json
   ```

4. Check the CID is pinned on at least two services. Local node:

   ```
   ipfs pin ls --type=recursive | grep $CID
   ```

   Remote pinning: `curl -s "https://api.pinata.cloud/data/pinList?hash=$CID" -H "Authorization: Bearer $PINATA_JWT" | jq '.count'`

5. Retrieve the same file from independent gateways and compare hashes:

   ```
   for g in ipfs.io cloudflare-ipfs.com dweb.link; do curl -sL "https://$g/ipfs/$CID/1.json" | sha256sum; done
   ```

6. For Arweave, resolve the tx and hash the payload: `curl -s https://arweave.net/$TX | sha256sum`.

7. Cross-check the CID recorded on-chain, if any, against the gateway result. The contract is the source of truth, not the marketplace page.

## Pitfalls

- A gateway returning the file proves nothing: gateways cache opportunistically and evict, so a resolvable CID may still be unpinned.
- An `ipfs://` URI with an IPNS root is mutable — IPNS names can be repointed.
- The JSON is often pinned while `image` points at a mutable CDN; audit every URL field including `animation_url`.
- Pinning individual file CIDs is not enough: the directory/manifest CID must be pinned or the files are garbage-collected.
- A metadata hash stored in a marketplace database is not durable; only a contract-committed hash counts.

## Verification

    for g in ipfs.io dweb.link; do curl -sL "https://$g/ipfs/$CID/1.json" | sha256sum; done

Pass: both gateways print the same hash and it equals the value returned by `metadataHash(1)` (where the collection commits one). Report the CID, the gateways tested, the pin services holding it, and any field still on a mutable host.
