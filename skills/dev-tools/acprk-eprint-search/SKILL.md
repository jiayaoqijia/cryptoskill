---
name: eprint-search
description: Search IACR ePrint (with a submission-date window) plus Crossref/DBLP from the command line. Use for novelty checks ("is this idea already taken?"), for building the related-work matrix, and for finding the public ePrint id of a paper before citing it.
---

# eprint-search

## Commands

```bash
S=skills/eprint-search/scripts/eprint_search.py
python3 $S "blind rotation" "programmable bootstrapping" --months 12      # union of phrasings, last 12 months
python3 $S "oblivious key-value store" --crossref --min-year 2019          # + published versions with DOI
python3 $S "division property" --title-only                                # title search only
python3 $S "..." --json > hits.json                                        # for scripting
python3 $S --selftest
```

Exit status 2 means *no source answered* (offline or blocked) — that is "novelty check not performed", never
"no hits". DBLP sometimes serves a bot challenge to scripts; the script detects it and you should add `--crossref`.

## Novelty-check procedure ("is it already taken?")

1. Write the idea as one falsifiable sentence (what object, what improvement, under which assumptions).
2. Generate **5–10 phrasings**: the technique name, the problem name, the object name, the synonym used by the
   neighbouring community (e.g. "digit extraction" / "lowest digit removal" / "floor function"), and the
   name of the closest known baseline.
3. Run them with `--months 12` (always) and without a window (for the classic literature). Add `--crossref`
   for published-only venues.
4. Read the abstract of every hit whose title shares two content words with the idea; open the PDF of any hit
   that shares the object *and* the technique. Snowball: check the "related work" of the 2–3 closest hits and
   the papers that cite the main baseline (Crossref/Google Scholar "cited by").
5. Verdict per idea, logged in `LITERATURE.md` → `## Novelty checks`:
   `- YYYY-MM-DD | query: "..." | sources: eprint,crossref | window: 12m | hits reviewed: N | verdict: clear|overlap:<key>|taken:<key>`
   * `clear`: nothing shares object + technique.
   * `overlap:<key>`: same object or technique, different claim → add a matrix row and a precise "our delta".
   * `taken:<key>`: same claim → stop, tell `pi-orchestrator`; salvage is a new decision, not a rewording.
6. Re-run every 2–4 weeks while the project is live and once more right before submission (ePrint moves fast;
   the `lit-matrix` linter fails if the newest check is older than 30 days).

## Pitfalls

- A concurrent ePrint published during your project is normal; record it with its date — reviewers accept
  "concurrent and independent" only if you can show when you knew.
- Do not trust search-engine summaries of a paper's content; read the paper.
- Title-only search misses papers that use a different name for the same object — always also run full-text.
