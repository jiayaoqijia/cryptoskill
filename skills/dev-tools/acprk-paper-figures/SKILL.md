---
name: paper-figures
description: Produce publication-quality figures for a cryptography paper in the house style (LNCS/ACM/IEEE sizes, Computer Modern or Times fonts, vector PDF, colour-blind-safe palette), starting from the pattern catalog and templates in figures/. Use when a paper needs a plot, a results table or a TikZ diagram, or when auditing existing figures before submission.
---
# paper-figures

Make every figure **at final size, in vector, from logged data, with a stated
take-away**. The toolkit lives in `figures/`: style sheets, `palette.py`,
16 matplotlib templates, 5 TikZ templates and `PATTERNS.md`.

## When to use
* Phase P7 (Writing + Figures): turning `results/` and EVIDENCE rows into figures.
* Phase P8 (camera-ready): re-rendering for a different venue class, or fixing
  reviewer complaints ("figure unreadable in print", "legend covers data").
* Any time a figure is drafted with default matplotlib settings.

## Procedure
1. **State the claim first.** Write the one sentence the figure must prove.
   It becomes the first sentence of the caption. If no claim exists, the
   answer is probably a table (C16) or no figure at all.
2. **Pick the pattern** from `figures/PATTERNS.md`:
   * ratio vs. a reference → C1
   * where the time goes → C2
   * asymptotics → C3
   * parameters → C4 or C14
   * two competing costs → C5
   * noise or depth → C6 or C7
   * S-box properties → C8
   * rounds and security margin → C9
   * failure probability → C10
   * approximation quality → C11
   * regime change → C12
   * linear-transform structure → C13
   * a speed-up claim a sceptic may doubt → add C15
   * a protocol or pipeline → D1 or D2
3. **Copy the template** (`figures/templates/pNN_*.py` or `tikz/*.tex`) into
   the project's `paper/figs/src/`. Replace the synthetic arrays with loaders
   that read `results/*.csv|json`. Never type numbers by hand.
4. **Size and font by venue.** Call `P.figure(venue, width="column"|"full"|fraction, aspect=...)`.
   * LNCS: 4.80 in (12.2 cm), Computer Modern.
   * ACM: 3.33 / 7.00 in, Libertine or STIX.
   * IEEE: 3.50 / 7.16 in, Times or STIX.
   * In LaTeX, `\includegraphics[width=\textwidth]` (or `\columnwidth`)
     with no further scaling.
5. **Encode redundantly.**
   * Ours is `P.OURS` and baselines use `P.baseline_style(i)`.
   * Every series gets a marker or dash in addition to its colour.
   * Categorical colours go in fixed order and never cycle past 8.
   * Sequential data uses one hue. Diverging data is blue↔red with a grey
     midpoint.
6. **Label directly.** End-of-line labels beat legends. Use one reference
   line with its name, not a bar. Print values only on the bars that carry
   the claim. Use a log axis once the range exceeds about 30×.
7. **Render and inspect.** `python3 paper/figs/src/fig_x.py`, then open the PNG. Check for:
   * label collisions and clipped text
   * a legend covering data
   * greyscale readability (`pdftoppm -gray -r 150 fig.pdf /tmp/g`)
   * tick labels shown as `2^k` for powers of two
8. **Link to evidence.** Add the figure script path and the input data file
   to each EVIDENCE row whose number appears in the figure.
9. **Run the checklist** at the end of `PATTERNS.md`, then commit the
   figure's PDF, its script and its data pointer.

## Checklist (quick)
- [ ] Vector PDF with fonts embedded (`pdffonts fig.pdf` shows no Type 3 fonts, unless usetex was used).
- [ ] Final size, and 7–8 pt text that matches the caption font family.
- [ ] One y-axis, with units in both axis labels.
- [ ] Ours is blue, baselines are grey, and every series has a marker or dash.
- [ ] Readable in greyscale and by colour-blind readers. The palette passes `python3 figures/style/palette.py`.
- [ ] No pies, no 3-D, no rainbow colormaps, no coloured plot backgrounds, no titles inside the axes that duplicate the caption.
- [ ] Every number traces to EVIDENCE, and synthetic or toy content is labelled as such.
- [ ] The caption's first sentence is the take-away, and it defines all abbreviations.
- [ ] Tables use booktabs, mark the best value in bold, and use consistent decimals.

## Tools
* `figures/style/palette.py`: `use`, `figure`, `size`, `line_style`, `baseline_style`, `direct_label`, `save`, `check_palette`.
* `figures/templates/run_all.py` renders every template, which is useful as a smoke test after style edits.
* `make -C figures/templates/tikz` builds the TikZ diagrams. `crypto-tikz.sty` can be `\usepackage`d in a paper.

## Anti-patterns seen in published crypto papers (in the harvested corpus)
* Pie charts used for stage breakdowns. Use C2 instead.
* Coloured plot backgrounds, bold sans-serif titles inside the axes, and default-library colours.
* Raster screenshots of plots that print at under 150 dpi.
* Speed-up claims shown without any run-to-run spread. Add C15.
* "Before" and "after" pipelines drawn with different layouts. Keep the layout identical and tint only the changed stage.
