---
name: metadata-and-privacy
domain: software-engineering/metadata-and-privacy
trigger: "Handling EXIF, sidecar data, and privacy-sensitive metadata in media."
anti_trigger: "Not for photo forensics, and not for capacity profiling."
scope: "EXIF and sidecar data, GPS/location fields, privacy scrubbing, extraction for indexing, and what must never ship to delivery."
status: seedling
---

# Metadata and privacy

## Standard

Media files carry data beyond pixels: **EXIF** blocks in JPEGs and TIFFs record camera model, orientation, timestamps, and — historically — **GPS coordinates** where the photo was taken. Video containers carry encoder settings, creation tools, and sometimes author identifiers. This data has two very different values: it is genuinely useful **inside** the pipeline (orientation normalisation, indexing by date, content classification), and it is a privacy liability **outside** the pipeline (a screenshot from a phone posted with location intact tells every viewer where the photographer stood).

The pipeline's rule is directionality: **metadata is extracted for internal use and stripped for delivery derivatives**. EXIF orientation is the classic gotcha — a rotated JPEG whose orientation flag is baked into the pixels at transcode time no longer needs the flag, but a thumbnail that strips the flag *without* baking the rotation ships sideways. The privacy and the correctness duties meet in the same code path, which is why the recipe treats them together: which fields are read, which are normalised into pixels, and which are dropped before the derivative is written.

Metadata extraction is also an ingest win: camera, creation date, duration, and codec data belong in the pipeline record, not laboriously reconstructed from derivative headers years later. Extract once, store with the source record, and let downstream consumers read pipeline metadata instead of re-parsing files.

## Decision rules

- Extract metadata (orientation, timestamps, dimensions, codec, GPS) into the pipeline record at ingest.
- Delivery derivatives strip privacy-sensitive fields: GPS, serial numbers, author, and toolchain fingerprints.
- Orientation is baked into pixels or preserved as EXIF — never half-removed.
- Sidecar data (XMP, IPTC) follows the same directionality rule as in-file metadata.
- The strip list is versioned in the recipe; new exfil-relevant fields are a recipe change, not a hotfix.
- Test derivatives for metadata leakage with a fixture file known to carry GPS and camera data.


## Procedure

1. At ingest, parse the source's metadata blocks; record what was found in the pipeline record.
2. Normalise what affects rendering (orientation especially) into the derivative generation step.
3. Configure the encoder to emit derivatives without privacy-sensitive metadata; make the strip list explicit.
4. Run a fixture test: a known-GPS camera image must come out clean on every derivative type.
5. Store extracted metadata with the source for internal indexing and search.
6. Change to the strip list bumps the recipe version; derivatives regenerate wholesale only when required.

## Anti-patterns

- Stripping EXIF orientation without baking it, shipping sideways thumbnails.
- Keeping GPS "because the field might be useful later" in publicly-served derivatives.
- Treating metadata stripping as a one-time project rather than a versioned strip list.
- Re-parsing derivative headers in downstream services instead of reading pipeline metadata.

## Done checklist

- [ ] Metadata extracted at ingest and stored with the source record.
- [ ] Orientation handled correctly in the derivative path.
- [ ] Strip list explicit, versioned, and applied to every derivative type.
- [ ] Fixture test proves GPS and camera fields are absent from derivatives.
- [ ] Sidecar data follows the same rules.
- [ ] Downstream consumers read pipeline metadata, not derivative headers.

## Sources

- MDN image file type and format guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types>
- Exchangeable image file format (EXIF): <https://en.wikipedia.org/wiki/Exchangeable_image_file_format>
