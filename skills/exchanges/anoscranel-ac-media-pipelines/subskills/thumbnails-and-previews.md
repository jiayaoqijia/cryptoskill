---
name: thumbnails-and-previews
domain: software-engineering/thumbnails-and-previews
trigger: "Generating thumbnail, poster, and preview renditions from sources."
anti_trigger: "Not for visual design critique, and not for capacity profiling."
scope: "Thumbnail and poster derivations at multiple aspect ratios and sizes; preview extraction; naming and scheduling."
status: seedling
---

# Thumbnails and previews

## Standard

Thumbnails exist because the alternative is loading the full image to decide whether to look at it. A media pipeline emits a **thumbnail set** at generation time — commonly something like 16:9 poster, 1:1 square, and one or two sizes inside each of those aspect ratios — because the delivery layer's layout grid cannot adaptively crop the file on the way out. The recipe describes exactly which crops and sizes emit for each media family, and the naming makes the set discoverable: a thumbnail URL is derived from the source-id and the size recipe, so the set can be enumerated or regenerated mechanically.

For video, the thumbnail problem is compounded by **time**: a poster frame must be chosen at a moment that represents the video. A video's first frame is often a black screen or a fade-in; naive "grab frame zero" pipelines product posters that look like nothing. The recipe therefore states **poster-frame selection**: either a fixed early offset (a few seconds in), a scene-detection pass picking the most representative frame, or — for user-uploaded media — a user-facing choice recorded at upload time and honoured by the pipeline.

**Preview extraction** extends the idea beyond static images: short looping previews for video, sprite thumbnails scrubbed from the timeline, or page-range thumbnails for documents. All are derivatives with recipes; all face the same constraint — the pipeline's job is to produce them once, deterministically, at ingest, rather than delegate expensive extraction to the delivery layer multiple times per request.

## Decision rules

- Emit the full thumbnail set at ingest, in one pass, from a stated recipe.
- Aspect-ratio packaging is a derivative property, never an on-the-fly delivery-layer crop.
- Poster-frame selection is stated in the recipe: fixed offset, scene detection, or user selection.
- Preview derivations (sprites, animated loops, document page extracts) are versioned derivatives like any other.
- Thumbnail failure is graceful: a missing thumbnail is a placeholder, not a failed source.
- All thumbnails go into the same naming scheme as other derivatives so regeneration is mechanical.


## Procedure

1. Define the thumbnail recipe per media family: aspect ratios, sizes, and naming.
2. For video, choose the poster-frame policy and encode it in the recipe.
3. Emit the full set at ingest in one pipeline pass; record per-derivative status.
4. Register the set with the delivery layer's layout grid; no layout-time cropping.
5. For previews, define the temporal extraction policy (duration, frame cadence) and treat it as a recipe.
6. Review the orphan-rate: derivatives that never get served point to an over-broad set.

## Anti-patterns

- Grabbing frame zero for a poster and shipping a black rectangle.
- Letting the client crop square thumbnails from full-size sources on every render.
- Emitting twelve sizes and serving two: the set is tuned, not accreted.
- Treating preview generation as a feature flag instead of a recipe.

## Done checklist

- [ ] Thumbnail recipe declared per media family with sizes and aspect ratios.
- [ ] Poster-frame selection policy encodable and recorded.
- [ ] Full set emitted at ingest; no lazy on-request generation.
- [ ] Preview extraction has a versioned recipe.
- [ ] Naming scheme tied to source-id and recipe-version.
- [ ] Over-broad sets pruned based on served-derivative analytics.

## Sources

- MDN image file type and format guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types>
- Web.dev image course, art direction and cropping: <https://web.dev/learn/images>
