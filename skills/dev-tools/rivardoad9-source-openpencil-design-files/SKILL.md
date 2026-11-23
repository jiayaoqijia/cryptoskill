---
name: openpencil-design-files
description: Build real .fig design files headlessly via OpenPencil CLI.
---

# OpenPencil headless design files

When Figma's API is blocked or out of MCP quota, produce a genuine `.fig` file by script instead of a screenshot. OpenPencil's `eval` runs the **Figma plugin API** headlessly and persists the file — no desktop app, no login.

## Standing spec for Do's mobile mock screens

Use these numbers unless he states otherwise; he re-checks them every iteration.

| Item | Value |
|---|---|
| Frame | 390 × 844 (iPhone 13) |
| Font | Plus Jakarta Sans |
| Page title | 24 px, ExtraBold |
| Section title | 18 px, SemiBold |
| Body | 14 px, Medium |
| Label / caption | 12 px |
| Card radius | 16 px |
| Side padding | 20 px |
| Icons | 24 × 24, inline SVG, 1.8 stroke |

**Keep one dummy identity across every screen and revision.** He asks for the same person repeatedly and counts drift as a defect: `Graceia` / `+12 3456 789` / avatar `GR`. Do not invent a new name or number per mock, and do not "fix" the number to +62 — it is placeholder data on purpose.

Deliver the `.fig` plus a 2× PNG preview, and QA the PNG by looking at it (bottom-nav overlap, invisible white-on-white chip text, a value printed twice in one row) before sending.

## Setup

```bash
mkdir -p ~/op && cd ~/op && npm init -y && npm i @open-pencil/cli
./node_modules/.bin/openpencil --help
```

Commands: `import`, `eval`, `export`, `info`, `lint`.

## Working recipe

1. Bootstrap an empty document (no `new` command works offline):
   ```bash
   printf '<html><body><div style="width:390px;height:844px"></div></body></html>' > blank.html
   ./node_modules/.bin/openpencil import blank.html -f fig -o base.fig
   ```
2. Write the design as plugin-API JS (frames, text, gradients, `figma.createNodeFromSvg` for icons) in `build.js`, then:
   ```bash
   ./node_modules/.bin/openpencil eval base.fig --stdin -w < build.js
   ```
   Clear the page first (`for (const c of [...page.children]) c.remove()`) and `return {...}` a small summary — the CLI prints the returned JSON.
3. Verify visually: `openpencil export base.fig -f png -s 2 -o check.png`, then actually look at the PNG. `openpencil info base.fig` prints node/font census.
4. Ship the `.fig` plus the PNG preview.

If he specifically wants the screen inside Figma, this file is not enough on its own: Figma's MCP is quota-gated per seat/plan, so check that before promising a canvas write — see `mcp-server-integration`. A `.fig` from this CLI opens in OpenPencil and is importable into Figma, but do not claim the Figma import was verified unless it was.

## Pitfalls (each cost a failed run)

- **`figma.listAvailableFontsAsync()` returns `[]` headless.** Never derive styles from it: `pick()` returns `undefined` and the loader throws `Cannot read properties of undefined (reading 'toLowerCase')`. Hardcode `{family, style}` and `await figma.loadFontAsync` directly — it works for system fonts.
- **Non-default fonts must be installed on the machine**: TTF into `~/.local/share/fonts` + `fc-cache -f`. Family and style must match exactly (`Plus Jakarta Sans`, `SemiBold`, `ExtraBold`).
- **`gradientTransform` must be `{m00,m01,m02,m10,m11,m12}`**, not a 2×3 array — nodes build fine, then encoding fails with `Missing required field "m00"`.
- **Alpha in SOLID fills is dropped** (`{...rgb(hex), a:0.14}` renders opaque, so white text vanishes). Pre-blend to an opaque hex.
- **Do not `import` a finished HTML page.** Absolute layouts collapse, gradients and SVG icons vanish, nav jumps to the top. HTML import is only for bootstrap; fidelity comes from `eval`.
- After a failed save, re-import `blank.html` before retrying — `base.fig` is left half-written.
