# Figma → Stitch fidelity pipeline

Goal: rebuild the screens of a Figma file in Stitch at the user's exact tokens, without
the model guessing layout or copy.

## 1. Inventory first

```bash
# pages + top frames, cheap
curl -s -H "X-Figma-Token: $PAT" \
  "https://api.figma.com/v1/files/<KEY>?depth=2" > file_depth2.json
```

Pick the canvas the user linked (node id in the URL). A file often holds a newest canvas plus
older copies (`Revisi`, `Scroll`) with the same screens — rebuild from the newest, and say which
canvas you used.

## 2. Tokens from the design, not from taste

Walk one dense frame and aggregate `fills[].color`, `style.fontFamily`, `style.fontWeight`,
`style.fontSize`. That gives the real palette and type scale; reconcile it with the user's written
spec (they usually restate the type sizes they want enforced).

## 3. The rasterized-text trap

Frames imported from HTML screenshots carry their labels as images: a content-heavy settings screen
can expose ~11 TEXT nodes while showing 40 labels. Consequences:

- Counting or reading TEXT nodes is not a complete content inventory.
- Export each frame as PNG (`/v1/images?ids=...&format=png&scale=2`, five ids per call) and read the
  pixels to recover copy, icon shapes and states.
- Never invent a label from a layer name; if the pixels are unreadable, ask or mark it unknown.

## 4. Build the HTML per screen

One self-contained document per frame:

- `body { width: 390px }`, content scrolling vertically, status bar 44 px, home indicator 34 px.
- Tokens in `:root` custom properties; type roles as fixed classes (page 24/700, section 18/600,
  body 14/400, label 12/500).
- Cards radius 16, page padding 20, icons 24 with 1.75 stroke.
- Draw the states: checkbox checked and empty, switch on/off, radio selected, buttons
  default/pressed/disabled/loading, field empty/filled/focus/error, badges success/pending/failed.
- Keep money formatting (`Rp1.250.000`) and the original language.

## 5. Push and verify

`generate_screen_from_text` creates the screen; `update_screen` with `htmlCodeBase64` replaces its
HTML with yours. Then render the screenshot and look at it — the HTML you sent is the design, so a
visual check catches overflow, clipped bottoms and missing icons that JSON never shows.

## 6. Order of work that survives review

1. Project + link to the user.
2. DESIGN.md uploaded.
3. One screen end-to-end (generate → push HTML → screenshot) as a proof of pipeline.
4. Remaining screens in batches of a few, iterating only after the first batch looks right.
