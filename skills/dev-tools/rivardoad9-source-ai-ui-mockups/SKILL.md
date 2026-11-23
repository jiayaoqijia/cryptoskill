---
name: ai-ui-mockups
description: "Use when showing UI mockups before building the app."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [ui, mockup, design, stitch, dashboard, mockup-first, screenshots]
    related_skills: [sketch, ui-ux-pro-max, claude-design, popular-web-designs]
---

# AI UI Mockups

Generate a real, high-fidelity UI screen with an AI design tool, show it as an image, get approval, then build. This is the fast path for "bikin dulu demonya, kalau oke baru bikin webnya".

## When to Use

- The user asks for a dashboard, app, tool, landing page, or any multi-screen interface and you would otherwise start writing code.
- The user says some variant of "bikin demonya dulu", "kasih gambar dulu", "coba pakai Stitch dulu".
- You need a design reference to implement against, fast, without a designer.

## The approval gate (hard rule)

When the user asks for an app/dashboard/tool, the first deliverable is **images of the design**, not a codebase. Sequence:

1. Generate 2–3 screens (e.g. overview desktop, second module desktop, mobile).
2. Show the PNGs inline in chat with a short list of what each screen contains.
3. State the defects you already see, in your own judgment — never present a generated screen as flawless.
4. Only after the user says the direction is OK, write the production implementation.

Do not ask "mau gw buatkan?" after delivering images — the gate is explicit: images → user verdict → build.

## Stitch route (preferred for full app screens)

The Google Stitch CLI ships as an npm package and authenticates with an API key — **no Google account login, no MCP server, no browser session**. If a Google AI Studio key exists in the profile it typically works as `STITCH_API_KEY`.

```bash
cd ~/stitch-work && npm i --no-audit --no-fund @google/stitch
KEY=~/.hermes/secrets/google_stitch.key
export STITCH_API_KEY="$(cat $KEY)"            # never echo the value
S="node node_modules/@google/stitch/dist/cli.js"
$S status                                       # expect authenticated: true, authMethod: api_key
```

### Create the project and first screen

```bash
$S generate screen --new-project "Zemiz Studio" --title "Zemiz Studio — Content Automation" \
  --device DESKTOP --prompt "$(cat prompt_desktop.txt)" --json > desktop.json
```

`--device` is `DESKTOP` or `MOBILE`. One prompt = one screen; write the prompt to a file first (multi-line prompt with quotes breaks shell escaping).

### Add screens to the same project

Same project id keeps the palette, font and spacing locked — this is what makes a 3-screen set look like one product instead of three unrelated mockups.

```bash
$S find projects --json | python3 -c "import sys,json;[print(p['name'],p['title']) for p in json.load(sys.stdin)['data']['items']]"
$S generate screen --project <projectId> --device MOBILE --prompt "$(cat prompt_mobile.txt)" --json > mobile.json
```

Do **not** pass `--title` here: it only names a brand-new project (`--new-project`) and the CLI hard-errors with `VALIDATION_ERROR` otherwise.

### Pull the render down

The generate JSON carries an `imageUrl` of the form `https://stitch.googleapis.com/v1/projects/<pid>/files/<fid>:download`. That endpoint returns a JSON envelope, not an image:

```bash
curl -s -H "X-Goog-Api-Key: $STITCH_API_KEY" "$IMAGE_URL" -o raw.json
python3 - <<'PY'
import json,base64
from PIL import Image
d=json.load(open('raw.json'))
open('shot.png','wb').write(base64.b64decode(d['dataString']))
print(Image.open('shot.png').size)
PY
```

Some file ids in the generate JSON are the **HTML export**, not a PNG; their `dataString` is markup and `base64.b64decode` raises `UnicodeEncodeError` on characters like `⌘`. Catch it and save the payload as `.html` — that export is the seed for the real build, so keep it.

### Prompt recipe that produces usable screens

Write it in English regardless of UI language; name the language of the labels explicitly. Include, in this order:

- Product + audience + one-line purpose.
- Exact structure: sidebar items, top bar controls, each card by name, table columns, footer bar.
- Real numbers in every KPI and row (Stitch fills plausible data; "1,84 jt +38,4%" beats "some metric").
- Explicit palette hexes for background, panels, borders, and each accent; one font family; corner radius; density qualifier.
- A quality anchor ("premium SaaS like Linear and Vercel") — it measurably tightens spacing and type.
- The brand string **twice**, spelled exactly.

## QA the render before the user sees it

Load each PNG with `vision_analyze` and check for the failure modes Stitch actually produces:

| Check | Typical defect |
|---|---|
| Brand spelling | Invents a sibling name ("Zenith Studio" for "Zemiz Studio") or drops the year |
| Data coherence | Filter says "7 hari" while the chart axis spans a month; KPI total impossible for the window |
| Truncation | Card titles elide mid-word in dense columns |
| Overlap | Floating status bar covers the last row of a kanban/table |
| Contrast | Secondary labels and axis ticks too dim on near-black |

Report these defects yourself when handing over the images. A mockup with a visible data contradiction still works as a design reference — say so plainly instead of hiding it.

## Hand-off to the real build

- Treat every number in the render as dummy data. Nothing from a Stitch screen is a data contract.
- Reuse the exported HTML/CSS for layout and tokens, then replace the data layer with real API calls; do not re-draw a layout Stitch already produced.
- Keep the design tokens in one place (`:root` vars) so the mockup palette survives into the implementation.
- Building it as a live app rather than a static page: follow `localhost-dashboard-serving` (stdlib
  server + SQLite + quick tunnel + keeper cron). The mockup's tokens map 1:1 onto its CSS variables,
  and the data-coherence defects from QA (window/filter mismatch, impossible KPI totals) get fixed by
  deriving every KPI delta from the same date window the chart plots.
- Fix the QA defects (brand, truncation, overlay) during implementation rather than regenerating the mockup for them.

## Fallback: hand-written HTML mockup

No key, or the user wants pixel control: write one self-contained HTML file per screen, then screenshot at the exact viewport with CDP instead of eyeballing in a window.

```python
cdp('Emulation.setDeviceMetricsOverride', width=1440, height=900, deviceScaleFactor=2, mobile=False)
new_tab('file:///home/ubuntu/dash_demo/overview.html')
wait_for_load(); print(capture_screenshot())
```

Then downscale with PIL before sending (2x renders are 2880×1800; Telegram compresses tall images hard). Check the font is actually installed first — `fc-list : family | grep -i "plus jakarta"` — a missing display font is the difference between a premium mockup and a default one.

## Pitfalls

- **`find screens` returning `items: []` does not mean generation failed.** Take ids and URLs from the `generate ... --json` output; the screens listing is not always populated for design-type projects.
- **Download endpoint returns JSON, not PNG.** Decoding `dataString` is mandatory; writing the curl output straight to `.png` yields a file that starts with `{`.
- **`--title` without `--new-project` is a hard validation error.** Screen titles are chosen by Stitch.
- **MOBILE renders a full-page tall image** (e.g. 780×2642 for a 390-wide design), not a 390×844 device frame. Crop or scale for presentation; don't assume the height.
- **Never print the API key.** Read it into an env var from the secrets file, and keep `status` output redacted.
- **Don't generate one giant prompt for five screens.** Screen-by-screen in one project gives far better structure than "dashboard with everything".
