# HTML → still image (posters, certificates, social cards)

Use when the artifact is a *picture* the user will post or send (poster, licence/certificate, meme card, contest entry), not a page they will open.

## Render recipe (one shot, exact pixels)

Design the HTML at the final pixel size — `html, body { width: 1080px; height: 1350px }`, no responsive CSS, no scrollbars — then render with the headless shell directly:

```bash
BIN=$(ls -d ~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell | tail -1)
"$BIN" --headless=new --no-sandbox --disable-dev-shm-usage --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --virtual-time-budget=9000 \
  --window-size=1080,1350 \
  --screenshot=/abs/path/poster.png \
  "file:///abs/path/poster.html"
```

Why this path is the default for a single still:

- `--window-size` **is** the output size — no clip rect to keep in sync with the layout, so the render cannot come back stretched or cropped.
- `--force-device-scale-factor=2` gives a 2x master (1080x1350 → 2160x2700) for crisp text at any downstream size.
- `--virtual-time-budget=9000` lets `@import`ed webfonts (Google Fonts) load before capture. Without it the shot lands first and the serif silently falls back — tracking looks wrong and nothing errors.
- One-shot process: nothing to keep alive, nothing to time out mid-capture.
- Keep `--headless=new` in the command: legacy `--headless` traps (`Trace/breakpoint trap`, core dumped) before any pixels are written, which reads like a broken browser instead of a flag problem.
- `zip` is not installed on this host — build any archive with Python `zipfile`.

Check the result is a real image of the expected dimensions before saying it worked: `file poster.png` should print the 2x size.

## Delivery sizes

| Use | Design at | Notes |
| --- | --- | --- |
| X / Instagram feed | 1080x1350 (4:5) | tallest feed crop, best engagement |
| Square card / meme | 1080x1080 | |
| Certificate, "document" prop | 1600x2000 | more room for body copy, still 4:5 |
| Story | 1080x1920 | keep critical text off the bottom 15% |

Ship a downscaled JPEG for chat (PIL `resize(..., LANCZOS)` + `quality=92, optimize=True, progressive=True`): 1080x1350 lands ~75 KB, 1600x2000 ~270 KB. Keep the 2x PNG master — chat clients recompress anyway, the master is what survives a re-export.

## Design pitfalls that cost a re-render

- **Void at the bottom third.** After the main content a certificate/poster leaves a dead band. Fix it by structure, not by nudging one element: put paired signature blocks on a shared baseline, centre the seal *under* them, keep the footer ~110 px above the frame, then re-render and look at the bottom third specifically.
- **Unequal paired rules.** Two signature rules of 520 px and 500 px read as sloppiness in a formal-document idiom. Equal widths, equal page margins.
- **Emoji as artwork.** A seal, paw, stamp or emblem drawn as emoji renders differently per platform and cannot take the ink colour. Draw it as an SVG group.
- **Texture that fights text.** Noise/grain overlays go `mix-blend-mode: multiply` (paper) or `overlay` (dark) at ≤0.5 opacity, and are added *last* in the DOM so they never sit above the text.
- **Generic vocabulary.** For a brand artifact, lift the subject's own phrases from its site/profile into the copy ("glass-walled treasury", "licence No. ????", internal ratios). Judges of brand contests score fidelity to the lore; generic crypto words read as copy-paste.

## Verify before sending

Same loop as diagrams — load the PNG with `vision_analyze` and ask specifically about text clipped by its box, blocks overlapping, mismatched baselines, and whether the central graphic reads as the object it is meant to be (a bell that reads as a lamp is a fail). Fix, re-render, look again. Never report a fix you have not seen in a new render.

## Handing an image back to the user for posting

When the platform write path is not available, deliver: the image(s), the exact caption text in a fenced block, and a prefilled compose link `https://x.com/intent/post?text=<urlencoded caption>`. State plainly that the post does not exist yet — never present assets as a completed entry.
