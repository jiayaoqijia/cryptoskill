---
repo: metamask-mobile
parent: notifications-category-sync
---

# Notifications Category Sync — MetaMask Mobile

## Where things live

| Concern | Path |
|---------|------|
| Fallback snapshot + `resolveNotificationCategories` (mobile filter, empty list → fallback) | `app/util/notifications/categories/notification-categories-api.ts` |
| Category request, loading state, and fetch-settled fallback behavior | `app/util/notifications/hooks/useNotifications.ts`; `app/util/notifications/categories/categories-fetch-settled.ts` |
| AUS key → i18n stem (`AUS_KEY_TO_I18N_STEM`) | `app/util/notifications/categories/notification-categories-i18n.ts` |
| Flag gate (`socialAI`) and in-app inbox preference filtering | `app/util/notifications/categories/notifications-settings-types.ts` |
| Notification list filtering and category-scoped mark-as-read | `app/components/Views/Notifications/index.tsx` |
| Inbox behavior tests, including category/All mark-as-read | `app/components/Views/Notifications/index.test.tsx` |
| Section registry (`NOTIFICATION_SETTINGS_SECTIONS`, slugs, deeplink resolver) | `app/components/Views/Settings/NotificationsSettings/notificationSettingsSections.ts` |
| Settings rows + unsupported-category `Logger.error` | `app/components/Views/Settings/NotificationsSettings/index.tsx` |
| Per-section detail maps (`SETTINGS_TYPE_BY_SECTION`, layout) | `app/components/Views/Settings/NotificationsSettings/NotificationSettingsSectionContent.tsx` |
| Preference key type (`NotificationPreferenceSection`) | `app/util/notifications/hooks/useNotificationStoragePreferences.ts` (derived from `@metamask/authenticated-user-storage`; `agenticCli` is made required via Omit/Required) |
| Tabs (testID from `categoryTestID(category_id)`) | `app/components/Views/Notifications/NotificationsCategory/` |
| Startup fetch | `useFetchNotificationCategoriesEffect` in `app/util/notifications/hooks/useStartupNotificationsEffect.ts` |

## Step details

1. **Diff**
   ```bash
   curl -s https://notification.api.cx.metamask.io/api/v4/notifications/categories \
     | jq -S 'map(.visible_on |= sort | .aus_keys |= sort | .notification_types |= sort)'
   ```
   Compare with `FALLBACK_NOTIFICATION_CATEGORIES` and update `notification-categories-api.test.ts`. The current resolver also uses the fallback when the category list is empty, not only when a request fails. If every new category has empty `aus_keys`, skip to Verify.
3. **Package**: check the key exists in the installed `@metamask/authenticated-user-storage` `NotificationPreferences` (`package.json`).
4. **Copy**: add the key to `AUS_KEY_TO_I18N_STEM`; add `app_settings.notifications_opts.<stem>_title` and `<stem>_desc` to `locales/languages/en.json` only. Other locale files are updated by the translation process, so leave them untouched. Extend `notification-categories-i18n.test.ts`.
5. **Registry**: add the kebab slug to `NotificationSettingsSectionSlug` and an entry to `NOTIFICATION_SETTINGS_SECTIONS` (`slug`, `type` = AUS key, `titleKey`, `descriptionKey`, a valid `IconName`, `showStatus`, `requiresSocialLeaderboard` only if flag-gated). Add the key to the maps in `NotificationSettingsSectionContent.tsx`; both are `Record<NotificationPreferenceSection, …>`, so `yarn lint:tsc` flags a miss. Update `notificationSettingsSections.test.ts` and the section content tests.
6. **Touchpoints**: grep `priceAlerts|price_alerts|price-alerts|agenticCli` across `app docs tests locales` (skip `tests/coverage`). Known hits:
   - `tests/api-mocking/mock-responses/defaults/user-storage.ts` (AUS preferences mock)
   - `docs/readme/deeplinking.md` (section slug list and the `notifications-settings` row) and `handleNotificationsSettingsUrl` tests
   - `featureNotificationsGateConfig.ts` and `notifications.feature_gate.<stem>.*` locale keys, only if the feature uses the gate
   - flag gate in `getNotificationsSettingsSectionConfigs` if the category is flag-gated
   - new `notification_types` needing inbox rendering: `notification-states/` and `TRIGGER_TYPES` from `@metamask/notification-services-controller`
7. **Tests**: `NotificationsSettings/index.test.tsx` and `NotificationsSettings.view.test.tsx`; the unsupported log uses `Logger.error` from `app/util/Logger`. Cover inbox filtering and category-scoped mark-as-read in `app/components/Views/Notifications/index.test.tsx`. The settings test checks one log on initial render; it does not guarantee deduplication across later category updates.

## Verify

```bash
yarn jest app/util/notifications app/components/Views/Settings/NotificationsSettings app/components/Views/Notifications
yarn lint:tsc
yarn lint
```

User-facing changes need a CHANGELOG entry (see the `pr-changelog` skill).
