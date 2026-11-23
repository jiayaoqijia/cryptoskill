---
name: docx
description: Create, read, edit, template, and review Word .docx files.
version: 1.1.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [word, docx, documents, office, templates, revisions, comments]
    category: productivity
    related_skills: [pdf, xlsx, powerpoint]
---

# Docx Skill

Create, read, edit, and template Microsoft Word `.docx` files with
python-docx via small CLIs. It handles text, styles, lists, tables,
images, headers/footers, `{{token}}` templating, tracked changes
(list/accept/reject), comments (list/add/delete), TOC and page-number
fields, and package health checks. It does not render documents itself
(PDF needs LibreOffice — see Converting to PDF) or edit legacy `.doc`.

Layout depth that is only needed sometimes lives in `references/`:

- **Building a designed document from scratch** (cover page, shaded tables, repeating
  header rows, caption pairing, PAGE field footer) plus the render-and-inspect loop:
  `references/python-docx-layout-recipes.md`

## When to Use

- The user asks to generate a Word document (report, letter, contract).
- You need the text, outline, styles, or embedded images of a `.docx`.
- You must change an existing `.docx`: replace text, edit table cells,
  insert/delete paragraphs, apply styles, merge fragmented runs.
- You have a `.docx` template with `{{placeholders}}` to fill from data.
- The document has tracked changes to review, accept, or reject.
- You need to read reviewers' comments, or add/delete comments.
- A `.docx` won't open or behaves oddly and you need corruption triage.
- The document needs a table of contents or "Page X of Y" footers.
- Not for: `.doc` (legacy), `.odt`, or WYSIWYG layout work.

## Prerequisites

- Python 3.10+ with `python-docx` installed:
  `pip install python-docx` (import name is `docx`; lxml comes with it).
- Comments `add` uses the native API on python-docx >= 1.2 and an XML
  fallback on older versions — both are automatic.
- For image blocks: the image files must exist locally (PNG/JPEG).

## How to Run

All helpers live in `scripts/` next to this file. Run them with the
`terminal` tool; each supports `--help` and prints JSON to stdout.

```bash
python scripts/docx_create.py spec.json out.docx
python scripts/docx_read.py out.docx --text
python scripts/docx_edit.py replace out.docx --find old --replace new
python scripts/docx_template.py tpl.docx values.json filled.docx
python scripts/docx_revisions.py list out.docx
python scripts/docx_comments.py list out.docx
python scripts/docx_validate.py out.docx
```

## Quick Reference

| Task | Command |
| --- | --- |
| Create from JSON spec | `docx_create.py spec.json out.docx` |
| Full text (body+tables+headers/footers) | `docx_read.py f.docx --text` |
| Heading outline + table shapes | `docx_read.py f.docx --structure` |
| Styles actually used | `docx_read.py f.docx --styles` |
| Extract embedded images | `docx_read.py f.docx --images outdir/` |
| Detect tracked changes/comments | `docx_read.py f.docx --revisions` |
| Find/replace (formatting kept) | `docx_edit.py replace f.docx --find A --replace B -o out.docx` |
| Set a table cell | `docx_edit.py set-cell f.docx --table 0 --row 1 --col 2 --text X` |
| Insert paragraph before index N | `docx_edit.py insert f.docx --index N --text X --style Normal` |
| Delete paragraph N | `docx_edit.py delete f.docx --index N` |
| Apply style to paragraph N | `docx_edit.py style f.docx --index N --style "Heading 1"` |
| Merge equal-format adjacent runs | `docx_edit.py normalize f.docx -o out.docx` |
| Insert TOC field before para N | `docx_edit.py toc f.docx --index N -o out.docx` |
| "Page X of Y" footer fields | `docx_edit.py page-numbers f.docx` |
| Fill `{{tokens}}` | `docx_template.py tpl.docx values.json out.docx --strict` |
| List revisions (id/author/date/text) | `docx_revisions.py list f.docx` |
| Accept / reject all revisions | `docx_revisions.py accept-all f.docx -o out.docx` (or `reject-all`) |
| Accept / reject one revision | `docx_revisions.py accept f.docx --id 3 -o out.docx` |
| List comments (+anchored text) | `docx_comments.py list f.docx` |
| Add comment anchored to text | `docx_comments.py add f.docx --target "phrase" --text "note" --author You` |
| Delete comment by id | `docx_comments.py delete f.docx --id 0` |
| Health-check the package | `docx_validate.py f.docx` (exit 1 on errors) |

## Procedure

1. **Create.** Write a JSON spec with `write_file`, then run
   `scripts/docx_create.py`. The spec supports: `page` (size + margins in
   mm), `header`/`footer` strings, `footer_page_numbers` (adds a
   "Page X of Y" field footer), `styles` (custom paragraph styles with
   font, size, bold/italic, hex `color`), and `blocks` — `heading`
   (level 1-9), `paragraph` (either `text` or a `runs` list where each run
   may set `bold`/`italic`/`underline`), `bullet_list`, `numbered_list`,
   `table` (`header` row rendered bold, `rows`, optional built-in table
   `style` such as `Table Grid`), `image` (`path`, optional `width_mm`),
   `toc` (Table of Contents field), and `page_break`. The full spec
   format is documented at the top of `scripts/docx_create.py`.
2. **Read.** Use `scripts/docx_read.py` with exactly one mode flag.
   `--text` returns body paragraphs, all table cell text, and
   header/footer text as JSON. `--structure` returns the heading outline
   plus paragraph/table/section counts. `--images DIR` copies every file
   under `word/media/` out of the package.
3. **Edit.** Use `scripts/docx_edit.py`. `replace` walks body, tables
   (nested included), headers and footers, and preserves run formatting;
   add `--body-only` to skip headers/footers. Pass `-o out.docx` to keep
   the original; omit it to edit in place. Paragraph indices for
   `insert`/`delete`/`style`/`toc` refer to `--structure`/`--text` body
   order. Run `normalize` first on documents that came out of heavy Word
   editing — it merges adjacent runs with identical formatting so later
   find-replace matches reliably.
4. **Review revisions.** `docx_revisions.py list` reports every `w:ins`
   and `w:del` (id, author, date, affected text) anywhere in body,
   tables, headers, or footers. `accept-all` / `reject-all` resolve them
   in bulk; `accept`/`reject --id N` handles a single revision. Accept
   keeps insertions and drops deleted text; reject does the reverse.
5. **Comments.** `docx_comments.py list` returns each comment's id,
   author, date, body text, and the document text it is anchored to.
   `add --target "some phrase"` anchors a new comment to the first
   occurrence of that phrase (runs are split as needed; formatting is
   preserved). `delete --id N` removes the comment and its markers
   without touching document text.
6. **Template.** Put `{{name}}`-style tokens in the document. Run
   `scripts/docx_template.py` with a JSON object of values. Use
   `--strict` to fail when tokens remain unfilled; the JSON output lists
   `filled` counts and `unfilled_tokens` either way.
7. **Verify** (always): re-read the output with `--text` or
   `--structure`, and run `docx_validate.py` on anything you produced
   via revision/comment surgery.

## Converting to PDF

No script needed. When LibreOffice is installed, convert headlessly:

```bash
soffice --headless --convert-to pdf --outdir outdir/ file.docx
```

Check availability first (`command -v soffice || command -v
libreoffice`). If neither exists, install the writer alone — it is the
dependency every layout check needs, and it is far smaller than the full
suite:

```bash
sudo -n apt-get install -y --no-install-recommends libreoffice-writer
```

python-docx cannot render PDFs, so without a real renderer pagination and
table overflow cannot be checked at all — install rather than reporting the
check as impossible.

## Pitfalls

- **Tokens split across runs.** Word often fragments text into several
  runs. The replace helpers collapse matched runs (replacement inherits
  the first run's formatting); running `docx_edit.py normalize` first
  reduces fragmentation for all later edits.
- **Revision coverage.** `docx_revisions.py` resolves run-level
  insertions and deletions (the overwhelming majority). Paragraph-mark
  and table-row revisions, format-change records, and moves are detected
  by `--revisions` but not auto-resolved — see
  `references/revisions-and-comments.md` and hand those to Word.
- **Comment threading.** Replies and "resolved" status live in
  `commentsExtended.xml`, which this skill ignores; comments it adds are
  plain top-level comments.
- **Field results are computed by Word.** `toc`, `page-numbers`, and the
  `toc`/`footer_page_numbers` spec options write *field codes*.
  Word/LibreOffice populates the actual entries and numbers when the
  file is opened (Word may prompt to update fields); python-docx never
  computes them, so placeholder text shows until then.
- **Validation is a health check, not schema validation.**
  `docx_validate.py` verifies the zip, required parts, relationship
  targets, image magic bytes, and referenced styles. It is NOT XSD
  validation — a file can pass and still contain XML Word dislikes.
- **Style names must exist.** Applying a style that isn't defined in the
  document raises `KeyError`. Built-ins like `Heading 1`, `List Bullet`,
  `List Number`, `Table Grid` exist in the default template; custom
  styles must be declared in the create spec first.
- **Numbered lists restart.** `List Number` relies on Word's default
  numbering; separate lists in one document may continue numbering
  instead of restarting. Warn users needing precise multi-list numbering.
- **Cell writes replace formatting.** `set-cell` uses `cell.text = ...`,
  which resets runs in that cell to plain formatting.
- **Encoding.** All JSON specs/values files are read as UTF-8 explicitly;
  never rely on locale defaults when writing your own glue code.
- **Don't unzip-and-sed the XML.** Edit through the scripts (or
  python-docx); raw text substitution in `document.xml` corrupts files
  easily. Use `patch`/`write_file` only for the JSON inputs, never on the
  `.docx` itself.
- **Table widths are a budget.** `autofit = False` alone does not fix a table: Word and LibreOffice
  lay out from the table grid, so also append `w:tblLayout w:type="fixed"` to `tblPr`, set
  `table.columns[i].width`, and set every cell's width. Keep the sum at or under the usable page
  width (A4 minus both margins). Nothing raises on overflow; the table runs past the right margin
  and the fault shows only in a render. Do not hand-pick widths per table — scale the proportions
  into the budget programmatically, or the sixth table will overflow:
  `widths = [w * USABLE_CM / sum(widths) for w in widths]`.
- **Cell margins eat the width a header needs.** Default cell padding is ~0.19 cm per side, so a
  column sized to the text still wraps its header mid-word ("Permint/aan"). For dense numeric
  tables shrink `w:tblCellMar` left/right (~0.08 cm) and drop the header font one or two points
  before stealing width from the label column; then confirm in the rendered PNG that no header
  broke inside a word.
- **Runs belong to a paragraph.** `Document` has no `add_run`; a run is
  created from the paragraph that holds it (`p.add_run(text)`), including
  inside table-cell paragraphs.
- **Pair headings and captions with their table.** `keep_with_next = True`
  on the caption or heading paragraph is what stops a short table from being
  orphaned at the top of the next page without its label.
- **Figures pair from the other side.** A caption placed *under* an image
  cannot pull the image with it, so set `keep_with_next = True` on the picture
  paragraph too; otherwise the chart sits alone at the page bottom and its
  caption opens the next page.
- **A table header can be orphaned on its own.** `keep_with_next = True` on the
  header-row cell paragraphs forces the first body row onto the same page;
  without it a table starting at the page bottom renders as a bare header strip
  with no data under it.
- **Rows split mid-sentence unless you forbid it.** Add `w:cantSplit` to the
  row properties of tables and single-cell callout boxes; without it a shaded
  callout breaks across a page boundary and its last line disappears under the
  margin.
- **`w:cantSplit` protects a row, not a table.** A short table still breaks after its
  first row and continues on the next page without a header, so the reader sees a fragment
  (`Between Groups` alone on one page). For tables that must stay whole, set
  `keep_with_next = True` on every cell paragraph in every row except the last — that
  chains the rows — and mark the header row `w:tblHeader` so any break that still happens
  repeats the header instead of dropping it.
- **Chaining every row is for SHORT tables only.** Apply the whole-table chain above when
  the table cannot fit a page break gracefully (roughly ≤15 rows); on a 25-row table the
  same chain makes LibreOffice move the entire table to the next page and leave 9–13 cm of
  white space above it, a defect worse than a clean split. Gate it on row count
  (`if len(rows) <= 15:` chain, else leave rows breakable and keep only `repeat_header`),
  and drop `keep_with_next` from the caption of a long table so caption and first rows can
  start on the current page.
- **Never slice generator source on a bare token.** `s.index("landscape_page()")` matches
  inside `def landscape_page():`, so a copy-paste block move silently deletes everything
  from that token to the paste point — a whole results section in this case. Anchor slices
  on line starts (`re.search(r"^marker", s, re.M)`, or `"\n" + marker`), copy the file to
  `.bak` before a bulk edit, and assert `py_compile` plus a plausible line count before
  rebuilding the document.
- **Identity text hides outside `paragraphs`.** python-docx does not see text boxes, and
  `docProps/core.xml` keeps `dc:creator` / `cp:lastModifiedBy` after a body edit. To scrub or
  replace a name, grep the unzipped package for the token (`word/document.xml`,
  `word/header*.xml`, `word/footer*.xml`, `docProps/core.xml`), edit the body through
  python-docx, then set both properties via `doc.core_properties`. A name that survives in
  metadata fails an anonymity or authorship check even when the visible text is clean.
- **Code blocks need their own font, shading and page rule.** A DAX/SQL snippet pasted as body text wraps as prose
  and splits across pages mid-statement. Give each line a Consolas run (≈8.5 pt), shade the paragraph
  (`w:shd` fill `F2EEE7`), indent it slightly, and set keep-lines so the block stays whole. Long measure
  definitions break after the comma inside the call, not in the middle of an identifier — break them where the
  reader would.
- **A spilled final line reads as a broken document.** After the layout
  settles, shorten prose rather than adding a page: two lines stranded on
  page 10 look like an error to the reader.

## Verification

- After create/edit/template, run `docx_read.py out.docx --text` and
  check the expected strings appear (and old strings are gone).
- After accept/reject, `docx_revisions.py list` should return `[]` (or
  only the ids you intentionally left); after comment surgery,
  `docx_comments.py list` should reflect the change and `--text` output
  must be unchanged.
- `docx_validate.py out.docx` exits 0 with `"ok": true` on a healthy
  package — run it after any revision/comment/field manipulation.
- When figures are revised, assert the change in the *render*, not just the
  source: extract text from the converted PDF and check the old tokens are
  absent and the new ones present (`"44,2" in t`, `"5,3" not in t`). Vision
  reads digits unreliably, so extracted text is the only trustworthy check.
- For templates run with `--strict`, or check `unfilled_tokens == []`.
- Structure checks: `--structure` should show the expected heading
  outline and table shapes; `--styles` confirms custom styles applied.
- Pagination: `python scripts/pdf_page_fill.py out.pdf` reports every page whose content
  ends more than 3 cm above the bottom margin — that is the objective signal for a table
  or figure that jumped pages, and it catches gaps a chars-per-page count hides.
- Caption series: extract every paragraph starting `Tabel `/`Gambar ` in body order and
  assert the numbers are consecutive for each series before delivering. Inserting one table
  late renumbers everything after it, and in-text `Tabel 4.5` references silently point at
  the wrong object until checked.
