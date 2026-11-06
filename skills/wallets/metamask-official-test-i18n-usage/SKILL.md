---
name: test-i18n-usage
description: Review locale keys, translation usage and locale-sensitive tests.
---

# Localization and locale-sensitive tests

Apply these checks to changed locale objects, translation call sites and their tests. Client-specific query conventions remain in the repository overlay.

Removing a translation call or its wrapper requires checking the affected keys and tests.

- **Duplicate JSON keys shadow new copy**: Verify the containing locale object has one definition and search rendered copy across every test layer. A test accommodating duplicate labels may hide an ambiguous product label.
- **Source-language translations** — keep user-facing copy behind translation helpers and update only the source-language file (`locales/languages/en.json` on Mobile; `app/_locales/en/messages.json` on Extension). The translation pipeline fills other locales; missing non-English strings are never a finding.
- **Orphaned locale keys** — when a PR deletes a function that called `strings(...)`, grep for the keys it used (e.g. `rg 'order_card\.(take_profit|stop|open_limit|close_limit)' app`). Dead keys accumulate silently and bloat the translation pipeline; flag them even when runtime is unaffected.
- **Test revert-sensitivity for locale keys** — mocked `strings` implementations that fall back to `|| key` render the raw key when a key goes stale, so an exact `getByText` assertion still fails on revert. Confirm that fallback exists before accepting a test as regression-proof; do not assume it.
