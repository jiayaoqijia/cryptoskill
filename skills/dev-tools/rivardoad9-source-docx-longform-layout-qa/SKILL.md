---
name: docx-longform-layout-qa
description: Use when generated DOCX pages have layout defects.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [docx, layout, pdf, qa]
    related_skills: [docx, pdf]
---

# Long-form DOCX layout QA

## When to Use

Use when a generated Word article, report, or thesis shows orphan captions, large white gaps, tables jumping pages, landscape figures that overflow, or a title breaking mid-phrase. Also run it as the final pass before delivering any generated long-form docx.

Generator scripts (python-docx) produce correct text with wrong layout. Diagnose by measuring the rendered PDF, not by eyeballing pages.

## Loop

1. Build docx, convert: `soffice --headless -env:UserInstallation=file:///home/ubuntu/.cache/lo_profile --convert-to pdf --outdir . file.docx`
2. Measure fill per page with PyMuPDF:

```python
import pymupdf
d = pymupdf.open('out.pdf')
for i in range(d.page_count):
    p = d[i]
    bl = [b for b in p.get_text('blocks') if b[3] < 790]  # drop footer page number
    gap = round((790 - max(b[3] for b in bl)) / 28.35, 1) if bl else 0
    print(i + 1, 'L' if p.rect.width > p.rect.height else 'P', gap)
```

Gap > 4 cm on a body page is a defect; a gap before a landscape section or at the end of references is normal.
3. Render only suspect pages at 115–120 dpi and check with vision (caption adjacency, header repeat, clipping).

## Causes and fixes

- **Caption orphaned from figure/table**: put `keep_with_next` on the paragraph *before* the caption (the picture paragraph, or the last row/paragraph of the table).
- **Long table jumping pages, half-empty page before it**: `keep_with_next` on every row forces the table to stay whole. Apply only when `len(rows) <= 15`; above that let rows split.
- **Mid-word breaks / table wider than margins**: `w:tblLayout type=fixed` plus explicit cell widths.
- **Landscape figure**: section break pair (`landscape` before, `portrait` after); caption and source live inside the landscape section, and that page must be measured too.
- **Title breaking mid-phrase**: insert an explicit break (`\n` in run text becomes `<w:br/>`) at a phrase boundary.

## Editing generated source safely

Never slice a generator by `s.index('token')` when `token` also appears as `def token()` — it silently eats function definitions. Use unique multi-line anchors, assert the slice, and `py_compile` before running.

Keep document content in a JSON spec (paragraph text plus size/bold/align/indent, table rows and widths, image path and width) extracted from a known-good docx. Then layout work is spec reordering plus renderer fixes, and numbers never get retyped.

## Final content checks before delivery

- Cross-check every β and p quoted in prose against the results JSON; list any value that is not found (a sensitivity run legitimately adds values from a second file).
- Verify every in-text citation has a reference entry and vice versa.
- Confirm hypothesis verdicts agree with their p-values.
- Table and figure numbers must ascend in document order after inserting a new table — renumbering is the most common miss.
