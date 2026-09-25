# 08 Main construction(s)

## Shape of each construction section

```
[opening]      One paragraph: what this section proves/builds and where it is used.
[definition]   New objects, numbered.
[theorem]      Main statement with ALL hypotheses explicit.
[proof/sketch] In place if ≤ 1 page, else a sketch + "full proof in Appendix A.2".
[construction] Algorithm float: name — one-line function; Input/Output with types;
               right-side comments; then walk through the key lines in prose.
[cost]         Cost proposition in the paper's cost unit (the one "currency" used in
               abstract, intro, construction and experiments).
[selection]    Rule that chooses parameters/configuration from the instance, with no
               search if possible; tie-breaking stated.
[example]      A tiny worked example whose numbers can be recomputed by a script.
[remarks]      Boundary cases, what is NOT claimed, relation to prior work.
```

## Rules distilled from review rounds

- **State every hypothesis.** "Generically" and "for typical parameters" invite a
  counterexample; replace with explicit conditions or "the upper bound holds
  unconditionally; attainment is verified computationally for the parameters in
  Table k".
- **Run your own parameter table through every theorem** before submission. A
  theorem whose hypothesis excludes some of your own parameter sets is a guaranteed
  catch.
- **Sufficient vs necessary.** Do not use a sufficient condition as if it were
  necessary (a classic source of counterexamples). If only one direction is proven,
  say so.
- **Every "clearly"/"it is easy to see" is a falsifier target.** Ask the `falsifier`
  agent for a small counterexample search (toy parameters, exhaustive).
- **Design choices need search evidence**, not "we chose": "we enumerated all ... and
  selected the one minimising ...", "we verified exhaustively that no ... exists".
- **Families, not single instances.** Present a parameterised family `Scheme[a,m,l]`
  plus a recommended instance. This defends against "it is just parameter tuning".
- **One cost currency** (e.g. external products per output bit; non-scalar
  multiplications; OPRF calls + bits) used identically everywhere; a cost formula
  with `\underbrace` labels per term helps.
- **Algorithm floats**: `Algorithm k  Name — one-line purpose.` with typed
  Input/Output lines; symbols identical to the body text.
- **Deliberately weaker variants** can belong in the paper if they carry a
  conceptual point (a new assumption, a new structure) — label estimated vs measured.

## Checklist

- [ ] All theorem hypotheses explicit and satisfied by every parameter set used.
- [ ] Each design choice backed by an enumeration/search statement (with script in artifact).
- [ ] Cost stated in the single paper-wide currency.
- [ ] Worked example reproducible by a script listed in EVIDENCE.
