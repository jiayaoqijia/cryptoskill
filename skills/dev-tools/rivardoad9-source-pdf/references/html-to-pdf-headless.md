# HTML/Markdown → PDF with headless Chrome

Use this when the deliverable needs real CSS layout, embedded screenshots, or many pages. reportlab is for structured specs; a designed report comes from HTML printed by Chromium.

## Pipeline

1. Author each document as Markdown (one file per document) so edits stay reviewable.
2. Convert with `python-markdown`:

```python
body = markdown.markdown(text, extensions=["extra", "tables", "fenced_code", "sane_lists"])
```

3. Inline every local image as a base64 data URI before printing. Headless Chrome frequently will not resolve `file://` subresources, and data URIs make the HTML self-contained for archiving:

```python
def img_to_data_uri(m):
    p = (DOCS / m.group(1)).resolve()
    if not p.exists():
        print(f"! missing image: {m.group(1)}")
        return m.group(0)
    data = base64.b64encode(p.read_bytes()).decode()
    return f'src="data:image/png;base64,{data}"'

body = re.sub(r'src="([^"]+)"', img_to_data_uri, body)
```

4. Print with Chromium directly (no wkhtmltopdf, no puppeteer):

```bash
chrome --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=out.pdf file:///abs/path/doc.html
```

Always pass `--print-to-pdf` an absolute output path; a relative path lands next to the Chrome binary.

## A4 CSS that survives print

```css
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
body { font-family: "DejaVu Sans", sans-serif; font-size: 10.5pt; line-height: 1.55; }
h1 { font-size: 22pt; margin: 0 0 4mm; }
h2 { font-size: 13pt; margin: 8mm 0 2.5mm; border-bottom: 1.2pt solid #17181c;
     page-break-after: avoid; }
img { max-width: 100%; height: auto; display: block; margin: 3mm 0 4mm;
      border: 1pt solid #d8d8d8; border-radius: 2mm; page-break-inside: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt;
        page-break-inside: auto; }   /* long tables must be allowed to split */
table.keep { page-break-inside: avoid; }   /* short tables: keep whole */
thead { display: table-header-group; }      /* header row repeats after a split */
tr { page-break-inside: avoid; }            /* never cut a row in half */
th { background: #17181c; color: #fff; text-align: left; padding: 2mm 2.5mm; }
td { padding: 1.8mm 2.5mm; border-bottom: .6pt solid #ddd; }
pre { background: #17181c; color: #eaeaea; padding: 4mm; font-size: 8.6pt;
      page-break-inside: avoid; }
```

## Paginating a long report

A one-page-per-chapter habit inflates the page count and leaves half-empty pages. Build the flow, then measure.

1. **Let sections flow.** `page-break-before: always` on every section is only right for short decks. For a report, use `padding-top` plus a hairline `border-top` on `.chapter` and reserve forced breaks for the cover.
2. **Split long tables, keep short ones.** A blanket `page-break-inside: avoid` on `table` pushes an eight-row table to the next page and leaves the previous one two-thirds blank. Set tables to `auto`, add `page-break-inside: avoid` only to short tables via a `keep` class, and wrap the header row in `<thead>` so it repeats.
3. **Measure with text volume, not the naked page count.** A PDF page object count (regex on `/Type /Page`) is unreliable; use pymupdf and print characters per page. Pages under ~400 characters after the first are spill pages from a bad break:

```python
import pymupdf
d = pymupdf.open("out.pdf")
for i, p in enumerate(d):
    t = p.get_text().strip()
    print(i + 1, len(t), t.split("\n")[0][:60] if t else "EMPTY")
```

4. **Render only the suspicious pages.** `d[i].get_pixmap(dpi=110).save(...)` avoids depending on poppler, then check the pages that split tables or carry the cover with `vision_analyze`.

Target density for a text report is roughly 1.800–2.800 characters per A4 page at 9.3–9.6 pt. A 30-page draft that lands at 15 dense pages after removing forced breaks is normal, not a loss of content.

## Pitfalls

- **Split tables lose their header.** Without `<thead>` (and `thead { display: table-header-group }`) a table that crosses a page boundary continues with unlabeled columns. Wrap the first `<tr>` of every table in `<thead>`; a regex pass over the file is enough.
- **A table that appears intact can still be the wrong shape.** Three-row tables look fine split across pages only until the reader hits column values with no header. Short tables belong in the `keep` class.
- **Markdown collapses consecutive lines into one paragraph.** A metadata block written as three bare `**Status:**` / `**Role:**` / `**Size:**` lines prints as one run-on sentence. Use list items or explicit `<br>`.
- **Broken images print silently.** Chrome renders a gap and still exits 0. Log missing `src` values during conversion and fix them before printing.
- **Chrome exits 0 on a blank page.** Check the PDF size and inspect the rendered page; never report "generated" from the exit code alone.
- **No poppler for inspection.** `pdftoppm`/`pdfinfo` are often absent. Screenshot the HTML instead — same layout engine, no extra install:

```bash
chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=794,1400 --virtual-time-budget=5000 \
  --screenshot=/tmp/page.png file:///abs/path/doc.html
```

A4 at 96 dpi is 794 px wide, so the screenshot matches the page width. Inspect it with `vision_analyze` for clipping, overlap, and missing images.
- **Keep screenshots ~1200 px wide.** Full-page captures at native resolution inflate a 6-page PDF past 1 MB with no visible gain.
- **Headings break badly at page edges.** `page-break-after: avoid` on `h2`/`h3` and `page-break-inside: avoid` on tables/images is what keeps a heading from sitting alone at the bottom of a page.

## Batch behaviour

Render every document from one script that takes filename filters, so a fix to the CSS or a replaced screenshot is one command. Re-render only the affected documents when iterating, then re-upload those files.