---
name: verify-blob-data-availability-on-l1
description: Use when you must confirm that data an L2 published in EIP-4844 blobs is actually retrievable within the availability window, for reconstruction or a DA check.
---

# Verify blob data availability on L1

A blob commitment on L1 proves data was *committed*, not that it is *still retrievable*; the data is
pruned from consensus after about 18 days, so a DA check must fetch the sidecar, verify it against the
versioned hash, and check how much of the window remains.

## Procedure

1. Find the L1 blob-posting transaction and extract its blob versioned hashes and the beacon block
   slot. A blob tx carries `blobVersionedHashes` in its fields.

       cast tx $L1_TXHASH --json --rpc-url $L1RPC | jq '.blobVersionedHashes'
       cast receipt $L1_TXHASH --json --rpc-url $L1RPC | jq '.blobGasUsed, .blobGasPrice'

2. Determine the slot containing the transaction, then fetch the blob sidecar from a beacon node:

       cast block $L1_BLOCK --rpc-url $L1RPC --field timestamp
       curl -s "$BEACON/eth/v1/beacon/blob_sidecars/$SLOT" | jq '.data[] | {index, kzg_commitment}'

3. Verify each sidecar against the versioned hash from the L1 transaction: the versioned hash is
   `0x01 || sha256(kzg_commitment)[1:]`. Recompute it locally and compare — a mismatch means the
   beacon node served the wrong blob.

       python3 -c "import hashlib; c=bytes.fromhex('$KZG_COMMITMENT'); \
         print('0x01'+hashlib.sha256(c).hexdigest()[2:])"

4. Optionally verify the KZG proof over the blob so you know the commitment actually binds the
   returned data (use a `c-kzg`/`kzg-rs` binding or `check_blob_kzg_proof` on the beacon API).

5. Compute remaining availability: the prune horizon is 4096 epochs from the block's epoch. If the
   sidecar is already gone, the data is only recoverable from the L2's own storage or an archive, so
   report unavailability as a finding, not a retry.

       python3 -c "epoch=$SLOT//32; print('prunes ~', epoch+4096, 'epochs; now', __import__('time').time())"

6. Reconcile the fetched blob data against the L2 batch it claims to carry (decode the frames and
   check the channel/compression), so you confirm it is *this* chain's data, not any blob at that slot.

## Pitfalls

- Treating the blob commitment as proof of retrievability; the commitment can be valid while the
  sidecar is long pruned.
- Fetching from a beacon node that is not synced to the slot and getting a 404, then concluding the
  data is pruned — retry across two beacon providers.
- Forgetting the version byte: a plain `sha256(commitment)` without the `0x01` prefix never matches.
- Assuming all clients retain all blobs; retention and pruning boundaries differ by client.
- Skipping the KZG check and trusting a sidecar whose data does not actually match the commitment.

## Verification

    curl -s "$BEACON/eth/v1/beacon/blob_sidecars/$SLOT" | jq -r '.data[0].kzg_commitment'
    python3 -c "import hashlib;print('0x01'+hashlib.sha256(bytes.fromhex('$KZG')).hexdigest()[2:])"
    # recomputed versioned hash == the hash in the L1 blob tx's blobVersionedHashes

Report the blob versioned hash, whether the sidecar was retrievable, the recomputed hash match, and
the remaining days before pruning — with the beacon endpoint used.
