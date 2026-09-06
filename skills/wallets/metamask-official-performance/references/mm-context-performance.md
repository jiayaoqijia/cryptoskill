---
title: Context Provider Performance (MetaMask)
impact: HIGH
tags: context, provider, re-renders, usememo, useContext
---

# Skill: Context Provider Performance

A React Context re-renders **every consumer** whenever the Provider's `value` changes by reference. Passing an inline object literal as `value` creates a new reference on every render of the Provider's parent — so all consumers re-render even when nothing they read changed.

## Quick Pattern

```jsx
// ❌ new object every parent render → every consumer re-renders
<MyContext.Provider value={{ theme, setTheme }}>
  {children}
</MyContext.Provider>

// ✅ memoize the value
const value = useMemo(() => ({ theme, setTheme }), [theme, setTheme]);
<MyContext.Provider value={value}>{children}</MyContext.Provider>
```

## Verified MetaMask instances

| File | Value |
|---|---|
| `HomepageDiscoveryTabs.tsx:342` | `<TabIconAnimationContext.Provider value={{ iconCollapseProgress }}>` |
| `Toast.context.tsx:25` | `<ToastContext.Provider value={{ toastRef }}>` |

`HomepageDiscoveryTabs` lives on the main wallet screen — a high-traffic render path — so every render of that screen re-renders all `TabIconAnimationContext` consumers for no reason.

## Fixes

**1. Memoize the value (smallest change):**
```jsx
const value = useMemo(() => ({ iconCollapseProgress }), [iconCollapseProgress]);
return <TabIconAnimationContext.Provider value={value}>{children}</TabIconAnimationContext.Provider>;
```

**2. If the value is a ref (like `toastRef`), it's already stable — still wrap so the object identity is stable:**
```jsx
const value = useMemo(() => ({ toastRef }), []); // toastRef identity is stable
```

**3. Animation progress should not be plumbed through Context as React state at all.** If `iconCollapseProgress` is animated, make it a Reanimated `useSharedValue` and read it via `useAnimatedStyle` in consumers — the value updates on the UI thread with **zero** React re-renders. See [mm-layout-animations.md](mm-layout-animations.md).

**4. Split contexts** when a value bundles independent pieces — consumers that only need one piece shouldn't re-render when another changes.

## How to find

```bash
# inline object/array values on a Provider
grep -rn "Provider value={{" app --include="*.tsx" | grep -v ".test."
grep -rn "Provider value={\[" app --include="*.tsx" | grep -v ".test."
```
Then check whether the Provider's parent renders frequently and how many consumers the context has. A rarely-rendering Provider with two consumers is low priority; a main-screen Provider with many consumers is high.

## Verify

React Native DevTools Profiler → record the parent render → confirm context consumers show "Memo" / do not appear in the commit after memoizing the value.

## Don't over-correct

- A Provider that renders once and never updates doesn't need a memoized value.
- Don't memoize a value whose dependencies change every render anyway — fix the dependency churn instead.

## Related

- [mm-layout-animations.md](mm-layout-animations.md) — move animated context values to shared values
- [js-profile-react.md](js-profile-react.md) — confirm consumers stop re-rendering
