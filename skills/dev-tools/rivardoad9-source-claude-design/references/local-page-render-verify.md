# Rendering and visually verifying a local HTML artifact

Use this when the deliverable is a self-contained HTML file (landing page, prototype, deck) and
you want to actually look at it — desktop and phone — before saying it is done. `vision_analyze`
reads a rendered PNG; it cannot read HTML.

## Recipe (browser_exec + CDP)

Open the file directly, drive the viewport through CDP, capture beyond the fold:

```python
import base64, time

new_tab("file:///home/ubuntu/project/index.html"); wait_for_load()

cdp('Emulation.setDeviceMetricsOverride',
    width=1440, height=900, deviceScaleFactor=1, mobile=False)
js("document.documentElement.style.scrollBehavior='auto'")

# prime scroll-triggered animations: one scroll per frame, with a real pause
H = js("document.body.scrollHeight"); y = 0
while y < H:
    js(f"window.scrollTo(0,{y})"); time.sleep(0.2); y += 700
js("window.scrollTo(0,0)"); time.sleep(0.5)

res = cdp('Page.captureScreenshot', format='png',
          captureBeyondViewport=True, fromSurface=True)
open("preview-desktop.png","wb").write(base64.b64decode(res['data']))

# phone: same call, width=390, height=844, mobile=True, deviceScaleFactor=2
```

Then crop with `vision_analyze(region=[x1,y1,x2,y2])` — bands about 1400 px tall, because a
full-page shot of a 5,000 px page gets downscaled until text is unreadable.

## Traps that cost a re-render

- **`scroll-behavior: smooth` breaks `window.scrollTo(0,0)` before capture.** The call animates,
the screenshot fires mid-scroll, and you get a blank strip at the top plus a sticky header sitting
over the middle of the page. Set `document.documentElement.style.scrollBehavior='auto'` first, and
confirm `window.scrollY` is actually 0.
- **A synchronous scroll loop does not trigger IntersectionObserver.** `for (y…) scrollTo(y)` in one
`js()` call moves the page but no callback renders a frame, so every `.reveal` section stays at
`opacity: 0` and the full-page screenshot is mostly white. Scroll in separate JS calls with a pause
between them, then assert `document.querySelectorAll('.reveal.in').length` equals the total before
capturing. If it does not, force the class on for the screenshot and fix the build separately.
- **`captureBeyondViewport` resizes the viewport**, so sticky/fixed elements can land in odd places.
For the hero check, take a second viewport-only shot (`cdp('Page.captureScreenshot', format='png')`
with no `captureBeyondViewport`) at scroll 0.
- **`deviceScaleFactor=2` doubles the pixel dimensions** of the PNG, and `vision_analyze` regions are
in original PNG pixels — double your crop coordinates for phone shots or you will review the wrong
area.

## Verification checklist (cheap, catches the real bugs)

```js
document.documentElement.scrollWidth          // must equal viewport width at 390: no h-overflow
[...document.querySelectorAll('[data-wa]')].map(a=>a.getAttribute('href'))   // links resolved
[...document.querySelectorAll('section[id]')].map(s=>s.id)                   // sections present
```

Reading these three back catches the failures screenshots hide: a `javascript:`-less anchor that
never got its `href`, a section silently missing, a single card overflowing the phone viewport.

## What to look for when reviewing the render

Overlapping decorative badges, a price or label truncated by its own card, sections that are
unevenly tall because one description runs long (push prices/buttons to the bottom with
`margin-top:auto` in a flex column), a nav that is invisible or has no CTA below 900 px, and
contrast on small tinted pills — small text on a light brand tint is the most common miss.
