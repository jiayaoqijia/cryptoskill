---
name: powerpoint
description: Build, read, edit .pptx decks and report layouts.
version: 1.1.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pptx, powerpoint, presentations, slides, office, python-pptx]
    category: productivity
    related_skills: [docx, xlsx, pdf]
---

# Powerpoint Skill

Create, inspect, and edit PowerPoint (.pptx) presentations using the
python-pptx library. Five helper scripts cover deck creation from a JSON
spec, structured read-back, in-place edits, template-driven brand decks,
and slide rendering — all offline, no PowerPoint installation required.

## When to Use

- The user asks to build a slide deck, report presentation, or pitch deck.
- You need to extract text, notes, tables, chart data, or images from a
  .pptx someone shared.
- You need to update an existing deck: replace text, refresh or patch
  chart data, swap a logo, duplicate/remove/reorder slides, set
  backgrounds, footers, hyperlinks, or speaker notes.
- You must produce an on-brand deck from a company .pptx template.
- Do NOT use this for .ppt (legacy binary) files — convert them first with
  `soffice --convert-to pptx old.ppt` if LibreOffice is available.

## Prerequisites

- Python 3.10+ with `python-pptx` installed
  (`pip install python-pptx`).
- Optional: LibreOffice (`soffice`) plus poppler (`pdftoppm` or
  `pdftocairo`) for rendering slides to PNGs and for PDF export.
  `pptx_render.py` detects both with `shutil.which` and degrades
  gracefully (reports `{"rendered": false, "missing": [...]}`, exit 0)
  when absent — all create/read/edit operations work without them.
- Check availability via `terminal`:
  `python -c "import pptx; print(pptx.__version__)"` and `which soffice pdftoppm`.
- Host note (this box): the Hermes venv has NO python-pptx; use
  `~/.hermes/tools/pptx-venv/bin/python` (3.12, python-pptx 1.0.2, made with `uv venv` +
  `uv pip install --python ...`). `soffice` IS installed here; `pdftoppm`/`pdftocairo` often
  are not. Install the rasterizer once into that venv:
  `uv pip install --python ~/.hermes/tools/pptx-venv/bin/python pymupdf`, then render
  `soffice --headless --convert-to pdf --outdir ./out deck.pptx` and page→PNG with PyMuPDF
  (`fitz.open(pdf)[i].get_pixmap(dpi=110).save(...)`) so each slide can go through
  `vision_analyze`. Never skip the visual check on the assumption that rendering is impossible.

## How to Run

All scripts live in `scripts/`, take `--help`, print JSON to stdout, and
exit non-zero on failure. Run them with `terminal`:

```bash
python scripts/pptx_create.py deck.json out.pptx
python scripts/pptx_read.py deck.pptx --outline      # full JSON outline
python scripts/pptx_read.py deck.pptx --notes        # speaker notes
python scripts/pptx_read.py deck.pptx --images ./img # export pictures
python scripts/pptx_edit.py deck.pptx --replace-text "Old Corp" "New Corp"
python scripts/pptx_edit.py deck.pptx --chart-data update.json
python scripts/pptx_edit.py deck.pptx --duplicate-slide 2
python scripts/pptx_edit.py deck.pptx --remove-slide 3 --move-slide 2 0
python scripts/pptx_from_template.py brand.pptx out.pptx --values vals.json
python scripts/pptx_render.py deck.pptx --outdir ./render  # slide PNGs
```

Author JSON specs with `write_file`; inspect script output and generated
JSON with `read_file`.

## Quick Reference

| Task | Command |
|---|---|
| New deck from spec | `pptx_create.py spec.json out.pptx` |
| 16:9 vs 4:3 | `"slide_size": "16:9"` or `"4:3"` in the spec |
| Outline as JSON | `pptx_read.py deck.pptx --outline` |
| Export images | `pptx_read.py deck.pptx --images DIR` |
| Replace text | `pptx_edit.py deck.pptx --replace-text OLD NEW` |
| Replace chart data | `pptx_edit.py deck.pptx --chart-data spec.json` |
| Patch one series | same flag, spec with `"ops"` (see below) |
| Swap picture | `pptx_edit.py deck.pptx --swap-image N NAME new.png` |
| Duplicate slide | `pptx_edit.py deck.pptx --duplicate-slide N` |
| Remove slide | `pptx_edit.py deck.pptx --remove-slide N` |
| Reorder slide | `pptx_edit.py deck.pptx --move-slide FROM TO` |
| Slide background | `pptx_edit.py deck.pptx --set-background N RRGGBB` |
| Hyperlink runs | `pptx_edit.py deck.pptx --hyperlink N TEXT URL` |
| Slide number on | `pptx_edit.py deck.pptx --enable-slide-number N` |
| Footer text | `pptx_edit.py deck.pptx --set-footer N TEXT` |
| Set notes | `pptx_edit.py deck.pptx --set-notes N TEXT` |
| Append notes | `pptx_edit.py deck.pptx --append-notes N TEXT` |
| Fill template | `pptx_from_template.py tpl.pptx out.pptx --values v.json` |
| Render slide PNGs | `pptx_render.py deck.pptx --outdir DIR` |

## Procedure

### 1. Create a deck

Write a JSON spec (see `pptx_create.py --help` for the full format), then
run `pptx_create.py`. Per slide you can set: `layout` (title,
title_content, section, two_content, title_only, blank), `title`,
`subtitle`, `bullets` (strings, or dicts with `level` 0-4, `size` pt,
`bold`, `italic`, `font`, `color` hex, `link` URL for a hyperlink),
`background` (solid hex), `footer` (text; enables the layout's footer
placeholder), `slide_number` (true; enables the layout's slide-number
placeholder), `images` (path + left/top/width/height in inches), `tables`
(`rows` as list-of-lists), `shapes` (rectangle, rounded_rectangle, oval,
diamond, right_arrow, chevron, with `fill` hex + optional `text`),
`charts` (bar, bar_h, line, pie with `categories` + `series`), and
`notes` (speaker notes).

### 2. Read a deck

`pptx_read.py deck.pptx --outline` returns slide size, layout inventory,
and per slide: layout name, all shape texts, table cells, image inventory
(filename/ext/bytes), chart categories/series/values, and speaker notes.
Use `--images DIR` to dump embedded pictures to files, then
`vision_analyze` on any exported image if you need to see its content.

### 3. Edit a deck

`pptx_edit.py` combines operations in one pass; use `--output` to keep the
original. Text replacement scans slide shapes, table cells, and notes.
Image swap retargets the picture's relationship id so position and size
are preserved. Slide removal drops the relationship and the `<p:sldId>`
entry; reorder moves the `<p:sldId>` element within `<p:sldIdLst>`
(python-pptx has no public API for either — the script does the XML-level
work). `--duplicate-slide N` appends an independent deep copy of slide N:
shape XML plus image/media/hyperlink relationships are cloned and rIds
remapped, so editing the copy never touches the original. Chart slides
are refused (see Pitfalls). `--set-notes`/`--append-notes` edit speaker
notes; `--set-background`, `--hyperlink`, `--enable-slide-number`, and
`--set-footer` handle deck polish.

Chart updates take a JSON spec via `--chart-data`. Full replace:
`{"slide": 0, "chart": 0, "categories": [...], "series": {...}}`. For
surgical edits, pass `"ops"` instead — a list of
`{"op": "update_series", "name": ..., "values": [...]}`,
`add_series`, `remove_series`, `rename_category` (`from`/`to` or
`index`), and `set_title`. python-pptx can only swap a chart's entire
dataset (`replace_data`), so ops are implemented as read-existing →
modify → replace; the per-part UX is a wrapper, and any chart data not
expressible as categories + numeric series will be normalized by the
round-trip.

### 4. Build from a template

`pptx_from_template.py` opens a brand .pptx, replaces every
`{{token}}` from a values JSON across slides/tables/notes, and can append
new slides that use the template's own layouts (by layout name or index)
so they inherit the master's fonts and colors. Tip: to start from a
template with zero slides, delete existing ones afterward with
`pptx_edit.py --remove-slide`.

### 5. Screenshot-driven deck (app screens, Figma frames)

The generic scripts assume text, tables and charts. When the deck has to
*present product screens* (a Figma page, a mockup set, a flow), build it with
ad-hoc python-pptx code instead and treat the screens as the layout grid.
Full recipe: `references/screenshot-deck.md`. The short version:

1. Prepare assets before writing slide code: rounded corners, soft shadow,
   and **two variants per frame** — true aspect (`p_*.png`) for hero slides,
   fixed 390×844 device frame (`d_*.png`) for rows. Equal height alone does
   not give equal width; frame aspect ratios differ per screen.
2. Fix the page grid once (13.333×7.5, margin 0.72, header rhythm, footer at
   6.86) and reuse it in every `header()`/`footer()` call.
3. Copy is a label, not an argument: headline = the screen's plain name,
   annotation = label + one short fact, and no sentence about the deck, the
   source file or the process. Colon-claims and "X, bukan Y" headlines read as
   AI and get cut; the presenter supplies the reasoning. Depth:
   `references/screenshot-deck.md` §4.
4. Findings are content: a numeric state that contradicts its own data, two
   status words for one state, a log entry that breaks its own rule. Keep each
   as one plain sentence carrying the number.
5. Render and measure before you redesign — `scripts/measure_render_geometry.py`
   checks widths, gaps and margins in inches; `vision_analyze` only judges
   hierarchy and legibility.
6. Ship the PDF next to the PPTX: the PDF embeds the font, the PPTX only
   stores its name.

### 6. Research deck from a paper or report

When the user hands over an article/report and asks for a class presentation,
build it as a report, not a pitch: tables instead of giant stat numbers, one
small grey section label, Arial instead of a decorative face, slide titles that
state the finding and carry its number (never a question), and a companion .docx
speaker script with `Yang diucapkan` and `Kalau ditanya` per slide. Full recipe, copy rules and the "too AI" recovery path:
`references/research-deck.md`.

If the user has not yet fixed a visual direction — or has already rejected one
look — do not build the full deck: make 4–5 two-slide style samples first and
let them pick. Recipe: `references/research-deck.md` §0.

### 7. Visual verification

`pptx_render.py deck.pptx --outdir ./render` converts the deck to PDF
with `soffice --headless` and splits it into one PNG per slide with
`pdftoppm` (or `pdftocairo`). Output JSON lists the PNG paths — review
each with `vision_analyze`. When either tool is missing the script exits
0 with `{"rendered": false, "missing": [...]}` and guidance; fall back to
the JSON outline from `pptx_read.py`, which verifies content and
structure, just not visuals.

## Converting to PDF

If LibreOffice is installed, export the finished deck to PDF directly:

```bash
soffice --headless --convert-to pdf --outdir ./out deck.pptx
```

The output lands at `./out/deck.pdf`. Fonts not installed on the host are
substituted, so render-verify (Procedure step 7) before shipping the PDF.
There is no offline pure-Python .pptx→PDF path; if `soffice` is absent,
say so rather than approximating.

## Pitfalls

- **Run splitting**: PowerPoint fragments paragraph text into runs at
  spell-check and edit boundaries. `--replace-text` first merges adjacent
  runs whose formatting is identical, so matches split across such runs
  are replaced with formatting fully preserved. Only when a match spans
  *genuinely differently-formatted* runs is the paragraph rewritten with
  the first run's formatting — verify those slides after replacement.
- **Chart slides cannot be duplicated**: each chart relationship embeds a
  separate XLSX workbook part; cloning that graph reliably is not
  supported, so `--duplicate-slide` refuses chart slides cleanly instead
  of corrupting the deck. Rebuild the chart on a new slide instead.
  External-hyperlink and image/media rels are carried over; layout and
  notes rels are recreated fresh.
- **Chart ops are a wrapper**: python-pptx replaces the whole dataset;
  `"ops"` round-trips existing plot data through `replace_data`, and
  changing chart *type* is not possible.
- **Reordering is XML-level**: python-pptx has no supported reorder API.
  `--move-slide` manipulates `<p:sldIdLst>` directly; safe for ordinary
  decks but re-read the deck afterward to confirm.
- **Copying slides between decks is unsupported** — duplication works
  only within one deck, where layouts and masters are shared.
- Footer/slide-number enablement copies the placeholder from the slide's
  layout; on layouts without those placeholders, `--set-footer` fails
  with a clear message (add a textbox instead).
- Hyperlinks apply to whole runs; `--hyperlink` links every run
  containing the given text on that slide.
- The default python-pptx template is 4:3; the create script sets 16:9
  unless the spec says otherwise. Custom templates keep their own size.
- Layout indexes vary by template. For brand templates, list layout names
  first: `pptx_read.py template.pptx --outline` (`layouts_available`).
- `slide.shapes.title` is None on blank layouts — the create script
  handles this, but remember it when writing ad-hoc python-pptx code.
- Always pass `encoding="utf-8"` when writing spec files; tokens like
  `{{city}}` may be filled with non-ASCII values.
- **`soffice --convert-to pdf` failing with "source file could not be loaded"
  usually means the Impress filter package is missing, not a corrupt deck.**
  Writer/Calc alone cannot import .pptx: install `libreoffice-impress`
  (`sudo apt-get install -y libreoffice-impress`), and launch with
  `-env:UserInstallation=file:///home/<user>/.cache/lo_profile` so headless
  runs do not fight a lock in the default profile. Verify a good file by
  reopening it with python-pptx (`Presentation(path)`) and `unzip -t` before
  blaming the deck.
- **Do not trust a vision model on pixel geometry.** It reports "ghost text",
  "uneven widths" and "clipped titles" on slides whose coordinates are
  measurably exact, and it misses real 4 px overlaps. Measure the rendered PNG
  (`scripts/measure_render_geometry.py`) and only then change the layout;
  reserve `vision_analyze` for hierarchy, contrast and whether a slide reads.
- **Font names travel, font files do not.** PPTX stores only
  `Plus Jakarta Sans`-style names; a machine without the font substitutes and
  the layout shifts. Deliver the PDF (fonts embedded) alongside the deck, and
  tell the user which font to install before editing.
- Text boxes created with `add_textbox` keep a fixed frame: a 34 pt headline
  in a 0.7 in box can overlap the content band below it. Content that follows
  a header must start below the subtitle line (≥2.10 in on the 7.5 in page
  with a subtitle present, ≥1.70 in without), not at the title's baseline.
- A zero-length connector (`add_connector` with identical start and end)
  makes some validators and LibreOffice reject the whole file; skip the call
  instead of drawing a 0-width divider.
- **Deleting copy re-opens the layout.** Remove a subtitle, a bottom note or a
  whole annotation block and the rest sits high with a dead band underneath;
  the slide then reads top-heavy even though nothing overlaps. Shift the
  remaining block (numbers, labels, note) back into the page centre and
  re-measure — never leave coordinates sized for text that no longer exists.
- **Quote UI strings from the extracted frame text, not from memory.** A
  paraphrase ("Tersimpan otomatis" when the screen says "Tersimpan aman")
  contradicts the screenshot printed inches away and is the first thing a
  reviewer catches. Grep the frame's `texts.json` for every quoted label.
- **Cutting trailing slides leaves page numbers behind.** Footers carry
  literal strings ("15", "16"), and speaker notes still reference them. After
  removing slides from the end, re-check each footer against its index and
  fix notes that name a deleted screen.
- **Native chart labels ignore the document language.** `plot.data_labels.number_format = '0.000'`
  renders `0.283` on an Indonesian deck where every other number uses a comma. Turn the plot-level
  labels off and set each point individually (`pt.data_label.has_text_frame = True;
  pt.data_label.text_frame.text = "0,283"`, then style `text_frame.paragraphs[0].runs[0].font`).
  Per-point labels are also the only way to drop a trailing zero the reader does not need.
- **`BAR_CLUSTERED` plots the first category at the BOTTOM.** Pass categories ascending so the
  largest value is last and lands on top; otherwise the reader meets the weakest bar first and the
  chart argues against the slide's own headline.
- **Highlight one bar with `series.points[i].format.fill`, never with a second series.** Point indices
  follow the category order, so after re-sorting the categories the highlighted indices move with
  them — recheck which bar is the accent colour before shipping.
- **A one-word rejection of the look means rewrite, not polish.** When the user
  says the deck is "too AI", change the layout grammar (kickers, stat rows,
  symmetrical blocks) and rewrite the copy together; recolouring or trimming a
  few sentences leaves the template grammar intact and gets rejected again.
- **Type1 fonts installed on the host do not survive PPTX rendering.** A `.pfb`
  face (e.g. Bitstream Charter) falls back to a sans face in LibreOffice, so the
  serif title you designed never appears; pick a TrueType face that is metric-
  compatible with what the user's machine has (Arial/Liberation Sans).
- **A stitched 2-up preview reads as one wide slide.** When showing several
  layout samples, paste the two rendered pages side by side with a visible
  gutter (44 px) and a caption strip above each page ("Gaya A · konsultan —
  cover / slide isi"); on a plain white canvas the reviewer sees a single
  26-inch slide and reports misalignment that does not exist.
- Table row height is a floor, not a height. A `row_h` smaller than the wrapped cell text makes
  the table grow down from its anchor and collide with the footer. Size two-line cells at ≥0.55 in and
  check the table's bottom edge against the footer band before rendering.
- **A question mark on a slide is a defect.** Titles that ask ("Kenapa polanya
  seperti ini?") or label sections without saying anything make the audience wait
  for a point the slide already has data for. Write the finding as a declarative
  sentence with its number. Gate it mechanically after export: extract the PDF text
  and assert `text.count('?') == 0`; the speaker-script docx is exempt because its
  `Kalau ditanya` blocks are questions by design.
- **Deck titles and the speaker script drift apart silently.** The .docx stores
  its own copy of every slide title in the page header, so retitling slides leaves
  the script describing a deck that no longer exists. Keep the titles in one list
  and rebuild both, or re-check each script heading against the rendered deck.
- **An academic cover is the user's own title, a mark, and nothing else.** No
  subtitle under the headline: the sample size and date belong in the first spoken
  line, not on the cover. Type the study's registered title verbatim — an invented
  hook headline gets the cover rejected even when the rest of the deck is fine.
  Put the institution logo small (≈0.8 in) in one corner on white, and put
  names/course below a short rule so they read as metadata rather than as a second
  title.

## Verification

1. After any create/edit, run `pptx_read.py OUT.pptx --outline` and check
   slide count, texts, tables, notes, and chart values match intent.
2. `--images DIR` then file-size check confirms pictures embedded.
3. Render every slide with `pptx_render.py deck.pptx --outdir ./render`
   and review each PNG with `vision_analyze` — this catches overlapping
   shapes, truncated text, and color problems the outline cannot. If the
   render tools are missing, the script says so; rely on the outline.
4. The bundled test suite is the full contract:
   `python -m pytest tests/ -q` (requires python-pptx + pytest).
