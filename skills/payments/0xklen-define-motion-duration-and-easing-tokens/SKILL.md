---
name: define-motion-duration-and-easing-tokens
description: Use when animations feel inconsistent or sluggish. Sets named duration and easing tokens by distance, keeps UI motion under 300 ms, and picks easing for entering vs exiting.
---

# Define motion duration and easing tokens

Ad-hoc motion ("0.3s ease on this, 0.15s linear on that") makes an interface feel assembled from parts. Named tokens make every transition predictable and reviewable.

## Procedure

1. Define duration tokens scaled to distance and importance, not chosen per component:
       --dur-1: 100ms;  /* micro: colour, opacity, icon */
       --dur-2: 180ms;  /* small: buttons, toggles, tooltips */
       --dur-3: 240ms;  /* medium: drawers, dropdowns, cards */
       --dur-4: 320ms;  /* large: full-screen sheets, page transitions */
2. Keep functional UI motion under **300 ms**; beyond that it stops reading as responsiveness and starts to feel laggy. Reserve 400 ms+ for deliberate, large, rare transitions.
3. Pick easing by role:
       --ease-out:    cubic-bezier(0.2, 0, 0, 1);    /* enter — start fast, settle */
       --ease-in:     cubic-bezier(0.4, 0, 1, 1);    /* exit — accelerate away */
       --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);  /* move between two on-screen states */
   Enter uses `ease-out` so the element lands softly; exit uses `ease-in` so it leaves quickly.
4. Never use `linear` for anything but a continuous determinate progress bar or a looping rotation; it reads as mechanical for state changes.
5. Avoid `ease`/the default keyword: it starts slow and ends slow, which feels sluggish on a 180 ms dropdown.
6. Make exit slightly faster than enter — a modal that takes 240 ms up and 200 ms down feels crisper than a symmetric one.
7. Invert the motion, not the timing, for a reversal: dragging a drawer open and flicking it closed should animate out from the current position, not restart the open animation backwards.
8. Route every `transition` through the tokens: `transition: transform var(--dur-2) var(--ease-out), opacity var(--dur-2) var(--ease-out);`.

## Pitfalls

- A 500 ms dropdown because it "feels smooth" in isolation; user testing reads it as lag.
- Transitioning `all` instead of named properties, which animates layout-affecting properties and causes jank.
- Easing tokens applied but durations still literal (`transition: opacity 0.3s`), so the scale is half-adopted.
- A spring/overshoot easing on a drag handle that overshoots past its bounds and back, feeling broken rather than playful.

## Verification

    # Every transition should reference a duration token:
    grep -rhoE 'transition:[^;]+' src/ | grep -vE 'var\(--dur' | sort -u
    # And confirm no literal duration sneaks in:
    grep -rnE '(transition|animation)[^;]*[0-9]+(\.[0-9]+)?(s|ms)' src/ | grep -v var

Both should be empty (or show only justified exceptions like an infinite spinner). Report the duration ladder, the easing triple, and any transition still using a literal time.
