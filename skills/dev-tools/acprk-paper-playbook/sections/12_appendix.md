# 12 Appendix

## Principle

Supplementary material: reviewers are not obliged to read it, so **nothing in the
appendix may be load-bearing for the body's claims**. Put this as a comment at the
top of the appendix source so every co-author sees it.

For journals that count reviewed material toward the page limit (e.g. some IACR
journals count proofs that require careful review), putting proofs in an appendix
does not save pages; check the CFP.

## Organisation

- Each appendix section opens with one paragraph stating which body results it
  supports, referencing body numbers with `\Cref` (no renumbering of restated
  theorems).
- Proofs appear in the order of the body theorems; worked examples come after the
  theorem they illustrate and must be recomputable by a script listed in EVIDENCE.
- Algorithms in the appendix use exactly the body's symbols.
- Appendix tables are generated from the same data files as body tables.
- Typical experiment appendix: D.1 full instance list, D.2 per-instance security
  estimates (with explanation of any "∞"/not-applicable entries), D.3 derived bounds,
  D.4 reproduction (scripts, commands, log paths, machine load reference), D.5
  operation counts, D.6 integration details.
- Every "see the appendix" in the body names the exact subsection label.
- Do not `\input` files that are entirely commented out.

## Full version vs proceedings version

Use one shared source with a switch (e.g. `\newif\iffull`) so the proceedings build
and the full version (ePrint/artifact) cannot drift apart. Floats that do not fit the
proceedings limit can live in `\iffull ... \fi`. If the proceedings version points to
a full version, the full version must actually be published before the camera-ready
goes out. See `skills/camera-ready`.

## Checklist

- [ ] "Not load-bearing" comment at the top of the appendix source.
- [ ] Each appendix section states which body results it supports.
- [ ] Restated theorems keep body numbering.
- [ ] All body pointers to the appendix are specific labels.
