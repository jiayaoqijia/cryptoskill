# 09 Security and correctness

The shape depends on the paper type; pick the matching block.

## A. Performance paper built on standard assumptions (FHE, protocols)

- **Security level statement**: which estimator (name, version/commit), which
  attacks were run, which attack is binding, which distributions (secret, error).
  Say "estimated security under <tool> at <commit>" rather than "verified security".
- **Parameter table carries a security column** for every instance used in any
  result table; instances below the claimed level are excluded from headline ranges
  and flagged.
- **Same security level as the baseline** for fair comparison; state it in a
  footnote if the estimator has drifted since the baseline was published.
- **Recent attacks**: check the last ~12 months of ePrint for attacks on your key
  distribution (sparse secrets, special rings). If an attack applies to both you and
  the baseline, measure both side by side and give a fix that applies to both.
- **Outsource security analysis to standard tools when possible.** A self-built
  estimator for a non-standard distribution makes a performance paper look like a
  cryptanalysis paper and satisfies neither audience.
- **Correctness/noise**: failure probability with its model (heuristic independence,
  CLT, worst case) and a measured noise column; decryption-verify every
  benchmarked run.
- **Pre-emptive defence of a known weakness** (four layers): acknowledge → relocate
  (e.g. failure happens once at key generation, rejection-sample) → quantify (≤ 1 bit
  leakage) → anchor to accepted theory (cite) → price the fallback ("with the
  conservative choice the speedup drops by a factor ≈ c").

## B. Symmetric design paper (ToSC/FSE)

- `Security claim.` as its own paragraph in the specification: bits of security and
  data limits per key/IV.
- Opening paragraph of the analysis section: state that internal parameters were
  chosen from this analysis; state the conservative adversary model; give the roadmap
  and what sits in the appendix.
- Attack checklist from generic to specific: generic/TMDTO → guess-and-determine →
  (fast) correlation → algebraic → fast algebraic → Gröbner/linearisation →
  structural/weak keys/invariants → related-key (if relevant) → implementation-level
  (decryption failure, noise leakage) → **summary table** attack × complexity × margin.
- Each attack: definition sentence → quantification formula → conclusion sentence
  comparing with the security claim's limits.
- When modifying an existing design, show explicitly that every changed parameter
  does not reduce security (e.g. wider outputs ⇒ divide data-complexity bounds by the
  width ratio and show the margin), and give a side-by-side table vs the original.
- Honest negative results ("our linear attempt did not match the predicted
  correlations") are accepted if framed as open problems.

## C. Cryptanalysis paper

- Complexities as (time, data, memory) triples plus success probability.
- Distinguishers verified experimentally on reduced versions ("implemented on reduced
  rounds as a proof of concept"), with the script in the artifact.
- Weak-key classes stated with their size.

## D. Theory / new assumption

- If a new assumption is introduced, build credibility by showing 2–3 equivalent
  formulations, search-to-decision and worst-to-average style reductions where
  possible, and an explicit list of attacks considered (linearisation, algebraic,
  lattice). End with "this assumption warrants further cryptanalytic study".

## Checklist

- [ ] Every instance in a result table has a security entry from a named tool.
- [ ] Binding attack named; inapplicable attacks justified with a citation.
- [ ] Known weaknesses handled with the four-layer pattern.
- [ ] Modified designs: parameter changes shown not to reduce security.
