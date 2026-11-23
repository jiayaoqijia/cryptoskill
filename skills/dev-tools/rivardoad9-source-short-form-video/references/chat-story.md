# Chat-story (two-panel dialogue) — geometry, timing, audio, QA

Genre: TikTok/Reels/S shorts where two characters trade chat messages across two stacked
panels. No voiceover; the bubbles are the story. Renders in minutes on CPU because everything
is vectors and type, so a whole episode costs zero API spend.

## Panel geometry (1080×1920)

| Element | Value |
|---|---|
| Panel size | 1080×880, two stacked |
| Divider | 40px band, accent at low opacity |
| Label (name + clock) | 34px from panel side, ≥90px from panel top |
| Meta line ("online", timestamp) | 40px from sides, ≥110px from panel bottom |
| Bubble max width | 620px, 22px radius, tail toward the speaker |
| Last bubble, lower panel | must END ≥180px above frame bottom |
| Accent per character | one hue each, reused for bubble stroke, label, and rim light |

Two hard rules, both learned from broken renders:

1. **Figure and bubbles on opposite sides.** A figure at centre-right plus bubbles stacked down
the middle means the head intersects bubble three. Place the figure at x≈320 and start bubbles at
x≈440–480, or mirror it.
2. **Panel edge ≠ safe area.** Platform UI eats the outer 120px top / 320px bottom of the frame,
which lands inside the panels. Labels at 26px and meta at 24px look fine in the editor and are
covered on the phone.

## Reveal mechanism

Keep the script as data and let the renderer place it:

```tsx
const MSGS = [{ panel: 'boy', text: 'udah tidur?', at: 0.6, x: 480, y: 110, color: CY }, ...]
// per message: spring off (frame - at*fps)/fps, damping 14, stiffness 180; rise 12px + fade 0→1
```

- Persist every message after its reveal (chat history stays on screen); only fade the whole panel
  on scene change.
- Show a three-dot typing indicator in the *other* panel for ~0.7s before each new bubble, aligned
  to the side that will answer.
- Aim for one message every 2.5–4s in the body; the last two messages should be 1.2–1.8s apart —
  acceleration is what makes the ending land.

## Audio recipe (ffmpeg)

```bash
# room tone: pink noise, low-passed, 30s, gentle fades
ffmpeg -f lavfi -i "anoisesrc=color=pink:amplitude=0.35" -af "lowpass=f=380,volume=0.10,afade=t=in:d=1.5,afade=t=out:st=28.5:d=1.5" -ar 44100 -ac 2 room.wav
# message ping: 1180Hz sine, short decay
ffmpeg -f lavfi -i "sine=frequency=1180:duration=0.18" -af "volume=0.18,afade=t=in:d=0.005,afade=t=out:st=0.1:d=0.08" ping.wav
```

Layer `<Audio src={staticFile('room.wav')} />` across the whole composition and one `<Sequence>`
per ping at its message time. Never music: a track locks the pacing and forces the bubbles to
follow it.

## Render + QA

```bash
node ~/remotion-opus-skill/node_modules/@remotion/cli/remotion-cli.js \
  render src/index12.ts NeonPilot out/neon_pilot.mp4 \
  --codec=h264 --concurrency=2 --crf=20 --overwrite
```

QA pass, in this order:

1. `remotion still` at the emotional turn — check that the figure reads as a body in a room, not
   floating shapes, and that no bubble touches a head.
2. `ffmpeg -i out.mp4 -vf "fps=1/5,scale=280:-1,tile=6x1" -frames:v 1 sheet.jpg`, then vision-check
   the strip: does the sequence read as one conversation, and is any frame empty or duplicated?
3. One still at the ending card — the card must be reachable without a fade to black.

A 28s pilot renders in ~6 minutes at `--concurrency=2`; budget ~1–2 hours for a full 3-minute
episode including the writing, which is the actual bottleneck.
