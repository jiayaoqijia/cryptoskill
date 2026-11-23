# Operating an adopted LLM-video CLI (`ros`, remotion-opus): producing a real film

Companion to `references/remotion-opus-install.md` (that one covers install; this one covers the run that
actually ships an MP4). Run on 2026-10-07, 2-core box, first film = 24 s Indonesian promo.

## Stage map — drive them individually, not only via `ros run`

```
ros new <slug> --brief "…" --duration N   # scaffolds projects/<slug>/{project.json,brief.md,facts.md}
ros concept <slug>   # director: engine / path / look / archetype → concept.json
ros plan <slug>      # builder: writes spec.json (JSON spec only — never React), capped at 5 lint attempts
ros audio <slug>     # ElevenLabs VO + SFX + word timings → words.json; --force regenerates VO
ros stills <slug>    # renders review/round-1/*.jpg + sheet-*.jpg contact sheets (local, no credits)
ros render <slug>    # landscape + portrait MP4s into out/
ros review <slug>    # vision verifier loop (needs an image-capable model)
```

`ros run` = all of it, but **running the stages yourself is what lets you skip a stage the current model
cannot do** (e.g. `review` when the fallback model has no vision) and re-enter at any point
(`plan` → `audio` → `render`). Probe cost is bounded: concept 3 attempts, plan 5 (`MAX_ROUNDS` caps review).

## Sourced `facts.md` (the linter rejects invented numbers)

`facts.md` is the only place on-screen numbers may come from, and each entry needs **source + date**.
Verify each number against a local artifact *before* writing the file — never from memory:

| on-screen number | verified from | command shape |
| --- | --- | --- |
| 12 files / 2.832 Python LOC | engine repo | `find . -name '*.py' \| wc -l`, `wc -l` sum, `git log -1 --format=%cs` |
| 55 whale wallets | `whale_scan_config.json` | `python3 -c "import json;print(len(json.load(open(f))['wallets']))"` |
| 38 scheduled jobs | Hermes cron list | count entries, not eyeballed |
| 6 assets real-time | portfolio snapshot JSON | `len(rows)` + `ts`/`wib` stamp |
| brand blurb / URL | the live site | fetch the title, don't paraphrase from memory |

Always close `facts.md` with a **"JANGAN diklaim"** block: no revenue/profit/sales figures, no
"terbaik/tercepat/nomor 1", no institution names the user didn't authorize. For a personal-brand film that
is what keeps the video postable.

## Provider credit dies but the KEY is fine — repoint, don't stall

Symptom (looks like a key problem, isn't):

```
▸ concept rivardo with anthropic/claude-opus-5.5
✗ Vikey balance too low: Insufficient balance. Available: Rp0.000000
```

`ros balance` returning `RpNaN` is the same thing (it can't parse a zero balance). `doctor` still shows the
models `✓ available` — **key valid, wallet empty**. Two branches:

1. **Top up** the gateway account (keeps the Opus art director + the vision reviewer). Tell the user the
   amount and what each buys before they spend.
2. **Repoint to any OpenAI-compatible endpoint** — `cli/env.ts` reads `VIKEY_BASE_URL` (default
   `https://api.vikey.ai/v1`), `VIKEY_API_KEY`, and the model ids `BUILDER_MODEL` / `DIRECTOR_MODEL` /
   `VERIFIER_MODEL`. Backup first, then swap, then restore-or-keep with a note:

```bash
[ -f .env.vikey.bak ] || cp .env .env.vikey.bak      # never overwrite an existing backup
KEY=$(grep -E '^HERMES_DEEPSEEK_API_KEY=' ~/.hermes/.env | cut -d= -f2- | tr -d '"')  # value never printed
# write VIKEY_API_KEY=$KEY, VIKEY_BASE_URL=https://api.deepseek.com/v1,
# BUILDER_MODEL/DIRECTOR_MODEL/VERIFIER_MODEL=<id from that provider's /v1/models>, MAX_ROUNDS=0
```

- Generic OpenAI-compatible endpoints accept the call, so `concept`/`plan` work on a cheap model
  (`deepseek-v4-pro` produced a clean 8-beat spec, ember-noir look, Indonesian VO, first try after one
  lint round).
- **Capability loss is real**: the reviewer needs to *see* stills. Without vision, set `MAX_ROUNDS=0` and do
  that QA yourself — `ros stills <slug>` then inspect `review/round-1/*.jpg` and `sheet-*.jpg` with your own
  vision tool. That caught a legibility defect (code panel too small) the local model could not.
- Model ids differ per provider (`deepseek-v4-pro` / `deepseek-flash` — not the verbatim id from
  `config.yaml`): list `{base}/models` first.
- Leave the box honest: mention the swap, keep `.env.vikey.bak`, and say which provider runs now.

## Free-tier ElevenLabs (voice, not a bug)

- Library voices are refused via API on free tier: `402 … Free users cannot use library voices via the API`
  (this includes the repo's default voice *and* the user's own library voice). Use a **premade** voice and
  pin `VOICE_ID` + `TTS_MODEL` in `.env`.
- Music: `402 paid_plan_required` → **no music bed on free tier**; you still get VO + SFX. Say so up front
  instead of promising a scored film.
- Quota ~10.000 chars/month; a 24 s film ≈ 200 chars of script (× takes) — tens of films fit. Accent of a
  premade US voice reading Indonesian is audible: report it as a limitation, don't hide it.

## Verify the shipped VO — the log lies, `words.json` doesn't

`projects/<slug>/words.json` = `{dur:{m01:…}, words:{m01:[[word,start,end],…]}, text:{m01:"…"}}`.
The per-line `text` is the **transcript of the take that shipped**. Audio synthesis logs warnings for takes it
*discarded* (e.g. `"Bangun" → "Ganggun"`, brand heard as `"Zemis Digital"`); quote a defect only after
comparing `text` against `spec.json.vo.lines[].text` — here all 6 lines matched 100 %, i.e. no defect.
Sanity totals: `sum(dur) + holdSec` should land on the target duration (21.79 + 2.2 ≈ 24 s).

`ros lint <slug>` run standalone assumes a **15 s** film (`lintSpec` default when no `durationSec` is passed),
so it can report *"VO too long for a 15 s film"* on a healthy 24 s project. The pipeline passes
`targetDuration` (from `project.json.duration` / the brief), so trust that path before "fixing" the script.

## Deliver + report

- `ffprobe` both aspects and confirm a video **and** audio stream, then copy to `/tmp/<name>-{landscape,portrait}.mp4`
  and send them as MEDIA attachments — the MP4 is the deliverable, not the render log.
- Timings on 2 cores: ~5 min per aspect for 15 s; a 24 s film ≈ 4.5 min + 5 min ≈ 10 min total render.
- Report the run like a producer: script lines, every sourced number, the cost actually incurred (which
  provider paid), and the honest defect list (missing music, accent, small text). Defects the user can
  re-buy with a top-up belong in the same message as the cost of that top-up.
