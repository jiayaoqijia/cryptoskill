---
name: image-optimisation
domain: software-engineering/image-optimisation
trigger: "Choosing image output formats and their compression settings."
anti_trigger: "Not for visual design critique, and not for capacity profiling."
scope: "Perceptual and format-level optimisation: progressive JPEG, WebP, AVIF; per-format reason-to-exist; picture element negotiation."
status: seedling
---

# Image optimisation

## Standard

Images dominate the weight of the modern web, and the format choice is the pipeline's biggest quality/size lever. The four working formats each have a reason to exist: **JPEG** for photographs with universal compatibility; **WebP** for the same images at meaningfully smaller sizes with near-universal modern support; **AVIF** for even smaller sizes where its slower encoding and patchier browser support are acceptable; and **PNG** for graphics with hard edges or where lossless is a requirement. A pipeline that serves only JPEG is leaving bandwidth on the table; a pipeline that serves only AVIF is betting on a support matrix it does not control.

**Progressive JPEG** is a rendering choice, not a format: the file is organised so a low-resolution version appears first and refines itself as more bytes arrive. For large photographic images on slow connections this is more important than the byte savings from switching formats — the user's perceived load time is the first meaningful appearance, not the final byte. The pipeline is where this is decided, because a progressive JPEG is a property of how the encoder was configured.

**Format negotiation** connects these choices to the browser. The pipeline produces multiple modern variants of the same source, and the delivery layer negotiates via the `<picture>` element or the `Accept` header. But this means the derivative set grows — one source produces JPEG, WebP, and optionally AVIF renditions at each size, and the pipeline's total storage and processing cost is the cross-product. The record documents this trade in the open, because "serve everything in AVIF' and "serve only JPEG" are both defensible positions that fail differently.

## Decision rules

- Choose the format per image family: photographs to JPEG/WebP/AVIF, hard-edged graphics to PNG, animations evaluated separately.
- Server-side negotiation via `Accept` or `<picture>`; never one-format-for-everyone without a recorded justification.
- Produce progressive JPEG for large photographic derivatives.
- Generate all variants (WebP, AVIF) at derivative-generation time, not on-demand.
- Record the format-per-purpose and note the browser-support matrix snapshot date in the recipe version.
- Strip metadata unless a specific downstream consumer requires it (see the privacy leaf).


## Procedure

1. Classify each source image (photograph vs graphic vs animation) after verification.
2. Select the primary format per class and the negotiation set per purpose.
3. Configure the encoder (quality, chroma subsampling, progressive mode) and lock it in the recipe.
4. Emit all size variants for each purpose in one pass.
5. Record the format choices, sizes, quality parameters, and the support-matrix snapshot date in the recipe.
6. Point the delivery layer's `Accept`-based negotiation at the derivative set.

## Anti-patterns

- Encoding once and hoping the delivery layer will figure out the format.
- Choosing a format based on benchmark blog posts instead of the measured target audience's support.
- Serving enormous PNGs because "lossless is safer" without a requirement saying so.
- Not producing progressive JPEGs for large photographic images on slow connections.

## Done checklist

- [ ] Per-family format policy written and in the recipe version.
- [ ] Negotiation variants generated at pipeline time.
- [ ] Progressive JPEG emitted for large photographic derivatives.
- [ ] Browser support matrix snapshot-dated in the recipe.
- [ ] Metadata stripping applied unless required otherwise.
- [ ] The format-per-purpose trade documented for review.

## Sources

- MDN image file type and format guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types>
- Web.dev image optimisation course: <https://web.dev/learn/images>
