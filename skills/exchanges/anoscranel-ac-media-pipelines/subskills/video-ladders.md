---
name: video-ladders
domain: software-engineering/video-ladders
trigger: "Designing the rendition ladder for adaptive video delivery."
anti_trigger: "Not for realtime transport, and not for capacity profiling."
scope: "One source → multiple renditions; adaptive bitrate and resolution ladders; HLS/DASH segments; the economics of duration × resolution × codec."
status: seedling
---

# Video ladders

## Standard

Video is not delivered at "one resolution" — it is delivered as a **ladder** of renditions at different bitrates and resolutions, and the player climbs or descends that ladder as bandwidth changes. A source video at ingest becomes, for example, five or eight renditions spanning "360p on a bad mobile connection" to "1080p high-quality on a good one", plus audio-only fallbacks for constrained contexts. The ladder is a property of the pipeline: it is defined at transcode time, emitted as a fixed derivative set, and packaged into streaming formats (HLS and DASH segment playlists) for adaptive playback.

The ladder is where the pipeline's economics become visible. Each rung costs transcoding time and storage, and the cost scales with duration × resolution × codec efficiency — a single source can generate an hour of encoding work across a full ladder, and the output can exceed the source's own size. The record therefore states the ladder per use case: a social-media clip served once needs a shorter ladder than a feature-length film served for years, and "transcode everything to every rung" is a policy that must be argued for, not defaulted into.

**Segment packaging** closes the loop. HLS and DASH cut each rendition into segments (commonly a few seconds each) and describe them in a playlist manifest; the player fetches the manifest, then pulls segments at the ladder rung the network currently supports. The pipeline's job is to emit consistent, correctly-keyframed segments — every rung must share the same segment boundaries and the same keyframe alignment, or the player's ladder transitions stutter visibly.

## Decision rules

- Define the ladder explicitly per use case: resolutions, bitrates, and codec, with a stated audience-quality floor and ceiling.
- Segment alignment across rungs: keyframes and segment boundaries match so ladder transitions are seamless.
- Rung cost is computed and recorded: transcode time and storage per rung, not just "did it finish".
- The ladder is derivative metadata: the manifest describes the set; the set is regenerable from source + recipe.
- Audio-only renditions are part of the ladder, not an afterthought.
- A ladder change is a recipe-version change; re-encoding is deliberate, not triggered by a config edit.


## Procedure

1. Choose the ladder rungs (resolution × bitrate × codec) per use case and audience.
2. Configure the encoder to emit all rungs with aligned keyframes and segment boundaries.
3. Package each rung into the streaming format's segments and manifests.
4. Record per-rung cost (transcode time, storage) alongside the recipe.
5. Deliver the manifest; the player negotiates rungs, the pipeline does not.
6. When the ladder changes, bump the recipe version and regenerate deliberately.

## Anti-patterns

- A single-rendition pipeline where "adaptive" is hoped for later.
- Ladders accreted by adding rungs without reviewing whether old ones still serve.
- Segment boundaries that differ across rungs, producing visible ladder-switch stutter.
- Choosing rungs by benchmark folklore instead of measured audience bandwidth.

## Done checklist

- [ ] Ladder defined per use case with floor and ceiling.
- [ ] Keyframe/segment alignment verified across rungs.
- [ ] Per-rung cost recorded in the recipe.
- [ ] Audio-only rungs included.
- [ ] Manifest and segments emitted as derivatives, regenerable from recipe.
- [ ] Ladder changes bump the recipe version.

## Sources

- MDN web video codec guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs>
- MDN media containers guide: <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Containers>
