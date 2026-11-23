---
name: browser-animation-capture
description: Turn a browser/canvas animation into an MP4.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, chromium, canvas, css, animation, ffmpeg, demo]
    related_skills: [remotion-opus, video-deliverable-qa, p5js, motion-prompt]
---

# Browser animation → video file

## When to Use

Trigger: the user wants to *see* a web effect actually moving — "bikin jadi nyata", "coba test effect-nya",
turn a CSS/canvas demo, a glitch title, a library sample or a dashboard micro-interaction into an MP4.
The deliverable is a playable file, not a screenshot and not a description of the code.

## Pick the capture path first

**Path A — the animation is a pure function of time (canvas `draw(u)`, any renderer you can feed a `t`).**
Add a `?t=` query param to the page that draws exactly one frame, then screenshot each `t`. Deterministic,
fast, no X server, and the same call renders any fps.

```bash
# page side: const t = new URLSearchParams(location.search).get('t'); if (t) drawOnce(+t);
seq 0 112 | xargs -P 4 -I{} sh -c 't=$(python3 -c "print($1*$DUR/113)"); \
  chromium --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
    --window-size=W,H --user-data-dir=/tmp/cr_$1 --screenshot=frames/$(printf %04d $1).png \
    "file:///abs/index.html?t=$t" >/dev/null 2>&1' _ {}
```

`--user-data-dir` per frame keeps parallel Chromium instances from fighting over the profile.
-4 parallel is about right on a 2-core box (~1.2 s/frame serial, ~0.35 s/frame at -P 4).

**Path B — the animation is CSS/JS/timer driven and you cannot make it a `t` function** (a third-party
glitch/hover library, a Lottie, a scroll animation). Record the live page over CDP screencast with
`scripts/cdp_screencast.py`: it launches headless Chromium, subscribes to `Page.screencastFrame`, acks each
frame and writes JPEGs. No Xvfb, no compositor, no window manager.

```bash
python3 scripts/cdp_screencast.py --url file:///abs/index.html --out frames --duration 9 --width 1200 --height 675
```

## Encode

```bash
FPS=$(python3 -c "print(len(__import__('os').listdir('frames'))/$DUR)")
ffmpeg -y -framerate $FPS -i frames/%04d.jpg -vf "pad=W:H_EVEN:0:0:black" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart out.mp4
```

Use `-framerate` = measured frames ÷ seconds, NOT the nominal fps: screencast delivers ~50 fps and forcing
24/30 there silently slows or drops the motion. `-crf 18` for text/gradients, `20` is fine for noise-heavy
FX. PNG frames if the source has hard edges, JPEG 90–92 for full-motion captures.

## Verify before sending

1. **Prove it moves.** Compare each frame to frame 0 with a pixel diff; a real effect shows a small median
   and a large peak (median ~500 px changed, peak ~30 000 px = a glitch burst, not a static page).
   Identical byte sizes across screenshots is the tell that nothing animated.
2. **Look at the peak frame** with vision — and check that text is not tofu: CJK needs a font present on the
   box (`fc-list :lang=ja`), otherwise the render quietly ships boxes.
3. `ffprobe` the output for duration/size/fps, then send the MP4 — Telegram plays `.mp4` inline.

## Pitfalls

- **H.264 needs even dimensions.** A 1200×675 stage fails with `Could not open encoder before EOF` /
  `Invalid argument` and writes a 0-byte file. Pad or scale to an even height (`-vf pad=1200:676:0:0:black`).
  This burns full encode attempts if you read the error as a codec problem.
- **`--screenshot` + `--virtual-time-budget` does not advance CSS/JS animations.** Every frame comes back
  byte-identical. Virtual time only helps layout/fonts settle; motion needs either `?t=` rendering (Path A)
  or a live capture (Path B).
- **Don't reach for `xvfb-run` + `ffmpeg -f x11grab` as the default.** It needs a live X screen and
  writes zero packets when the grab matches nothing. CDP screencast needs neither and yields real frames.
- **Fonts decide whether the test is meaningful.** A font fallback can turn an elegant demo into Arial, and
  missing CJK fonts produce tofu you will only catch in the vision check.
- **Report the frame budget honestly.** State resolution, duration and file size, and say which parts you
  verified by eye versus by pixel diff.

## Support files

- `scripts/cdp_screencast.py` — headless Chromium → JPEG frame sequence over CDP (URL, duration, size as flags).
