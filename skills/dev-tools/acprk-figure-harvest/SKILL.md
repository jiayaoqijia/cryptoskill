---
name: figure-harvest
description: Harvest figures from a local corpus of public crypto papers (PDF), classify them by type, score their quality, and browse them in a local HTML contact sheet to learn which figure patterns work for a topic. Use before designing figures for a new paper or when extending figures/PATTERNS.md. Output is local-only (copyright).
---
# figure-harvest

Learn figure patterns from the papers closest to yours: related work,
same-venue papers, or the baseline papers. The distilled lessons go into
words. The harvested images are never committed.

## When to use
* At the start of P7 (Writing + Figures), on the related-work PDFs gathered in P1.
* When the target venue or sub-field has conventions you do not know yet.
  Examples: symmetric papers use trail tables and round diagrams, FHE
  papers use bit layouts and pipelines, MPC papers use functionality boxes.
* When extending `figures/PATTERNS.md` with a new pattern.

## Procedure
1. **Assemble the corpus.** Use a directory of *public* PDFs, such as ePrint
   downloads of the related-work list. Exclude your own drafts and anything
   under embargo:
   ```bash
   python3 figures/harvester/harvest.py related_work/papers \
       --out /tmp/fig_gallery --exclude drafts --exclude ours --exclude '.zip' \
       --jobs 8 --timeout 90 --max-pages 60
   ```
   * `--exclude` takes a substring glob, or `re:REGEX` for a regular expression.
   * Directories are searched recursively.
   * Duplicate PDFs are skipped, detected by hash or by first-page text.
2. **Browse.** Run `python3 figures/harvester/gallery.py /tmp/fig_gallery` and
   open `index.html`. The page groups figures by type and sorts them by
   quality. It has a type filter and a minimum-quality slider.
3. **Inspect the best 10–20** for your planned figure types. For each one, note in words:
   * what makes it readable
   * which encodings it uses
   * how it handles baselines, units and log axes
   * what you would not copy
4. **Distil.** Update the project's `paper/figs/NOTES.md`, or
   `figures/PATTERNS.md` if the pattern is new. Follow
   `figures/gallery_index.template.md`:
   * pattern name
   * public ePrint ID and figure number ("see e.g.")
   * what works
   * pitfalls
   * the template that implements it (create one if missing: synthetic data,
     plus a PDF+PNG in `figures/examples/`)
5. **Discard.** Delete the gallery, or keep it outside the repository.
   Never `git add` a harvested PNG.

## How it works (so you can trust or tune it)
* **Captions.** A text block counts as a caption if its first line matches
  `Fig.|Figure|图 <n>` followed by punctuation, or starts with a bold label.
  Running-text mentions such as "Fig. 3 shows…" are rejected.
* **Clip.** The clip is seeded with drawings or images that lie within
  40 pt above the caption (then below, as a fallback). It then grows through
  vertically adjacent graphics with gaps under 14 pt. Growth stops at
  paragraphs of running text (wide, multi-line, not overlapping graphics) and
  at other captions. Nearby label text is absorbed, and the clip is padded
  by 4 pt. Figures made only of text, such as unframed algorithms, fall back
  to the band between the preceding paragraph and the caption.
* **Statistics:**
  * path item counts (lines, curves, rects, filled rects)
  * horizontal and vertical ticks (an axis needs both)
  * arrowheads and XOR glyphs
  * grid detection
  * vector colour count and rendered-pixel colour count
  * whitespace fraction and words per square inch
  * effective raster dpi
* **Type:** the classifier combines caption-keyword scores with statistic rules.
* **Quality:** the score starts at 50.
  * Vector content: +20.
  * Rasters: from +15 down to −15, depending on dpi.
  * Colours: +10 for 2–7 colours, −10 for more than 14.
  * Whitespace: +10 for 45–90%.
  * Very small crops and very dense text are penalised.
* **Robustness:** each PDF runs in a forked process with a timeout, and
  per-page exceptions are recorded without stopping the run.
  `--selftest` builds a synthetic PDF and checks the full pipeline.

## Known limitations
* Classification is about 70% accurate. Plots whose text was converted to
  outlines, and figures that are only rasters, rely on caption keywords.
* Multi-panel figures that sit side by side with separate captions can merge
  into one crop.
* Two-column layouts (ACM/IEEE) sometimes pull in the neighbouring column's
  graphics. Check the crops.
