---
name: media-upload-verification
domain: software-engineering/media-upload-verification
trigger: "Verifying an uploaded media file before processing it."
anti_trigger: "Not for realtime transport, and not for capacity profiling."
scope: "Accepting and verifying uploads before media processing; magic bytes vs claimed type; size limits; transactionality."
status: seedling
---

# Media upload verification

## Standard

Everything the pipeline does later assumes the bytes are what they claim to be. The upload interface's declared Content-Type is only a suggestion: the file is verified by **magic bytes** (the signature at the start of the file), by **structural parseability** (the container must open), and by **semantic consistency** (the claimed resolution/duration must match what the demuxer reads). Each layer exists because the previous one is spoofable: a payload pasted after a valid JPEG header survives magic-byte checks, a truncated MP4 parses partially, and a video whose declared dimensions are smaller than actual can carry a decompression-bomb payload.

Verification is also where **size limits** are enforced. A media pipeline that accepts unbounded uploads is a denial-of-service amplifier: a single 40-gigabyte "image" will pin a worker for hours if the limit is checked after the transcode starts, not before. Limits are declared per media family (images in megabytes, video in gigabytes or durations in seconds), and checked at three points: header-time (a first read of the file's declared size, done as early as possible to reject absurd claims), transfer-time (streaming the upload and aborting past the limit), and at decode-time (because the declared size in the container can lie about reality).

**Transactionality** is the third leg. A file that fails verification must leave no trace — no half-written derivatives in cold storage, no orphaned cache entries. This is why the media pipeline treats uploads the way databases treat transactions: the upload session ends with a validated source entering the pipeline's storage, or with a clean rejection and the bytes discarded; there is no third state.

## Decision rules

- Verify every upload by magic bytes before processing; never trust the declared Content-Type.
- Enforce size ceilings per media family, at header-time, transfer-time, and decode-time.
- Reject, not quarantine, files that fail a structural parse unless an explicit quarantine flow exists for later review.
- Every upload is a transaction: either a validated source enters storage or nothing persists.
- Record the verification verdict (accepted/rejected and the layer that decided) with the source record for audit.
- Rate-limit and quota uploads at the application edge so the pipeline is not the first line of defence.


## Procedure

1. Check declared size and Content-Type at first read; reject absurd claims cheaply.
2. Open the file as a container; read the actual header; confirm magic bytes.
3. Decode a probe (first frames, or metadata) and compare declared vs actual dimensions and duration.
4. Enforce the per-family size ceiling at the streaming layer.
5. On success, commit the file to source storage with checksums and metadata for indexing.
6. On failure, discard the bytes entirely and return an actionable error.

## Anti-patterns

- Trusting the Content-Type, the file extension, or the declared size in the container metadata.
- Accepting the upload, then finding out later that decoding fails on a truncated file.
- Moving unverified files into processing storage because "the pipeline rejects them anyway".
- Erroring with "unsupported media" without saying which layer failed.

## Done checklist

- [ ] Magic-byte verification runs before the transcode worker starts.
- [ ] Size ceilings enforced at the streaming layer, not after full upload.
- [ ] Declared-vs-actual dimension/duration cross-check implemented.
- [ ] Failure path discards the bytes fully; no orphaned work products.
- [ ] Verification verdict recorded with the source record.
- [ ] Upload endpoint rate-limited at the edge.

## Sources

- MDN image file type and format guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types>
- MDN web video codec guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs>
