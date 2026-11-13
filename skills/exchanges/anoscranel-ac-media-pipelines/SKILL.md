---
name: ac-media-pipelines
description: 'Building the pipeline that turns user uploads into web-usable media: the transcoding job and its state, upload verification before processing, image optimisation and format negotiation, thumbnail and poster generation at multiple sizes, video ladders from a single source rendition to adaptive bitrate, the async worker pattern with progress, metadata extraction and privacy scrubbing, and the written media pipeline record. It explains how media is processed in a pipeline; it never recommends a codec and never promises a file size. Use when asking ''transcoding'', ''ffmpeg'', ''video pipeline'', ''thumbnail generation'', ''image optimisation'', ''WebP'', ''AVIF'', ''adaptive bitrate'', ''video ladder'', ''HLS rendition'', ''progressive JPEG'', ''EXIF strip'', ''upload then process'', ''source then derivatives''. Not for the security of accepting uploads (ac-security-engineer), not for realtime peer-to-peer media transport (ac-realtime-media-transport), not for capacity planning and profiling (ac-performance).'
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Media pipelines

## Overview

A media pipeline runs after the upload: it takes a source file, verifies it, and produces a fixed ladder of derivatives. The user's browser fits the URL and content-type into a webpage; the pipeline backfills the heavy lifting asynchronously. A YouTube or Twitter-scale company's most-visited computational artefact is not their database; it's this pipeline running on every video upload, turning gigabytes into renditions that stream over mobile and Wi-Fi.

## When to use

- Transcoding video and/or audio into a delivery format and adaptive ladder.
- Generating thumbnails, posters, and preview renditions for visual media.
- Optimising images and choosing modern formats (WebP, AVIF, JPEG) for the web.
- Extracting or stripping metadata, scrubbing it of privacy-sensitive payloads.
- Designing asynchronous upload-then-processing with progress and delivery URLs.
- Reasoning about transcoding time/cost and the derivatives a workload needs.

## When NOT to use

- For the application-security side of accepting uploads (verification of bytes, type sniffing, storage naming, and malware scanning are critical but covered by ac-security-engineer).
- For realtime peer-to-peer media transport (see ac-realtime-media-transport).
- For capacity planning, runtime profiling, and cost accounting of the encoding service itself (see ac-performance and ac-cost-aware-engineering; both treat media-processing as an application of their general mechanics).
- For CDN+edge caching and delivery-tier decisions of already-encoded files (see ac-network-edge-and-delivery).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/source-and-derivatives.md` | `software-engineering/source-and-derivatives` | Source files and their immutable derivative set; what must exist before the first byte of processing. |
| `subskills/media-upload-verification.md` | `software-engineering/media-upload-verification` | Accepting and verifying uploads before media processing; magic bytes vs claimed type; size limits; transactionality. |
| `subskills/image-optimisation.md` | `software-engineering/image-optimisation` | Perceptual and format-level optimisation: progressive JPEG, WebP, AVIF; per-format reason-to-exist; picture element negotiation. |
| `subskills/thumbnails-and-previews.md` | `software-engineering/thumbnails-and-previews` | Thumbnail and poster derivations at multiple aspect ratios and sizes; preview extraction; naming and scheduling. |
| `subskills/video-ladders.md` | `software-engineering/video-ladders` | One source → multiple renditions; adaptive bitrate and resolution ladders; HLS/DASH segments; the economics of duration × resolution × codec. |
| `subskills/async-processing-jobs.md` | `software-engineering/async-processing-jobs` | The worker pattern for expensive media work: queueing, progress tracking, partial results, cancellation, and SLA. |
| `subskills/metadata-and-privacy.md` | `software-engineering/metadata-and-privacy` | EXIF and sidecar data, GPS/location fields, privacy scrubbing, extraction for indexing, and what must never ship to delivery. |
| `subskills/media-pipeline-record.md` | `software-engineering/media-pipeline-record` | The written record: source→derivative inventory, transcode parameters, errors and retries, cold-storage and retention policy. |

## Status and honest limits

Media pipelines exist because raw media is unusable in the form it arrives in; every pipeline decision is a trade between fidelity, storage, bandwidth, and decode compatibility. This skill teaches the trade-space and the mechanics. It never recommends a codec, never promises a file size, and never pretends the trade-space has a universal optimum - browser support, codec licensing, and delivery networks move faster than any static recommendation survives.
