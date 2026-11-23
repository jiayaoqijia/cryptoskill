# Spec-driven level charts (one generator, many tickers)

Companion to `rendered-chart-qa.md`. Pattern from the 2 Okt 2026 daily deep-dive work: instead of
hand-writing a new SVG per candidate, one generic generator renders every price/level chart from a
JSON spec. Two paying cases in one session (an AAVE report chart and an ad-hoc TNSR chart) — the
second cost 2 minutes instead of an hour.

## Contract

`python3 ~/.hermes/scripts/diag/make_setup_chart.py --spec /tmp/spec.json`

```json
{"symbol":"TNSR","days":180,"out":"/tmp/charts/tnsr_dd.png",
 "title":"TNSR (Tensor) — struktur 180 hari & peta level",
 "sub":"harga $0,0409 | +1,7% 24j | pos90 70% | MA30 $0,0369 | vol7/30 2,12x",
 "levels":[{"label":"trigger breakout 0,0440-0,0458","lo":0.044,"hi":0.0458,"kind":"band","color":"green"},
           {"label":"invalidasi 0,0369 (MA30)","v":0.0369,"kind":"line","color":"red"},
           {"label":"target 1: 0,0557-0,0585","lo":0.0557,"hi":0.0585,"kind":"band","color":"amber"}]}
```

Rules that make it safe to drive from an LLM-written spec:

- The generator **fetches its own klines** (exchange daily candles) and computes `price, ma30, ma90,
  pos90, dist_high90, vol_ratio, ch24/7d/30d`. The JSON it prints is the *official* number set — the
  prose in the report must equal it, and the chart is never built from numbers the model typed.
- Out-of-range / non-listed ticker → skip the image, send text only. Never substitute another ticker
  just to have something to attach.
- Level colour vocabulary kept constant across charts: green = entry/trigger band, red = invalidation
  line, amber = target band/line, white = current price.
- Price decimals by magnitude (`>=1` → 2 dp, `<1` → 4 dp, `<0.01` → 6 dp) with the locale helper
  (`1.234,56`) — otherwise a $4 and a $0.0000124 chart use the same tick style and read wrong.

## Auto-anchor long right-column labels (instead of hand-shortening)

"Keep labels ≤ ~210 px" is a rule the writer has to remember; enforce it in code after the collision
`resolve()` pass:

```python
adj = []
for (y, txt, col, x, anchor, size, wt) in resolve(rows, gap=24):
    est = len(str(txt)) * size * 0.62          # measured: 14 px font ≈ 8.7 px/char
    if anchor == "start" and x + est > 1360 - 26:
        adj.append((y, txt, col, 1360 - 26, "end", size, wt))   # text-anchor="end" at the edge
    else:
        adj.append((y, txt, col, x, anchor, size, wt))
```

Tuning that mattered: a `0.56` factor with an 18 px margin did **not** fire for a 35-char label and the
clip shipped; `0.62` with a 26 px margin did. Tell-tale that a threshold never triggered: the
re-rendered PNG is **byte-identical** (`md5sum` consecutive renders) — then re-verify with vision and
ask about the *longest* label **by name**, not "are the labels ok".

## QA before attaching

1. `ok: true` and `content_ratio` inside `0.02–0.9` (bright-pixel fraction; on a dark theme
   `1 - bright` always reads ~0.95 and would flag every good chart).
2. `vision_analyze` the PNG and ask specifically: longest right-hand label fully visible? bands and
   lines where expected? current price on the correct side of entry vs invalidation? volume panel and
   date ticks present?
3. Sanity-check the level geometry in prose before sending: trigger above spot, invalidation below,
   targets above — a chart with a "trigger" under the current price is a spec bug, not a market view.

## Wording that keeps it honest

Charts ship with 2–4 lines of "cara bacanya" in chat, and the caption states explicitly that the levels
are **scenario, not advice** (the generator's footer says the same). The ad-hoc case is the same as the
gated case: a chart for the ticker the user asked about is fine even when the candidate didn't clear
the conviction gate — the caption just has to say the trigger hasn't fired yet.
