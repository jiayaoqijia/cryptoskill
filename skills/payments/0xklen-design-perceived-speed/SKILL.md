---
name: design-perceived-speed
description: Use when a page is fast enough on paper but feels slow to users. Applies skeletons, optimistic UI and immediate feedback instead of spinners.
---

# Design Perceived Speed

Users judge speed by responsiveness, not by a network waterfall. A 300 ms action that paints an instant acknowledgement feels faster than a 200 ms one that shows nothing.

## Procedure

1. Set the interaction budget: feedback must paint within 100 ms of a tap. Below that, a control feels attached to the finger.
2. For network-bound views, render a skeleton that matches the final layout's shape and dimensions rather than a centred spinner.
3. For writes (like, save, follow), apply the change optimistically and reconcile on response:

       setLiked(true);
       await api.like(id).catch(() => setLiked(false));

4. For renders over 50 ms, keep the previous content visible and swap on completion; never blank the page.
5. Use `transition` on `opacity`/`transform` only, and gate motion behind `@media (prefers-reduced-motion: no-preference)`.
6. Add a deliberate delay only when it is honest: a 400 ms "Saving" that resolves faster than the eye can track at least confirms the tap.
7. Show progress with position, not a looping indeterminate bar, once an operation exceeds roughly 10 s.
8. Keep the tab title and favicon responsive too; a background render that freezes the spinner communicates nothing.
9. Measure the perceived gap by hand: tap a control, count the milliseconds until the first pixels change, and treat anything over 100 ms as a bug.

## Pitfalls

- Spinners that flash for 80 ms and vanish read as a glitch; hold a skeleton for a minimum visible duration or skip it.
- Optimistic updates with no rollback, so a failed write leaves the UI lying about state.
- Skeletons with a different height than the loaded content, which reintroduces layout shift.
- Blocking the whole page on an above-the-fold fetch instead of streaming the rest.
- Animating layout properties (`top`, `width`) which stutter on mid-tier hardware and read as slow.

## Verification

    npx lighthouse https://shop.example.com --only-categories=performance --preset=desktop --quiet --output=json | jq '.audits."first-contentful-paint".numericValue'

FCP under 1800 ms plus a sub-100 ms interaction handler budget. Report the FCP number and the interaction you measured by hand.
