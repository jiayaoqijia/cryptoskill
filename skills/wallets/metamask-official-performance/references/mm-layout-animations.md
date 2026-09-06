---
title: Layout Animations on the JS Thread (MetaMask)
impact: HIGH
tags: animated, usenativedriver, reanimated, layout, jank
---

# Skill: Layout Animations on the JS Thread

The legacy `Animated` API **cannot** use the native driver for layout properties (`width`, `height`, `flex`, `top`/`left`). Animating those forces `useNativeDriver: false`, which runs the animation on the **JS thread** — so it competes with React rendering and stutters whenever JS is busy (exactly when the user is interacting).

## How to spot it

```jsx
Animated.timing(widthAnim, {
  toValue: target,
  duration: 300,
  useNativeDriver: false,   // ← forced, because width is a layout prop
}).start();
```
`useNativeDriver: false` animating a **layout** prop = JS-thread animation. (`false` for `backgroundColor`/other non-layout props is a different, smaller issue.)

## Verified MetaMask instances (12 across 6 files)

| File | Notes |
|---|---|
| `WalletHomeOnboardingSteps.tsx` (×2) | progress-bar **width** during onboarding — first-run UX, worst place for jank |
| `Carousel/animations/useTransitionToEmpty.ts` | **height** collapse (comment even says "Height needs layout thread") |
| `NetworksManagement/hooks/useExpandableFormAnimation.ts` (×4) | height expand/collapse — 4 JS-thread animations on one interaction |
| `WhatsNewModal.tsx` | layout property |
| `TabsBar.tsx` (×2) | tab indicator |

## Fix — Reanimated v3 (already installed)

Reanimated v3 **can** animate layout props on the UI thread.

```jsx
// BEFORE — legacy Animated, JS thread
const widthAnim = useRef(new Animated.Value(0)).current;
Animated.timing(widthAnim, { toValue: target, duration: 300, useNativeDriver: false }).start();
// style={{ width: widthAnim }}

// AFTER — Reanimated v3, UI thread
import Animated, { useSharedValue, useAnimatedStyle, withTiming } from 'react-native-reanimated';
const width = useSharedValue(0);
const animatedStyle = useAnimatedStyle(() => ({ width: width.value }));
width.value = withTiming(target, { duration: 300 });
// <Animated.View style={animatedStyle} />
```

For a progress bar, animate a `0→1` shared value and `interpolate` to width, or animate `transform: [{ scaleX }]` (a transform — even cheaper, and works with the native driver in legacy `Animated` too if you can express it as a transform).

> Use **v3** APIs only (`useSharedValue`, `useAnimatedStyle`, `withTiming`, `runOnJS`). `react-native-worklets` / `scheduleOnRN` are **v4** and not installed — see [js-animations-reanimated.md](js-animations-reanimated.md).

## When you can't avoid layout

If a true layout reflow is unavoidable (content-driven height with unknown size), consider:
- `transform: scaleX/scaleY` instead of `width`/`height` where visually acceptable (GPU, no reflow).
- `LayoutAnimation` for one-shot layout transitions (still native-driven).
- Keeping the JS-thread animation but ensuring no heavy JS runs concurrently (last resort).

## How to find

```bash
grep -rn "useNativeDriver: false" app --include="*.tsx" --include="*.ts" | grep -v ".test."
```
For each, check the animated style prop: layout prop (`width`/`height`/`flex`/`top`/`left`) → migrate to Reanimated v3 or a transform. Non-layout prop → lower priority.

## Verify

- Perf Monitor: **UI thread** FPS holds ~60 during the animation, even if you trigger JS work mid-animation.
- React Native DevTools: the animation drives **no** React re-renders (shared values bypass React).

## Designed / vector animations → Rive

For complex *designed* animations (not value-driven UI motion), prefer **Rive** (`rive-react-native`, already installed) over Lottie — smaller files, GPU-driven, state-machine support. Usage + a real in-app example (`OnboardingAnimation.tsx`) are in [`docs/readme/animations.md`](../../../../docs/readme/animations.md).

## Related

- [js-animations-reanimated.md](js-animations-reanimated.md) — full v3 API + patterns
- [mm-context-performance.md](mm-context-performance.md) — don't plumb animated values through Context as React state
- [js-measure-fps.md](js-measure-fps.md) — confirm the FPS win
