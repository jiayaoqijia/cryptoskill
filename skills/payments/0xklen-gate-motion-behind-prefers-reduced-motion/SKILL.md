---
name: gate-motion-behind-prefers-reduced-motion
description: Use when a UI animates and some users have vestibular disorders. Wraps decorative motion in a prefers-reduced-motion media query while keeping essential state changes visible.
---

# Gate motion behind prefers-reduced-motion

Parallax, large slides and looping spinners can trigger nausea and migraine for people with vestibular sensitivity. The OS exposes that preference; honouring it is a media query, not a redesign.

## Procedure

1. Default to motion and remove it when the user asks — or default to none and add it up. Either works; state which in a comment so the team stops flip-flopping.
2. Wrap every decorative transition and keyframe animation:
       @media (prefers-reduced-motion: reduce) {
         *, *::before, *::after {
           animation-duration: 0.01ms !important;
           animation-iteration-count: 1 !important;
           transition-duration: 0.01ms !important;
           scroll-behavior: auto !important;
         }
       }
   This collapses motion to near-zero rather than removing it, so `animationend` and transition listeners still fire and no logic hangs waiting for an event that never comes.
3. Keep essential feedback. A loading state must still read as loading — swap a spinning loader for a static "Loading…" label or a progress bar that updates without transforming.
4. In JS, read the preference once and re-read on change:
       const q = matchMedia('(prefers-reduced-motion: reduce)');
       let reduce = q.matches;
       q.addEventListener('change', e => reduce = e.matches);
5. For programmatic scrolls use `behavior: reduce ? 'auto' : 'smooth'`; smooth scrolling is a common trigger and easy to gate.
6. Gate autoplaying video and looping background animation too — CSS is not the only source. Pause `<video autoplay muted loop>` behind the same check.
7. Do not set `animation: none`, which can skip a fill-forwards animation that was positioning an element and leave it in the wrong place.
8. Test by toggling the OS setting, not by editing code — that catches motion you added outside the media query.

## Pitfalls

- Wrapping only `transition` and missing `@keyframes` animations, so an attention-grabbing loop survives the setting.
- Killing motion entirely with `animation: none`, which strands elements mid-keyframe and breaks event-driven flow.
- Forgetting JS-driven animation (GSAP, framer-motion, `requestAnimationFrame`): they ignore the CSS query and must be gated at the library or code level.
- Removing the loading affordance entirely, so reduced-motion users cannot tell the app is busy.

## Verification

    # Confirm the media block exists and covers transitions and animations:
    grep -n "prefers-reduced-motion" -A6 src/styles/*.css
    # Confirm JS respects it:
    grep -rn "prefers-reduced-motion\|matchMedia" src/ | grep -v node_modules

Then launch with the OS reduce-motion setting on and record a short capture: no element should translate, scale, or scroll smoothly. Report the gated selectors and the JS gate location.
