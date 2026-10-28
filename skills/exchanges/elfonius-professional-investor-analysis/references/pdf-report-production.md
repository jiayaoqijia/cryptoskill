# PDF Report Production

Purpose: turn the analysis into a professional, readable PDF without losing evidence or introducing layout defects.

## Toolchain that works on this machine

1. Write a self-contained HTML file with CSS for A4, fonts, colors, tables and charts.
2. Render charts with matplotlib at 200–220 dpi; use a font that supports Turkish characters (DejaVu Sans works).
3. Print HTML to PDF with headless Chromium:
   `chrome --headless=new --disable-gpu --no-sandbox --allow-file-access-from-files --virtual-time-budget=1500 --no-pdf-header-footer --print-to-pdf=out.pdf file:///.../report.html`
4. Add page numbers, footer and metadata with PyMuPDF; embed a Turkish-capable TTF (Segoe UI on Windows; DejaVu Sans or Noto Sans on macOS/Linux) because base-14 Helvetica cannot encode Turkish characters.
5. Render selected pages to PNG and inspect them visually before delivery.

## Layout rules

- A4; 18–20 mm margins; 9.5–11 pt body; 1.45–1.55 line height; serif body + sans headings is readable and premium.
- Cover: title, one-line thesis, verdict, 4–6 key metrics, date/source, contents line.
- One-page executive summary: four short paragraphs, decision matrix, what to monitor, scope limits.
- Sections start on new pages only when the section is substantial; avoid near-empty pages.
- Tables: 8–9 pt, header background, right-aligned numbers, no empty rows.
- Charts: one message per chart; source/date caption; no 3D, no gridlines on both axes, no unreadable legends.
- Callouts: one key insight per section, not decoration.
- Footer: `asset · report · date` left, `page / total` right; skip the cover.
- No internal checklist, placeholder braces or "lorem" text in the delivered PDF.

## Content checks

- Every chart/table has a source and as-of date.
- Numbers in the text match the tables and charts; rounding is consistent.
- Turkish: `dd.mm.yyyy`, thousands `.` and decimals `,`, expand acronyms on first use, keep tickers/contract names verbatim.
- The executive summary states the verdict, the gate and the three numbers a reader must remember.
- The conclusion states the conditions that would reverse the verdict.
- The PDF exists at a user-accessible path and opens without errors.

## Common failures

- Chrome ignores a page break because a table/figure is taller than the page; split the table or reduce the font.
- A section overflows by a few lines, creating a near-empty page; compress the CSS or remove a non-essential paragraph.
- Base-14 fonts drop Turkish glyphs in the footer; embed Segoe UI or DejaVu Sans.
- Images fail to load under `file://`; use `--allow-file-access-from-files` and relative paths in the same folder.
- The cover height creates a blank page; set `@page :first { margin: 0; }` and keep the cover height just under A4.
