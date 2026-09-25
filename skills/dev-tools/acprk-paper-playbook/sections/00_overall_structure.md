# 00 Overall structure, page budget, layout rules

## Default skeleton (IACR LNCS conference paper)

Page counts are for a body limit of roughly 25–30 LNCS pages; scale proportionally.
Always check the current CFP for the actual limit and for what counts toward it.

| § | title | share of body | job |
|---|---|---|---|
| — | Abstract + keywords | page 1 | state of the art → our technique → results + artifact |
| 1 | Introduction | ~5% | funnel from field to bottleneck; pipeline; objective equation; open question |
| 1.1 | Related Work | ~7% | comparison table + axis paragraphs + bridge + "Our work" |
| 1.2 | Our Contributions | ~4% | lead-in + 3–4 ordered bullets |
| 1.3 | Technique Overview | ~12–15% | recall prior routes → reduce to precise questions → insights → figure |
| 1.4 | Organisation (optional) | 2–3 lines | only if the paper is long |
| 2 | Preliminaries | ~12–18% | notation table; scheme recap; only what is reused later |
| 3–5 | Main construction(s) | ~35% | theorem → construction → cost / selection rule → algorithm |
| 6 | Security / correctness | varies | security claim, attack checklist, noise/failure analysis |
| 7 | Implementation and evaluation | ~12–15% | baselines, platform, parameters, configurations, results, ablation, comparison |
| 8 | Conclusion | ≤ 0.5 page | two to three sentences |
| A– | Appendix | unlimited | proofs, extra tables, reproduction details |

Variants:

- **Symmetric design papers (ToSC/FSE):** security analysis is usually the largest
  section (roughly a quarter to a third); a separate *Design rationale* section is
  longer than the specification itself; related work may sit in a "state of the art"
  subsection of the constraints section.
- **Cryptanalysis papers:** the target's specification goes in §1 (e.g. §1.2), not in
  its own section; the core distinguishing property gets its own section, the attack
  another.
- **Security conferences (CCS/S&P/USENIX/NDSS/PoPETs):** two-column formats; threat
  model and system overview are expected early; evaluation carries more weight.
- **Theory venues (TCC):** no experiments section; the technique overview often
  becomes the main exposition.

## Page discipline

Legal ways to save space, in order of preference:

1. Tighten floats: algorithms `\footnotesize`, tables `\scriptsize` with
   `\arraystretch` 0.88–0.92, `\tabcolsep` 2.5–3pt.
2. Reduce global float/display glue in the preamble (`\textfloatsep`, `\intextsep`,
   `\floatsep`, `\abovedisplayskip`): modest reductions only.
3. Scale TikZ figures by 5–15%.
4. Remove footnote URLs duplicated elsewhere.
5. Only then cut sentences — cut adjectives before content, never cut numbers'
   scoping sentences.

**Forbidden (desk-reject risk):** `geometry` or any margin change, font-size change,
line-spacing change, removing page numbers when the CFP requires them.

**Overprinting trap:** a negative `\vspace` immediately before a float
(`algorithm`/`table`/`figure`) can make text overprint the float in the PDF while the
editor preview looks fine. Put negative glue *inside* the float before `\end{...}`,
or delete it; scan the PDF with the camera-ready overlap checker.

After every edit near the limit, rebuild and confirm the conclusion still ends on the
last allowed page (see `skills/camera-ready`).

## Notation and naming freeze (before writing, grep after writing)

- One concept, one symbol. Keep a table in `paper/NOTATION.md` (symbol, meaning,
  first defined in §). Replace globally and grep for the old symbol afterwards —
  including glued macros like `\inS` produced by careless replacement.
- One name for the framework/object: pick one word (e.g. "unified" vs "general") and
  use it in the title, section headings, figure captions, contributions and overview.
- Write membership as `$x \in S$`, not `$S \ni x$`.
- Theorem numbers in the appendix refer back with `\Cref` to the body numbering; do
  not renumber restated theorems.
- Formulas in the overview are **copied** from the body statements, not retyped.

## Global style rules (distilled from author preferences)

- Avoid em/en dashes as sentence punctuation; use commas, colons or separate
  sentences. (Ranges like `2--3` are fine.)
- No "explanatory" mini-headings such as "Why X is needed" or "Where the cost goes";
  they read as padding. Use statement-style paragraph headings (see overview file).
- Keep the notation table compact and inside the Notation subsection.
- Make the paper standalone for a general cryptographic reader: the first pages
  (title, abstract, introduction) must summarise the contribution without the body.

## Checklist

- [ ] Section shares roughly match the budget; the conclusion is on the last body page.
- [ ] No layout-changing package; page numbers present; paper size as required.
- [ ] Notation table frozen; old symbols grep to zero.
- [ ] Framework name identical in title, headings, captions, contributions, overview.
