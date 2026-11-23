# Annotations and labels on top of the data (chart additions, 29 Sep 2026)

Second companion to `references/render-verification-pitfalls.md`. Both defects below were caught by
`vision_analyze` on a candle chart (price panel + performance-bar panel), and both were re-renders.

## 1. Dashed price-level annotations belong in the margin, not over the candles

Horizontal support/resistance/EMA level lines need their text label, and placing it at the left
(`x = PAD + 4`) drops it straight onto the candles of that period — the vision check reported "labels
overlap the candles" on a chart where everything else was clean.

Fix: anchor level labels at the **right** edge, outside the plotted data:

```python
# line first, then its label right-anchored in the margin
out.append(f'<line x1="{PAD}" y1="{y}" x2="{W-PAD}" y2="{y}" stroke="{col}" stroke-dasharray="5 4" opacity="0.5"/>')
out.append(T(W - PAD - 6, y - 5, label, 10.5, col, anchor='end', mono=True))
```

Keep the price-scale ticks and the level labels on the same side only when their y positions cannot
collide; if they can, move the ticks to the left axis. Six level labels stacked in the right margin read
fine as long as each line's colour matches its label.

## 2. On a log-scale price chart, say what the levels ARE

Labels like `EMA50w 0,2035 — target/atap pertama` beat bare numbers: the reader needs the *reason* (EMA,
prior high, prior low) to judge whether a break matters. Name support and invalidation levels with the same
specificity as targets.

## 3. Interval abbreviations are ambiguous in Indonesian — write them out

`24j` / `7h` in a subtitle got read back as "7 jam" (hours) when it meant 7 days, and the ambiguity also
propagated into the vision verification. Use `24 jam`, `7 hari`, `30 hari` in the subtitle and in bar
labels. Never mix `j` and `h` in one line.

## 4. Ask vision about the label/overlap specifically

Generic "cek chart" prompts miss these. Ask: *"Apakah label level menimpa candle? Sebutkan semua label
level dan warnanya."* — that question is what surfaced both the overlap and the misattributed values.
