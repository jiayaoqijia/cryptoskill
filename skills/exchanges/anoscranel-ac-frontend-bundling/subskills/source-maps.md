---
name: source-maps
domain: software-engineering/source-maps
trigger: "Making production errors readable without shipping readable source."
anti_trigger: "Not for runtime error tracking products, and not for editor debugging."
scope: "Debuggable production output without leaking source."
status: seedling
---

# Source maps

## Standard

Minified production code is unreadable by design, and a source map restores the mapping to the original files so a stack trace in production can point at real lines. The map is a build artefact with a decision attached: where it lives. Generated and uploaded to an error-tracking service, it serves production debugging while exposing nothing to the browser; served publicly alongside the bundle, it makes debugging possible for anyone who asks, including anyone who prefers reading source to reading your intentions in minified form.

The decision is therefore an exposure decision, made per environment. The useful pattern is to generate maps for every production build, upload them to a private error store, and never publish them. That keeps the debugging capability while the only source a visitor can read is what the bundle itself exposes.

Primary source: <https://web.dev/learn>.

## Decision rules

- Record which environments generate maps and where each map is stored.
- Prefer uploading maps to an error-tracking store over serving them publicly.
- Verify a real production stack trace resolves to a correct original line before relying on the pipeline.
- Track the build identifier with each upload so a trace maps to the exact build that produced it.
- Watch stack-frame accuracy across async boundaries; mappings can be misleading after transformations.
- Include the map's own source content decision in the record — embedded sources make a leaked map a full leak.

## Procedure

1. Record the mapping pipeline: transforms, minifier, and their map settings.
2. Choose storage per environment; document the exposure choice.
3. Generate a production build, upload its maps, and record the build identifier.
4. Trigger a known error and verify the trace resolves to the original line.
5. Test a trace across an async boundary.
6. Record the pipeline and the exposure decision.

## Anti-patterns

- Serving maps publicly because debugging was hard one afternoon.
- Skipping maps entirely and decoding minified traces by hand.
- Uploading maps without a build identifier, so traces map to the wrong build.
- Assuming vendor-library frames map as well as first-party ones.
- Embedding sources in public maps under the impression they are hidden.

## Done checklist

- [ ] Pipeline and map settings recorded.
- [ ] Storage and exposure decided per environment.
- [ ] Maps uploaded with build identifiers.
- [ ] Known-error trace verified.
- [ ] Async-boundary trace checked.
- [ ] Exposure decision documented.

## Sources

- Source maps specification: <https://tc39.github.io/source-map-spec/>
- Debugging production with maps: <https://web.dev/learn>
- Error monitoring and stack traces: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error>
