# Render & verification pitfalls (learned 29 Sep 2026)

Hard-won additions to the pipeline in SKILL.md. Each of these cost at least one re-render.

## 1. Never trust a hand-computed document height — render tall, then auto-crop

The SKILL.md advice "compute the exact height and pass it to Chromium" fails quietly: `--window-size`
is a viewport, so anything below `H` simply does not exist in the PNG. Two real defects from this:
a 4-row table lost its 4th row, and a footer note disappeared — both looked "fine" at a glance.

Robust sequence:

```bash
CH=~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome
"$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars \
      --force-device-scale-factor=2 --window-size=1280,2400 \
      --screenshot=/tmp/chart_full.png "file:///tmp/chart.html"
python3 - <<'PY'
from PIL import Image
im = Image.open('/tmp/chart_full.png').convert('RGB'); w, h = im.size
px = im.load(); bg = px[3, h-3]; last = h - 1
for y in range(h - 1, -1, -1):
    if any(sum(abs(a-b) for a, b in zip(px[x, y], bg)) > 12 for x in range(0, w, 7)):
        last = y; break
im.crop((0, 0, w, min(h, last + 50))).save('/tmp/chart.png')
PY
```

PIL is available even though matplotlib is not, so this is a safe fallback: over-provide height, crop the
trailing background. Keep the `print(f"H=...")` height print for reference, but do not depend on it.

## 2. Draw order: an opaque panel/box drawn later covers earlier text

A verdict/summary box (`<rect fill=#131c33>`) rendered **after** the bar labels sat exactly on top of the
negative bar's `−$62` / `38 trd` labels and hid them. Rules:

- Emit every background box/panel rect **before** the text that lives inside or near it, then the text.
- Reserve vertical space explicitly: the box was moved from `base_y + 108` to `base_y + 190` once the
  diverging bars needed room below the baseline. Budget the deepest label first, then place the box.
- When a label must sit near a following block, verify that block's top coordinate > label baseline.

## 3. Diverging bars (positive up / negative down)

- Use **separate scale maxima** for the positive and negative sides; a single `maxnet` makes the negative
  bar look arbitrarily short.
- Put the value label *outside* the bar end (`base_y - h - 8` up, `base_y + h + 16` down) and the
  secondary label (trade count) further out again — never inside a short bar.
- X-axis category labels go on one row **below** both directions or the negative labels will collide.

## 4. Series an order of magnitude apart → split panels, don't share a y-axis

When one curve ends at $6.009 and another at $598, a shared linear axis flattens the second into a line
along the floor. Two side-by-side panels (one per setting/regime), each with its own axis and its own
"modal awal" dashed line, reads far better than log-scaling a single plot. Log axes are acceptable when
the comparison is *within* one panel, but label the axis ticks explicitly.

## 5. Verify by asking specific questions, not "does it look ok?"

`vision_analyze` with a generic prompt missed a whole missing table row. Ask pointed questions:

- "How many data rows does the table have, and what is the last row?"
- "Is there a footer/note block below the table — quote it."
- "Is any bar's label hidden or cut at the image edge?"
- "Is there a large empty area at the bottom?"

Then fix and re-verify the specific defect. One idea per figure still holds: a figure that carries the
funnel or the comparison table survives being forwarded without your chat text.
