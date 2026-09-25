# 07 Preliminaries

## Job

Fix notation and recall exactly the background the later sections use. Nothing more:
standard material that is not referenced later goes to an appendix or is cited.

## Structure

```
2.1 Notation              compact table (symbol | meaning), 8–15 rows, 2 columns or a
                          4-column (symbol | meaning | symbol | meaning) layout
2.2 The <scheme/model>    e.g. "The <X> scheme", "Security model", "Threat model"
2.3 The <pipeline stage>  the procedure the paper modifies, in the paper's notation
2.4 <prior technique A>   one subsection per prior technique the construction builds on,
2.5 <prior technique B>   stated as definitions/lemmas with citations
2.6 <math tool>           e.g. characters, lattices, Walsh spectra, hashing bounds
```

## Rules

- The notation table stays inside the Notation subsection, is short, and lists only
  symbols reused at least twice. Declare deviations from common conventions
  explicitly ("our indexing differs from the one traditionally used for AES").
- Distinguish rings/fields precisely (F_p vs Z_{2^k}); define operators used with
  non-standard meaning (e.g. "+" for XOR).
- Short proofs of recalled facts may be given in place if a reviewer asked for them
  or if they fix a gap in the literature; otherwise cite.
- Prior techniques are recalled at the level needed to state your theorems, in your
  notation, with the original cost formula.
- If a reviewer is likely to be unfamiliar with the area (general IACR audience),
  keep one paragraph of intuition per subsection; newcomers flag "background too
  brief" as a weakness.

## Checklist

- [ ] Every symbol in the notation table is used in ≥ 2 sections.
- [ ] Each later theorem's hypotheses are expressible with what §2 defines.
- [ ] No material here that no later section uses.
