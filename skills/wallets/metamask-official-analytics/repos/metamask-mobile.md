---
repo: metamask-mobile
parent: analytics
---

# Analytics — MetaMask Mobile

Human-facing file map: `app/core/Analytics/README.md`. A/B enrichment SSOT: `docs/ab-testing.md`.

## Canonical API

| Role | Path |
|------|------|
| Helper (non-React) | `app/util/analytics/analytics.ts` → `analytics.trackEvent` |
| Helper (UI) | `app/components/hooks/useAnalytics/useAnalytics.ts` → `useAnalytics` |
| Engine (controllers) | `app/core/Engine/utils/analytics.ts` → `trackEvent`, `buildAndTrackEvent` |
| Event builder | `app/util/analytics/AnalyticsEventBuilder.ts` → `AnalyticsEventBuilder.createEventBuilder` |
| Catalog | `app/core/Analytics/` → `MetaMetricsEvents` at call sites; `EVENT_NAME` in catalog modules |
| Typed helpers | `app/util/analytics/actionButtonTracking.ts` (sibling files matching `*Tracking.ts`) |
| A/B registry | `app/util/analytics/abTestAnalyticsRegistry.ts` (feature-local `abTestConfig.ts`, e.g. `app/components/Views/Homepage/abTestConfig.ts`) |
| Test factory | `app/util/test/analyticsMock.ts` → `createMockUseAnalyticsHook` (default); `createMockEventBuilder` (optional standalone double) |

`useAnalytics()` returns `trackEvent`, `createEventBuilder`, `identify`, `enable`,
`isEnabled`, `getAnalyticsId`, and data-deletion helpers.

Controllers that already talk to Engine import `trackEvent` / `buildAndTrackEvent`
from `app/core/Engine/utils/analytics.ts`. Those helpers always wrap the
messenger call in try/catch. `enrichWithABTests` runs only when the event name
is registered in `app/util/analytics/abTestAnalyticsRegistry.ts` (fed by
feature-local `abTestConfig.ts`). New experiment events: follow
`docs/ab-testing.md`. Do not copy Engine-util internals.

`createMockEventBuilder()` default `build()` is
`{ name: 'mock-event', properties: {}, sensitiveProperties: {} }`. Use it only
as a standalone builder double, wrapped in `jest.fn(() => createMockEventBuilder())`.

## Requirements

- UI: platform `useAnalytics` from `app/components/hooks/useAnalytics/useAnalytics.ts`
- Non-React: `analytics.trackEvent`
- Controllers: `trackEvent` / `buildAndTrackEvent` from `app/core/Engine/utils/analytics.ts`
- When a typed helper exists in `app/util/analytics/` (files matching `*Tracking.ts`) for this event, call it
- Call sites (new and existing) import `MetaMetricsEvents.*`. Register new names as `EVENT_NAME` + `generateOpt` in catalog modules, then emit via `MetaMetricsEvents`. Reuse a catalog name only when this control is the same interaction as existing call sites (same event, same product meaning).
- Properties via `.addProperties(...).build()`
- UI tests: `createMockUseAnalyticsHook` wrapping `useAnalytics`, including when the file already mocks the hook. Default: `createMockUseAnalyticsHook({ trackEvent: mockTrackEvent })`. Tests that assert `addProperties` keep `AnalyticsEventBuilder.createEventBuilder`
- Non-React tests: assert `AnalyticsEventBuilder.createEventBuilder` and `analytics.trackEvent` or Engine `trackEvent` / `buildAndTrackEvent`

Generic UI (`app/components/UI/BalanceEmptyState/BalanceEmptyState.tsx`):

```ts
import React from 'react';
import { MetaMetricsEvents } from '../../../core/Analytics';
import { useAnalytics } from '../../hooks/useAnalytics/useAnalytics';

const BalanceEmptyState: React.FC<BalanceEmptyStateProps> = ({
  testID = 'balance-empty-state',
  ...props
}) => {
  const { trackEvent, createEventBuilder } = useAnalytics();

  const handleAction = () => {
    trackEvent(
      createEventBuilder(MetaMetricsEvents.RAMPS_BUTTON_CLICKED)
        .addProperties({
          button_text: 'Add funds',
          location: 'BalanceEmptyState',
          ramp_type: 'UNIFIED_BUY_2',
        })
        .build(),
    );
  };
```

Typed helper (`app/components/Views/Homepage/components/HomepageActionButtonsGrid/buttons/SendButton.tsx`):

```ts
import React, { useCallback } from 'react';
import { useAnalytics } from '../../../../../hooks/useAnalytics/useAnalytics';
import {
  ActionButtonType,
  ActionLocation,
  trackActionButtonClick,
} from '../../../../../../util/analytics/actionButtonTracking';

const SendButton = ({
  actionPosition,
  allowTwoLineLabel,
  onSend,
}: SendButtonProps) => {
  const { trackEvent, createEventBuilder } = useAnalytics();

  const handlePress = useCallback(() => {
    trackActionButtonClick(trackEvent, createEventBuilder, {
      action_name: ActionButtonType.SEND,
      action_position: actionPosition,
      button_label: label,
      location: ActionLocation.HOME,
    });
    onSend();
  }, [actionPosition, createEventBuilder, label, onSend, trackEvent]);
```

Non-React (`app/util/analytics/accountAccessTracking.ts`):

```ts
import { MetaMetricsEvents } from '../../core/Analytics/MetaMetrics.events';
import { analytics } from './analytics';
import { AnalyticsEventBuilder } from './AnalyticsEventBuilder';

analytics.trackEvent(
  AnalyticsEventBuilder.createEventBuilder(
    MetaMetricsEvents.APP_UNLOCKED_FAILED,
  )
    .addProperties({
      unlock_error_type: unlockErrorType,
      forced_reset: forcedReset,
    })
    .build(),
);
```

Controllers:

```ts
import { buildAndTrackEvent } from '../../core/Engine/utils/analytics';
import { MetaMetricsEvents } from '../../core/Analytics';

buildAndTrackEvent(
  initMessenger,
  MetaMetricsEvents.PROFILE_ACTIVITY_UPDATED.category,
  {
    profile_id: profileId,
    feature_name: 'Contacts Sync',
    action: 'Contacts Sync Contact Updated',
  },
);
```

`createEventBuilder` copies only `category` from `IMetaMetricsEvent`. When
migrating a wrapper that used `generateOpt(name, action, description)`, re-apply
`properties.action` and `properties.name` with `addProperties`.

`generateOpt` belongs in catalog modules: `app/core/Analytics/MetaMetrics.events.ts`,
`app/core/Analytics/events/`, and feature-local `<feature>/analytics/events.ts`
(see SampleFeature). Component files import catalog entries; they do not call
`generateOpt` themselves.

Tests mock the hook with the factory, not a hand-built object.
Call `createMockUseAnalyticsHook` again in `beforeEach` after
`jest.resetAllMocks()` — that wipes mock implementations. `jest.clearAllMocks()`
does not.

```ts
import { useAnalytics } from '../../hooks/useAnalytics/useAnalytics';
import { createMockUseAnalyticsHook } from '../../../util/test/analyticsMock';

jest.mock('../../hooks/useAnalytics/useAnalytics');

beforeEach(() => {
  jest.resetAllMocks();
  jest.mocked(useAnalytics).mockReturnValue(
    createMockUseAnalyticsHook({
      trackEvent: mockTrackEvent,
    }),
  );
});
```

Standalone builder double (only when the test needs one):

```ts
createEventBuilder: jest.fn(() => createMockEventBuilder()),
```

## Reject

- `addSensitiveProperties` on new tracking. Existing call sites: drop those
  fields only. Moving the last sensitive field into `addProperties` flips
  `isAnonymous` (true iff `sensitiveProperties` is nonempty). Do not relocate
  without human sign-off.
- A new feature-local tracker that is not a file matching `*Tracking.ts` under
  `app/util/analytics/`, a feature-local `abTestConfig.ts`, or a catalog
  `generateOpt` module (`app/core/Analytics/MetaMetrics.events.ts`,
  `app/core/Analytics/events/`, `<feature>/analytics/events.ts`)
- Replacing `MetaMetricsEvents.*` at a call site with `EVENT_NAME.*`
- Reintroducing `useMetrics` (removed) or MetaMetrics internals at call sites
- Dropping `generateOpt` `action` / `name` when migrating `IMetaMetricsEvent` call sites (until the catalog migration lands)
- Hand-built `useAnalytics` mock objects — use `createMockUseAnalyticsHook`
- Raw `initMessenger.call('AnalyticsController:trackEvent', …)` when Engine
  `trackEvent` / `buildAndTrackEvent` is available
- Defaulting UI tests to `createEventBuilder: jest.fn(() => createMockEventBuilder())`
  when `createMockUseAnalyticsHook()` already stubs the builder
- Attaching a new control to a catalog event whose live call sites are a different product (example: `VIEW_ALL_ASSETS_CLICKED` is wallet tokens/NFTs `asset_type`, not a homepage section)
- Firing an existing catalog event at a new lifecycle (example: `TOKEN_DETECTED` on controller init). Add a catalog name for that lifecycle.
