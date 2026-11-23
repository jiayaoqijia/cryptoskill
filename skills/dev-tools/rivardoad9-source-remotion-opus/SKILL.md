---
name: remotion-opus
description: "Make premium launch / promo videos (any length; landscape 1920x1080 + portrait 1080x1920, Remotion) with a few API calls instead of an expensive agent loop. Opus 5.5 (via the Vikey API) picks a fresh concept, writes the voice-over and reviews rendered frames. Spec mode fills fixed motion engines (3D fly-through, editorial poster, kinetic type); code mode lets an Opus agent write a bespoke scene with its own components. Use for model/product launches, price announcements, feature promos and UI-motion explainers."
version: 0.2.1
author: direkturcrypto
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [video, remotion, motion-graphics, promo, launch, vikey]
prerequisites:
  commands: [node, npm, ffmpeg, ffprobe, git]
---

# remotion-opus — Opus-grade launch videos from cheap models

You drive the `ros` CLI from https://github.com/direkturcrypto/remotion-opus-skill. You never write React or
animation code for a video: the engine owns camera, typography, easing, captions, SFX and both aspect ratios, and a
creative-director step makes every film look different from the last ones. Quality comes from three things you
control: **the brief, the facts, and following the loop.** Keep your own token use low: don't read the engine source
or the rendered images unless something fails — run the commands and read the short reports.

## 0. Setup (once)

**Installed from a chat?** Users often just send "install skill ini https://github.com/direkturcrypto/remotion-opus-skill"
in Hermes Desktop or Telegram and expect you to do the rest. Then, in that same conversation:

1. Install the skill if it isn't yet: `hermes skills install direkturcrypto/remotion-opus-skill/skill/remotion-opus --yes`
   (other agents: `npx skills add direkturcrypto/remotion-opus-skill -y`). Report the security-scan verdict.
2. Clone the repo, `npm install`, `node bin/ros.mjs init` (commands below). Check node, npm, git, ffmpeg.
3. Ask the user, in plain words, for what is missing: their **Vikey API key** (required — vikey.ai dashboard) and an
   **ElevenLabs API key** (optional — only for the voice-over and music). Suggest a dedicated key for the agent.
4. When they reply, write the keys into `.env` yourself. Never echo a key back in chat or into logs.
5. Run `node bin/ros.mjs doctor` and tell them it's ready, then offer to make the first video in this same chat.

```bash
git clone https://github.com/direkturcrypto/remotion-opus-skill.git && cd remotion-opus-skill
npm install
node bin/ros.mjs init        # creates .env, synthesizes SFX, checks ffmpeg
# edit .env: VIKEY_API_KEY=vk-…  (VIKEY_BASE_URL=https://api.vikey.ai/v1)
#            ELEVENLABS_API_KEY=…  (optional — voice-over eleven_v4 + music; without it: captions + SFX only)
node bin/ros.mjs doctor      # must show builder + verifier "✓ available"
```

`ros` below means `node bin/ros.mjs` run from the repo root.

## 1. Gather facts BEFORE anything else

Every number on screen (price, %, context size, version, benchmark) must be in `facts.md` with its source and
date — the linter rejects any on-screen number that is not in the facts. Read the official pages yourself
(pricing pages are often JS-rendered: use a browser tool, not a plain fetch). Write down what NOT to claim
(e.g. "official cache is cheaper — no cache discount"). Never claim "forever/selamanya", "unlimited", "fastest"
unless a source says so.

## 2. Create the project

```bash
ros new <slug> --brief "<what launches, for whom, the ONE message, required CTA line, language, brand + colour>"
# then edit projects/<slug>/facts.md (bullets: fact — source, date)
```

A good brief names: the product, the audience/angle, the single takeaway, the exact CTA if the client wants one
(e.g. must end with "pakai Vikey!"), language for VO and captions, brand name/url/colour, and things to avoid
(e.g. "no Xiaomi logo, model name as text").

## 3. Pick a mode

- `ros run <slug>` — **spec mode**: fixed, polished engines (flythrough / poster / kinetic). Cheapest, most predictable.
- `ros code <slug>` — **code mode**: an Opus agent writes a bespoke scene with its own components for this story,
  renders and looks at its own frames, then an art director reviews it. Use it when the client wants something
  that doesn't look like any previous video. ≈Rp30–35k per film on Vikey.
Length: `ros new <slug> --duration 30` (or "30 detik" in the brief); otherwise the director picks.

## 3b. Run the loop (spec mode)

```bash
ros run <slug>     # concept → plan → audio → review rounds (stills → Opus verify → fix) → render
```

Or step by step when you want control:

```bash
ros concept <slug>   # director picks engine/path/look/archetype/angle → concept.json (differs from recent films)
ros plan <slug>      # builder writes projects/<slug>/spec.json from the concept (retries until the linter passes)
ros lint <slug>      # schema + facts + cue + pacing + look-variety checks
ros audio <slug>     # ElevenLabs eleven_v4 VO (+ STT word timings) and music; SFX always
ros review <slug>    # up to MAX_ROUNDS of stills → Opus review → patch/fix
ros render <slug>    # MP4s in projects/<slug>/out/ + automatic frame-jump scan
```

## 4. Read the results — don't just trust the exit code

- `projects/<slug>/review/round-N/review.md` — Opus's verdict, score, issues. `sheet-L.jpg` / `sheet-P.jpg` are
  contact sheets of the frames it saw. Look at them yourself if your agent can see images.
- `ros render` prints "unexpected frame jump(s)" with frame numbers if something pops — render a still at that
  frame (`ros stills`) and look.
- VO: `ros audio` warns when STT didn't hear the brand name (TTS mispronounced it). Re-take one line with
  `ros audio <slug> --only m04 --force`, or rewrite the line so the brand ends the sentence.
- `ros usage <slug>` — tokens per model (the builder does the heavy writing; Opus only sees frames).

## 5. Editing a finished spec by hand

`spec.json` is the single source of truth. Allowed edits: copy, cue words, `look.preset`, `path`, `camera.zoom`,
`camera.moves`, `punches`, widget fields. After any edit: `ros lint <slug>` then `ros review <slug> --rounds 1`.
Widget catalog and limits: `prompts/builder.md`. Cue format: `"m02:gambar"` = the moment the word "gambar" is
spoken in VO line m02 (use words from the spoken `text`, not the caption).

## Rules

- Don't edit `src/engine` or `src/widgets` to fix one video — fix the spec. Engine changes are for everyone and
  need a full re-test of `ros example` + `ros render mimo-example`.
- Variety is enforced: the concept may not reuse the last film's engine or the last two looks
  (`projects/.history.json`). If the user wants a specific style, put it in the brief ("pakai gaya poster").
- Portrait and landscape always ship together.
- If the review keeps failing on the same issue after 3 rounds, stop and report the issue + the contact sheet
  to the user instead of looping.

## Troubleshooting

| symptom | fix |
| --- | --- |
| `model … not available` | check `ros doctor`; set `BUILDER_MODEL` / `VERIFIER_MODEL` in `.env` to ids from Vikey `/v1/models` |
| builder keeps failing lint | read the errors — usually an invented number (add the fact or drop the claim) or a cue word that isn't spoken |
| text cut off / overlapping | the verifier usually patches it; otherwise shorten the text (limits in `prompts/builder.md`) |
| no voice in the MP4 | `ELEVENLABS_API_KEY` missing, or `projects/<slug>/public/vo/*.mp3` incomplete → `ros audio <slug> --force` |
| first render slow | Remotion downloads Chrome Headless Shell once (~90 MB) |
