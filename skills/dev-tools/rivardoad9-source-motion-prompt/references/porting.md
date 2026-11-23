# Porting a Motion Prompt element

`get <id>` returns one text file per element:

```js
// Motion Prompt #012 · MIT License (c) 2026 Shohei Ohtaki · https://showheyohtaki.github.io/motion-prompt/#012
// name, what it shows, spec lines, when to use it, size, cycle, "Needs: kit <pack>", live demo URL
// @element 12
CELLS[11] = (k, w, h, u) => { … };     // k = CanvasRenderingContext2D, w/h = card size, u = seconds in [0, cycle)
```

`kit <pack>` returns the code the element depends on: the card size, the cycle length, the palette object `C`, font stacks and helper functions (easing, text, shapes). The kit's own header shows how to run one element by itself. Read it; it is the reference for how the pack expects to be called.

Before porting, read the element's **spec** lines. They state the order of the motion and every number that matters. The code is the source of truth; the spec is the same information in words.

Decide first which of two kinds of port this is:

- **Run the code** (sections 1 and 2): the project can draw on a Canvas 2D context. The element's function runs unchanged and you only supply `u`, a size and a place.
- **Move the numbers** (sections 3 and 4): the project animates some other way. You rebuild the move there and carry over the timings, easing and amounts.

## Time: loop or play once

Every element is written as a loop of `cycle` seconds. Most contain an entrance, a hold and an exit or reset so that the loop closes.

- **Looping use** (backgrounds, indicators, a gallery): `u = t % cycle`, where `t` is the time since the scene started.
- **Play once and stay** (a title or caption that enters and remains): `u = Math.min(t, uHold)`, where `uHold` is a time inside the hold, after the entrance has finished. Find it from the spec lines or from the phase boundaries in the code. Do not let `u` run on into the exit.
- **Play once with an exit**: drive `u` through the entrance, keep it at `uHold` for as long as the scene needs, then continue from the start of the exit when the scene ends. This keeps the entrance and exit at their designed speed whatever the scene's length.
- **Fitting a fixed slot** (a swap into an existing scene): lengthen or shorten the hold, not the motion. Only if the slot is shorter than the entrance plus the exit, scale time evenly (`u = t * k`) and say so in your report.
- Never pass `u` outside `[0, cycle)`. Start a scene at whatever `u` gives a clean first frame; that is usually `0`, but check the element.

## 1. A plain Canvas engine (a function of time that draws a frame)

Set the code up once per pack, in one scope:

1. the kit (keep its first line),
2. the element blocks you fetched (keep each first line),
3. references to the cells you use, for example `const morph = CELLS[11];`.

If the project is a module, put these in one file and export the cells. Do not copy helpers into each element; they share the kit.

**Two packs never share a scope.** Every kit declares the same top-level names (`CW`, `CH`, `CYC`, `C`, `CELLS` and its own helpers), so pasting two kits into one script or module is a syntax error. Give each pack its own module or its own function scope, and export what you need under names that say which pack they come from:

```js
// motion-prompt-motion.js      (kit "motion" + elements #012 …)
export const morph = CELLS[11];  export const MOTION = { w: CW, h: CH, cycle: CYC };
// motion-prompt-camera.js      (kit "camera" + elements #045 …)
export const wipe = CELLS[20];   export const CAMERA = { w: CW, h: CH, cycle: 9.4 };  // use the Cycle value in the element header; in this kit CYC is half of it
```

Packs can differ in card size and cycle, so always pass each cell the size and cycle of its own pack.

**Placing a card in a 1920×1080 frame.** Elements draw in card coordinates (`w` × `h` from the header). Scale the context, not the numbers:

```js
function drawElement(ctx, cell, u, x, y, scale, W, H) {   // W, H = the card size from the header
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);
  ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.clip();        // elements may draw past their card
  cell(ctx, W, H, u);
  ctx.restore();
}
// full width of a 1920 frame, centered vertically:
const s = 1920 / W;  drawElement(ctx, typewriter, u, 0, (1080 - H * s) / 2, s, W, H);
```

- Always pass the card's own `w, h`. Passing `1920, 1080` changes the layout, because sizes inside an element are written for the card.
- The card's aspect ratio is not 16:9. Either place the card as a band or panel inside your layout, or scale it to cover the frame and accept the crop. Check that the important part stays in view.
- Many elements paint their own card background, often through a kit helper called on the element's first line. To place one over footage or another layer, find that call or fill, and remove or replace it. Report that change.
- Text sharpness: scaling the context keeps text and shapes as vectors, so no extra step is needed. Draw on a canvas whose pixel size is the final frame size.

**Several elements in one frame.** Call them in back-to-front order, each inside its own `save()`/`restore()` as above, each with its own `u` computed from its own start time: `u = sceneClock(t - start)`. Reset `globalAlpha`, `filter` and `globalCompositeOperation` between cells if your engine does not already do so.

**Elements that use an offscreen canvas.** Some elements create a canvas with `document.createElement('canvas')` for masks, blur or compositing.

- In a browser this works as written.
- In Node (node-canvas, skia-canvas, @napi-rs/canvas) there is no `document`. Provide the one call they need before the kit runs, for example `globalThis.document = { createElement: () => createCanvas(1, 1) }`, using your library's `createCanvas`.
- An offscreen canvas is sized in card pixels. When the card is scaled up a lot, its content is upscaled and softens. If that shows, render the element at a larger card scale by scaling inside the offscreen canvas as well, and compare a frame against the demo.
- `ctx.filter` is not available in every canvas library. If an element uses it, test a frame early.

**Fonts.** Kits use system font stacks. A renderer without those fonts falls back silently and the layout shifts. Either register the project's font and change the font constants in the kit, or confirm that the stack resolves on the rendering machine. If a pack declares font files, load them before drawing the first frame.

## 2. Remotion

Draw on a `<canvas>` from the current frame. The element stays a pure function, so every frame renders the same way in preview and in export.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { useEffect, useRef } from 'react';
import { typewriter, CARD_W, CARD_H, CYCLE } from './motion-prompt-motion';   // one module per pack: kit + its elements, license lines kept

export const Typewriter: React.FC<{ hold?: number }> = ({ hold }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ref = useRef<HTMLCanvasElement>(null);
  const t = frame / fps;
  const u = hold === undefined ? t % CYCLE : Math.min(t, hold);   // loop, or play once and stay
  useEffect(() => {
    const ctx = ref.current!.getContext('2d')!;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, CARD_W, CARD_H);
    ctx.save();
    typewriter(ctx, CARD_W, CARD_H, u);
    ctx.restore();
  }, [u]);
  return <canvas ref={ref} width={CARD_W} height={CARD_H} style={{ width: '100%' }} />;
};
```

- `useCurrentFrame()` inside a `<Sequence>` starts at 0, so `t` is already the scene's own time.
- For a sharp result, give the canvas the pixel size it has on screen: set `width`/`height` to the card size times your scale and call `ctx.scale(scale, scale)` before the cell.
- Do not use `requestAnimationFrame`, `Date.now()` or `performance.now()`. Time comes from the frame only.
- If the pack loads font files, wait for them with `delayRender()` / `continueRender()`.

## 3. Moving the numbers to CSS, SVG, Lottie or After Effects

Here you do not run the code. You rebuild the move with the target's own tools and copy its values.

1. From the code and spec, write a small table per animated property: start time, end time, start value, end value, easing. Take every number from the source. Convert distances with the same factor you use for the card (for example `1920 / W`); angles, scale factors and durations carry over unchanged.
2. Map the easing. Find the easing helper in the kit and translate it:
   - a cubic-bezier → `cubic-bezier(a, b, c, d)` in CSS, `keySplines` in SVG, the same four numbers as bezier handles in Lottie and After Effects keyframes;
   - a power or exponential ease → the closest standard bezier; state which one you chose;
   - a spring or overshoot → keyframes at the peak and the settle points with the element's own values (for example scale `0 → 1.12 → 1.0` at the stated times). A CSS `linear()` easing or sampled keyframes also work. Do not replace it with a plain ease-out.
3. Rebuild the shapes with the target's primitives and the element's proportions.
4. Staggers: keep the per-item delay and the order.

Target notes:

- **CSS**: one `@keyframes` per property group, `animation-duration` equal to the cycle (or to the entrance when it plays once, with `animation-fill-mode: both`). Percentages are `time / duration`.
- **SVG**: stroke drawing maps to `stroke-dasharray`/`stroke-dashoffset`; masks map to `clipPath` or `mask`.
- **Lottie**: keyframe times are frames, `time * fps`. Keep the frame rate of the project.
- **After Effects**: set keyframes with the values above, or write an expression on the property using `time - inPoint` as `u`. Expressions are JavaScript, so an easing function from the kit can be pasted into the expression and applied to the same values. Include the license line as a comment in a script file; for values typed into keyframes, name the element in the layer or comp comment.

Per-pixel effects (blur, glow, grain, compositing with an offscreen canvas) often have no direct equivalent. Use the target's nearest effect, compare against the demo and report the difference.

## 4. Prompts for video-generation models

Write sentences, not code. Use the element's English name and spec:

- what is on screen and what moves,
- the order of the motion and the duration of each part in seconds,
- how it eases (starts fast and settles, overshoots slightly and returns, constant speed),
- where it comes to rest and how long it holds,
- for camera elements: the move, its direction, its speed and the framing at the start and end.

Then add the user's subject, visual style, aspect ratio and clip length. Keep one move per shot; these models handle a single clear move better than a list. For text on screen, state the exact words and expect to check them, since generated text is often wrong. Describe the result in the report as "based on #ID", not as a port.

## Colors

Elements take colors from the palette object `C` in the kit. Read the kit to see which key plays which role (background, text, accents); the key names differ between packs. To re-theme, change the values in `C` once. Do not edit color literals inside elements unless an element defines its own. Keep the contrast relationships: text that was light on a dark ground stays readable, and each accent keeps its role. If the project has brand colors, map them to the palette roles and list the mapping in the report.

## Content

The words, numbers and names inside an element are sample content. Replace them with the user's. Text is measured and laid out for the sample's length, so check long replacements: reduce the font size constant or split lines rather than letting text leave the card. Japanese and Latin text have different widths at the same size; check both if the video is bilingual.

## License line

Keep each element's first line, `// Motion Prompt #ID · MIT License (c) 2026 Shohei Ohtaki · https://showheyohtaki.github.io/motion-prompt/#ID`, above the code made from it, and the kit's first line above the kit. When only numbers were carried over (section 3), put the same line as a comment where the target format allows comments.

## Check before reporting

- the first frame, a frame in mid-motion and the resting frame of each ported scene, compared with the demo when you can view it
- the loop point, if the element loops: the last frame and the first frame match
- scene boundaries: nothing pops in or out when a scene starts or ends
- replaced text fits, and the fonts are the intended ones on the rendering machine
- the output frame size and frame rate are the project's, not the card's
