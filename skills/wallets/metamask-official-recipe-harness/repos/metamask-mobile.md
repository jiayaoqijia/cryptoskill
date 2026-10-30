---
repo: metamask-mobile
parent: recipe-harness
---

# Mobile

- Exclude harness overlay paths from product diffs/PR evidence.
- Pin one explicit device when more than one is connected. Native screenshot provider and selected-device provenance are discoverable with `mm-harness actions --action ui.screenshot --json`.
- Prefer DevLogger or a run-scoped log watch for non-visual reproduction speed.
- Recover only through `mm-harness` and the `Next:` commands it prints; never run `yarn watch:clean`, `expo run:ios`/`run:android`, `xcodebuild`, `watchman` or cache deletes yourself.

## Source-build feature gates

For release QA, inspect the frozen branch's selector rather than assuming it has main's local environment fallbacks. `OVERRIDE_REMOTE_FEATURE_FLAGS=true` makes `validatedVersionGatedFeatureFlag` ignore controller flags. A controller value of `enabled: true` therefore does not prove that the UI feature is enabled. Mobile 8.14.0's Pro selector falls back to false in this configuration, even if a newer farm template supplies `MM_PERPS_PRO_MODE_ENABLED=true`.

Use `OVERRIDE_REMOTE_FEATURE_FLAGS=false` for release-like source QA unless the selected scenario explicitly tests local fallbacks. Apply the environment before starting the owned Metro runtime, pin any scenario-specific flags through the harness, then verify the app's visible entry point. Record the environment/flag variant with the build identity. An environment change may require a JavaScript rebundle; it is not by itself a reason to rebuild or reinstall the native app. Keep this setup outside the proof window.
