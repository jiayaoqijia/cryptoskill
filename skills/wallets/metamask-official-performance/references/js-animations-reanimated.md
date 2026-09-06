---
title: High-Performance Animations (Reanimated v3)
impact: MEDIUM
tags: reanimated, animations, worklets, ui-thread, usenativedriver
---

# Skill: High-Performance Animations (Reanimated v3)

Run animations on the UI thread so they stay smooth even when the JS thread is busy.

> **MetaMask note (verified):** This app is on **`react-native-reanimated@3.19.0`** and uses the **v3 API** (`runOnJS`/`runOnUI`, 83 usages; `scheduleOnRN`/`scheduleOnUI`: 0). **`react-native-worklets` is NOT installed.** Do **not** use the Reanimated v4 APIs (`scheduleOnRN`, `scheduleOnUI`, `react-native-worklets/plugin`) — they don't apply here. The reanimated babel plugin (`react-native-reanimated/plugin`) is already configured **last** in `babel.config.js`, which is required for `'worklet'` directives.

## Quick Pattern

**Incorrect (animation runs on the JS thread; janky when JS is busy):**

```jsx
const opacity = useRef(new Animated.Value(0)).current;
Animated.timing(opacity, { toValue: 1, useNativeDriver: true }).start();
```

**Correct (UI thread via Reanimated v3):**

```jsx
import Animated, { useSharedValue, useAnimatedStyle, withTiming } from 'react-native-reanimated';

const opacity = useSharedValue(0);
const style = useAnimatedStyle(() => ({ opacity: opacity.value }));
opacity.value = withTiming(1);
// <Animated.View style={style} />
```

## The MetaMask problem this targets: layout animations on the JS thread

There are **12 instances of `useNativeDriver: false`** across 6 files (e.g. `WalletHomeOnboardingSteps`, `Carousel/animations/useTransitionToEmpty`, `NetworksManagement/useExpandableFormAnimation`, `TabsBar`). `useNativeDriver: false` is required by the **legacy `Animated` API** whenever you animate **layout** props (`width`, `height`, `flex`) — the native driver can't drive layout. So these animations run entirely on the JS thread and compete with React rendering.

**The fix is Reanimated v3**, which *can* animate layout props on the UI thread:

```jsx
// BEFORE — legacy Animated, JS thread (blocks during heavy JS)
Animated.timing(widthAnim, {
  toValue: target,
  duration: 300,
  useNativeDriver: false,   // forced, because width is a layout prop
}).start();

// AFTER — Reanimated v3, UI thread
const width = useSharedValue(0);
const style = useAnimatedStyle(() => ({ width: width.value }));
width.value = withTiming(target, { duration: 300 });
```

See [mm-layout-animations.md](mm-layout-animations.md) for the full list of instances and the per-file migration.

## When to use

- Animation drops frames or feels janky
- UI freezes during an animation while JS is doing work
- Gesture-driven animation (drag, swipe, pan)
- You see `useNativeDriver: false` animating `width`/`height`/`flex`

## Key concepts (v3)

| Thread | Best for |
|---|---|
| **UI thread** (worklets) | Visual animations, transforms, layout, gestures |
| **JS thread** | State updates, data processing, API calls |

| API (v3) | Use |
|---|---|
| `useSharedValue` | The animated value (lives on UI thread) |
| `useAnimatedStyle` | Maps shared values → style (runs on UI thread) |
| `withTiming` / `withSpring` / `withDecay` | Animation drivers |
| `useAnimatedScrollHandler` | Scroll-driven animation on the UI thread |
| `useAnimatedReaction` | React to a shared value changing |
| `runOnJS(fn)(args)` | Call a JS function **from** a worklet (e.g. set React state at the end) |
| `runOnUI(fn)()` | Run a worklet **from** JS |

## Patterns

### Run a JS callback when an animation finishes

```jsx
import { runOnJS, useSharedValue, useAnimatedStyle, withTiming } from 'react-native-reanimated';

const scale = useSharedValue(1);
const onDone = () => trackEvent('animation_complete');

const press = () => {
  scale.value = withTiming(1.2, { duration: 200 }, (finished) => {
    'worklet';
    if (finished) runOnJS(onDone)();
  });
};
const style = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));
```

### Scroll-driven UI without JS-thread work

```jsx
const scrollY = useSharedValue(0);
const onScroll = useAnimatedScrollHandler((e) => {
  scrollY.value = e.contentOffset.y;
});
const headerStyle = useAnimatedStyle(() => ({
  opacity: interpolate(scrollY.value, [0, 100], [1, 0], Extrapolation.CLAMP),
}));
// <Animated.ScrollView onScroll={onScroll} scrollEventThrottle={16} />
```

## Common pitfalls

- **Heavy work inside `useAnimatedStyle`** — it runs every frame on the UI thread; keep it to value reads/interpolation.
- **Forgetting the `'worklet'` directive** on inline callbacks passed into reanimated (the babel plugin handles component-level worklets, but explicit callbacks may need it).
- **Reading React state inside a worklet** — use `useSharedValue`, not `useState`.
- **Reaching for v4 APIs** (`scheduleOnRN`/`scheduleOnUI`/`react-native-worklets`) — not installed here; use `runOnJS`/`runOnUI`.
- **Animating a plain `View`** — must be `Animated.View`/`Animated.Text`.

## Verify

- Open Perf Monitor; the **UI thread** FPS should hold ~60 during the animation even while you trigger JS work.
- React Native DevTools should show **no** component re-renders driven by the animation (shared values don't re-render React).

## Related

- [mm-layout-animations.md](mm-layout-animations.md) — the MetaMask instances + migration list
- [js-measure-fps.md](js-measure-fps.md) — confirm the frame-rate win
- [js-concurrent-react.md](js-concurrent-react.md) — React-level deferral for state-driven work
