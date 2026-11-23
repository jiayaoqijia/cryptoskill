# Long-form designed reports with reportlab

For a 10+ page document that needs a cover, running footer, dense tables,
callout boxes and a typographic hierarchy — and where no headless browser is
available on the host. Build it as a Python script, never as a JSON spec:
long reports need helper functions, and the content has to be edited by hand
many times before the layout settles.

Keep the build script next to the output (`build_pdf.py`) and regenerate the
PDF from it every time a number changes. Never patch a PDF in place.

## Fonts

Liberation is the reliable family on a bare Linux host: it ships Regular,
Bold, Italic and BoldItalic. DejaVu has no oblique file, so `<i>` silently
renders upright.

```python
F = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Sans", F + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", F + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-I", F + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BI", F + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B",
                              italic="Sans-I", boldItalic="Sans-BI")
```

`registerFontFamily` is what makes `<b>` inside a Paragraph resolve; without
it, bold text in table cells renders as regular.

## Page templates

`BaseDocTemplate` with two `PageTemplate`s: a `Cover` template whose `onPage`
draws the background bands, and a `Body` template whose `onPage` draws the
footer rule, document label and page number. Switch with
`NextPageTemplate("Body")` followed by `PageBreak()` after the cover.

## Flowables that carry the design

- A `Rule(Flowable)` subclass for hairlines and section rules — strokes at an
explicit width instead of a full-width `HRFlowable`.
- `callout(text, kind)`: a one-cell `Table` with a tinted `BACKGROUND`, a
  `LINEBEFORE` accent bar, and an inline small-caps label (`INTINYA`,
  `HATI-HATI`) as a bold run inside the paragraph. This is what makes a long
  document skimmable and it is three lines of code.
- `table(headers, rows, widths_mm)`: dark header row, zebra body rows,
  `repeatRows=1` so the header repeats when a table spans pages.
- `kv_table(rows)`: two-column label/value table for definitions and specs.

## The pagination trap

Do **not** put `PageBreak()` between chapters. Chapters in a real document run
1.1–1.4 pages, so a forced break after each one leaves a page that is 70%
empty and nearly doubles the page count. One build went from 19 pages to 15
purely by deleting nine page breaks, with no content change.

Instead:

- start each chapter block with `Spacer(1, 20)`;
- set `keepWithNext=1` on the kicker, `h1` and `h2` styles so a heading never
  lands alone at the bottom of a page;
- let body content flow continuously across chapter boundaries.

Keep an explicit `PageBreak()` only after the cover and after the
contents/"how to use" page.

## reportlab 5: the story must be flat

`story.append([flowable, flowable])` raises
`AttributeError: 'list' object has no attribute 'getKeepWithNext'`.
Append each flowable individually:

```python
def add_all(items):
    for f in items:
        story.append(f)
```

Older reportlab versions flattened nested lists; 5.x does not.

## Cover layout

Two things go wrong by default: the text block sits in the top third leaving a
dead middle, and the bottom label collides with the trim edge.

- Set the cover frame's bottom edge above the footer band, not at the page
  margin.
- Anchor the credits/byline block with a large `Spacer` (280–300 pt) so the
title sits upper-left and the byline sits just above the band. A top-aligned
  block looks like a missing image; a bottom-anchored byline looks deliberate.
- Keep footer text at least 20 mm from the page edge.

## Verify before sending

Chars-per-page is the fastest blank-page detector:

```python
import pymupdf
d = pymupdf.open(path)
for i, page in enumerate(d, 1):
    print(i, len(page.get_text().strip()))
```

On a body page, anything under ~800 characters means a bad break. Then render
the cover plus two or three representative pages at 100 dpi and look at them:
clipped table columns, orphan headings, text near the trim edge, and a table
split so that its header is on the previous page.

Compute every derived cell in Python from the same variables (cost, revenue,
profit, break-even) rather than typing the result. When a supplier quote
changes, the table must move with it — a hand-typed total that contradicts the
rows above it destroys the document's credibility faster than a typo.

## Shape of a learning document for this user

A 14–16 page / 4,000–5,000 word document works well. Structure that has landed:

1. "How to use this document" with three reading paths (5 minutes, 30 minutes,
   deep) that point at the callout boxes and the Q&A chapter.
2. Concepts before numbers: what the product is, who buys it and why, then the
   supply side, then price and margin.
3. A chapter of "questions people will ask you" with one-paragraph answers —
   this is the chapter the user actually reads before a conversation.
4. A glossary of the supplier-side jargon, because the user will hear it in
   the next WhatsApp thread.

Mark every number as either field data (with the date and source) or an
estimate, and say out loud when two public sources contradict each other
rather than picking the nicer one. The user's stated goal is to be able to
answer questions from understanding, not to quote impressive figures.
