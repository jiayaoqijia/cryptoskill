---
repo: metamask-mobile
parent: device-capability
---

# Device capability — MetaMask Mobile

Canonical API doc, thresholds, latency cutoffs, sampling rules and file map: `app/util/deviceCapability/README.md`. The README wins over the matrix in this skill.

## Canonical API

| Signal | API | Import | Returns |
|--------|-----|--------|---------|
| Hardware tier | `getHardwareTier()` | `app/util/deviceCapability` | `'LOW' \| 'MID' \| 'HIGH' \| null` |
| Network tier | `useNetworkTier()` | `app/hooks/useNetworkTier` | `'NONE' \| 'SLOW_CELLULAR' \| 'FAST_CELLULAR' \| 'WIFI' \| null` |
| Network tier plus resolution | `useNetworkTierState()` | `app/hooks/useNetworkTier` | `{ tier, isResolved }` |
| Live latency | `useNetworkLatency()` | `app/hooks/useNetworkLatency` | `'UNKNOWN' \| 'OK' \| 'SLOW'` |
| Settled latency | `useSettledNetworkLatency()` | `app/hooks/useNetworkLatency` | `'UNKNOWN' \| 'OK' \| 'SLOW'` |

- `getHardwareTier()` is a function, not a hook. RAM is static for the process.
- Use `useNetworkTierState()` only when the flow must tell NetInfo's initial loading state from a resolved but unclassified transport.
- Use `useSettledNetworkLatency()` for UI that must survive an app resume, such as a banner. It keeps the last `OK` or `SLOW` reading. `useNetworkLatency()` resets to `UNKNOWN` on resume.
- The hardware tier only calibrates the latency cutoffs. It never changes the network tier.
- `useNetworkTier()` does not read latency and does not re-render on it. `SLOW_CELLULAR` still means 2g and 3g only.
- `null` means unknown. `'NONE'` means known no usable internet. Never treat `null` as LOW or offline.

Examples of the matrix in use: `app/components/UI/Money/hooks/useMoneyVaultState.ts`, `app/components/UI/PredictNext/homeSection/internal/next/NextHomeDiscovery.tsx`, `app/components/UI/PredictNext/trending/internal/next/useTrendingLiveDataAllowed.ts`.

## Forbidden

- `DeviceInfo.getTotalMemory` and `getTotalMemorySync` outside `app/util/deviceCapability`.
- Mapping NetInfo `type` or `cellularGeneration` to a custom enum outside `computeNetworkTier`.
- Reimplementing `LATENCY_THRESHOLDS` or the `SLOW` entry and exit rules.
- Treating iOS simulator RAM as a device tier. It can be the Mac's RAM.

Latency samples hold only durations. Never send them, or anything derived from a URL or host, to Redux, Sentry or analytics. See the README.

## Testing

Follow `mobile-testing`. Mock `getHardwareTier` and the hooks. For each adapted behaviour, cover at least one constrained cell and one `null` or `UNKNOWN` case.

## Maintenance

A change to the matrix in `app/util/deviceCapability/README.md` updates `domains/platform/skills/device-capability/skill.md` in the same release cycle.
