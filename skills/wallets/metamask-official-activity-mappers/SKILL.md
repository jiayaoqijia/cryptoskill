---
name: activity-mappers
description: >-
  Guidance for Activity List and Activity Item changes: start in
  `@metamask/client-utils/mappers` to share behavior across the mobile and
  extension apps. Prefer API data, or the keyring transaction for non-EVM;
  avoid massaging local state. Use when changing Activity List, Activity Item,
  or their data mapping.
---

# Activity Mappers

## When To Use

- Changing the Activity List or Activity Item
- Changing the data used to render an Activity List or Activity Item

## In Scope

- Extension: `ui/pages/activity`, `ui/pages/details`, `shared/lib/activity`
- Mobile: `app/components/views/Activity`, `app/components/views/ActivityDetails`, `app/util/activity-adapters`

## Workflow

1. Start in [`@metamask/client-utils/mappers`](https://github.com/MetaMask/core/tree/main/packages/client-utils/src/mappers).
2. Prefer data from the API. For non-EVM activity, use the keyring transaction.
3. Avoid massaging local state because it does not exist in other instances.
4. Add or update the unit tests in the mappers package.