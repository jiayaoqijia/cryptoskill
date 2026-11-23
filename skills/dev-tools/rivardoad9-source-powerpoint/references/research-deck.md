# Research deck from a document, plus the speaker script

Use when the user hands over a paper, report or article and asks for a
presentation, especially a class presentation with a required section order
(background, novelty, questions, theory, prior studies, hypotheses, sample,
results, discussion, conclusion).

## 0. Pick the look before building

Do not hand over a finished 14-slide deck as the first artifact when the user
has not chosen a visual direction, and never as the second attempt after a
rejection. Build the style menu first.

1. Take one content slide and the cover of the real material — same numbers,
   same titles — and build it five times, each in a different design grammar:
   consulting (action-title + dense table), editorial (full-bleed photo + big
   headline), academic (university band + serif + numbered chapters + grid
   tables), data-first (chart dominant, text as annotation), dark (near-black
   page, white type, one accent). Colour swaps over one layout are not options;
   if two samples share a grid, the user sees one option twice.
2. Render each variant to PDF, then PNG at ~110 dpi with PyMuPDF, and composite
   the two pages of a variant side by side in PIL: 34 px padding, 44 px gutter,
   cream canvas, and a caption strip above each page ("Gaya A · konsultan —
   cover / slide isi"). Without gutter and caption the composite reads as one
   very wide slide and the reviewer reports alignment problems that are not
   there.
3. Send the previews as photos, one sentence per option naming who it suits and
   the risk (dark decks on a bright projector, photo-led decks with heavy tables,
   formal templates that look dated), then one recommendation. Stop and wait.
4. Only after the pick, build the full deck in that grammar, plus the speaker
   script, and keep the samples' coordinates as the grid.

Licensing: a photo lifted from Wikimedia Commons is usually CC BY-SA — fine in
class, but it needs a credit line on the slide, so mention that when offering
the photo-led option.

## 1. Mine the source before designing

Freeze the hypothesis-to-variable mapping from the source and write each table
row out by hand. A results table sorted by coefficient size reorders the
variables, and if the H numbers are generated from that order, H1 ends up on
whatever had the biggest beta — a reviewer who knows the model spots it
immediately.

Extract the document text (`zipfile` + regex on `word/document.xml` for .docx),
then list every number the deck may use, with the page/section it came from:
sample size, profile percentages, construct means, loadings, alpha/CR/AVE,
HTMT, VIF, R², each path coefficient with p, f² and CI.

Rules that keep the deck honest and keep the user's trust:

- Every number on a slide must exist in the source. If a slide needs a figure
  the source does not have, delete the figure, not the caveat.
- Separate population/market claims from sample claims in the wording:
  "pada sampel ini", not "konsumen Indonesia".
- When a survey question allowed multiple answers, say so next to the number;
  a matrix-question 84% is not market share and will be read as one otherwise.
- Group-level financials (revenue, margin) belong in a separate footnote block
  labelled as consolidated group figures, never inside the respondent table.
- Report the rejected hypothesis on its own slide beat and in the conclusion.
  Users notice when a negative result disappears.

## 2. Layout: report, not pitch

The tell of an AI deck is not colour, it is the template grammar: a coloured
accent kicker on every slide, a hairline rule used as decoration, three giant
stat numbers in a row, symmetrical two-column blocks, and a one-line mic-drop at
the bottom. Strip those. What survives — one muted grey label and one grid
repeated on every page — is what makes a report deck look edited instead of
generated.

Working system for a 13.333×7.5 page:

- Margins 0.8 in left/right, content width 11.73 in.
- One header block, repeated on every slide so the deck reads as a system rather
  than fourteen layouts: grey uppercase label 8.5 pt at y 0.60; title 26–28 pt
  bold at y 0.95, max two lines; one hairline at y 2.42; body starts at 2.60.
- Body 10.5–11.5 pt, line spacing 1.45–1.5; footnote 9–10 pt grey.
- Footer band at y 7.06: deck/course caption 7.5 pt grey left, page number right.
- Cover: the study's registered title, word for word, no subtitle. Never swap in a
  hook headline you invented — the user knows their own title and will send the
  cover back. Institution mark 0.8 in wide in the top corner on white; a 0.9 in
  rule under the title, then names 10 pt bold and one metadata line 9.5 pt grey.
  Sample size, method and date belong in the first spoken paragraph, not on the
  cover.
- A long title is a typography problem, not a reason to shorten it. Set it in 3
  balanced lines at the largest size that keeps every line inside the 6.4 in text
  column. Measure rather than eyeball:
  `ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', pt*96//72).getlength(line)/96`
  returns inches; a 39-character line at 23 pt measured 5.93 in and fitted with
  margin. Break at phrase boundaries, never end a line on a preposition
  (`terhadap`, `pada`, `dan`), and never leave a two-word orphan (`pada Konsumen`).
- Tables instead of stat triptychs. Header row: bold, black hairline above,
grey hairline below, no fill, no vertical rules.
- One chart maximum per deck (path coefficients), grey bars, the
  non-significant bar in a lighter grey, per-point comma labels.

Font: Arial. It maps to Liberation Sans on Linux, exists on every Windows and
macOS machine, and keeps the layout identical between the render check and the
user's laptop. Decorative fonts that only exist on this host (Type1 Charter,
Plus Jakarta Sans) change the layout on the user's machine or fall back to a
sans face inside the PPTX.

Institution mark: a university site behind a Cloudflare block refuses `curl`, but
its favicon is public — `https://www.google.com/s2/favicons?domain=<domain>&sz=256`
returns a 192 px PNG, which is ~245 dpi at 0.8 in and enough for a corner mark.
Open it with `vision_analyze` first and confirm it is the right logo (not a
favicon placeholder) before placing it.

Table borders with python-pptx need XML: turn `tbl.first_row` off, fill every
cell white, then append `a:lnB` (and `a:lnT` for the header) with a solidFill
srgbClr to each `tcPr`. Row height is a floor — two-line cells need ≥0.55 in.

## 3. Copy rules for slides

- Titles are findings, not labels, and never questions: state what the data shows
  and carry the number ("H&M dipilih saat berbelanja, bukan saat mengingat",
  "Kualitas paling kuat, keberlanjutan tidak terbukti"). A label only says which
  section this is; a question ("Kenapa polanya seperti ini?") makes the room wait
  for an answer the slide already has. A contrast clause is fine when both halves
  are measured (14% versus 84%); it is banned only as decoration without numbers.
- Mechanical gate: after export, pull the text out of the PDF and require
  `''.join(p.get_text() for p in pymupdf.open('deck.pdf')).count('?') == 0`.
  The speaker script is exempt — its `Kalau ditanya` blocks are questions.
- No sentence that comments on the deck ("ini bagian yang paling sering salah"),
  no importance puffery, no closing aphorism.
- One idea per slide, stated as a fact with its number. If a slide needs three
  symmetric columns to look full, the content is probably two slides or a table.
- Indonesian copy: digits with comma decimals (0,283), no em dashes.

## 4. Companion speaker script (.docx)

Deliver it with the deck whenever the user says they need to understand the
material, not just present it. One page per slide, in this shape:

- `Slide N` (small accent label), slide title, `Dibawakan: <name>`.
- `Yang diucapkan` — spoken paragraphs, not bullet points. Numbers written the
  way they are said aloud ("nol koma dua delapan tiga") because digits get
  misread under pressure; a digits table sits in the appendix for checking.
- `Kalau ditanya` — two or three likely questions with a short answer that
  carries the actual number.
- `Catatan` on the cover slide only, for delivery advice.

Close with an appendix table of every number in the deck and four or five
method questions (why PLS-SEM, is n=100 enough, what p=0,197 means, why the
failed screeners were kept).

Page numbers: put a `PAGE` field (`w:fldSimple` with `w:instr="PAGE"`) in a
second, right-aligned footer paragraph next to the left-aligned caption
paragraph. A single paragraph with a right tab stop at the text width places the
number mid-footer as soon as the caption text changes length.

Include the human parts: the moment the team was puzzled by a number, the
argument about four respondents, what the study cannot claim. A script with no
admission reads as generated; one honest aside per few slides reads as a person.

Assign speakers per block and label the split as a suggestion. In a group
presentation this is the first thing the group edits.

Retitling the deck desynchronises the script: each page header stores its own copy
of the slide title. Keep the titles in one list, rebuild both files from it, then
grep the script PDF for any heading that no longer matches the deck.

## 5. When the user says the output is "too AI"

Do not tweak colours, spacing or a few sentences. Replace both systems at once:

1. Change the layout grammar (drop accent kickers, stat rows, symmetric blocks)
   and the font to a portable one.
2. Rewrite the copy from scratch in a plainer voice; keep every number.
3. Re-render and check the dense pages (tables, chart, three-column closing)
   for collision with the footer band.

`vision_analyze` calling the result "clean, modern, consulting-style" is a
warning, not praise: that is the look the user is rejecting.

### Reading the complaint

"Ganti modelnya" / "modelnya kurang" refers to the design grammar, not the LLM
behind the chat. Rebuild the visual system; only discuss switching the AI model
if the user names it explicitly ("model AI-nya", "ganti ke Claude"). Answering a
design complaint with a model switch, or the reverse, both read as not listening.

"Rapi dan terstruktur" is a request for one repeated grid, not more decoration:
same label position, same title size, same hairline, same footer on every slide.
Adding rules, boxes or accent colours to look organised does the opposite.
