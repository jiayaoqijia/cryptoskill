---
repo: metamask-mobile
parent: feature-flags
---

# Feature flags — MetaMask Mobile

Human-facing file map: `docs/readme/version-gated-feature-flags.md`.

## Canonical API

| Role | Path |
|------|------|
| Helper | `app/util/remoteFeatureFlag/index.ts` → `validatedVersionGatedFeatureFlag`, `hasMinimumRequiredVersion` |
| Raw flags | `RemoteFeatureFlagController.remoteFeatureFlags` (no client version gating) |
| Selectors | `app/selectors/featureFlagController/` or `**/selectors/featureFlags/` |
| Names (when the flag is overrideable in dev tools) | `app/constants/featureFlags.ts` → `FeatureFlagNames` |

`validatedVersionGatedFeatureFlag` compares against the native binary version from `react-native-device-info` `getVersion()`, not `package.json`. Progressive-rollout wrappers `{ name, value: { enabled, minimumVersion } }` are unwrapped in the helper.

`hasMinimumRequiredVersion` is the lower-level compare used inside the helper. Import it from the util only for a standalone version check.

Multi-version flags shaped `{ versions: { "7.53.0": value } }` are resolved at fetch time by the controller. Consumers read the processed value — no helper call for that shape.

## Requirements

- Selectors call `validatedVersionGatedFeatureFlag`. UI and hooks only `useSelector(selectXEnabled)`.
- Non-standard flag shapes (e.g. `active` instead of `enabled`) map to `{ enabled, minimumVersion }` before the helper.
- Remote flag wins when valid. Use `?? env/local` when the helper returns `undefined` (invalid shape, or `OVERRIDE_REMOTE_FEATURE_FLAGS=true`).

```ts
import { createSelector } from 'reselect';
import { selectRemoteFeatureFlags } from '../index';
import {
  validatedVersionGatedFeatureFlag,
  type VersionGatedFeatureFlag,
} from '../../../util/remoteFeatureFlag';

export const selectMyFeatureEnabled = createSelector(
  selectRemoteFeatureFlags,
  (remoteFeatureFlags) => {
    const localFlag = process.env.MM_MY_FEATURE_ENABLED === 'true';
    const remoteFlag =
      remoteFeatureFlags?.myFeature as unknown as VersionGatedFeatureFlag;

    return validatedVersionGatedFeatureFlag(remoteFlag) ?? localFlag;
  },
);
```

Non-standard shape:

```ts
validatedVersionGatedFeatureFlag({
  enabled: depositConfig.active ?? false,
  minimumVersion: depositConfig.minimumVersion ?? '',
}) ?? false;
```

UI:

```ts
const isEnabled = useSelector(selectMyFeatureEnabled);
```

## Reject

- Local copies of `hasMinimumRequiredVersion` or `validatedVersionGatedFeatureFlag`
- Inline `compare-versions` + `getVersion` for feature-flag gating outside `app/util/remoteFeatureFlag`
- Version checks in hooks or components (`getVersion()`, `compare-versions`, or a local helper)
- Duplicate util files under `app/components/UI/**/utils/` or `app/core/redux/slices/**/`
