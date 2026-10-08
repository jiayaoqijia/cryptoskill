---
name: pair-dark-mode-tokens-by-role
description: Use when adding a dark theme. Maps semantic tokens to two palettes by role and re-derives surfaces and shadows instead of inverting colours.
---

# Pair dark mode tokens by role

Inverting a light palette produces muddy mid-greys and glowing whites because dark mode is a different material, not a negative. The durable approach is semantic tokens with two values per role.

## Procedure

1. Name tokens by role, never by hue: `--surface`, `--surface-raised`, `--text-primary`, `--text-muted`, `--border`, `--accent`. `--grey-200` cannot carry a different meaning in two themes.
2. Define both palettes on the same token names, scoped to a theme attribute:
       :root[data-theme="light"] { --surface:#ffffff; --surface-raised:#f7f7f8; --text-primary:#111318; }
       :root[data-theme="dark"]  { --surface:#0e1117; --surface-raised:#1a1f27; --text-primary:#e8eaed; }
3. In dark mode make raised surfaces lighter, not darker. Elevation reads as "closer to the light source" in both themes; a dark card must be lighter than the page behind it.
4. Lower pure whites: use `#e8eaed`-range text on dark, not `#ffffff`. Full white on near-black vibrates and is the single most common dark-mode mistake.
5. Re-pick accent colours. A saturated blue tuned for white has too little contrast on `#0e1117`; lighten it and re-check at 4.5:1 rather than reusing the hex.
6. Replace drop shadows with a lighter border or a subtle top highlight in dark mode — shadows are invisible on dark and the element loses separation.
7. Handle images and logos: a black wordmark disappears on dark. Serve a swapped asset via `<picture>` with `prefers-color-scheme`, or place it on a light chip.
8. Set `color-scheme: dark` on the root so form controls, scrollbars and the default canvas follow the theme.

## Pitfalls

- Inverting with a CSS filter (`filter: invert(1)`), which mangles images, brand colours and photos.
- Only theming the page background and leaving modals, tooltips and menus on the light palette because they render in a portal outside the themed root.
- Reusing semantic names bound to one theme, so `--background` means white in light and someone hard-codes it as the card colour.
- Assuming the OS preference equals the app preference; store an explicit user override and apply it before first paint.

## Verification

    # Confirm both themes define the same token set (no gaps):
    for t in light dark; do
      grep -oE "\-\-[a-z-]+:" src/styles/tokens.css | sort -u > /tmp/$t.txt
    done
    diff <(grep -A20 'data-theme="light"' src/styles/tokens.css | grep -oE '\-\-[a-z-]+') \
         <(grep -A20 'data-theme="dark"'  src/styles/tokens.css | grep -oE '\-\-[a-z-]+')

An empty diff means both palettes cover the same roles. Then screenshot both themes and confirm no element is a light surface on the dark page. Report the token strategy and any role defined in one theme only.
