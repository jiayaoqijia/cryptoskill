---
name: sage-check
description: Numeric sanity check of every lemma, identity and parameter claim on small parameters, with exhaustive search where feasible. Use it before writing a proof, before Lean formalisation, and whenever a falsifier needs a counterexample search. Works with SageMath if installed and falls back to pure Python/sympy otherwise.
---
# sage-check: test every lemma on small cases first

## Why

Proving a false lemma wastes days, and formalising one in Lean wastes weeks. Most
wrong statements fail on a toy instance: a small prime, a small ring dimension, a
2×2 case. Run a finite check **before** proving and **before** formalising.

## Protocol

1. **Transcribe the statement exactly** as in THEORY.md. Include every quantifier and
   side condition. Each checked statement gets an ID matching THEORY.md / CLAIMS.md.
2. **Choose a parameter grid.**
   - Include every smallest case (p ∈ {2, 3, 5, 7, 11, 13}, n ∈ {1, 2, 4, 8}).
   - Cover both residue classes the statement distinguishes (for example p ≡ 1 and
     p ≡ 3 mod 4).
   - Include the boundary of any inequality hypothesis, on both sides.
   - Include at least one parameter as large as the experiments use, if it is feasible.
3. **Test the hypotheses too.** Check that the hypotheses are satisfiable on the grid,
   because a vacuous theorem "passes" every check. Then check the conclusion.
4. **Search exhaustively** wherever the space is finite and small (≤ 10⁷ cases).
   Otherwise use random sampling with a fixed seed, and report the seed and the sample
   size.
5. **Also test the converse.** If a condition is claimed to be necessary *and*
   sufficient, test both directions separately.
6. **Use exact arithmetic**: `ZMod`/`GF`, `Integer`, `QQ`, `sympy.Rational`. Use no
   floats unless the statement is about floats. For asymptotic claims, check the exact
   finite formula on a range and fit the trend; do not trust a plotted curve.
7. **Output one JSON line per check**:
   `{"check": ID, "params": {...}, "cases": N, "passed": bool, "counterexample": {...} | null}`.
   Save the script under `checks/` and the output under `results/checks/`, then add an
   EVIDENCE row if any number from it reaches the paper.
8. If a check fails, give the **minimal** counterexample (smallest parameters) to
   `falsifier` and `theorist`. Do not patch the statement silently.

## Script template

`scripts/sanity_check_template.py` is a runnable skeleton with a guarded Sage import,
a `check(...)` helper that stops at the first counterexample, and a toy statement
about roots of unity mod p. Copy it, then replace the `STATEMENTS` list.

```bash
python3 skills/sage-check/scripts/sanity_check_template.py          # pure Python
sage -python skills/sage-check/scripts/sanity_check_template.py     # uses Sage if present
```

## Typical checks by area

| area | what to check on toy parameters |
|---|---|
| algebra | existence and order of roots of unity mod p; factorisation of Φ_m mod p (number and degree of factors = ord_m(p)); injectivity of encodings; polynomial identities coefficient by coefficient |
| FHE | noise bound vs measured noise on a toy scheme (the bound must hold on every sample); correctness of the claimed decryption condition at its boundary; operation counts by instrumented toy evaluation |
| lattice | toy LWE instances solved by LLL/BKZ in small dimensions, compared with the estimator's predicted β |
| symmetric | S-box properties (DDT/LAT/differential uniformity) by exhaustive computation; small-round trail probabilities by exhaustive search on scaled-down versions |
| protocols | secret-sharing reconstruction thresholds; OT/PSI correctness on small sets; communication formulas vs counted messages |

## Tooling notes

- In Sage, `GF(p)`, `Zmod(n)`, `CyclotomicField(m)` and `cyclotomic_polynomial(m)`
  cover most checks. Run with `sage -python script.py` so the same file stays
  importable as plain Python.
- In pure Python, `sympy` (`cyclotomic_poly`, `factor_list(..., modulus=p)`,
  `n_order`, `primitive_root`) and `pow(a, -1, p)` are enough for most toy checks.
- Mathematica, if connected, is useful for closed forms and series. Treat its output
  as a hint, then recheck with exact finite computation.
