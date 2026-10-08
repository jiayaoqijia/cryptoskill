---
name: checksum-data-across-the-pipeline
description: Use when data moves between systems and silent corruption is possible. Computes and verifies checksums at each hop so bad bytes are caught at the boundary, not at restore.
---

# Checksum Data Across the Pipeline

Bytes corrupt in transit, on disk, and during transformation; only a checksum re-computed on the far side detects it. Verify at each boundary so a corrupt byte fails the hop that introduced it instead of surfacing during a restore.

## Procedure

1. Choose the algorithm by purpose: SHA-256 for integrity and provenance, xxHash/CRC32C for high-throughput transit, MD5 only as a legacy fallback.
2. Compute at the source before upload and store the digest alongside metadata: `sha256sum data.csv > data.csv.sha256`.
3. Verify after each transfer: `sha256sum -c data.csv.sha256` on the destination, or `aws s3api head-object --checksum-mode ENABLED` to read the stored `ChecksumSHA256`.
4. Use the transport's own integrity where present — S3 multipart uses per-part checksums, `rsync -c` re-hashes, TLS protects transit but not at-rest.
5. Force end-to-end verification on object upload: `aws s3 cp --checksum-algorithm SHA256`, and prefer `aws s3api put-object` with `ChecksumSHA256` so the service validates.
6. Re-verify at restore time from the archive's manifest, not from a fresh hash, so a corrupt archive is caught rather than trusted.
7. Store digests in a manifest written once at creation, and treat any mismatch as a hard failure that halts the pipeline.
8. For derived data, checksum inputs and the transform version together so the same output is reproducible.

## Pitfalls

- Trusting TLS for at-rest integrity; TLS protects the wire, and a bad disk block reads back wrong after a clean transfer.
- Using the object store's `ETag` as if it were always the file MD5 — multipart uploads make it a composite, not a plain hash.
- Computing the checksum after decompression on one side and before on the other, so the digests never match by construction.
- Storing the hash in the same object/row as the data, so corruption that hits the data usually hits the hash too.
- Verifying at upload and never at read, so a bit flip that happens months later goes undetected until restore.
- A weak hash (CRC32) used where deliberate tampering matters; CRC32 is for errors, not adversaries.
- Dropping the manifest during a migration, losing the reference that made verification possible.

## Verification

    sha256sum -c data.csv.sha256                     # expect: data.csv: OK
    aws s3api head-object --bucket acme --key data.csv \
      --checksum-mode ENABLED --query 'ChecksumSHA256'

Source and destination digests match, the manifest stores the original values, and a deliberately corrupted sample fails `-c` with `FAILED`.

Report: "Verified <n> objects across <h> hops; all checksums match source manifest; injected corruption on <sample> was caught at <hop>."
