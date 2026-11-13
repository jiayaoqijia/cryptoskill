---
name: storage-and-integrity
domain: crypto-trading/storage-and-integrity
trigger: "Append-only raw frames, checksums, schema versioning, a second copy on a different medium, and the rule that collected evidence is committed/persisted before any analysis reads it."
anti_trigger: "Not for the analysis itself, not for the trade record or risk budget."
scope: "Append-only raw frames, checksums, schema versioning, a second copy on a different medium, and the rule that collected evidence is committed/persisted before any analysis reads it."
status: seedling
---

# Storage and Integrity

## Standard
Empirical market research integrity requires absolute immutability of collected raw data. Pipelines must store raw ingestion frames in append-only files accompanied by cryptographic checksums, maintain explicit schema versioning, store redundant copies across distinct physical or cloud media, and strictly enforce the rule that collected evidence is committed to disk before any analytical script reads it.

Primary sources for the claims in this step: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html> and <https://docs.python.org/3/library/hashlib.html>.

## Decision rules
- **Append-only storage:** Raw ingestion payloads are written exclusively to append-only JSONL files or write-once object storage partitions. In-place file edits or deletions are strictly prohibited.
- **Cryptographic verification:** Every stored file or batch partition must generate a SHA-256 checksum upon closure to detect accidental corruption or tampering.
- **Explicit schema versioning:** All stored records must carry a schema version identifier (`schema_version: "1.0.0"`) in their metadata header.
- **Read-write isolation:** Analytical scripts and statistical models must operate in read-only mode against collection storage directories, never writing derived outputs back into raw data partitions.

## Procedure
1. Establish structured storage directories partitioned by data product, exchange venue, and UTC date (`data/raw/{product}/{venue}/YYYY-MM-DD/`).
2. Serialize incoming collection frames into JSONL format and write them to disk using atomic file operations.
3. Compute SHA-256 checksums for completed batch files and write them to corresponding `.sha256` sidecar files.
4. Replicate storage partitions asynchronously to a secondary medium (e.g., separate disk volume or cloud object store) to ensure fault tolerance.
5. Grant read-only file permissions to analytical users and scripts interacting with the raw storage corpus.
6. Run daily integrity verification scripts comparing file checksums against stored sidecar records.

## Anti-patterns
- **Mutable file formats:** Storing raw time-series data in unversioned relational database tables with enabled UPDATE and DELETE privileges.
- **Missing checksums:** Storing valuable multi-gigabyte ingestion corpuses without verifying file integrity over time.
- **Shared read-write workspaces:** Allowing analytical scripts to modify, clean, or overwrite raw ingestion files during exploratory data analysis.
- **Single-medium storage:** Maintaining all collected datasets on a single local disk without redundant backups or off-site replication.

## Done checklist
- [ ] Raw frames are stored exclusively in append-only files with atomic write operations.
- [ ] SHA-256 sidecar checksums are generated for every completed storage partition.
- [ ] Schema version identifiers are embedded in all ingested record headers.
- [ ] Read-only access controls prevent analytical scripts from modifying raw ingestion files.

## Sources
- Python Software Foundation. (2026). Hashing algorithms and cryptographic security in Python (`hashlib`). Retrieved from https://docs.python.org/3/library/hashlib.html
- Apache Parquet Documentation. (2026). Columnar storage formats, compression, and append-only file structures. Retrieved from https://parquet.apache.org/documentation/
- Linux Foundation. (2026). POSIX file permissions, access control lists, and read-only storage security. Retrieved from https://www.kernel.org/doc/html/latest/
- AWS S3 Documentation. (2026). Object immutability, object lock, and versioning best practices for data lakes. Retrieved from https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
