---
name: build-a-modular-type-scale
description: Use when setting heading and body sizes for a UI. Picks one ratio, sizes everything in rem, and clamps display type so the scale stays legible from 360 px to 1440 px.
---

# Build a modular type scale

A type scale is one ratio applied to a base size, not a pile of arbitrary pixel values. Without it every new screen invents its own heading size and the page loses rhythm.

## Procedure

1. Set the body size to `1rem` (16 px). Do not set `html { font-size: 62.5% }` to make arithmetic easy — it defeats browser and OS base-font settings that rem exists to honour.
2. Choose exactly one ratio and hold it: `1.200` (minor third) for dense product UI, `1.250` (major third) for marketing pages, `1.333` (perfect fourth) for editorial. Mixing ratios per section is what makes a layout feel noisy.
3. Generate steps outward from the base and store them as custom properties:
       :root {
         --step--1: 0.833rem;   /* 13.3px */
         --step-0:  1rem;       /* 16px   */
         --step-1:  1.2rem;     /* 19.2px */
         --step-2:  1.44rem;
         --step-3:  1.728rem;
         --step-4:  2.074rem;
       }
4. Map roles to steps, never components to raw pixels: `--text-body: var(--step-0); --text-h3: var(--step-2); --text-h1: var(--step-4);`.
5. Tie line-height inversely to size — small text needs more leading, large text less. Body `1.5`, h3 `1.25`, h1 `1.1`.
6. Clamp display growth so a hero cannot overflow a 360 px viewport:
       font-size: clamp(2rem, 1.5rem + 3vw, 3.5rem);
7. Tighten tracking as size grows: `letter-spacing: -0.02em` at display sizes, `0` at body. Never space body text negatively.
8. Audit the rendered page and cap distinct sizes at roughly six. If a screen uses nine different font sizes, the scale has silently failed — consolidate before shipping.

## Pitfalls

- Sizing in px only, so a user who raises their browser base font sees no change; rem respects that preference and px ignores it.
- A large ratio (1.5, 1.618) that yields a 5× jump from body to display, so headings consume the viewport on mobile.
- Line-height left at a single global `1.4`, which crams small captions and floats display headings too far apart.
- Only one step between body and h3, so hierarchy reads as a flat wall of two sizes.

## Verification

    # Count the distinct font-size values actually computed on a page:
    node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto(process.argv[1]);const s=await p.$$eval('*',els=>[...new Set(els.map(e=>getComputedStyle(e).fontSize))]);console.log(s.length+' sizes:',s.sort());await b.close();})()" http://localhost:3000

Distinct sizes should be 6 or fewer, every value derived from a step token, and the smallest ≥ 12 px. Report the ratio chosen, the step list, and the rendered size count.
