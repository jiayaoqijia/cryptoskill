# QA on rendered chart PNGs (verify before you send)

Hard-won rules from rendering dark-theme price charts with headless chromium and shipping them to a
chat (both hand-built SVG and a spec-driven generator). Every chart that goes to a user gets checked
once; an unverified render is how broken labels and blank panels reach the user.

## 1. Verify with vision, every time — and expect the vision pass to misread decimals

Sending `vision_analyze` on the generated PNG caught real defects that code review would not:
labels clipped at the right canvas edge, two level labels drawn ~19 px apart (visually touching),
a legend sitting on top of the plot, a 105 px volume panel that made bars unreadable, and an axis
stretched by one far-away target line.

But: **the vision pass also hallucinates**. In the same session it reported dots as Indonesian comma
decimals (it read `$2,50` as `$2.50` and claimed the format was inconsistent) and reported a label as
duplicated. Before "fixing" a reported defect, grep the generated HTML for the actual text node:

```python
import re; ts = re.findall(r'<text[^>]*>([^<]*)</text>', open('/tmp/chart.html').read())
```

Fix what the markup confirms; ignore what it doesn't. Re-verify after each fix, and check the *tail*
of the last note line — clipping always hits the longest line first.

## 2. A blankness metric for a dark theme

A naive "blank ratio" (`1 - bright/total`) reports ~0.95 for **any** dark chart, so `ok` is always
false and the alarm is useless. Count content instead and treat it as a band:

```python
im = I.open(png).convert("RGB").resize((160, 200))
bright = sum(1 for r, g, b in im.getdata() if r + g + b > 120)
content_ratio = round(bright / (160 * 200), 3)   # good dark chart: ~0.02-0.4
ok = os.path.exists(png) and 0.02 <= content_ratio <= 0.9
```

Print `{ok, px, content_ratio, symbol, price, ma*, pos, vol_ratio, levels[].pct}` as JSON so a
non-visual caller (e.g. a cron agent without vision) has something machine-checkable, and so the
report's prose numbers can be asserted equal to the chart's numbers.

## 3. Don't let an out-of-scale level flatten the price action

Adding a "2x target" line 90% away from spot stretched the y-axis and squashed the actual price
history into the bottom third. Rule: compute the axis from the price series first, then only include
levels within roughly ±0.5–0.6 × the price span; clamp anything further to the panel edge and mark the
label `▲ di atas skala` / `▼ di bawah skala` so it can't be misread as a real level at that height.

## 4. Layout numbers that survived review (1360 px canvas, device-scale 2)

- Price panel `L=118, R=1055`, plot `PT=100 → PB=880`; volume panel `930 → 1050`; svg height 1105.
- Right-hand labels start at `R+14` at font 13.5; keep every label ≤ ~210 px or it clips at 1360.
- Resolve label collisions with a generic pass: sort rows by y, push each down until it is ≥ 24 px
  from every already-placed label (19 px was still too tight at 14 px font).
- Legend goes **above** the plot area (y = PT − 20), horizontal, one short word per series.
- Volume bars: use `log1p` scaling or one early spike sets the scale and every other bar reads flat.
- Decimal style: one helper for the locale (`1.234,56`) and use it for ticks *and* annotations, or the
  axis and the labels disagree and readers (and vision models) flag it.

## 5. Wrap the render in a script, don't hand-write SVG per call

Spec-driven generator (`--spec spec.json`, levels as `{label, lo|v, kind: band|line, color}`) returns
the PNG path plus the computed numbers, so callers never hand-type prices into prose. Keep the chrome
command inside the script, discover chromium via `~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome`,
and size the window to the computed document height (header lines included) so the screenshot has no
dead space at the bottom.

## 6. Regenerating is cheap — re-render after every text change

Text-only fixes (shorter note lines, renamed labels) still require a re-render *and* a re-check;
skipping the check is how the "first line of the note is clipped, lines 2-3 are fine" defect shipped
twice in a row.
