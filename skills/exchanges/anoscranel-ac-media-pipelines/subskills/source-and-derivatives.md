---
name: source-and-derivatives
domain: software-engineering/source-and-derivatives
trigger: "Setting the source-derivative model that the pipeline implements."
anti_trigger: "Not for realtime transport, and not for capacity profiling."
scope: "Source files and their immutable derivative set; what must exist before the first byte of processing."
status: seedling
---

# Source and derivatives

## Standard

The pipeline's first decision is the relationship between the uploaded file and its outputs. The uploaded file is a **source**: after verification it is immutable, and everything downstream — thumbnails, renditions, variants — is a **derivative** with a name, a purpose, and a set of generation parameters. A derivative that cannot answer "which source at which version with which arguments" is an orphan, and orphan derivatives are how storage fleets die: the delete-after-upload cleanup job disappears, the source is kept "temporarily", and three years later storage audit finds forty percent of volume is unreachable by any URL.

Because the source is immutable, derivatives are **fully determined** by (source, recipe). The same source and the same recipe should always produce the same derivative, which is what makes the cache key and the debug story simple — but it also means the moment a recipe is fixed, every previously-generated derivative that recipe produced either matches it or is stale. Recipes therefore need versions, and stale derivatives need a re-generation path that is not "wipe everything and re-encode the archive overnight".

## Decision rules

- Source files are immutable after verification; derivatives carry (source-id, recipe-version, arguments) as part of their identity.
- Derivative naming is content-addressable and reproducible; the same inputs and recipe always give the same output.
- Every derivative type declares its purpose inline in its recipe; nothing is generated "just in case."
- Regeneration, not manual repair, is the path for stale or corrupted derivatives.
- The source must outlive all derivatives; lifecycle (cold storage, retention) is a property of the source, not of derivatives.


## Procedure

1. Classify the uploaded file by media family (image, video, audio, document) after verification.
2. Define the derivative set per family before processing: thumbnails, renditions, variants, and the reason each exists.
3. Version the recipe (transcode parameters, image dimensions, format targets) and lock it per derivative.
4. Emit derivatives with names derived from source-id and recipe-version, not from the user's filename.
5. Record the source's retention tiering (hot for regeneration, cold for archival) and the process that enforces it.

## Anti-patterns

- Accepting a derivative as a source, silently breaking the immutability model.
- Regenerating derivatives on a different date with an edited recipe, then treating the mismatch as a mystery.
- Burying the source in cold storage without a hot-standby copy for regeneration.
- Tooling arbitrary derivative types ad-hoc per request with no recipe version.

## Done checklist

- [ ] Source immutability enforced by the storage layer or by checksum at ingest.
- [ ] Derivative recipes versioned and named.
- [ ] Derivative identity carries (source-id, recipe-version, arguments).
- [ ] Cold-storage tiering policy for sources defined.
- [ ] Regeneration path tested for a stale derivative.
- [ ] No orphan derivatives: every output maps to a source and recipe.

## Sources

- MDN image file type and format guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types>
- MDN web video codec guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs>
