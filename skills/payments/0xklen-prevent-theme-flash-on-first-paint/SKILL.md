---
name: prevent-theme-flash-on-first-paint
description: Use when a saved light/dark preference flashes the wrong theme on load. Resolves the theme in a blocking inline script before first paint and avoids hydration mismatches.
---

# Prevent the theme flash on first paint

If the theme is applied after the JavaScript bundle loads, a dark-preferring user sees a white page for 100–400 ms. The fix is a tiny blocking script the browser runs before it paints.

## Procedure

1. Store the preference as one of three values: `light`, `dark`, or `system` (no explicit choice). Persisting only a boolean loses the "follow the OS" state.
2. Add an inline script in `<head>`, before any stylesheet that paints, that reads the stored value and sets the attribute synchronously:
       <script>
         (function () {
           try {
             var t = localStorage.getItem('theme') || 'system';
             var dark = t === 'dark' || (t === 'system' && matchMedia('(prefers-color-scheme: dark)').matches);
             document.documentElement.dataset.theme = dark ? 'dark' : 'light';
           } catch (e) {}
         })();
       </script>
   No `defer`, no `async`, no external file — a network fetch would reintroduce the flash.
3. Also set `color-scheme` on the root so the browser paints scrollbars and the canvas in the right scheme before CSS loads:
       <meta name="color-scheme" content="light dark">
4. Keep the CSS keyed off `html[data-theme="dark"]`, so the attribute the script sets is the same selector the styles use. No class/attribute mismatch.
5. In a server-rendered app (Next.js, Remix), render the attribute from a cookie the server can read, so the HTML arrives already correct and the inline script only handles client-side changes. This eliminates the flash entirely for SSR.
6. Avoid hydration mismatches: mark any theme toggle icon as client-only or suppress hydration warnings on the element whose value comes from `localStorage`, since the server does not know the preference.
7. Read the preference before paint on `matchMedia('(prefers-color-scheme: dark)')` change events too, so an OS switch while the tab is open updates the theme live.
8. Do not fetch the theme from an API on load — that is always after first paint.

## Pitfalls

- The theme applied in a `useEffect` or on `DOMContentLoaded` from an external bundle, which runs after a visible paint.
- Reading `localStorage` in a `try` block but not guarding against it being disabled (private mode), throwing and leaving the default light theme regardless of OS.
- Setting a `dark` class in JS while the CSS selectors expect a `data-theme` attribute, so the attribute is set and nothing changes.
- A cookie read on the client only, so a cold server render still flashes for a user who set dark on another device.

## Verification

    # Simulate a dark preference with no stored choice and capture the first frame:
    npx playwright screenshot --color-scheme=dark --wait-for-timeout=50 \
      http://localhost:3000 /tmp/first-frame.png
    # The frame must already be dark; then confirm the inline script is in <head>:
    grep -n 'dataset.theme' index.html | head -1

The 50 ms screenshot must match the resolved theme (no white flash), and the script must appear before the first stylesheet link. Report the storage key, the resolution order, and whether SSR is used.
