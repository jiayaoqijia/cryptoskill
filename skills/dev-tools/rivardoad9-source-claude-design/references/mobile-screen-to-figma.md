# Mobile screen mockup → HTML → Figma

For requests shaped like: "here is a reference screenshot, here is my spec, make screen X in that
style". The spec (frame size, type scale, radius, padding, icon size) is fixed; the reference only
supplies style (palette, gradients, shadow language, nav pattern).

## 1. Files and structure

One HTML file per screen in the scratch dir, sized to the frame:

```css
body{width:390px;height:844px;overflow:hidden}
```

Give every spec value its own rule so the code can be audited against the brief later:
`.title{font-size:24px;font-weight:800}`, `.sectitle{font-size:18px;font-weight:600}`,
`.rname{font-size:14px}`, `.sub{font-size:12px}`, `.card{border-radius:16px}`, `.body{padding:0 20px}`,
icons 24x24 as inline SVG with `stroke-width:1.8`.

Sample data discipline: reuse the exact name/phone/number the user gave, and keep them identical in
later revisions. Changing sample values between versions reads as carelessness even though the layout
did not change.

## 2. Fonts without a font server

Pull the woff2 from Google Fonts and inline it, so the render does not depend on network or on the
user having the font:

```python
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}
css=urlopen(Request("https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800",headers=UA)).read().decode()
# parse @font-face blocks, download each url(...woff2), base64 them
```

Google serves a **variable** font: the same woff2 comes back for 400/500/600/700/800 (identical md5).
Embed it once:

```css
@font-face{font-family:'PJS';src:url(data:font/woff2;base64,…) format('woff2');font-weight:200 800;font-display:block;}
```

Five duplicate `@font-face` blocks inflate the file by ~150 KB and do nothing.

## 3. Render and verify

Render with the one-shot headless recipe in `html-to-image-export.md` — that file owns the command,
the flag notes and the delivery sizes; do not keep a second copy of it here. Two additions for a
phone frame:

- `--window-size=<spec W>,<spec H>` plus size the HTML to the same pixels, so nothing reflows.
- Read the PNG back with vision and ask a **specific** QA question — "is the bottom card clipped by
  the nav", "is the name and phone correct" — not "does it look good". Vague questions return a
description of the whole image and miss the defect.

Vertical budget, worked out before writing CSS (390x844 example):

| Block | Height |
|---|---|
| status bar | 44 |
| header | 52 |
| hero card | ~136 |
| section (label 22 + card 2 rows) | 120 + 32 |
| section gap | 14 |
| bottom nav | 80 |

Three sections + hero + nav lands around 810–830 px. If the sum exceeds `frame height − nav`, trim
section gaps and row padding first, not the type scale.

## 4. Figma handoff

The Figma REST API cannot create or edit design nodes (read-only for file content), and `figma.com`
plus `api.figma.com` may be blocked or token-gated from a server. Two usable routes:

**A. Plugin that rebuilds the frame natively** (default, works offline, fully editable):

- `templates/figma-importer/` holds a working skeleton: `manifest.json` + `code.js`.
- The user installs it once: Figma desktop → Plugins → Development → Import plugin from manifest →
  pick `manifest.json`, then Plugins → Development → the plugin name.
- Coordinates are explicit (no auto-layout) so the result matches the HTML 1:1: header at y=52,
  hero at y=104, section cards at y=286/452/618, nav at y=764 for a 390x844 frame.
- Load fonts defensively (`figma.loadFontAsync` for each weight, catch → fall back to Inter and toast
  which font is missing). A missing font throws and kills the whole plugin run otherwise.
- Gradient text is not a thing; gradient fills are `GRADIENT_LINEAR` with `gradientTransform` and
  `gradientStops`. Icons: `figma.createNodeFromSvg` with an inline SVG string, colour baked into the
  `stroke` attribute (Figma will not inherit `currentColor`).
- Zip the two files and send the zip; state plainly that the resulting link is the user's own file,
  because a link cannot be produced from the server.

**B. Programmatic screen generation via Stitch MCP** (when the ask is "generate screens from a
prompt" rather than "match this spec"):

```python
POST https://stitch.googleapis.com/mcp
headers: Content-Type: application/json, Accept: application/json, text/event-stream,
         X-Goog-Api-Key: <AQ.… key>
body: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}
      {"jsonrpc":"2.0","id":2,"method":"tools/list"}
      {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_projects","arguments":{}}}
```

16 tools: create/get/delete/list projects, list/get screens, `generate_screen_from_text`,
`edit_screens`, `generate_variants`, `download_file` (HTML or screenshot), plus five design-system
tools (`upload_design_md`, `create_design_system`, `apply_design_system`). Responses come back as
JSON-RPC; if the body is SSE, parse the first `data: ` line. Tool results are nested:
`result.content[0].text` is a JSON string.

## Pitfalls

- Do not restyle a locked spec because the reference "looks better" — the numbers were the instruction.
- Do not deliver only a PNG when the user says "in Figma"; a PNG is a preview, the plugin is the asset.
- Check the sample-data fields every revision; names and phone numbers drift silently.
