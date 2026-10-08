---
name: snap-spacing-to-a-4pt-grid
description: Use when margins and padding drift into arbitrary pixel values. Replaces one-off numbers with a small spacing scale on a 4-point base so rhythm holds across components.
---

# Snap spacing to a 4-point grid

Spacing that is chosen per component produces 7 px here and 9 px there; the eye reads the inconsistency even when no single value is wrong. A shared scale fixes the rhythm by removing the choice.

## Procedure

1. Define the scale as a fixed set of steps on a 4 px base, named by index rather than value:
       --space-0: 0;
       --space-1: 0.25rem;  /*  4px — icon to label      */
       --space-2: 0.5rem;   /*  8px — inside a chip       */
       --space-3: 0.75rem;  /* 12px — input padding       */
       --space-4: 1rem;     /* 16px — card padding        */
       --space-6: 1.5rem;   /* 24px — between cards       */
       --space-8: 2rem;     /* 32px — section rhythm      */
       --space-12: 3rem;    /* 48px — page section break  */
2. Reserve 4 px and 8 px for tight, intra-component gaps; 16 px and up for between-component and section gaps. Compact spacing is for elements that read as one unit.
3. Keep vertical spacing inside a component smaller than the gap to the next component. A card whose internal padding exceeds the space below it looks like it belongs to the block beneath.
4. Use `gap` on flex and grid containers instead of sibling margins. `margin-bottom` on every child collapses unpredictably and leaves a trailing gap after the last item.
5. Grow spacing super-linearly with section size, not linearly: doubling a section's visual weight usually wants 1.5×, not 2×, the whitespace.
6. When an off-grid value looks "right", change the surrounding scale or the component, not that one number. Absorbing the exception is how the grid dies.
7. Round any computed spacing to the nearest step with a small helper before it reaches CSS:
       const s = (n) => Math.round(n / 4) * 4;  // s(13) => 12
8. Document the scale in one `tokens.css` and forbid raw `margin: 13px` in review.

## Pitfalls

- A 5-point or 8-point base chosen ad hoc, so 12 px and 13 px both appear and nothing lines up.
- Vertical rhythm that ignores line-height: a 16 px gap under 24 px line boxes leaves a visibly tight seam.
- Spacing tokens named by value (`space-16`) so a rescale to a 4-point base renames everything downstream.
- Using margin collapse as a feature to save writing a gap, then being surprised it collapses differently inside a grid.

## Verification

    # Find spacing declarations that are off the 4px grid:
    grep -rnoE '(margin|padding|gap)[^;]*:\s*[0-9]+(\.[0-9]+)?px' src/ \
      | awk -F'px' '{v=$1; sub(/.*[^0-9.]/,"",v); if (v*100 % 400 != 0) print}'

No output means every raw pixel spacing value is a multiple of 4. Report the scale steps and any remaining off-grid values with their file and line.
