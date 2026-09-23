# Pro Mode UI Gating

Pro market UI renders only when the remote flag (`selectPerpsProModeEnabledFlag`) and the controller mode (`PerpsMode.Pro`) are both active; a PR that checks one gate ships a silent no-op that looks like a feature flag bug.

- **Single-gate assumption** — checking only `selectPerpsProModeEnabledFlag` (remote feature flag) without also verifying the controller mode is `PerpsMode.Pro`. Both must be true for Pro UI to render.
- **Fixture runs lite-only** — CI fixtures and agent slots do not force Pro mode by default. If a PR adds Pro-mode-only UI that cannot be reached in lite fixtures, plan `generate-internal` + unit tests as the validation path instead of attempting live CDP navigation to Pro screens.
- **Pro-only code tested only via live UI** — pure business logic shared between lite and Pro (e.g., `orderSizing`, `orderParams`, `tpslValidation`) should be extended in the shared helper, not re-inlined in either form. Tests against the shared helper work in any fixture mode.
- **Modal wrapper omitted in width-constrained layouts** — in the Pro layout, parent columns are width-constrained; bottom sheets must be wrapped in a Modal so they are not clipped. Android additionally requires `onRequestClose` on the Modal and a plain `View` (not a styled container) as the immediate wrapper child.
- **Hardcoded tab index across feature gates** — derive selection from the rendered tab configuration or a stable tab ID. Test each supported gate combination so a newly inserted tab cannot move another tab's content or controls.
