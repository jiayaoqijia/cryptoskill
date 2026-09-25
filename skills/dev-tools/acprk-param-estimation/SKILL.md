---
name: param-estimation
description: Estimate concrete security and cost for proposed parameters. Covers lattice schemes via lattice-estimator or a built-in core-SVP model, symmetric-key margins, and MPC/PSI communication and round costs. Use whenever a paper states a security level, picks parameters, or compares against a baseline whose parameters might not be equally secure.
---
# param-estimation

## Lattice (LWE / RLWE / MLWE / NTRU)

### Tooling

- **lattice-estimator** (public, a Sage library) is the default. Pin its commit in the
  project MANIFEST. Invocation:

  ```python
  # sage -python est.py
  import sys; sys.path.insert(0, "/path/to/lattice-estimator")
  from estimator import LWE, ND, RC
  params = LWE.Parameters(n=1024, q=2**27, Xs=ND.UniformMod(3), Xe=ND.DiscreteGaussian(3.2), m=1024)
  r = LWE.estimate(params, red_cost_model=RC.MATZOV)       # full run
  r = LWE.estimate.rough(params)                            # fast core-SVP-style screen
  ```

  Sparse or ternary secrets use `ND.SparseTernary(n_plus, n_minus, n)`. NTRU uses
  `NTRU.Parameters` / `NTRU.estimate`. Parse the output with `crbench parse --parser lattice-estimator`.
- **Built-in core-SVP model** (for quick screens and sanity):
  `cost ≈ 0.292·β` (classical sieve) or `0.265·β` (quantum). β is the smallest block size
  meeting the GSA/uSVP success condition, with `δ(β) = ((πβ)^{1/β} β / (2πe))^{1/(2(β−1))}`.
  The `lib/cryptomath` lattice module provides this. Use it to screen; use the estimator
  for final numbers.

### Protocol

1. **Record the convention**: estimator commit; cost model (`RC.MATZOV`, `RC.BDGL16`,
   `RC.ADPS16`...); secret distribution (dense ternary, sparse with weight h, uniform,
   Gaussian); error σ; number of samples m; how q is rounded. Round q **up**, which is
   the attacker-favourable and therefore conservative choice.
2. **Model the real distribution.** Check the library's actual secret sampler. For
   example, a library may default to a dense ternary secret with weight about n/2, or
   to a sparse one. The estimate must match what the code samples, not what the paper
   says.
3. **Run all attacks** (usvp, bdd, bdd_hybrid, bdd_mitm_hybrid, dual, dual_hybrid).
   Report the **minimum**, and name the attack that achieves it.
4. **Non-power-of-two cyclotomics and structured rings.** The estimator treats the
   instance as plain LWE. State that algebraic attacks (subfield attacks, overstretched
   NTRU, small-Galois-orbit structure) were considered separately, or were not.
5. **Put one table per parameter set in EVIDENCE**: `n, log q, secret, σ, attack →
   log2(rop), β`. Keep the raw JSON or log.

### Pitfalls

- **An NTRU "fatigue point" is not a modulus ceiling.** The fatigue point is where the
  dense-sublattice attack becomes cheaper than key recovery. It is *not* where security
  collapses. The largest modulus still meeting a target security level can be much
  larger. Treating one as the other can underestimate usable parameters by many bits
  and can wrongly rule out whole designs. Always find the ceiling by running the
  estimator over a q-grid, and leave margin near any cliff where a new attack becomes
  applicable.
- **Check the function shape, not just constants.** When you claim a scaling law
  ("secure log q grows like f(N)"), fit it on at least four points. A wrong shape
  (logarithmic vs linear) is a bigger error than a wrong constant.
- **Estimator performance patches.** Some scripts need cache-size or laziness patches
  to handle very large n. Record each patch, and confirm the results on small n match
  the unpatched commit bit for bit.
- **Module or matrix variants can be weaker** than the circulant or ring version with
  the same dimension. Estimate them separately.
- **Keys generated for the benchmark** may use weaker parameters than the paper's
  headline. Compute the security of key-switching and bootstrapping keys too, since
  they sometimes use a smaller dimension or a larger modulus.
- **Compare baselines at equal security.** If your parameters give 118 bits and the
  baseline's give 128, the speed-up is not comparable. Re-parameterise one side.

## Symmetric primitives

- Report the **security margin** as (rounds attacked by the best known distinguisher or
  key recovery) versus (full rounds). State the attack type (differential, linear,
  integral, algebraic, cube, MitM) and whether it is a distinguisher or key recovery.
- For FHE- or MPC-friendly ciphers, **algebraic attacks** (Gröbner, linearisation,
  interpolation, higher-order differentials) often dominate. Estimate the degree growth
  and the number of monomials, and use a published complexity formula with its
  citation.
- A "keystream looks random" test is **not** a security argument. Run vectorised
  distinguishers and algebraic-degree checks on the actual component (for example a
  whole-table S-box analysis) before claiming anything.
- Trail search: use SAT/MILP models (CryptoSMT, CaDiCaL, HiGHS). Report solver, version,
  time limit and whether the bound is proven optimal or only the best found.

## MPC / PSI cost

- Report **communication (bytes), rounds, and computation separately**, for each party
  and for each phase (offline or pre-processing vs online).
- Simulate the network explicitly, for example LAN at 10 Gbit/s with 0.1 ms delay and
  WAN at 100 Mbit/s with 40 ms delay, using `tc netem`. State the settings.
- Match the security model (semi-honest or malicious; honest or dishonest majority),
  the statistical security parameter (for example 40) and the computational one (128).
- Check asymptotic cost formulas against measured traffic on at least two set sizes.

## Output

A section in THEORY.md ("Parameters and security") plus EVIDENCE rows for each printed
security level. Use `scripts/core_svp_screen.py` for a quick, dependency-free screen.
