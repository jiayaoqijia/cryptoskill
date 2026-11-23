---
name: caption-templates
description: Style captions in Palmier Pro from a fixed catalog of 28 verified presets (Clean Creator, Keyword Yellow, Karaoke Fill, Meme Classic, Documentary, Floating Pill, Marker Highlight, Comic Book POW, Retro VHS, TikTok Meme Bottom Bar, and more) instead of guessing at fonts, colors, sizes, and animations. Use whenever adding, restyling, or choosing a look for captions/subtitles in Palmier Pro — "add captions", "caption this", "subtitles", "make the captions pop", "karaoke captions", "podcast captions", "TikTok-style captions", "change the caption style".
---

# Palmier Pro caption templates

Caption styling is where an agent most easily produces something ugly: it pairs a font with a size that doesn't suit it, picks a neon color that fights the footage, or stacks an outline + background + shadow that no editor would ship. This skill replaces that guesswork with a default. Every value below was read out of a real Palmier project and confirmed against rendered frames.

## Hard rules

1. **Pick exactly one template. Paste its config verbatim.** Do not blend two templates, do not "improve" a color, do not add an outline or background a template doesn't have.
2. **No style at all is a valid answer.** If the user just says "add captions" with no aesthetic intent, call `add_captions` with **no** `style` / `animation` / `transform` — the app's own default is clean and correct. Reach for a template only when the user signals a look ("bold", "podcast", "TikTok", "make them pop", "match my brand", names a vibe).
3. **Match orientation.** Vertical templates are authored for 1080×1920, horizontal for 1920×1080. Using the wrong set gives text that is comically large or unreadably small — see [Porting across canvas sizes](#porting-across-canvas-sizes).
4. **Fonts outside this catalog are fair game — but verify them.** Palmier's font list is far larger than the 13 families used here; this catalog is a curated slice, not the available set. Set whatever font the user asks for. What doesn't change: after setting an unfamiliar font, render a frame with `inspect_timeline` and confirm it actually resolved instead of silently falling back to a default.
5. **Always verify.** After `add_captions` or `update_text`, run `inspect_timeline` on a frame inside the caption range and actually look at it.

## Workflow

```
- [ ] 1. get_timeline — canvas width/height, fps, which track has speech
- [ ] 2. Pick ONE template from the picker below (or none — see rule 2)
- [ ] 3. add_captions with that template's exact block
- [ ] 4. inspect_timeline mid-caption — confirm it renders as described
- [ ] 5. Report the template name you used
```

Restyling captions that already exist? Skip to [Switching a template on existing captions](#switching-a-template-on-existing-captions) — it is **not** just passing the new style.

## Picker

Ask what the video is, not what color the user likes. The left column is the answer to "what is this?"

### Vertical (1080×1920 — Reels / TikTok / Shorts)

| Use it for | Template | Look |
|---|---|---|
| **Default vertical.** Talking head, any topic | **Clean Creator** | White Inter bold, soft shadow, lower-third. Safe everywhere. |
| Punchy retention edit, keyword emphasis | **Keyword Yellow** | Inter bold, active word pops yellow |
| Music / lyric / high-energy | **Karaoke Fill** | Poppins bold, words fill in left-to-right |
| Max energy, big phrases | **Phrase Pop** | Manrope 72 bold, gold word pop |
| Podcast clip, understated | **Minimal Podcast** | Inter on a rounded translucent black pill |
| Podcast clip, modern | **Modern Podcast** | DM Sans bold, sky-blue active word |
| Playful, bouncy | **Bounce** | Poppins 76, word-by-word pop |
| Loud hook / cold open | **Punch Zoom** | Anton 100 ALL CAPS, dead center |
| Meme / reaction | **Meme Classic** | Impact ALL CAPS, thick black outline |
| One word at a time, hypnotic | **One Word** | Inter bold, single word, centered |

### Horizontal (1920×1080 — YouTube / web / landscape)

| Use it for | Template | Look |
|---|---|---|
| **Default horizontal.** Anything | **Podcast Clean Captions** | Helvetica Neue, white, bottom. Invisible in a good way. |
| Broadcast / interview / accessibility | **Documentary** | Arial on a translucent black bar, full sentences |
| Emphasis without shouting | **Number Callout** | Inter bold, active word turns orange |
| Highlighter effect | **Marker Highlight** | Dark text under a sweeping yellow block |
| Clean, designed, brand-safe | **Floating Pill** | Dark text on a white rounded pill |
| Aggressive emphasis | **Shake Emphasis** | Anton CAPS, red word pop |
| Editorial / essay / interview | **Editorial Serif** | Georgia, quiet, no gimmicks |
| Film / trailer / title-card feel | **Cinematic Title** | Avenir CAPS, wide tracking, centered |
| Two-line / translation stack | **Bilingual Stack** | Inter bold, sits higher for a second line |
| Big graphic statement over a backdrop | **Footage Stencil Bold** | 120pt CAPS knocked out of the footage ⚠️ [see gotcha](#gotchas) |
| Tech / terminal / hacker | **Typewriter Terminal** | Green Courier on a black bar, types out |
| Comic / gaming / loud | **Comic Book POW** | Yellow Impact, black outline, hard drop shadow, tilted |
| Ambient, barely-there | **Minimalist Whisper** | Tiny lowercase grey at the very top |
| Retro / VHS / 80s | **Retro VHS** | Cream Courier CAPS with cyan fringe, over+underlined |
| Wedding / luxury / lifestyle | **Elegant Wedding Serif** | Times New Roman, warm cream, tracked out |
| Kids / cartoon / family | **Kids Cartoon Bubbly** | Pink Comic Sans, white outline, purple shadow |
| Reel-style over landscape footage | **Instagram Reel Bold Yellow** | Yellow Helvetica CAPS, black outline, centered |
| Meme bar / hard-cut humor | **TikTok Meme Bottom Bar** | Black CAPS on a solid white bar at the very bottom |

---

# The catalog

Every block below is a complete `add_captions` payload. Copy it whole. Add `trackIndex` only if auto-detection picks the wrong speech track.

Colors follow Palmier's defaults: text `color` omitted = white; `outline.color` / `background.color` / `shadow.color` omitted = black.

## Vertical — 1080×1920

### Clean Creator
White Inter bold in the vertical safe zone. The default for any short-form talking head.

```json
{
  "maxWords": 3,
  "animation": "fadeIn",
  "style": {
    "fontName": "Inter", "fontSize": 64, "bold": true,
    "shadow": { "enabled": true, "blur": 8, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.5 }
  },
  "transform": { "centerY": 0.72 }
}
```

### Keyword Yellow
Same body as Clean Creator, one size up, active word pops yellow. Retention edits.

```json
{
  "maxWords": 3,
  "animation": "popIn",
  "highlightColor": "#FFD900",
  "style": {
    "fontName": "Inter", "fontSize": 70, "bold": true,
    "shadow": { "enabled": true, "blur": 8, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.45 }
  },
  "transform": { "centerY": 0.72 }
}
```

### Karaoke Fill
Words fill in white left-to-right as spoken. Music, lyrics, high tempo.

```json
{
  "maxWords": 3,
  "animation": "wordReveal",
  "highlightColor": "#FFFFFF",
  "style": {
    "fontName": "Poppins", "fontSize": 66, "bold": true,
    "shadow": { "enabled": true, "blur": 0, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.55 }
  },
  "transform": { "centerY": 0.72 }
}
```

### Phrase Pop
Biggest of the vertical body styles, gold word pop. Maximum energy.

```json
{
  "maxWords": 3,
  "animation": "popIn",
  "highlightColor": "#FACC15",
  "style": {
    "fontName": "Manrope", "fontSize": 72, "bold": true,
    "shadow": { "enabled": true, "blur": 10, "offset": { "x": 0, "y": 4 }, "color": "#000000", "opacity": 0.55 }
  },
  "transform": { "centerY": 0.72 }
}
```

### Minimal Podcast
Non-bold Inter on a rounded translucent black pill, sitting low. Understated podcast clips.

```json
{
  "maxWords": 3,
  "style": {
    "fontName": "Inter", "fontSize": 54,
    "background": {
      "enabled": true, "color": "#000000", "opacity": 0.65,
      "cornerRadius": 16, "padding": { "x": 24, "y": 14 }
    },
    "shadow": { "enabled": true }
  },
  "transform": { "centerY": 0.85 }
}
```

### Modern Podcast
DM Sans bold with a sky-blue active word. Cleaner and cooler than Keyword Yellow.

```json
{
  "maxWords": 3,
  "animation": "fadeIn",
  "highlightColor": "#5CC8FF",
  "style": {
    "fontName": "DM Sans", "fontSize": 62, "bold": true,
    "shadow": { "enabled": true, "blur": 0, "offset": { "x": 0, "y": 2 }, "color": "#000000", "opacity": 0.4 }
  },
  "transform": { "centerY": 0.72 }
}
```

### Bounce
Large Poppins with a per-word bounce. Playful, no color accent.

```json
{
  "maxWords": 3,
  "animation": "wordPop",
  "style": {
    "fontName": "Poppins", "fontSize": 76, "bold": true,
    "shadow": { "enabled": true }
  },
  "transform": { "centerY": 0.72 }
}
```

### Punch Zoom
Anton 100 ALL CAPS, dead center, two words at a time, no animation. Cold opens and hooks.

```json
{
  "maxWords": 2,
  "style": {
    "fontName": "Anton", "fontSize": 100, "bold": true, "fontCase": "uppercase",
    "shadow": { "enabled": true }
  }
}
```

### Meme Classic
Impact CAPS with a thick black outline, hard against the bottom. Shadow is deliberately **off**.

```json
{
  "maxWords": 3,
  "style": {
    "fontName": "Impact", "fontSize": 72, "bold": true, "fontCase": "uppercase",
    "outline": { "enabled": true, "width": 9, "color": "#000000" },
    "shadow": { "enabled": false }
  },
  "transform": { "centerY": 0.88 }
}
```

### One Word
One word at a time, centered. Hypnotic pacing; produces ~3.5× as many caption clips.

```json
{
  "maxWords": 1,
  "style": {
    "fontName": "Inter", "fontSize": 52, "bold": true,
    "shadow": { "enabled": true, "blur": 8, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.5 }
  }
}
```

## Horizontal — 1920×1080

### Podcast Clean Captions
Plain white Helvetica Neue at the bottom, no animation. The horizontal default.

```json
{
  "maxWords": 5,
  "style": {
    "fontName": "Helvetica Neue", "fontSize": 40,
    "shadow": { "enabled": true, "blur": 4, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.5 }
  },
  "transform": { "centerY": 0.9 }
}
```

### Documentary
Arial on a translucent black bar, full sentences, hard bottom. Broadcast and accessibility.

```json
{
  "maxWords": 8,
  "style": {
    "fontName": "Arial", "fontSize": 42,
    "background": { "enabled": true, "color": "#000000", "opacity": 0.45 },
    "shadow": { "enabled": true }
  },
  "transform": { "centerY": 0.9 }
}
```

### Number Callout
White Inter bold; the active word recolors orange and scales. Emphasis that stays readable.

```json
{
  "maxWords": 5,
  "animation": "highlightPop",
  "highlightColor": "#FF6B00",
  "style": {
    "fontName": "Inter", "fontSize": 54, "bold": true,
    "shadow": { "enabled": true, "blur": 8, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.5 }
  },
  "transform": { "centerY": 0.8 }
}
```

### Marker Highlight
Dark text with a yellow block sweeping across the active word. ⚠️ Un-highlighted words are `#111111` with no outline — they wash out over light footage. Use Number Callout instead if the plate is bright.

```json
{
  "maxWords": 5,
  "animation": "highlightBlock",
  "highlightColor": "#FFD23F",
  "style": {
    "fontName": "Inter", "fontSize": 52, "bold": true, "color": "#111111",
    "shadow": { "enabled": false }
  },
  "transform": { "centerY": 0.85 }
}
```

### Floating Pill
Near-black text on an opaque white rounded pill. Brand-safe and designed-looking. Shadow **off**.

```json
{
  "maxWords": 5,
  "animation": "popIn",
  "style": {
    "fontName": "Inter", "fontSize": 46, "bold": true, "color": "#1A1A1A",
    "background": {
      "enabled": true, "color": "#FFFFFF", "opacity": 1,
      "cornerRadius": 40, "padding": { "x": 28, "y": 16 }
    },
    "shadow": { "enabled": false }
  },
  "transform": { "centerY": 0.82 }
}
```

### Shake Emphasis
Anton CAPS with a red word pop. The loudest horizontal option.

```json
{
  "maxWords": 5,
  "animation": "wordPop",
  "highlightColor": "#FF2A2A",
  "style": {
    "fontName": "Anton", "fontSize": 62, "bold": true, "fontCase": "uppercase",
    "shadow": { "enabled": true, "blur": 8, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.5 }
  },
  "transform": { "centerY": 0.78 }
}
```

### Editorial Serif
Georgia, not bold, no accent color. Essays, interviews, anything that shouldn't shout.

```json
{
  "maxWords": 5,
  "animation": "fadeIn",
  "style": {
    "fontName": "Georgia", "fontSize": 50,
    "shadow": { "enabled": true, "blur": 0, "offset": { "x": 0, "y": 2 }, "color": "#000000", "opacity": 0.4 }
  },
  "transform": { "centerY": 0.82 }
}
```

### Cinematic Title
Avenir CAPS with wide tracking, centered, static. Reads as a title card rather than a caption.

```json
{
  "maxWords": 3,
  "style": {
    "fontName": "Avenir", "fontSize": 48, "fontCase": "uppercase", "tracking": 8,
    "shadow": { "enabled": true }
  }
}
```

### Bilingual Stack
Plain Inter bold sitting higher than a normal lower-third, leaving room for a translation line beneath.

```json
{
  "maxWords": 5,
  "animation": "fadeIn",
  "style": {
    "fontName": "Inter", "fontSize": 54, "bold": true,
    "shadow": { "enabled": true, "blur": 8, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.5 }
  },
  "transform": { "centerY": 0.74 }
}
```

### Footage Stencil Bold
120pt CAPS knocked out of the layers below. ⚠️ **Requires a distinct backdrop under the caption track** — over the same footage it renders invisible. `get_timeline` does not report `fillMode`, so it reads back looking like an ordinary group.

```json
{
  "maxWords": 5,
  "animation": "wordPop",
  "style": {
    "fontName": "Inter", "fontSize": 120, "bold": true, "fontCase": "uppercase", "tracking": -2,
    "outline": { "enabled": true, "width": 10, "color": "#000000" },
    "shadow": { "enabled": false }
  }
}
```

Then, in a second call, switch the group to stencil fill:

```json
{ "captionGroupId": "<from add_captions>", "fillMode": "footage" }
```

### Typewriter Terminal
Terminal green Courier, lowercase, typing out on a near-black bar. Tech and dev content.

```json
{
  "maxWords": 8,
  "animation": "typewriter",
  "style": {
    "fontName": "Courier New", "fontSize": 42, "fontCase": "lowercase", "color": "#33FF66",
    "background": {
      "enabled": true, "color": "#0A0A0A", "opacity": 0.85,
      "cornerRadius": 0, "padding": { "x": 32, "y": 18 }
    }
  },
  "transform": { "centerY": 0.85 }
}
```

### Comic Book POW
Yellow Impact CAPS, heavy black outline, hard offset drop shadow, tilted 4° and sitting high. Gaming and comedy.

```json
{
  "maxWords": 5,
  "animation": "wordPop",
  "style": {
    "fontName": "Impact", "fontSize": 96, "bold": true, "fontCase": "uppercase", "color": "#FFDE00",
    "outline": { "enabled": true, "width": 12, "color": "#111111" },
    "shadow": { "enabled": true, "blur": 0, "offset": { "x": 6, "y": 6 }, "color": "#111111", "opacity": 1 }
  },
  "transform": { "centerY": 0.45, "rotation": -4 }
}
```

`fontSize` reads back near 95.98 — Palmier auto-fits long captions. Author 96.

### Minimalist Whisper
Tiny lowercase grey at 80% opacity, parked at the top of frame. Ambient; not for accessibility.

```json
{
  "maxWords": 5,
  "animation": "fadeIn",
  "style": {
    "fontName": "Inter", "fontSize": 30, "fontCase": "lowercase", "tracking": 3,
    "color": "#EAEAEACC",
    "shadow": { "enabled": false }
  },
  "transform": { "centerY": 0.1 }
}
```

### Retro VHS
Cream Courier CAPS with a cyan chromatic fringe offset left, over- and underlined, top of frame.

```json
{
  "maxWords": 5,
  "style": {
    "fontName": "Courier New", "fontSize": 44, "fontCase": "uppercase", "tracking": 4,
    "color": "#FFF8E7", "underline": true, "overline": true,
    "shadow": { "enabled": true, "blur": 0, "offset": { "x": -3, "y": 0 }, "color": "#00E5FF", "opacity": 0.8 }
  },
  "transform": { "centerY": 0.12 }
}
```

### Elegant Wedding Serif
Times New Roman in warm cream with light tracking, low in frame. Weddings, luxury, lifestyle.

```json
{
  "maxWords": 5,
  "animation": "fadeIn",
  "style": {
    "fontName": "Times New Roman", "fontSize": 44, "tracking": 2, "color": "#F5EFE0",
    "shadow": { "enabled": true, "blur": 0, "offset": { "x": 0, "y": 3 }, "color": "#000000", "opacity": 0.4 }
  },
  "transform": { "centerY": 0.88 }
}
```

### Kids Cartoon Bubbly
Pink Comic Sans with a white outline and a purple hard shadow; active word goes orange.

```json
{
  "maxWords": 5,
  "animation": "wordPop",
  "highlightColor": "#FF7A00",
  "style": {
    "fontName": "Comic Sans MS", "fontSize": 66, "bold": true, "color": "#FF5FA2",
    "outline": { "enabled": true, "width": 8, "color": "#FFFFFF" },
    "shadow": { "enabled": true, "blur": 0, "offset": { "x": 4, "y": 4 }, "color": "#7A2E8C", "opacity": 1 }
  },
  "transform": { "centerY": 0.72 }
}
```

### Instagram Reel Bold Yellow
Yellow Helvetica CAPS with a thin black outline, centered. Reel energy on a landscape canvas. Shadow **off**.

```json
{
  "maxWords": 5,
  "animation": "popIn",
  "style": {
    "fontName": "Helvetica Neue", "fontSize": 72, "bold": true, "fontCase": "uppercase",
    "tracking": -1, "color": "#FFE600",
    "outline": { "enabled": true, "width": 5, "color": "#000000" },
    "shadow": { "enabled": false }
  }
}
```

### TikTok Meme Bottom Bar
Black CAPS on a solid white bar pinned to the very bottom. Hard-cut meme humor.

```json
{
  "maxWords": 5,
  "style": {
    "fontName": "Helvetica Neue", "fontSize": 46, "bold": true, "fontCase": "uppercase",
    "color": "#000000",
    "background": {
      "enabled": true, "color": "#FFFFFF", "opacity": 1,
      "cornerRadius": 0, "padding": { "x": 16, "y": 6 }
    },
    "shadow": { "enabled": false }
  },
  "transform": { "centerY": 0.95 }
}
```

---

## Parameter reference

**`maxWords` is the density dial** and the single biggest driver of feel. Palmier still breaks on natural pauses, so it is a cap, not a quota.

| maxWords | Feel | Templates |
|---|---|---|
| 1 | One word at a time, hypnotic | One Word |
| 2 | Rapid-fire | Punch Zoom |
| 3 | Standard vertical / short-form | all vertical, Cinematic Title |
| 5 | Standard horizontal | most horizontal |
| 8 | Full sentences, broadcast | Documentary, Typewriter Terminal |

**`animation`** — `fadeIn` (safe, default), `popIn`, `slideUp`, `typewriter`, `wordReveal` (karaoke fill), `wordSlide`, `wordPop` (per-word bounce), `wordCycle`, `highlightPop` (active word recolors + scales), `highlightBlock` (active word gets a colored block behind it), `off`. Word-timed presets read the transcript, so they cost nothing extra. `highlightColor` only does anything with `wordReveal`, `wordPop`, `highlightPop`, `highlightBlock`, and the `popIn`/`fadeIn` variants that carry one.

**`transform.centerY`** — 0 = top, 1 = bottom. Omitting it centers at 0.5. The catalog's positions:

| centerY | Zone | Templates |
|---|---|---|
| 0.10–0.12 | Top overlay | Minimalist Whisper, Retro VHS |
| 0.45–0.50 | Dead center | Punch Zoom, Cinematic Title, Footage Stencil Bold, Comic Book POW, Instagram Reel Bold Yellow, One Word |
| 0.72–0.74 | Vertical safe zone (above UI chrome) | most vertical, Bilingual Stack |
| 0.78–0.85 | Standard lower-third | Shake Emphasis, Editorial Serif, Floating Pill, Marker Highlight, Number Callout, Minimal Podcast, Typewriter Terminal |
| 0.88–0.95 | Hard bottom | Meme Classic, Documentary, Elegant Wedding Serif, Podcast Clean Captions, TikTok Meme Bottom Bar |

**Color defaults, so you know what "omitted" means:** text `color` defaults to **white**, `outline.color` and `background.color` and `shadow.color` default to **black**. `shadow.enabled` defaults to false — a shadow block with blur and offset but no `enabled: true` renders nothing.

**Sizes are canvas points**, where the canvas equals the project's pixel dimensions. Every number in this catalog is authored for a 1080-line canvas.

### Porting across canvas sizes

- **Same orientation, different resolution (4K, 720p):** multiply `fontSize`, `outline.width`, `shadow.blur`, `shadow.offset`, `background.padding`, and `background.cornerRadius` by `targetHeight / 1080`. `centerY`, `tracking`, and opacities are already normalized — leave them.
- **Vertical template on a horizontal project (or vice versa):** don't. Pick the equivalent from the other table. The two sets are tuned differently on purpose — vertical runs 54–100pt on a 1080-wide canvas, horizontal runs 30–72pt on a 1920-wide one.

## Switching a template on existing captions

`update_text` is a **partial patch** — omitted properties keep their old values. Switching from a template with an outline to one without leaves the outline on. Always explicitly clear what the outgoing template set:

```json
{
  "captionGroupId": "<from get_timeline>",
  "animation": "off",
  "fillMode": "color",
  "style": {
    "color": "#FFFFFF", "tracking": 0, "fontCase": "mixed",
    "bold": false, "italic": false, "underline": false, "overline": false,
    "outline": { "enabled": false },
    "background": { "enabled": false },
    "shadow": { "enabled": false }
  }
}
```

Send that reset first, then the new template's `style` / `animation` / `transform` in a second call. Two calls, reliably correct, beats one call that half-applies.

`maxWords` cannot be changed by `update_text` — it decides how the transcript was split. To change caption density you must delete the caption clips and re-run `add_captions`.

## Gotchas

- **Footage Stencil Bold renders invisible over a single video layer.** It uses `fillMode: "footage"`, which knocks the letters out of whatever is *below* — with the same footage below, the result is pixel-identical to the footage. It needs a distinct backdrop (a color matte, a blurred copy, a b-roll layer) beneath the caption track. Also note `get_timeline` does **not** report `fillMode`, so a stencil group looks like an ordinary one when you read it back.
- **Marker Highlight only reads on the highlighted word.** Its base text is `#111111` with no outline; over light footage the un-highlighted words nearly disappear. That is the intended effect, but confirm the footage is dark enough — otherwise use Number Callout, which keeps the base text white.
- **`shadow.enabled` is easy to lose.** Several catalog templates carry shadow blur/offset values with the shadow switched *off* (Meme Classic, Floating Pill, Marker Highlight, Footage Stencil Bold, Minimalist Whisper, Instagram Reel Bold Yellow, TikTok Meme Bottom Bar). Copy `enabled` exactly; don't assume a shadow block means a visible shadow.
- **`get_timeline` omits anything at its default.** Reading a group back and seeing no `color` means white, not "unset". Don't round-trip a read into a write and expect fidelity — write from this catalog.
- **`fontSize` may come back fractional** (e.g. 95.977 instead of 96). Palmier auto-fits the box for long captions. Author the round number; ignore the drift on read.

## Expanding beyond the catalog

When the user wants something not in the catalog, **start from the nearest template and change one axis**, keeping everything else:

| User asks | Change |
|---|---|---|
| "brand colors" | `style.color` and/or `highlightColor` only |
| "bigger" / "smaller" | `fontSize` only, ±20% steps |
| a specific font | `style.fontName` only — then `inspect_timeline` to confirm it resolved, and re-tune `fontSize` if the new face runs wider or narrower |
| "higher" / "lower" | `transform.centerY` only, ±0.05 steps |
| "more/less energy" | swap `animation` within the same family (`fadeIn` ↔ `popIn` ↔ `wordPop`) |
| "tighter" / "looser" captions | `maxWords`, and re-run `add_captions` |
| "add a background" | copy the `background` block from Minimal Podcast, Documentary, Floating Pill, Typewriter Terminal, or TikTok Meme Bottom Bar wholesale |

Changing two or more axes at once is how captions get ugly. If the user's request genuinely needs a new look, build it, then `inspect_timeline` and show them the frame before moving on.
