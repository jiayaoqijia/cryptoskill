---
name: record-dataset-provenance
description: Use when a dataset enters an analysis. Captures its origin, license, version, and hash so every derived number can be traced back.
---

# Record Dataset Provenance

A number you cannot trace to one specific, hashable snapshot of one specific dataset is not evidence — it is a memory. Pin the source before you compute.

## Procedure

1. For each input, add a `PROVENANCE.md` row: dataset name, publisher, exact retrieval URL (endpoint, not homepage), UTC retrieval time, license, and version/revision id.
2. Hash the bytes and keep the manifest: `shasum -a 256 data/*.csv | tee data/CHECKSUMS.txt`. If upstream edits the file, the hash must change — a stable hash is your guarantee you analysed a frozen copy.
3. Capture the query, not just the URL. Store the full request so it is replayable:
   `curl -sG 'https://api.example/v2/rows' --data-urlencode 'since=2024-01-01' -o raw.json`
4. Record every transform. Each derived table gets one line: source file, filter, row count in → row count out. Unexplained row shrinkage is the most common silent bug.
5. State the license and its limits (`CC-BY-4.0` requires attribution; `CC-BY-NC-4.0` forbids commercial use; "research use only" forbids redistribution).
6. Note known collection issues from the publisher's own doc: coverage gaps, imputation, sampling design, revision policy.
7. Freeze: copy raw inputs into `data/raw/` and make downstream code read only from there.

```bash
mkdir -p data/raw && cp /tmp/download/*.csv data/raw/
shasum -a 256 data/raw/*.csv > data/RAW_MANIFEST.sha256
wc -l data/raw/*.csv      # record baseline counts next to the manifest
```

## Pitfalls

- Re-pulling "the same" endpoint silently returns a newer revision; without a hash you cannot tell the dataset changed under you.
- Vendored rows from a second-hand mirror (Kaggle, Hugging Face) may be an undeclared subsample — always reach the original.
- Licenses attach to a specific version; a later release can relicence.
- A CSV whose row count differs from the stated `n` means dropped/filtered rows you have not accounted for.
- Timestamps without a timezone are ambiguous; store UTC and say so.

## Verification

    shasum -a 256 -c data/RAW_MANIFEST.sha256

All checksums OK and `PROVENANCE.md` has a license + version for every file. Report: "Analysis on dataset <name> v<rev>, sha256 <hash>, retrieved <UTC date>, licence <X>; 11,204 raw rows."
