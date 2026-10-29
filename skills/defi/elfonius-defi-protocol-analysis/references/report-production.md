# Report Production

## Output contract

| Mode | Pages | Contents |
|---|---|---|
| Screen | 1 | Header, bottom line, 3 themes, scorecard, verdict, sources |
| Standard | 3–5 | Executive summary, sections, 2–3 tables, decision, monitoring |
| Deep | 8–15 | Cover, one-page executive summary, 13 sections, charts, IC summary, workpaper |

Deep mode must include:

- a cover with title, verdict, date and four metrics;
- a one-page executive summary;
- charts with source and as-of captions;
- a valuation/scenario table;
- a risk matrix;
- a monitoring dashboard;
- page numbers and a footer;
- no internal checklist, unfilled placeholder or empty table.

## Structure

1. Cover.
2. Executive summary: what it is, why now, verdict, three numbers, scorecard, what to monitor.
3. Decision frame and exact target.
4. Full stack.
5. Product/mechanism.
6. Market/competition.
7. Usage/demand.
8. Fees/revenue/unit economics.
9. Token/value capture.
10. Liquidity/exit.
11. Collateral/oracle.
12. Security/audits.
13. Governance/legal.
14. Dependencies/systemic risk.
15. Market/technical/community.
16. Valuation.
17. Risk/stress/portfolio fit.
18. Decision and monitoring.
19. Sources and methodology.

## PDF pipeline

1. Write the report as semantic HTML with CSS page rules.
2. Render charts at 200–220 dpi with a font that supports the report language.
3. Print to PDF with headless Chromium:
   `chrome --headless=new --disable-gpu --no-sandbox --allow-file-access-from-files --virtual-time-budget=1500 --no-pdf-header-footer --print-to-pdf=out.pdf file:///.../report.html`
   If a system Chrome is absent, use Playwright's bundled Chromium (`p.chromium.executable_path`) rather than skipping the PDF.
4. Add page numbers, footer and metadata with PyMuPDF; embed a Unicode TTF for Turkish/other non-ASCII text.
5. Render selected pages to PNG and inspect before delivery.

## Pagination and flow

- Do not force every section onto its own fixed A4 page. Short sections leave 30–50% blank; use a continuous flow with page breaks only for cover, executive summary and IC summary.
- Keep headings with the next block (`break-after: avoid`), and keep tables/charts `break-inside: avoid`; a full-bleed cover can use `@page:first { margin:0 }` with normal `@page` margins for the body.
- Render, count pages, and inspect **every page** for orphan headings and blank bottoms. A 19-page report with half-empty pages is a layout defect, not depth; a 15-page flow is fine.
- Bookmark with a unique heading phrase; a generic phrase can match the executive summary. Add metadata and footer/page numbers after Chromium; skip the cover.
- Keep chart captions short or wrap them; at 7.6 pt a long caption clips at the page edge.

## Design rules

- A4, 18–20 mm margins, 9.5–11 pt body, 1.45–1.55 line height.
- Sans-serif headings; readable body; no decorative chartjunk.
- One idea per section; a chart must answer a question, not fill space.
- Every chart: title, unit, source, as-of date, caption.
- Tables: one unit and one period per column; right-align numbers; no empty rows.
- Use color to distinguish, not to decorate; ensure grayscale readability.
- Keep the verdict visible on the cover and in the executive summary.
- Do not put the workpaper in the report; the report is the argument, the workpaper is the evidence.

## Quality checks

- [ ] Every material number has a source and date.
- [ ] TVL, fees, revenue, tokenholder revenue and FDV definitions are stated.
- [ ] APY decomposition is visible.
- [ ] Gate status and the deciding component are explicit.
- [ ] Top three risks and falsifiers are on one page.
- [ ] Exit path and queue are described.
- [ ] Charts have captions and sources.
- [ ] No placeholders, internal notes or empty tables.
- [ ] Every page inspected; no orphan heading or blank-bottom page.
- [ ] Page numbers and metadata are present.
- [ ] The report reads as one argument, not a checklist.
