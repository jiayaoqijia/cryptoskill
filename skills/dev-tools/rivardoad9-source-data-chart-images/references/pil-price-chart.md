# Candlestick / level-line charts with Pillow (no browser)

Use when the figure is **price candles + horizontal levels** — entry, TP, SL, and a shaded band for an
LP bin range: the shape of a trading-terminal screenshot. Pillow (`PIL`, 12.x, installed on this host)
is the short path: exact pixel control over every candle, no document height to compute, no Chromium
start. Curve/panel/table figures stay on the HTML+SVG+Chromium pipeline in SKILL.md.

Working reference implementation to copy from: `~/.hermes/scripts/fm_lp_chart.py`
(candle 1h + bin band + ENTRY/TP/SL + footer; CLI: `--spec spec.json` or `--selftest`).

## Recipe

1. **Supersample 2×, then downscale once.** That single LANCZOS downscale is what makes lines and text
   look anti-aliased; drawing at final size looks cheap at Telegram zoom.

```python
SS = 2                                   # W, H = final size in "css" units
def s(v): return int(round(v * SS))      # every coordinate goes through s()
img = Image.new("RGB", (s(W), s(H)), BG)
d = ImageDraw.Draw(img, "RGBA")          # RGBA mode => alpha fills work
...
img.resize((W, H), Image.Resampling.LANCZOS).save(out, "PNG", optimize=True)
```

2. **Fonts:** `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` and `-Bold.ttf`. The handwriting fonts
   under `~/.hermes/assets/fonts/` are for documents, not price charts.
3. **Geometry:** plot box `left, right = margin, W - label_gutter` (right gutter holds the price ticks),
   `top, bottom` above a ~110px footer. One y-mapping closure
   `Y = bottom - (v - ymin)/(ymax - ymin) * (bottom - top)` used by candles, grid, band and lines.
   `ymin/ymax` from candle lows/highs **plus every level value**, then padded 6% so TP/SL lines are
   never off-canvas.
4. **Candles:** `x = left + (i + 0.5) * slot`; wick as one `d.line`, body as a `d.rectangle` with a
   `max(o,c)/min(o,c)` height floor (~1.5px) so doji bars don't vanish. Green up / red down.
5. **Band + levels:** band = `d.rectangle` with a 4-tuple fill (green, alpha ~46). Dashes are a loop
   (`for x in range(left, right, 14)`), not a dash API. Entry solid, TP green, SL red.
6. **Right gutter:** price ticks every nice step and always label in the user's number format
   (`0,012340` — see `id_num()` in the reference script).
7. **Label collisions** are the #1 defect: TP/SL/entry/band edges bunch up in a thin price range. Keep a
   spread helper and draw each label on a small semi-opaque pill so it stays readable over candles:

```python
def spread(ys, gap, lo, hi):
    order = sorted(range(len(ys)), key=lambda i: ys[i]); out = list(ys); prev = None
    for i in order:
        y = out[i]
        if prev is not None and y - prev < gap: y = prev + gap
        out[i] = y; prev = y
    over = out[order[-1]] - hi
    if over > 0:                       # push the whole stack back up if it ran past the plot
        shift = min(over, max(out[order[0]] - lo, 0.0))
        for i in order: out[i] -= shift
    return out
```

8. **Verify with `vision_analyze`** before sending: cut text, overlapping labels, unreadable numbers.
   `--force-device-scale-factor` equivalent here is the 2× supersample; nothing else to tune.

## Data + honesty rules

- Candle data must come from a source you can name and that the consumer's own tooling already uses
  (for FlowMetrix pools: GeckoTerminal `/networks/solana/pools/<pool>/ohlcv/hour?aggregate=1&limit=N&currency=usd&token=base`).
  Cache per pool on disk (15 min is plenty) and back off on HTTP 429 — the free tier limits rate and a
  live engine may share the same quota.
- **No data → no chart.** If the fetch fails or returns too few bars, return `None` / print `NONE` and
  ship the text alone. Never fill a chart with invented numbers to keep the layout.

## Delivery

Send with a plain `MEDIA:/absolute/path.png` line — that works both in a normal reply and in a cron
`no_agent` job's stdout (`cron/scheduler.py` extracts the tag and the adapter posts it as a photo).
Default media policy accepts any existing file outside the credential denylist; strict mode needs an
allowlist or a freshly-created file. Palette used for these: bg `#0b1020`, panel `#111a2e`, text
`#e6edf7`, muted `#93a1b8`, grid `#1e2740`, up `#2ecc71`, down `#ef5350`, entry `#f5c451`.
