# Isometric pixel-art scene in inline SVG

Recipe for the office map: rooms drawn entirely in code, no image assets and no libraries, so the page
renders identically offline and a room can be re-styled per agent with a one-line change.

## Projection

Pick the floor diamond, then derive everything from it. In a `0 0 220 176` viewBox with corners
`left(22,100) top(110,56) right(198,100) bottom(110,144)`:

```js
function P(u,v,h){ h = h || 0; return [22 + 88*(u+v), 100 - 44*u + 44*v - h]; }  // u,v in 0..1
```

`u` runs to the upper-right, `v` to the lower-right, `h` lifts straight up in px. Props get placed as
fractions (`u,v,du,dv,h`), so a room rescales with the viewBox and nothing is hard-coded in pixels.

## Builders

Each returns an SVG string; concatenate them in depth order.

- `box(u,v,du,dv,h,c)` — isometric box: top face `shade(c,1.25)`, left face `shade(c,0.6)`, right face
  `shade(c,0.92)`. Emit a contact-shadow quad FIRST (the footprint at `h=2`, `#10141f`, opacity `.68`).
  Without it every prop reads as floating no matter how correct the geometry is — this is the single
  highest-value line in the whole scene.
- `wpanelL(u0,u1,v,h,c)` / `wpanelR(u,v0,v1,h,c)` — wall-mounted boards, signs and screens as a FLAT quad
  coplanar with the wall (constant-`v` wall and constant-`u` wall). A wall sign built from `box()` looks
  like a panel stuck in mid-air, because a box has volume and its base sits on the floor. Give panels a
  1px dark stroke so they read as mounted rather than painted on.
- `flat(u,v,du,dv,c,op)` — floor quads: rug, ink lines, grid.
- `guy(u,v,skin,shirt,pants,acc)` — worker: shadow ellipse, two legs, body, head, hair, optional hat.

Room shell: two back walls as quads rising `H` px from the back edges (`left→top` and `top→right`), then
the floor diamond, then faint 1px floor grid lines, then the props.

## Painter's order

SVG paints in document order, so depth is manual:

1. shells + floor, 2. rug, 3. wall panels, 4. props sorted by increasing `u2+v2`, 5. the worker last (so
his figure is never clipped).

The trick that makes desks look occupied: put anything that belongs ON a desk at a `v` slightly BEHIND the
desk's back edge, with `h = deskHeight + itemHeight`, and emit it BEFORE the desk. The desk then hides the
item's base and the top sticks out — monitor, mixer, laptop all read as sitting on the desk without adding
an elevation parameter to `box()`.

## Scene design

One room per agent, and let the props SAY the job:

- trading desk: three glowing monitors, a wall chart panel with green/red candles, a safe with a gold
  stack, a filing shelf.
- news desk: mixer with coloured pads, mic on a stand, mug, a tall wall screen, a red lit ON AIR panel.
- admin desk: laptop, letter tray, tall filing cabinet with drawer lines, wall calendar with a couple of
  filled dates, plant.
- inbox desk: sorting rack with coloured parcels stacked on top, conveyor, parcels on the floor, desk with
a paper pile.

Tie the room to its agent with a rug in `shade(agentAccent, .26)` at ~.45 opacity, and reuse the agent's
accent on the figure's shirt (lightened, see SKILL.md pitfalls).

## Poster export

```js
bb  = document.querySelector('.mapwrap').getBoundingClientRect();
res = cdp('Page.captureScreenshot', format='png',
          clip={x:bb.x, y:bb.y, width:bb.width, height:bb.height, scale:2});
open(path,'wb').write(base64.b64decode(res['data']));
```

Hide tabs/header/sidebar/mobbar and set the roof text a notch larger before capturing. In a CSS-grid
layout also set `gridTemplateColumns='1fr'` — the grid keeps the sidebar's empty track, and the capture
silently comes out as a narrow vertical strip (e.g. 296x1800 instead of 2400x1520) with no error.

## QA loop

Screenshot at phone (390x844) and desktop (1280x900) widths, then `vision_analyze` the 2x poster: a 390px
phone shot is too small for the inspector to judge props, and the code tells you nothing about how it
reads. Expect over-reporting — it will call correct geometry "floating" and "not flush with the wall".
Act on the mechanical subset (missing contact shadow, figure too small, prop colour matching the carpet, a
status label contradicting the roster), iterate once or twice, then send the poster PNG as part of the
delivery — a shareable image is usually what the user wanted out of a screenshot-driven request.
