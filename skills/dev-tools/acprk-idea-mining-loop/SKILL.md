---
name: idea-mining-loop
description: Run the 8-step idea-mining loop (probe, free a fixed parameter, exact/SAT synthesis, spot an anomaly, algebraic root cause, control experiment, real-system validation, generalise + lower bound) with a pre-gate and two gates. Use when a direction has a measurable bottleneck and intuition-driven attempts have stalled.
---

# idea-mining-loop

Reverse-engineered from how real results were found: an idea is not *chosen*, it is what **survives**. The
loop turns "numbers look odd" into "theorem + bound", and it is designed to let most candidates die cheaply.

Worked, runnable example (public textbook fact, Gold exponents): `python3 skills/idea-mining-loop/scripts/toy_mining_demo.py`.
It shows an honest Gate-B failure (even n), an anomaly, a naive hypothesis killed by a control experiment,
a real-cost metric, and a matching lower bound.

## When to use / not use

Use: a performance/complexity bottleneck you can compute in a few lines; 1–2 intuitive attempts already stalled;
you suspect a design constant (modulus, base, radix, ordering, round count, chunk size, hash count, folding factor)
was fixed by habit rather than proven optimal. Do **not** use when you already have a precise theorem target —
just prove it.

## Pre-gate 0 — security-bearing object or computational substrate? (5 min)

Write one sentence: *"The object I want to compress/restructure is ___; it is / is not part of the scheme's
security definition, because ___."*
- **Security-bearing** (public key map, trapdoor/sampler output distribution, anything the adversary sees and
  must look random): exclude structurally. Any exploitable structure you find there is a cryptanalytic result
  (an attack), not a free optimisation. History: extra algebraic structure on public maps / trapdoors is the
  usual source of breaks.
- **Substrate** (field arithmetic, key-switching bookkeeping, packing/transform scheduling, NTT layout, OT/OKVS
  plumbing): allowed — but passing this gate is necessary, not sufficient. Step 6 is still mandatory.
If you cannot write the sentence, the target is not specific enough: go back to Step 0.

## The steps (every step writes a dated note `notes/<slug>_<YYYY-MM-DD>.md`; never overwrite old notes)

| step | do | time box | output |
|---|---|---|---|
| 0 Probe target | State the bottleneck as a number computable in a few lines + baseline value + success criterion. Bad: "bootstrapping is slow". Good: "number of non-linear multiplications to evaluate map M on domain D; baseline 40". | 5 min | `probe_target` note |
| 1 Cheap probes | One ≤50-line offline script per candidate direction; answers only "is there any hope in principle?". Kill if the small-scale probe cannot approach the target, or the gain is dwarfed by overhead. Keep negative results. | ≤30 min/direction | `<direction>_probe` note (also for dead ones) |
| 2 Representation tricks | Read neighbouring work asking "what did they turn from FIXED into a FREE variable?" — one line per paper. | 1–2 h | `representation_tricks` note |
| **Gate A** | Name the parameter that is fixed by history/engineering default, not by proof. Cannot name one → back to 2, or the direction has no minable freedom. | | line in IDEAS.md |
| 3 Parametrise + sweep | Make it a CLI parameter; sweep a range deliberately **wider** than intuition; cheap proxy metric first; structured output (JSON/CSV), not logs. | ≤1 h | `<param>_planner.py` + `results/<param>_sweep/` |
| 4 Exact synthesis | On survivors, let a solver (SAT/SMT/ILP/exhaustive search) find the true optimum (min terms, min depth, min mults, min rounds). Per-call timeout ≤5 min. **Re-verify every solver model with independent code.** | ≤2 h | table: candidate → optimum → re-verified? |
| **Gate B** | Look for an *outlier* — "better out of proportion, not explained by the other candidates" — not the best value. Smooth monotone curve → record "no anomaly", return to Step 2. | | IDEAS.md verdict |
| 5 Algebraic root cause | Test which algebraic relation the outlier satisfies (order, characteristic polynomial, divisibility, subgroup/coset, self-map of the support, fixed points). Target: one provable/refutable sentence "anomaly ⟺ property P". Keep the Sage/Wolfram code. | ≤1 h | `algebraic_root_cause` note + code |
| 6 Control experiment (**never skip**) | Build a candidate that shares the naive explanation's surface feature but lacks property P (and vice versa). Anomaly must vanish/appear accordingly. If not → P is wrong/incomplete, back to 5. | ≤30 min | `## Control experiment` section of the Step-5 note |
| 7 Real-system validation | Wall-clock in the real library/protocol, baseline vs candidate vs a control candidate, same flags/threads/machine, interleaved runs, ≥3 repeats (median + spread). Report component *and* end-to-end (Amdahl), absolute *and* relative. | ½ day | `results/<slug>_real/` + EVIDENCE rows |
| 8 Generalise + lower bound | (a) Replace the specific value by a family (one exponent → all k; one prime → all primes; one ring → all rings of the class) and re-run 4–7. (b) Prove how close the result is to a lower bound (counting, information-theoretic, degree, rank). "X% faster" becomes "within Y of optimal". | 1–2 d | THEORY.md + CLAIMS.md entries |

## Mini-examples across areas (toy, for orientation)

| area | fixed-by-habit parameter (Gate A) | cheap probe / proxy | what an anomaly + control would look like |
|---|---|---|---|
| Symmetric | S-box exponent e in x^e (textbook uses e = 3 or inverse) | differential uniformity per cyclotomic class | APN outliers at e = 2^k+1; control: same Hamming weight, gcd(k,n)>1 → δ = 2^gcd (see demo) |
| FHE | gadget base B and digit count ℓ in key switching | noise variance × #NTTs per switch | a base where noise drops more than the ℓ-reduction explains → check if B aligns with the RNS primes; control: same ℓ, misaligned B |
| Lattice | block size schedule in progressive BKZ | simulated GSA slope per unit cost | a schedule beating the smooth trend → check dimension-for-free effect; control: same schedule without the extra dims |
| MPC/PSI | number of hash functions / load factor in cuckoo hashing or OKVS | failure probability vs size via simulation | sharp threshold (phase transition) → graph-theoretic cause (2-core/peeling); control: same load factor, different hash family |
| ZK | FRI folding factor / Reed–Solomon rate | proof size × verifier work | a factor where both drop together → check field/domain structure; control: same factor, different domain size |
| PQC | rejection-sampling bound / norm check in Fiat–Shamir-with-aborts | acceptance rate × signature size | an outlier bound → check the distribution's tail geometry; **pre-gate first**: the output distribution is security-bearing, so the "optimisation" must provably preserve independence from the secret |

## Prompt patterns that produced real ideas (generalised)

1. **Read before thinking.** First make the agent summarise *tried / abandoned / current best*. No free association in a vacuum.
2. **Ignition = concrete book chapter + concrete step.** "Use the structures in <textbook, chapter> to attack <specific algorithm step>" — never "give me ideas".
3. **Human step: spot the constant.** For every specific object in the agent's output ask "why this one? what if it varied?" — this is Gate A and is the least automatable step.
4. **Exhaust and falsify.** "Not only the value that worked — every member of the family, including the ones theory says should be better — run them for real."
5. **Reachability audit.** "Check item by item whether each theoretical saving is actually reachable."
6. **Theorem-ise the survivor**, then **ask for the lower bound** and "how far from it are we?".
7. **Measured, not predicted.** Any number without a command and a log is a prediction; say so.
8. **Ask for the price.** "Why is the speedup so large? What got worse (communication, key size, depth, precision)?"
9. **Let branches die, and file them.** A failed branch becomes a documented negative result or a pure-theory remark — never a drag on the main claim.

## Anti-patterns (from real post-mortems)

- Trusting a hand proof over a computation: an "established" theorem later found false. Verify every algebraic claim in Sage/Lean before it enters a draft.
- Skipping Step 6: correlation (a shared surface feature) mistaken for cause.
- Sweep range too narrow: outliers often sit outside the "sensible" range.
- One real-system run: that is a smoke test, not a result.
- Comparing hand-written code with a library without matching compiler flags / build options first: a large "anomaly" that is only `-march=native`.
- Reporting only the ratio: the component speedup can rise while the end-to-end gain falls, because the denominator shrank.
- A cost model that ignores fan-out/hidden terms: a solver "finds" a 30× gain that an explicit simulation erases. Validate the cost model on a small instance by direct simulation before trusting any optimum.
- Structure that exists only for one specific value (an algebraic coincidence of one constant) rarely generalises; test the generalisation early (Step 8a) before building a paper on it.

## Log

Append one row per run to the project's `IDEAS.md` table:
`| date | target | freed parameter | anomaly | root cause | control passed? | real-system result | verdict |`.
