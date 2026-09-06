---
title: Planning & System Design for Performance (MetaMask)
impact: HIGH
tags: planning, system-design, architecture, risk, acceptance-criteria
---

# Skill: Planning & System Design

The cheapest performance fix is the one you make before writing code. Catch architectural risk in the ticket/PRD and design phases.

## What to do with a feature description / ticket

1. Ask about the **data profile** (volume, update frequency, growth, sources).
2. Map answers to the risk table below.
3. Output a **risk checklist + mitigations** to paste into the ticket, plus **performance acceptance criteria**.
4. Flag for Mobile Platform review if it hits any Critical/High risk.

## Risk table

| Risk | Trigger question | Default mitigation |
|---|---|---|
| Real-time / WebSocket data | Updates faster than once per user action? | Never put it in Redux. Local state / shared value / direct UI update. Manage subscribe/unsubscribe by visibility + app foreground/background; avoid double-subscribe. See [mm-redux-antipatterns.md](mm-redux-antipatterns.md). |
| Unbounded data | Can the list/dataset grow without ceiling? | Paginate + virtualize from day one; plan server-side filtering. |
| Large lists | >~50 items now, infinite later? | FlashList v2 with stable keys + `getItemType`; no heavy work per item. [js-lists-flatlist-flashlist.md](js-lists-flatlist-flashlist.md) |
| New selector / derived state | Adding `createSelector`? | Decide memoization + equality up front; never identity/mutation. [mm-selector-memoization.md](mm-selector-memoization.md) |
| Heavy computation | Big transforms, sorts, regex on large input? | Server offload, or memoize, or defer with `useDeferredValue`. |
| Crypto | Hashing/signing/derivation in hot path? | `react-native-quick-crypto` (already installed); keep off the JS thread. |
| New npm dependency | Adds to `package.json`? | Check size (Expo Atlas / bundlephobia); avoid main-package/barrel imports; reuse existing libs (we already have dayjs, luxon, lodash). [bundle-library-size.md](bundle-library-size.md) |
| Multiple API calls per screen | 3+ independent fetches on mount? | Aggregate / `Promise.all` / BFF proxy. |
| High-frequency dispatch | >~1 Redux dispatch/sec steady state? | Keep Redux for persistence; transient state local. |
| Images / animations | New hero images or animations? | Compressed images via `expo-image`; **Rive** (already installed) over Lottie. |
| New screen in a tab navigator | Heavy screen mounted eagerly? | Lazy-load (`React.lazy`) or defer heavy work off the startup path. |
| Layout animation | Animating width/height/flex? | Reanimated v3 on the UI thread, not `Animated` + `useNativeDriver:false`. [mm-layout-animations.md](mm-layout-animations.md) |

## System-design checklist

- **State shape:** new Redux slice for real-time data? → flag. New selector? → memoization + equality decided now.
- **Subscription lifecycle:** diagram subscribe/unsubscribe tied to mount/unmount + foreground/background; no double-subscribe; cleanup guaranteed.
- **List strategy:** ScrollView only for <20 fixed items; FlashList for anything that can grow; no `.map()` in JSX for growable lists.
- **Data flow:** minimize how many components subscribe to a frequently-updating selector.
- **Instrumentation up front:** which flows get a `trace()` span? Add the `TraceName` now. [native-measure-tti.md](native-measure-tti.md)
- **Test plan:** which components get a Reassure perf-test; does the flow warrant an E2E performance gate.

## Acceptance-criteria template

```
- [ ] No FPS drop below ~55 on a mid-range Android during [interactions], power-user data
- [ ] [Flow] completes within [X] ms under the power-user scenario (trace())
- [ ] Memory stays flat over an [N]-minute session with power-user data
- [ ] Verified on Android with ~30 accounts / ~90 assets
- [ ] Reassure perf-test added for [component] / E2E perf gate added for [flow] (if applicable)
```

## Team gate

Include the Mobile Platform team in PRD review for features that hit real-time data, unbounded lists, heavy computation, or new core-flow selectors.

## Related

- [mm-power-user-scenario.md](mm-power-user-scenario.md) — the baseline these criteria assume
- [mm-audit-playbook.md](mm-audit-playbook.md) — verify the implementation against this plan
