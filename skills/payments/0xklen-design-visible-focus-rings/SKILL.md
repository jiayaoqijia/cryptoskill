---
name: design-visible-focus-rings
description: Use when keyboard users lose track of where they are. Replaces outline:none with a visible :focus-visible ring that meets 3:1 and clears the element's own border.
---

# Design visible focus rings

Removing the default outline to "clean up" the design makes a keyboard-navigable app unusable. The fix is not to delete focus styling but to replace it with one that matches the brand and is always visible.

## Procedure

1. Never write `outline: none` without a replacement. If a design review demands it, pair it with a custom ring in the same rule, or delete the line.
2. Style `:focus-visible` (not `:focus`) so mouse clicks do not flash a ring on every button, while tabbing always shows one:
       :focus-visible {
         outline: 2px solid var(--focus-ring);
         outline-offset: 2px;
         border-radius: 2px;
       }
3. Give the ring a 3:1 contrast ratio against the adjacent background and, if it sits on a coloured button, add a second contrasting ring with a box-shadow halo:
       .btn:focus-visible {
         outline: 2px solid #0b5fff;
         box-shadow: 0 0 0 4px #fff;   /* visible on dark and light buttons */
       }
4. Set `outline-offset` so the ring clears the element's border and is not clipped by `overflow: hidden` parents. If a container clips it, move the ring to the container or add padding.
5. Never suppress the ring for keyboard input. If a specific control looks wrong, fix that control's contrast, not the ring's presence.
6. Provide a `:focus-within` treatment for composite widgets (a fieldset, a card of radio buttons) so the group shows focus while a child is active.
7. Keep tab order matching visual order; a ring that jumps around the page is worse than none. Check with the Tab key, not a mouse.
8. Use a token like `--focus-ring` so the colour is themeable and the same across components.

## Pitfalls

- `:focus-visible` styled only on some components, so links show a ring and buttons do not — inconsistent but not obviously broken, which is why it ships.
- A ring colour that is the brand blue on a brand-blue button, producing a ring that is effectively invisible.
- `outline-offset: -2px` used to avoid clipping, which draws the ring inside the element and hides it under a filled background.
- Relying on a `box-shadow` only: shadows are removed in forced-colors/high-contrast mode, so include a real `outline` alongside.

## Verification

    # Any outline:none must be on the same line as a replacement ring
    grep -rn "outline:\s*none\|outline:\s*0" src/ | grep -v "focus-visible"
    # then in the browser, tab through the page and confirm every stop shows a ring

Tab from the address bar through all interactive elements; each must show a visible ring that contrasts ≥ 3:1. Report any component that showed no ring, with its selector.
