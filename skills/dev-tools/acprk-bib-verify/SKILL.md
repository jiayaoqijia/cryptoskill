---
name: bib-verify
description: Verify every BibTeX entry against IACR ePrint, Crossref/DataCite and DBLP and flag fabricated, garbled or placeholder references. Use before any draft leaves the machine, after any agent adds citations, and as the P1 and P8 gate item.
---

# bib-verify

A fabricated reference is a research-integrity failure, not a typo. Typical LLM-era failure modes seen in
practice: invented co-author lists on a real paper; a placeholder like `{Chen and others}` + a journal name
propping up a row of a comparison table and a "nobody has done X" claim; a key that points at a *different*
paper by the same group; an ePrint number written from memory that belongs to another paper. When this repo's
own reading lists were drafted from memory, the verifier caught three such errors out of ~110 entries.

## Procedure

1. Run the checker (network needed; polite 1 req/s):
   ```bash
   python3 skills/bib-verify/scripts/verify_bib.py refs.bib --json bib-verify.json > bib-verify-report.md
   ```
   Resolution order: ePrint id (from `eprint=`, `url=`, `howpublished=`...) → OAI record; `doi=` → Crossref,
   then DataCite (Zenodo/LIPIcs/arXiv DOIs); otherwise a title search (DBLP if it answers, else Crossref).
2. Triage every non-`VERIFIED` row by hand:
   | status | meaning | action |
   |---|---|---|
   | `MISMATCH` | the id/DOI resolves to a *different* title or author set | fix the id or the metadata; if the cited claim was about the other paper, re-read and re-check the sentence that cites it |
   | `NOT_FOUND` | nothing plausible exists | treat as fabricated: delete, or find the real source and re-cite; re-check every sentence that relied on it |
   | `WEAK` | similar title only | open the landing page, compare authors/year/venue manually |
   | `UNCHECKED` | offline / service error | re-run later; never ship with UNCHECKED rows |
3. Lint flags (placeholder authors, `and others` only, missing year, `% UNVERIFIED` marker, duplicate titles) must
   be cleared too.
4. For every *changed* entry, grep the paper for its key and re-read the citing sentence: a wrong reference often
   props up a wrong claim (a comparison row, a novelty statement, a parameter).
5. Record the run in `LITERATURE.md` (date, counts) and keep `bib-verify-report.md` next to `refs.bib`; the
   `phase-gate` script checks that the report is newer than the bib and clean.

## Rules

- Prefer the published version (DOI) for the final paper; keep the ePrint id in `eprint=` so it can be re-checked.
- Never "fill in" missing authors from memory. Copy from the ePrint/DOI landing page.
- Anything added without checking gets a `% UNVERIFIED` line directly above the entry until verified.
- Venue strings are not machine-verified; check them on the DOI landing page.
- Offline: `--offline` still runs the static lint; the gate stays closed until an online run passes.

## Files

- `scripts/verify_bib.py` — dependency-free checker (`--selftest`, `--selftest-online`, `--only k1,k2`, `--offline`).
