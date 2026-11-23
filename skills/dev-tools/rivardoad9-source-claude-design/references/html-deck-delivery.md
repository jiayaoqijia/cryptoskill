# Building and delivering an HTML deck

Use when the user wants a presentation: a deck designed from scratch, or a PPTX that has to become HTML. Covers canvas, vertical rhythm, fonts, export to PDF/PPTX, serving, and visual verification.

## 1. Shape of the artifact

One self-contained `.html` file: inline CSS + inline JS + the data as a JSON block
(`<script id="payload" type="application/json">__DATA__</script>`), then inject the real JSON with a
5-line python step so the build stays reproducible and the data is never hand-typed.

- Desktop: a fixed 1920x1080 `#stage` scaled with `transform: scale(min(vw/1920, vh/1080))`, one slide
  visible at a time, nav by arrow keys / dots / swipe.
- Phone: **never** rely on that scale (390px viewport => 5px type). Add a `@media (max-width:900px)`
  branch that turns the stage static and stacks the slides vertically with their own px type scale.
  A deck opened from Telegram is nearly always opened on a phone.
- Deep links: `location.hash = '#' + (i+1)` in the nav function plus a `hashchange` listener. This also
  makes headless screenshots of individual slides possible.
- Charts: SVG built in JS from the embedded data, `viewBox` + `width:100%` so they scale in both modes.

## 2. Serving it

Loopback-only stdlib server on a spare port (8787-8799 on this box) behind a `cloudflared tunnel --url`
quick tunnel, and serve the deck only under `/d/<random slug>` (404 everything else) because decks carry
the user's positions. Local verification is not enough: this host's resolver cannot resolve
`*.trycloudflare.com` at all, so verify the public URL with a DoH lookup plus an explicit edge IP:

```
curl -s 'https://1.1.1.1/dns-query?name=HOST&type=A' -H 'accept: application/dns-json'
curl -s -o /dev/null -w '%{http_code}' --resolve HOST:443:EDGE_IP https://HOST/d/SLUG
```

`200` plus the byte count matching the local file proves the tunnel really serves the final build.

## 3. Verify the looks, do not assume them

A structural check (slide count, no JS errors) says nothing about whether it is ugly. Loop:

1. Playwright screenshots at 1600x900 and at an iPhone-ish 390x844 (also assert
   `document.documentElement.scrollWidth <= innerWidth`).
2. Read them with the vision tool, ask for concrete flaws, fix, re-shoot. Crop (`region=`) to inspect
   the small stuff instead of paying for a whole-slide read twice.

For a full deck, review in two passes. First a contact sheet — one image, all slides:

```python
from PIL import Image
import glob
files = sorted(glob.glob("hi/s*.png")); w, h = 480, 270
sheet = Image.new("RGB", (4*w+50, 6*h+70), "#222")
for i, f in enumerate(files):
    sheet.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS),
                (10 + (i % 4)*(w+10), 10 + (i // 4)*(h+10)))
sheet.save("contact.png")
```

Ask which slide numbers look off; that finds the top-heavy, half-empty and overflow slides for one
vision call instead of twenty-four. Then read only the flagged slides full size. The flaws this catches every time: duplicate slide numbers (in-slide footer plus a HUD counter),
label collisions in narrow SVG viewBoxes (a caption wider than 520 units renders cut off),
gridlines drawn in the near-black line colour (invisible), "n lines" Monte Carlo fans that read as
fog (use a p5-p95 polygon + a median line instead), and claims the chart itself contradicts
("the only loser" while three bars are red).

## 4. Pitfalls

- Editing HTML through a python string: `'\\u2014'` lands in the file as a literal `\u2014` and shows up
  as text. Only escapes inside `<script>` get interpreted; in markup write the real character.
- `write_file` refuses to overwrite a file this session has not read; run the build script through
  `execute_code`/terminal instead of rewriting the artifact by hand.
- Do not launch servers or tunnels with `nohup`/`setsid` from the terminal tool; start them as tracked
  background processes, then verify readiness separately.
- Long cloudflared log lines dump every inherited environment variable, so a key exported globally can
  surface in a log file. Keep secrets in a `.env` the app reads, not in the shell environment.

## 5. From-scratch deck: canvas, rhythm, chrome

- Fixed canvas (1600x900 or 1920x1080) with `transform: scale(min(vw/W, vh/H))` on a `#stage`,
  `transform-origin: top left`, centred by flex. One slide visible at a time.
- Tokens in `:root`: paper, ink, muted, line, plus two or three accents, and `--pad-x/--pad-top/--pad-bottom`.
  Pick the type pairing from the subject and the reference material, not Inter by reflex.
- Three blocks per content slide: title group, content, one-line takeaway. `.pad{display:flex;
  flex-direction:column;justify-content:space-between}` distributes them; without the third block the
  content stops a third of the way up and the slide looks unfinished.
- When the content is genuinely short, give the content block `margin-top:auto` so the whitespace sits
  under the title as a deliberate pause instead of a caption floating alone at the bottom.
- Inject chrome from JS: a section label top-left, the slide title and `NN / NN` bottom. Do not also
  put a per-slide kicker in the markup with the same words; the duplicate reads as a bug. Keep a
  `SECTION[i]` array in the JS and skip injection entirely for `.divider` slides.
- Deep links (`#7`) double as deterministic screenshot targets.

## 6. Fonts and headless rendering

Self-host the fonts so a render never waits on a CDN:

```bash
curl -s -A "Mozilla/5.0" "https://fonts.googleapis.com/css2?family=Archivo:wght@400..900&family=Inter:wght@300..700&family=Instrument+Serif:ital@1" -o fonts/fonts.css
grep -o 'https://fonts.gstatic.com/[^)]*' fonts/fonts.css | sort -u   # download each woff2, then rewrite the css to local paths
```

Render with the Playwright chromium cache when the system has no Chrome:

```bash
CHROME=~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome
$CHROME --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --hide-scrollbars \
  --window-size=1600,900 --force-device-scale-factor=2 --virtual-time-budget=1600 \
  --screenshot=hi/s07.png "file:///path/index.html#7"
```

Verify the cover, one dense slide and the closing slide before batch-rendering all of them.

## 7. PDF and PPTX export

```python
import glob, pymupdf
from pptx import Presentation
from pptx.util import Inches

files = sorted(glob.glob("hi/s*.png"))            # 3200x1800, device_scale_factor=2
doc = pymupdf.open()
for f in files:
    page = doc.new_page(width=960, height=540)     # 13.333x7.5 in at 72 dpi
    page.insert_image(pymupdf.Rect(0, 0, 960, 540), filename=f)
doc.save("Deck.pdf", deflate=True, garbage=3)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]
for f in files:
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(f, 0, 0, width=prs.slide_width, height=prs.slide_height)
prs.save("Deck.pptx")
```

- Page size 960x540 pt matches a 16:9 canvas exactly, so the PDF has no letterboxing.
- Keep a `build.py` with a `--shoot` flag and import playwright inside that branch, so assembling
  PDF/PPTX from existing screenshots works even where playwright is not importable.
- python-pptx takes a full-bleed picture per slide; that is the trade for exact fidelity. Tell the user
  the text is not editable in the PPTX and point them at the HTML if they want changes.

## 8. Source fidelity when the deck presents someone else's material

- A scanned source has no text layer: render at 300 dpi and OCR it, then verify every figure by
  cropping its word box at 2x and reading it again (see `ocr-and-documents`). Do not build a stat
  slide from a single full-page OCR pass.
- Quotes stay in the original language, serif italic, with publication and page; body copy is
  translated. If a slide feels thin, cut a slide rather than invent a number.
- When the user supplies a style reference, extract its grammar from the rendered pages before
  designing: background, alignment, typeface count, accent count, words per slide, focal element.
  Match those invariants; do not import a design language the reference never had. Copy posture,
  never a proprietary layout.

## 9. Archetypes that go thin

Every layout must survive its emptiest version — one short line, one icon, no body. If that version
looks unfinished, the template is wrong, not the content.

- **Split slide with an icon-only column.** A 120px icon floating in a 500px column reads as a blank
  slide. Give that column a full-height tinted panel (pale accent background, icon + short uppercase
  label + one-line caption) so its mass balances the text side.
- **Quote slide on plain white.** A centered pull quote alone reads as empty. Put a full-bleed pale
  tint behind it and keep the attribution inside the same block; one tinted slide in a white deck also
  gives the middle of the deck a beat.
- **Three-line story slides.** Centered paragraphs of unequal length look ragged. Use a 3-column grid
  with a 2px accent rule above each line (`.steps`) and equalize the line lengths; the rule supplies
  structure without adding decoration.
- **Divider versus page number.** The giant section numeral and the `NN / NN` footer compete in the
  same corner. Move the numeral to the opposite side or below the fold, and flip the footer to white
  on the accent background.
- **Progress bars print as chrome errors.** A 1–2px `#bar` at the viewport top shows up in every
  screenshot as a stray line over the slide edge. Drop it (`#bar{display:none}`) unless it is part of
  the design.
- **Footer duplication.** Auto-injected section label plus a per-slide kicker saying the same words
  reads as a bug; pick one source of that text.
