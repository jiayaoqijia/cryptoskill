---
name: falsify
description: Red-team protocol for trying to refute a research claim (theorem, speed-up, security level, novelty) before anyone else does. Use at the P6 falsification gate, before any number or theorem goes into the paper, and whenever a sub-agent reports a surprisingly good result. Produces a verdict of survived, weakened or refuted, with evidence, in CLAIMS.md.
---
# falsify: try to break the claim before a reviewer does

## Principle

The job is to **refute** the claim, not to confirm it. An agent handed a framework
tends to collect supporting evidence and amplify a wrong premise. In
practice, most refuted claims in multi-agent rounds turn out to be the
*orchestrator's own* hypotheses. So:

- The proposer first writes the claim as a **falsifiable statement**. It names exact
  quantifiers and parameters, gives a *kill switch* (the observation that would refute
  it), and describes the smallest experiment that could refute it.
- The falsifier's prompt says: "Your primary task is to verify this, not to redo it.
  If it is wrong, say exactly where; that is worth more than a confirmation."
- Every attempt must **actually run** something: a computation, a script or a search.
  Report real outputs. Never invent them.
- If no counterexample is found, say "could not refute" and list what was tried. Do not
  hide behind vague wording.

## Input

A row in `CLAIMS.md` (`ID | claim | proposer | status | falsifier evidence | EVIDENCE refs`)
with status `open`, plus the sources it cites (THEORY.md section, EVIDENCE rows, logs,
code).

## Attack order (cheap and decisive first)

Work through all six. Stop early only on a clean refutation.

1. **Definitions.** Are all objects well-defined for every parameter allowed? Does a
   symbol mean the same thing in the abstract, the theorem and the experiment? Typical
   failures: two different definitions of the same quantity (for example, a padded
   length and a polynomial degree written with one symbol); an "element of order r"
   that is not guaranteed to exist; a cost measure that counts different operations in
   the two arms.
2. **Quantifiers.** Is it "for all" or "there exists"? For all parameters, or only for
   those satisfying an unstated side condition? Does the proof use the hypothesis in
   the direction stated? Is the claimed injectivity or existence only checked on the
   examples? Is a necessary condition presented as sufficient? Write the negation and
   try to satisfy it.
3. **Edge parameters.** Try the smallest values (p = 2, 3; n = 1; r = 1, 2), boundary
   values (p ≡ 3 mod 4 when the claim needs p ≡ 1; B at the admissibility threshold),
   degenerate cases (a trivial group, a zero polynomial, an empty set) and the
   *largest* parameter used in the experiments. Do a small exhaustive search wherever
   feasible, for example with `skills/sage-check`. One finite counterexample settles
   the question.
4. **Numeric recomputation.** Recompute every number in the claim from the raw logs.
   Do not use the paper's table or a previous summary. Check:
   - that the rows of a table come from the *same* configuration. Mixing the
     fastest-time column from one setting with the fewest-operations column from
     another is a classic failure;
   - that "best vs best" is really best vs best, and the ratio uses the stated protocol;
   - arithmetic inside tables (sums, degrees, ratios, rounding: `round` vs `ceil` can
     differ by exactly 1);
   - that the same number is identical everywhere it appears: abstract, introduction,
     evaluation, appendix;
   - that failure modes are attributed correctly. An uncaught exception with a core
     dump is not a "graceful noise-budget exhaustion" until the error message says so.
5. **Hidden baseline unfairness.** Different parameters (the library's real preset vs
   the one printed in the paper), threads, compiler flags, machine, day or load; a
   stale build; a weaker baseline than the strongest available; a cited number never
   reproduced locally; offline work moved out of the timed region; a
   single-configuration win reported as general. Cross-check with
   `skills/baseline-pin` and `skills/bench-protocol`.
6. **Literature pre-emption.** Search for the core identity or algorithm under other
   names. Check: the target paper's own citations; ePrint from the last 24 months;
   follow-ups citing the baseline; the textbook treatment (ask `math-librarian`).
   A reformulation of known work ("X is exactly Y viewed as a module over Z") downgrades
   novelty even when everything is correct. Record the ePrint or DOI. Never cite from
   memory; if a reference cannot be verified, write "needs verification".

## Verdict taxonomy (write into the CLAIMS.md status column)

| verdict | meaning | required evidence |
|---|---|---|
| `survived` | every attack in the order above was attempted and none succeeded | list of attempts, with commands and outputs or the searches run |
| `weakened` | true only under an extra hypothesis, over a smaller parameter range, with a smaller constant, or with less novelty than claimed | the precise restated claim, plus the counterexample or recomputation that forced it |
| `refuted` | a counterexample, a recomputation contradicting the number, or prior art containing the result | a minimal reproducible counterexample (script plus output) or the exact prior-art citation |

A `weakened` verdict must include the **replacement claim text**. The proposer either
adopts it or appeals to `pi-orchestrator`. Keep `refuted` rows in the table with
their reason, so no one repeats the dead end.

## Output format

```markdown
| C7 | For every prime p ≡ 1 (mod 4) and every B ≤ B_max(p), map φ_B is injective | theorist | weakened | sage-check exhaustive p<200: first failure p=13, B=2 (script: checks/c7.py, output: results/c7.txt). Holds when 2(|A|+1)B < p (sufficient, not necessary). Replacement: "... if 2(|A|+1)B < p" | E14 |
```

Also append to the shared errata section (`STATE.md` → "Errata and rolling updates")
when a verdict changes something other agents rely on. State which source now wins.

## Veto

`falsifier` holds a veto. No claim with status `open` or `refuted` may appear in
`paper/`. A `weakened` claim may appear only in its restated form. `writer` checks
CLAIMS.md before each section, and `submission-rebuttal` re-checks before submission.

## Review-brief pattern (for parallel falsifier sub-agents)

When fanning out, give each sub-agent:

- one group of claims (arithmetic and units; performance numbers; artifacts and links;
  argument completeness; novelty);
- the verdict labels required on the first line (`REFUTED` / `CONFIRMED` / `UNVERIFIABLE`);
- a "do NOT do" list naming what the other sub-agents cover;
- an instruction to read the other sub-agents' outputs and **explicitly adjudicate any
  conflicts**.
