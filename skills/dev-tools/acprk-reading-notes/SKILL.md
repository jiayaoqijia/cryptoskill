---
name: reading-notes
description: Write structured, dated, falsifiable reading notes for a paper (claims, parameters, numbers with page pointers, hidden assumptions, reusable tricks, open problems). Use whenever an agent reads a paper that may be cited, compared against, or mined for ideas.
---

# reading-notes

Notes are the compressed layer every later agent reads *before* opening PDFs (retrieval order: own notes →
papers → textbooks → baseline code). They must be trustworthy enough to cite from and honest about what was
not read.

## File and naming

`notes/papers/<year>-<id-or-shortname>.md` (e.g. `notes/papers/2021-266-vole-psi.md`). One file per paper;
append dated sections on re-reads instead of overwriting.

## Template

```markdown
---
key: RS21                       # bib key in refs.bib (must pass bib-verify)
eprint: 2021/266                # or doi
read: 2099-01-31 (sections 1-4, 6; appendix skipped)   # say what you did NOT read
reader: lit-scout
---
## One-line contribution
## Setting (model, parameters, security level, hardware)
## Claims (numbered, each falsifiable, with page/section)
C1. ... (Thm 3, p.12)
## Concrete numbers (value, unit, parameters, source pointer)
## Technique in 5 lines (the mechanism; which object is changed)
## Hidden assumptions / fixed parameters
(e.g. "power-of-two ring only", "sparse secret", "LAN only", "the base B is fixed to 2^k without justification")
## Representation tricks (one line each: "turns X from fixed into a free variable")
## Weak points / what a reviewer would attack
## Open problems stated by the authors (quote + page)
## Relevance to us: compare | reuse | mine | ignore  — and why
```

## Rules

- Every number carries a source pointer; every claim is phrased so it could be wrong.
- Distinguish "the paper proves", "the paper measures", "the paper conjectures/heuristic".
- Record what you skipped. "Read all 28 papers" is a claim the PI may audit.
- If the note disagrees with another note, add it to the project's errata section and tell `pi-orchestrator`.
- Never paste long verbatim passages; paraphrase and point.
- Negative notes ("this line does not help because ...") are kept — they stop the next agent repeating the read.
