---
name: notifications-category-sync
description: >-
  Sync a client with the backend-driven notifications category manifest when the
  backend adds or changes a notification category, notification type, or
  preference (AUS) key. Use when asked to support a new notification category or
  type, add a notifications settings row, refresh the category fallback
  snapshot, or when logs report an unsupported notification category.
maturity: stable
---

# Notifications Category Sync

The notifications backend publishes a category manifest (`GET /api/v4/notifications/categories`, unauthenticated, same for every user). Clients render tabs and settings rows from it, but keep presentation (copy, icon, slug, detail screen) locally, keyed by the user-storage preference key (`aus_keys`). This skill closes the gap when the manifest gains or changes entries.

## When to use

- Backend added, removed, renamed or re-ordered a category, or changed its `aus_keys`, `notification_types` or `visible_on`
- A new preference key must get a settings row
- The local fallback snapshot no longer matches the live response
- Logs report an unsupported notification category

Out of scope: rendering a new notification type's body or push payload (notification-state mapping), and gating a feature behind notifications.

## Manifest contract

Each entry: `category_id`, `aus_keys[]`, `notification_types[]`, `visible_on[]`.

- Array order is display order.
- A client renders only entries whose `visible_on` includes its platform. Empty `visible_on` means hidden on every platform but still present in the manifest.
- `aus_keys` are the toggle pivot. Non-empty with no local section is a client bug: log the error and hide the row. Empty means display-only (inbox tab and filtering, no settings row, no error).
- `category_id` is backend-owned and may not match local naming. Resolve local sections and copy through `aus_keys`, never `category_id`.
- `notification_types` is advisory; notifications carry a server-resolved `category` (`''` means uncategorized).
- Keep the fallback snapshot aligned with the live response, including hidden entries and backend order. Clients may also use the fallback when the endpoint returns an empty category list. Check the consuming client’s resolver for its exact fallback condition.

## Workflow

1. **Diff live against the fallback.** Fetch the endpoint, normalize (sort keys and arrays), compare with the client's fallback snapshot. List added, removed and changed categories.
2. **Classify each change.**
   - New entry with empty `aus_keys`: display-only. Update the snapshot and its test, then verify.
   - New entry with an `aus_key` the client already supports: update the snapshot only.
   - New `aus_key`: full local support (steps 3-6).
   - Changed `visible_on`, `notification_types` or order: snapshot and tests only.
3. **Confirm the preference key exists** in the client's preference types. If the installed storage package lacks it, stop and report; a dependency bump is a separate decision.
4. **Add presentation for the key**: copy (title and description, in the source locale; other locales follow the repo's translation process), icon, deeplink slug, whether the row shows channel status, and any feature-flag gate.
5. **Register the section** in the local registry and every per-key map the compiler flags (analytics settings type, detail-screen layout).
6. **Mirror per-key touchpoints.** Grep an existing key in all spellings (camelCase, snake_case, kebab-case) and update every per-category list: deeplink docs and tests, API mocks, feature-gate config.
7. **Update the fallback snapshot and tests**: snapshot mirror, settings-row rendering, the unsupported-category log for non-empty `aus_keys` with no section, and display-only skipping. Assert the intended logging frequency separately if the client promises deduplication.
8. **Verify.** Re-run step 1 (no diff left), then the repo's unit tests, type check and lint.

Do not guess a multi-key category's copy or icon; ask. Do not bump dependencies silently.

## Common mistakes

- Keying local logic on `category_id` instead of `aus_keys`
- Dropping hidden entries from the fallback so it no longer mirrors the live response
- Adding a settings row for a display-only category
- Updating the section registry but not the type-keyed maps, which only fail at compile time
