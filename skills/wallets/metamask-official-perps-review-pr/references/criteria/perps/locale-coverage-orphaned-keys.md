# Locale Coverage & Orphaned Keys

Removing a `strings(...)` call or deleting a helper that wrapped locale keys is a regression risk that is cheap to catch during review.

- **Hardcoded string replacing a `strings(...)` call** — verify locale coverage across `locales/languages/*.json` before accepting the change. A key translated in only some of the supported locales is a quantified regression, not a nit.
- **Orphaned locale keys** — when a PR deletes a function that called `strings(...)`, grep for the keys it used (e.g. `rg 'order_card\.(take_profit|stop|open_limit|close_limit)' app`). Dead keys accumulate silently and bloat the translation pipeline; flag them even when runtime is unaffected.
- **Test revert-sensitivity for locale keys** — mocked `strings` implementations that fall back to `|| key` render the raw key when a key goes stale, so an exact `getByText` assertion still fails on revert. Confirm that fallback exists before accepting a test as regression-proof; do not assume it.
