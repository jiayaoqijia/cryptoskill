---
name: data-chart-images
description: "Use when delivering a chart image without matplotlib."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [charts, svg, headless-chromium, dataviz, telegram, reporting]
    related_skills: [flowmetrix-ops, strategy-backtest-validation]
---

# Data chart images (no plotting library required)

Use when the user asks for a **picture of numbers** — "kasih contoh/gambar ga", equity curves, Monte
Carlo cones, before/after bars, comparison tables rendered as image — and you must deliver an actual
image file (Telegram `MEDIA:` attachment, vault note, report).

Why this pipeline: on this host **matplotlib is not installed** (system python + every venv checked;
PEP 668 blocks a casual `pip install`). Don't spend turns hunting for it. Build the chart yourself as
SVG inside a small HTML file and let headless Chromium rasterise it — full layout control, no
dependency, offline, real fonts.

## Pipeline (5 steps)

1. **Dump the data first.** Never hand-type numbers into the chart. Have the analysis script write
   JSON (curve arrays, MC percentile bands, fold windows, table rows), then read that JSON in the
   generator. In a repo context add a `--dump=<path>` flag to the analysis runner instead of a second
   analysis script.
2. **Generate HTML+SVG in Python (stdlib only).** One script per figure set; emit stacked
   `<svg width=W height=H>` blocks on a dark page. Copy `templates/chart_page.py` and replace the
   panel bodies. The page title + sub-line must state **what the numbers are and are not** (source,
   window, caveat) — the image travels to the user without your chat text attached.
3. **Compute the exact document height and pass it to Chromium.** `--window-size=W,H` is a viewport,
   not auto-height: if H is short, the bottom silently disappears. Track heights as you build
   (`top + sum(panel heights) + footer`), print it (`print(f"H={h}")`), capture in shell.
4. **Screenshot:**

```bash
CH=~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome
"$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars \
      --force-device-scale-factor=2 --window-size=1360,$H \
      --screenshot=/tmp/chart.png "file:///tmp/chart.html"
```

   `--force-device-scale-factor=2` gives a crisp 2× PNG that survives Telegram compression. stderr
   noise (`Failed to connect to the bus`, dbus) is harmless — the PNG is written anyway.

   Two knobs that matter for type-led pages (posters, certificates, infographics):

   ```bash
   HS=~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell
   "$HS" --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
         --virtual-time-budget=9000 --window-size=1600,2000 \
         --screenshot=/tmp/poster.png "file:///tmp/poster.html"
   ```

   `--virtual-time-budget=9000` lets a Google Fonts `@import` land before the shot; without it the
   first frame rasterises in the fallback serif and reads as a layout bug you then chase. The
   lighter `chrome-headless-shell` binary accepts the same flags and needs no CDP session, so it is
   the fallback when the full `chrome` binary or a long-lived browser daemon is not answering —
   same pixels, nothing to babysit.
5. **Verify with vision before sending.** `vision_analyze(image_url='/tmp/chart.png', question='cek
   teks terpotong? label tumpang tindih? angka terbaca?')`. Fix → re-render → verify again. Then copy
   the PNG to `~/obsidian-vault/attachments/` and send with `MEDIA:<absolute path>`.

## Pitfalls (each one cost a re-render)

- **Literal `\n`**: in a normal Python string `"\\n"` renders as backslash-n. Use a real `\n` and
  count lines when computing header height.
- **Outlier blow-up**: one lucky MC curve at $7.000 makes the y-axis huge → tick labels pile into a
  black column. Cap the axis at a percentile of the final values (e.g. `p95 * 1.35`) and clip outliers
  with `<clipPath>` on the cloud group.
- **Tick density**: choose the step in a loop (`while (ymax-ymin)/step > 12: step *= 2`), never a
  fixed 100 over a variable range.
- **Label collisions**: put series values in a right-hand label column outside the plot area
  (`x = R + 16`) with the series' trade/pool count under it, instead of floating over the lines.
- **Bottom note clipped** is the most common defect: the paragraph under a table needs ~120px more
  than you think. Verify the last sentence, not just the table.
- One idea per bar panel, with its heading row ~60px above the tallest bar, else the value label
  collides with the panel title.

## Deliverable conventions (this user)

- 1–5 PNGs, each with a short caption; the chat text explains how to **read** the picture — the
  picture carries the numbers.
- Save the generator at `~/.hermes/scripts/diag/make_<topic>_chart.py`, the PNG at
  `~/obsidian-vault/attachments/<topic>-<n>-<slug>.png`, and link both from the note/report.
- Dark theme: bg `#0b1020`, text `#e6edf7`, muted labels `#93a1b8`, grid `#1e2740`. Meaning colour:
  green = actual/good, red = bad / as-shipped-live, amber & blue = variants, purple = counterfactual.
- Every chart in this account carries a caveat line when the data is a backtest (upper bound, sample
  size) — see `strategy-backtest-validation`.
