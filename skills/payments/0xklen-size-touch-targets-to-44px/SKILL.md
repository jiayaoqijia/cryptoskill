---
name: size-touch-targets-to-44px
description: Use when buttons, links or icon controls are small or closely packed. Enforces a 44×44 CSS-px hit area with 8 px spacing, decoupled from the visual size of the control.
---

# Size touch targets to 44 px

A 16 px icon with a 16 px tap area fails anyone with a tremor, a gloved hand, or a phone in one hand. The hit area and the drawn control are separate concerns — make the area finger-sized and the drawing can stay small.

## Procedure

1. Set a floor of **44×44 CSS px** for any tappable control (WCAG 2.5.5 AAA; 24 px is the AA floor and still cramped). That is 2.75 rem at the 16 px base.
2. Decouple hit area from visual size with padding or a pseudo-element:
       .icon-btn { position: relative; width: 24px; height: 24px; }
       .icon-btn::after {
         content: ""; position: absolute; inset: -10px;   /* 24 + 20 = 44 */
       }
   The pseudo-element extends the clickable region without changing the layout box.
3. Space adjacent targets by at least 8 px so a near-miss does not hit the neighbour. In a row of icon buttons use `gap: 0.5rem`.
4. Keep the target a square or wider; a 44 px tall, 24 px wide link is a vertical sliver that is fine to click but awkward to acquire.
5. For inline text links, accept the line box as the target but avoid tiny link text with no padding between two adjacent links; separate them with a comma or a space.
6. Meet the same floor on desktop — do not shrink to 24 px at `md` just because a mouse is assumed; touch laptops and pointer-replacement users exist.
7. Check the control's own bounding box, not the button's padding box. A `0 padding` anchor wrapping a 12 px glyph is 12 px tall, whatever its parent styles say.
8. Audit again after any zoom: at 200% a 44 px target stays 44 CSS px but its neighbours may be pushed together.

## Pitfalls

- A visible 44 px button with a 44 px parent but `pointer-events: none` on an overlay that swallows taps in the margin.
- Icon buttons in a dense toolbar at 32 px apart, so every tap is a coin flip between two actions.
- Padding used to enlarge the box, which shifts neighbouring elements because padding participates in layout — the pseudo-element approach does not.
- Assuming desktop-only means small targets are fine; trackpads and touch screens make this a real defect on laptops.

## Verification

    # List interactive elements whose rendered box is under 44px:
    node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.setViewportSize({width:390,height:844});await p.goto(process.argv[1]);const small=await p.\$\$eval('a,button,[role=button],input',els=>els.map(e=>{const r=e.getBoundingClientRect();return{rw:Math.round(r.width),rh:Math.round(r.height),t:(e.textContent||e.getAttribute('aria-label')||'').trim().slice(0,24)}}).filter(o=>o.rw<44||o.rh<44));console.log(small);await b.close();})()" http://localhost:3000

The array should be empty (inline text links may be exempted with a comment). Report each undersized target, its size, and the pseudo-element or padding added to reach 44×44.
