---
name: figma-design-review
description: Use when a Figma link must become a review or deck.
version: 1.0.0
author: Nous Research
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [figma, design-review, decks, ux]
    category: creative
    related_skills: [powerpoint, ui-ux-pro-max, design-md]
---

# Figma design review

Turning a Figma link into something you can actually reason about: a critique, a deck, or a
build spec. The hard part is rarely the critique — it is getting clean per-frame pixels when the
file is view-only or the API is rate-limited.

## When to use

- "Ini desain gw, bikin PPT / review / implementasi dari sini."
- Any Figma URL with `design/` or `file/` plus an optional `node-id`.
- You need frame names, colours, copy, or layout measurements out of a design file.

## Decide the access path FIRST

Do this before writing a single line of the deliverable; the deliverable's quality is capped by
asset quality, and the wrong route burns a dozen tool calls.

| Access you have | Route |
|---|---|
| File owner / editor | Figma MCP tools (`whoami` → `get_metadata` → `get_design_context` / `get_screenshot`) |
| MCP returns a plan/quota error | Do not plan around MCP. Use the REST API with a PAT (below) |
| Viewer via public link | Browser + canvas screenshots for layout, then ask for a PDF export for per-frame detail |
| Nothing but the URL | Ask for either a page PDF export or a read-only PAT — one message, both options |

A Figma personal access token with only `file_content:read` unlocks everything headlessly:

```bash
curl -s -H "X-Figma-Token: $FIGMA_PAT" \
  "https://api.figma.com/v1/files/$KEY/nodes?ids=49:2&geometry=paths"   # structure + text
curl -s -H "X-Figma-Token: $FIGMA_PAT" \
  "https://api.figma.com/v1/images/$KEY?ids=1:2,1:3&format=png&scale=2"  # per-frame renders
```

`node-id=49-2` in a URL is the same node as `49:2` in the API — swap the dash for a colon.

Two export details that waste a round-trip if you miss them:

- `/v1/images` takes **at most 10 ids per call** — batch in tens and read the returned `images` map
  (a null entry means that node failed, not that the token is bad).
- Every node carries `characters`, so one `nodes?ids=<page>` dump gives you structure *and* the exact
  copy of all screens at once. Quote captions from that, never from what a screenshot looks like it says.
- Store the PAT in a mode-600 file (`~/.hermes/secrets/figma_pat`, 46 bytes) and read it per call; it is
  never printed back into chat.

## Browser route (public link, view-only)

1. **Override the user agent before navigating.** The default headless UA gets served a
   CloudFront block page on `figma.com`, while `curl` from the same host returns 200 — so the
   block is fingerprint-based, not network-based.

   ```python
   cdp('Network.setUserAgentOverride',
       userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
       acceptLanguage='en-US,en;q=0.9', platform='MacIntel')
   ```

2. **The canvas is one `<canvas>`.** `document.body.innerText` yields only the chrome; frame names
   and labels come from pixels, so screenshot + `vision_analyze`, never DOM scraping.
3. **Zoom through the menu, not the keyboard.** Figma's canvas swallows synthetic key events; the
   only reliable control is the zoom widget (aria-label like `"5%, zoom and view options"`), whose
   menu contains `Zoom to 50%`, `Zoom to 100%`, `Zoom to fit`. Programmatic ctrl+wheel overshoots
   (5% → 25600% in six steps).
4. **Dismiss the sign-up banner first** — it covers the bottom ~110px of the canvas.
5. **Pan with middle-button drag** (`Input.dispatchMouseEvent`, `button='middle'`, `buttons=4`),
   not with space-drag.

View-only gets you layout and hierarchy. It does not get you a clean per-frame render: at zoom-to-fit
frames are ~20px wide, and at 50% they are readable for structure but not for copy. **Don't sweep
the canvas hoping to reconstruct 20 screens from screenshots** — ask for the PDF/PAT.

## Reviewing what you got

For each frame record: purpose, primary action, states shown, and what is missing (empty, error,
loading, permission). A deck built from this reads as a design critique; one built from admiration
("clean, modern") reads as filler.

- Name screens by their frame label, not by guesswork.
- Note inconsistencies across frames (button radius, spacing scale, one screen with a different
  header) — that is the content a group presentation actually needs.
- Keep the original palette: pull hex values from the frames you were given. Do not restyle the
  designs in the deck.
- Deck copy stays plain: headline = the screen's frame label, annotation = one short fact, and never
  a sentence about the file or the process. Claim headlines and "X, bukan Y" framing read as AI.
  Voice rules and the deck recipe live in the `powerpoint` skill (screenshot-deck reference, §4).

## Pitfalls

- `node-id` in a shared URL usually points at the *page*, not a frame; a page render shows every
  screen scaled down, which is useless for reading copy.
- Presentation/`proto` mode only works when the file has prototype links; otherwise clicking
  Present does nothing.
- Signed-out viewers have no Export button — if the UI has `Sign up to comment` in the corner,
  stop looking for export.
- The Figma MCP tools are plan-metered; a `whoami` that succeeds says nothing about whether
  `get_metadata` will. Test the smallest call first.
- **Frames do not share an aspect ratio.** One page mixes scrolling screens (≈0.29), ordinary screens
  (≈0.50) and modal boards (≈0.44), and each export comes back at the scale that frame was drawn at.
  Placing them in a row at equal height produces wildly unequal widths that read as broken layout;
  normalise to a fixed device frame (cover-scale + centre-crop to 390×844) or place by width instead;
  the deck-side recipe is the screenshot-deck reference inside the `powerpoint` skill.
