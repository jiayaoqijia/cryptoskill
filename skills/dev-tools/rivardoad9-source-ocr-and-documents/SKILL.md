---
name: ocr-and-documents
description: "Extract text from PDFs/scans (pymupdf, marker-pdf)."
version: 2.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [pdf, docx, powerpoint]
---

# PDF & Document Extraction

For DOCX: see the `docx` skill (create/edit) or use `python-docx` for structured reads.
For PPTX: see the `powerpoint` skill (full create/read/edit support).
For PDF manipulation (merge, split, forms, watermarks, creation): see the `pdf` skill.
This skill covers **text extraction from PDFs and scanned documents**.

> **Coming from a `read_file` EXTRACTION COVERAGE WARNING?** `read_file` auto-converts local PDFs but reads the text layer only; the warning footer lists the pages that yielded no text (scanned images). For a handful of pages, render + vision is fastest: `pdftoppm -jpeg -r 150 -f N -l N file.pdf /tmp/page` then `vision_analyze` each image. For bulk OCR of many pages, use marker-pdf below (Step 2).

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Scanned PDF with no text layer (tesseract, light)

When `page.get_text()` returns almost nothing, the PDF is pages of images. For a handful of pages,
skip the 3-5 GB marker install and use tesseract:

```bash
python - <<'PY'
import pymupdf
doc = pymupdf.open("scan.pdf")
for i, page in enumerate(doc):
    page.get_pixmap(dpi=300).save(f"p{i+1}.png")
PY

for f in p*.png; do
  tesseract "$f" "${f%.png}" -l eng --psm 3
  tesseract "$f" "${f%.png}" -l eng --psm 3 tsv
done
```

`--psm 3` handles multi-column magazine pages better than the default. The `.tsv` output is one word
per row with `left top width height conf`, which is how you locate a specific figure on the page.

**Verify every number before it reaches a deliverable.** Search the figure in the `.tsv`, take its
bounding box, crop it with a margin at 2x LANCZOS, and read the crop with `vision_analyze`. A single
full-page OCR pass confuses `1`/`l`, `0`/`O` and `%`/`4`, and drops apostrophes in contractions, so a
stat or quote copied straight from the text can be wrong while looking perfectly legible. Confirm the
crop, then write it.

Feed `vision_analyze` a copy scaled to about 1600 px on the long side; full-resolution 300 dpi pages
are larger than the image endpoint accepts.

---

## Unlimited-OCR 2 (Baidu) via HF Space, GPU-free

`baidu/Unlimited-OCR` (30k stars, MIT) parses tens-to-hundreds of pages in one pass with SR-SWA, so
memory stays flat as the document grows. Weights are ~10 GB and the reference run is an A800-80GB,
so it cannot run on a 2-core/3 GB CPU box. Use the Space: `baidu/Unlimited-OCR-2` runs on ZeroGPU
a10g, and its API takes `/parse_page` (one image) or `/parse_document` (list of images), returning
`{text, markdown, done}` where blocks carry `[x1,y1,x2,y2]` boxes and tables come out as HTML.

Wrapper on this box: `python3 ~/.hermes/scripts/ocr_doc.py file.pdf [--dpi 140 --max-pages 20]`
writes `file.md` beside the source.

Measured at 140 dpi on a text-and-table PDF: 23 s per prose page, 48 s per dashboard page, every
unique word of the text layer recovered with zero invented words, tables preserved as HTML. On a page
holding a screenshot of SQL, the code image was skipped entirely, so check image-only blocks before
trusting a full-page parse.

**Quota trap:** anonymous ZeroGPU allows only ~2 runs, then `AppError: You have exceeded your ZeroGPU
runs limit`. A free Hugging Face token raises it; with no token the Space is a demo, not a pipeline.

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
