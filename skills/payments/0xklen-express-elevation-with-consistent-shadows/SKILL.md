---
name: express-elevation-with-consistent-shadows
description: Use when cards, popovers and modals each have a different shadow. Defines a small elevation ladder with two-layer shadows and pairs each level with a z-index.
---

# Express elevation with a consistent shadow

A modal with a 4 px blur and a tooltip with a 30 px blur read as unrelated. Elevation is an ordinal ladder — layered the same way each step — and it should map to both shadow and stacking order.

## Procedure

1. Define a fixed ladder, usually four to five levels: `flat` (0), `raised` (cards on hover), `overlay` (dropdown, popover), `modal`, `toast` (always top). No in-between levels.
2. Build each shadow from two layers — a tight contact shadow and a wide ambient one — so the element reads as above the surface rather than as a blurry blob:
       --elev-1: 0 1px 2px rgb(0 0 0 / .06), 0 1px 3px rgb(0 0 0 / .10);
       --elev-2: 0 2px 4px rgb(0 0 0 / .06), 0 4px 8px rgb(0 0 0 / .10);
       --elev-3: 0 4px 8px rgb(0 0 0 / .08), 0 12px 24px rgb(0 0 0 / .12);
       --elev-4: 0 8px 16px rgb(0 0 0 / .10), 0 24px 48px rgb(0 0 0 / .16);
3. Increase y-offset and blur with the level; a higher element casts its shadow further down. Varying only opacity looks wrong.
4. Pair elevation with z-index tokens and keep them in the same file so they cannot drift apart:
       --z-dropdown: 1000; --z-modal: 1300; --z-toast: 1400;
5. Avoid shadows on the base surface. Content sitting directly on the page (`elev-0`) is defined by a border or a background change, not a shadow, or the whole page looks lifted.
6. In dark mode drop `elev-0`/`elev-1` shadows (invisible) and use a 1 px lighter border instead; keep the ladder from `overlay` up.
7. Combine elevation with a focus ring and a border radius token so an elevated element looks like one family — roundness and lift should move together.
8. Do not stack shadows to fake a level; a card with four stacked shadows is a level that does not exist.

## Pitfalls

- Very dark, tight shadows (`0 2px 2px rgba(0,0,0,.6)`) that look like a hard edge, not depth.
- The same `box-shadow` reused on a button and a modal, so a click target looks like it floats above the page.
- z-index armed by a sibling's shadow level, so a raised card clips a dropdown that should be above it.
- Missing the dark-mode branch, leaving a card with no separation on a dark surface.

## Verification

    # List every distinct box-shadow and check it maps to a ladder level:
    grep -rhoE 'box-shadow:[^;]+' src/ | sort | uniq -c
    # Confirm z-index values come from tokens, not literals:
    grep -rnE 'z-index:\s*[0-9]+' src/ | grep -v var

The distinct shadow set should equal the ladder (≤ 5 values) and each appear as a token. Report the ladder, the z-index mapping, and any literal shadow or z-index that bypasses a token.
