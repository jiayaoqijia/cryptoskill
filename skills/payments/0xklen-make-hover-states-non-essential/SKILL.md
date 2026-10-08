---
name: make-hover-states-non-essential
description: Use when interactions reveal content or actions on hover. Duplicates every hover affordance for touch and keyboard so a tap or a focus reaches the same state.
---

# Make hover states non-essential

Hover-only menus, tooltips and row actions are unreachable on a touchscreen and invisible to keyboard users. Every hover affordance needs a pointer-independent twin.

## Procedure

1. Inventory hover-only behaviour: dropdowns that open on `:hover`, tooltips, row actions that appear on row hover, cards that expand on hover. Each is a bug on touch.
2. The portable rule: **if it is only reachable by hover, it is not reachable on 60% of sessions.** Add a click/tap and a focus path for each.
3. Tooltips that hold essential text must appear on focus, not only hover, and be dismissible:
       .tip:focus-visible + .tip-text, .tip:hover + .tip-text { opacity: 1; }
   Better, `aria-describedby` to the text so screen readers get it without hover.
4. Row actions hidden until hover: reveal them on `:focus-within` on the row, and keep them always visible on coarse pointers:
       @media (hover: none) { .row-actions { opacity: 1; } }
5. Detect capability, not device — `@media (hover: hover)` and `@media (pointer: fine)` gate hover enhancement; `(hover: none)` is the touch case. Do not sniff for iPhone.
6. Sticky-hover on touch: a `:hover` style that never clears after a tap leaves a button stuck in the hover state. Guard hover styles inside `@media (hover: hover)`.
7. Ensure hover and focus states are visually equivalent so a keyboard user gets the same cue a mouse user does; do not give hover a background and focus only a 1 px outline.
8. Hover must never be the only signal that something is interactive — a control that looks like static text until hovered fails discovery.

## Pitfalls

- A mega-menu opened by `:hover` with a 200 ms close delay that on touch opens and cannot be closed.
- A card's "Edit" button revealed on hover; on touch it never appears, so the feature is effectively missing.
- An `aria-label`-only tooltip that sighted touch users cannot read and screen-reader users get, or the reverse.
- A hover style defined outside any `(hover: hover)` guard, so a tap on a link leaves it underlined and coloured until the user taps elsewhere.

## Verification

    # Every hover rule should be inside a hover-capable media query or paired with a focus rule:
    grep -rn ':hover' src/ | grep -v 'hover: hover' | grep -v ':focus'
    # Report what remains as unguarded hover-only behaviour.
    # Then in devtools, toggle device emulation to a touch device and try to open each menu.

Each hover affordance must have a tap and a focus path; hover styles outside `@media (hover: hover)` are flagged. Report the affordances, their pointer-independent twins, and any that remain hover-only.
