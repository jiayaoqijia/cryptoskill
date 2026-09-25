---
name: camera-ready
description: Use after acceptance to produce the final version. Checklist for page limits as the CFP defines them, copyright/licence forms, author-list change policy, full-version vs proceedings builds, artifact links, and final compile checks (0 undefined references, all fonts embedded via pdffonts, no significant overfull boxes, no overprinting).
---

# Camera-ready

## 0. Collect the rules (day 0)

Quote into `SUBMISSION.md` §Camera-ready, with URL and date:

- page limit **and exactly what counts** (e.g. "N pages excluding the bibliography
  only" means title page, abstract, body, acknowledgements and any appendix all
  count; "excluding references and appendices" is different). When in doubt, satisfy
  the strictest reading.
- template/class version, paper size, fonts ("Springer standard fonts, font sizes and
  margins"), whether page numbers must be removed or kept.
- copyright / licence form (IACR copyright agreement, Springer consent to publish,
  ACM rights form, open-access licence choice) and who must sign.
- presentation / video-recording agreements, registration requirement.
- deadline with timezone (AoE vs UTC vs local); convert to your timezone in writing.
- whether the camera-ready is automatically posted (e.g. to ePrint) by the chairs.

## 1. Author-list and metadata changes

- Changes to the author list after acceptance normally require the program chairs'
  approval. Ask early, by e-mail, with a short justification. Typical outcomes:
  approved; or "keep the submitted authors in the proceedings and thank the new
  contributors in the Acknowledgements; list them as co-authors in the full
  version/ePrint". Record the ruling verbatim in `DECISIONS.md`.
- Fill every placeholder (`[[FILL IN]]`) for names, affiliations, ORCID, grants.
- De-anonymise consistently: restore author block, acknowledgements, own repository
  URLs (replace anonymous mirrors with the permanent artifact URL/DOI), self-citations
  may now be first person if the style allows.

## 2. Content changes

- Build `CHANGES.md`: each reviewer request → section/page where it is answered in
  the final version (from the rebuttal triage table). Promised changes must all be
  present.
- Do not add new results that were never reviewed unless the chairs allow it; label
  any post-review corrections.
- Every number still traces to `EVIDENCE.md`; diff all numbers against the reviewed
  version (`pdftotext` both, extract numbers, diff) and explain any change.

## 3. Proceedings build vs full version

- One shared source (`paper.tex`) + two drivers (`main.tex` proceedings,
  `main_full.tex` full version) with a switch (`\newif\iffull`), so the versions
  cannot drift.
- Floats/sections that do not fit the limit live in `\iffull ... \fi`; the
  proceedings version says "see the full version [ePrint ref]" and **the full version
  must be published before the camera-ready deadline** (ePrint entry or artifact
  repository), or the pointers dangle.
- Space tuning allowed only in elastic glue around floats/displays/captions inside
  the proceedings branch; never margins, fonts, `\textwidth`, `\textheight`.
- A `pagemap` helper prints section → page for the built PDF; rerun after each edit.

## 4. Final compile checks (must all pass)

```bash
latexmk -pdf main.tex                     # twice if BibTeX changed; latexmk handles it
python3 skills/camera-ready/scripts/pdf_checks.py main.pdf --log main.log --limit <N>
pdffonts main.pdf                         # every font 'emb yes'; avoid Type 3 bitmap fonts
grep -c '??' <(pdftotext main.pdf -)      # 0
```

- [ ] 0 undefined references/citations, 0 multiply defined labels, no "Rerun" warning.
- [ ] All fonts embedded (fix: vector figures with embedded fonts; `pdflatex` with
      standard `cm-super`/`lmodern`; re-export matplotlib figures with `pdf.fonttype: 42`).
- [ ] No overfull box > ~1pt in the body; report remaining ones with size.
- [ ] No overprinting (overlap scan), especially after negative `\vspace` near floats.
- [ ] References start after the last counted page; the body ends within the limit.
- [ ] Title + abstract + keywords on page 1 if required or desired.
- [ ] Bibliography: published versions over preprints; DOIs where available; braces
      protect acronyms; ePrint author lists match the ePrint page.
- [ ] Figures readable at print size (≥ ~7pt text), colour-blind-safe, captions
      self-contained.
- [ ] PDF metadata: title and authors set correctly now (not empty).
- [ ] Source package (if required) compiles from a clean directory; no unused large
      files; no private comments (`%` notes to co-authors) left in sources.

## 5. Artifact and links

- Replace the anonymous mirror by the permanent URL (repository tag or archive DOI);
  check every URL with `curl -sI` (HTTP 200).
- Tag the exact commit used for the final numbers; mention it in the artifact README.
- If an artifact evaluation track exists, see [artifact-pack](../artifact-pack/SKILL.md).

## 6. Submission

- Upload the PDF + sources + forms; download the uploaded PDF back and compare
  `sha256sum`/`md5sum` with the local file.
- Keep a `camera_ready/README.md` listing files, build commands, page-limit
  verification, and the author checklist (forms signed, full version posted, slides).
