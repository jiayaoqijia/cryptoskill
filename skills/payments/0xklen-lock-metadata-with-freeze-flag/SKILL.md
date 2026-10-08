---
name: lock-metadata-with-freeze-flag
description: Use when a collection claims permanent metadata and you must verify a one-way freeze actually locks every input. Checks the flag gates all setters and cannot be reset by an upgrade.
---

# Lock metadata with a freeze flag

A one-way `freeze` turns "permanent metadata" into something verifiable: after it is called, `tokenURI` and every input that feeds it cannot change, and the event proves when.

## Procedure

1. Find the freeze function and confirm it is one-way:

   ```
   grep -nE 'freeze|frozen|lockMetadata|isFrozen|unfreeze' src/*.sol
   ```

2. Confirm the frozen flag gates every metadata mutator:

   ```
   grep -nE 'require\(!frozen|require\(!metadataFrozen' src/*.sol
   ```

   A `setBaseURI` that does not check the flag is a backdoor.

3. Check the flag slot cannot be reset by an upgrade. For a proxy, read the implementation and look for a public setter on `frozen`:

   ```
   cast call $PROXY "implementation()(address)" --rpc-url $RPC     # ERC-1967/UUPS
   ```

4. Confirm freeze is callable only by the intended role and emits an event you can locate:

   ```
   cast logs --address $NFT "MetadataFrozen()" --from-block 0 --json
   ```

5. Verify the freeze covers all inputs, not only `baseURI` — any `setProvenance`, `setRevealSeed`, or trait setter must also be gated.

6. Ensure there is no `unfreeze` and no setter that can flip `frozen` back to false.

7. After freezing, a metadata write must revert:

   ```
   cast send $NFT "setBaseURI(string)" "ipfs://evil" --rpc-url $RPC --private-key $OWNER_KEY
   ```

8. Record the freeze transaction so the timestamp is auditable independently of the project.

## Pitfalls

- Freezing before the reveal leaves the placeholder metadata frozen forever.
- A `frozen` bool that lives in the implementation is reset to false by a later implementation upgrade.
- Freezing the base URI while a per-token override mapping is still writable leaves a side door.
- An event emitted on a code path that later reverts proves nothing; confirm the state changed, not just the log.
- Freezing the URI but not the `contractURI` (collection-level metadata) leaves the collection page mutable.

## Verification

    cast send $NFT "setBaseURI(string)" "ipfs://x" --rpc-url $RPC --private-key $OWNER_KEY

Pass: the call reverts after freeze, and `MetadataFrozen` appears exactly once in the logs. Report the freeze tx, the event block, and every metadata setter confirmed gated.
