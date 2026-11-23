# Screenshot-driven deck (product screens as the layout)

For decks whose evidence is app screens: a Figma page review, a design
handoff, a UX case study, a flow walkthrough. Charts and bullet slides are not
the point — the screens are, and the layout exists to make them legible.

## 1. Assets before slides

Pull frames at `scale=2` and extract the text (`characters`) in the same pass,
so captions quote the real copy instead of your reading of a JPEG.

Prepare every frame twice, in one script:

```python
# rounded corners + soft shadow, transparent canvas
def shadowed(im, radius=18, pad=34, blur=22, alpha=70, tint=(9, 27, 66)):
    ...  # mask a rounded rect, blur a +8px offset copy, composite, hairline border
```

- `p_<id>.png` — true aspect, shadowed. Used for hero slides (one big screen).
- `d_<id>.png` — **fixed device frame**: cover-scale the raw screen to 390×844,
  centre-crop, then round + shadow. Used for any row of 2+ screens.

Why two variants: a Figma page mixes full scrolling screens (aspect ≈0.29),
ordinary screens (≈0.50) and modal boards (≈0.44). Placing them all at the
same height yields widths from 0.87 in to 1.75 in in the same row — it reads
as broken layout even though the code is uniform. Equal *frame* fixes it.

## 2. Page grid (13.333 × 7.5 in)

| Element | Value |
|---|---|
| margin | 0.72 in both sides |
| kicker | y 0.52, 10 pt, uppercase |
| rule under kicker | y 0.83 |
| headline | y 1.02, 34 pt bold (60 pt on the cover), line spacing 1.12 |
| subtitle | y 1.72, 13.5 pt, max width 9.4 in |
| content start | y ≥ 2.10 with a subtitle, ≥ 1.70 without |
| content bottom | ≤ 6.60 |
| footer rule / text | 6.86 / 7.00 |

Row maths: device assets are 458×912 px after padding → `width = height × 0.502`.
Fit check before drawing: `N×w + (N-1)×gap ≤ 11.85`.

## 3. Slide set that actually presents

A 15–17 slide arc that survives questions:

1. Cover — product name, section, "N layar, dua peran, satu sistem".
2. Scope — counts as data (screens, artboards, modules, roles) + what is out of scope.
3. Map — every screen as a thumbnail, numbered, colour-bar per module.
4. System — real tokens pulled from the file: hexes, type scale, radius, components.
5. User flow — 5–6 screens, ascending numbers, connectors on one horizontal line.
6. Other-role flow — same rhythm, different job.
7–14. One screen or pair per slide: claim in the headline, 4–5 numbered
   annotations, one finding box.
15–17. Optional: decision table (problem → decision → which screens prove it),
   open gaps, three-takeaway close. Good for a client or studio review; for a
   group/course presentation the deck is expected to end on its last evidence
   slide, so build the core arc only and add these when asked. Cutting them
   means re-checking footer numbers.

Numbering: use **Roman numerals for sections** (I, II, … XV) so the header
never collides with the screen numbers (01–22) used inside the slides. If the
source numbering has holes (a deleted frame), renumber the screens sequentially
and update every later reference — a missing "04" reads as an error, not as a
file quirk.

## 4. Copy that is not AI slop

- Headline = the screen's plain name: "Verifikasi e-KTP", "Audit trail",
  "Batas transaksi", "Profil saya". A colon-claim ("Settlement: setiap angka
  harus bisa ditelusuri") or an antithesis ("bukti, bukan keyakinan",
  "satu-satunya sumber kebenaran", "memutuskan, bukan mengisi") is the fastest
  way to read as AI copy — cut it and let the presenter make the argument.
- Zero meta. No sentence about the deck, the source file, or the process:
  "semua nilai diambil dari file Figma", "angka ini kami hitung dari file,
  bukan perkiraan", "yang tidak kami kerjakan", "ini yang kami rapikan di
  revisi berikutnya". Anything describing how the deck was made is spoken,
  never printed.
- Annotation = label + one short fact ("Pemisah tipis, tanpa border."), not
  label + fact + why it matters. Two clauses is already one too many.
- Findings stay — they are the value — but as one plain sentence carrying the
  number: "Di state Rp 25 juta, sisa kuota masih Rp 8.550.000." Drop "Temuan:"
  essays and hedges like "bisa dibaca sebagai".
- Section kicker = one word from the module ("DASAR", "PENGGUNA",
  "OPERASIONAL"), never a repeat of the headline sitting right under it.
- Palette follows the user's taste, not the design's chrome: Do rejects dark +
  purple decks. White page, navy `#091B42` ink, one soft accent, red only for
  findings.

## 5. QA loop that converges

```bash
~/.hermes/tools/pptx-venv/bin/python build.py \
  && soffice --headless -env:UserInstallation=file://$HOME/.cache/lo_profile \
     --convert-to pdf --outdir render deck.pptx
python -c "import pymupdf; d=pymupdf.open('render/deck.pdf');\
 [p.get_pixmap(dpi=120).save(f'render/s{i+1:02d}.png') for i,p in enumerate(d)]"
```

- Measure first: `scripts/measure_render_geometry.py render/s05.png --band 2.1 5.3`
  prints each run's left edge, width and gap in inches. Equal numbers = the
  layout is fine; a vision model claiming "uneven phones" is then simply wrong.
- Then `vision_analyze` for what measurement cannot see: is the headline clear
  of the content, does the finding box read as a finding, is any caption orphaned.
- Rebuild the whole deck each pass (build.py is idempotent); never patch the
  .pptx in place while iterating — the next build overwrites it anyway.

## 6. Delivery

- PPTX for editing + PDF for presenting; the PDF has the font embedded.
- Cover credit is the group or course label only ("Kelompok desain produk",
  month/year). Never put the user's own name on the cover unless asked — for
  group work the deck belongs to the group, and he will strip it.
- If the design font is not a system font, attach or name it (Google Fonts,
  OFL) and warn that editing without it shifts the layout.
- Speaker notes per slide (2–4 sentences) are part of the deliverable — they
  are what lets a non-designer present the deck without improvising. Keep
  them even when the visible copy is stripped down to labels.
