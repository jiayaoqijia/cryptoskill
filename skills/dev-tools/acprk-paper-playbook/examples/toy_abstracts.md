# Toy abstracts — good vs bad

All three papers are **invented**. Every number is **illustrative only** and marked
`[ill.]`; none comes from a real measurement. Citations like [A23] are placeholders.

---

## T1 — Faster PBS via LUT packing (FHE)

### Bad

> Fully homomorphic encryption is a very important and novel technology. In this
> paper we propose a novel and efficient method for programmable bootstrapping.
> Our method uses packing. We implemented it and it is significantly faster than
> previous methods, up to 9.1× [ill.]. We also prove rigorous guarantees on its
> correctness. Code is available at https://github.com/<real-username>/lutpack.

What is wrong: no bottleneck, no prior routes, no open question; "novel",
"significantly" without scope; the ratio has no baseline or scope; "rigorous
guarantees" overstates; the link de-anonymises the submission.

### Good

> Programmable bootstrapping (PBS) is the dominant cost of TFHE-style schemes, and
> circuits over small integers spend most of their time evaluating many small
> lookup tables. Existing work amortises PBS either by evaluating several tables in one
> PBS of doubled ring degree [A23] (EUROCRYPT'23) or by tree-based evaluation of a
> larger table [B24] (CRYPTO'24). Whether k small tables can share a single blind
> rotation at the original ring degree has remained open.
>
> We present packed test polynomials, which view k tables as interleaved windows of
> one test polynomial. We show that the window width, not the number of tables,
> bounds the packing factor, giving k ≤ N/(2tw), and that the k outputs are separated
> by key switching alone. Prior multi-value PBS is the case w = 1 of our construction.
> The resulting evaluator costs one blind rotation plus k key switches for k tables.
>
> On 6 [ill.] parameter sets at ≥128-bit estimated security, packing k = 4 [ill.]
> tables reduces the per-table PBS latency by 2.1–3.4× [ill.] over the strongest
> baseline in the same library, e.g. 11.0 → 3.9 ms [ill.] for 4-bit tables. Our
> implementation is publicly available.\footnote{anonymous link}

---

## T2 — New differential distinguisher (symmetric cryptanalysis)

### Bad

> We study the security of ToySPN-64. Using SAT solvers, we found a new
> distinguisher. Our distinguisher is the best one. This shows ToySPN-64 is insecure.

Wrong: "study" with no result; no prior best; "best" without comparison; overclaims
insecurity from a distinguisher on reduced rounds.

### Good

> ToySPN-64 is a lightweight 64-bit SPN whose designers claim resistance to
> differential cryptanalysis beyond 4 rounds [C22]. Prior analyses search
> characteristics one trail at a time [C22, D23] and reach 4 rounds with
> probability 2^{-60} [ill.]; clustering of trails into differentials has not been
> exploited.
>
> We model truncated differences and trail clustering jointly in one SAT
> instance, counting all characteristics compatible with a fixed input/output
> difference. We show that the S-box admits a 2-round iterative truncated pattern
> that the designers' bound does not cover.
>
> This yields a 6-round distinguisher with probability 2^{-58} [ill.], two rounds
> beyond the designers' claim, verified experimentally on 5 rounds with 2^{30} [ill.]
> pairs. The full-round cipher is not affected. Our models and verification scripts
> are available.\footnote{anonymous link}

---

## T3 — PSI with lower communication (protocols)

### Bad

> PSI has many applications. We give a new PSI protocol which uses less
> communication than all other protocols.

Wrong: no setting (balanced/unbalanced, semi-honest/malicious), "all other
protocols" is unfalsifiable, no numbers.

### Good

> Unbalanced private set intersection, where a client with m items queries a server
> with n ≫ m items, is dominated by communication linear in n in OPRF-based protocols
> [E21] (CCS'21) and by expensive homomorphic evaluation in FHE-based ones [F22]
> (USENIX'22). Whether OPRF-based protocols can reach communication sublinear in n
> without homomorphic encryption has remained open.
>
> We present a cuckoo-filter variant whose false-positive rate depends on the
> fingerprint length only, not on the load factor, and use it to compress the
> server's OPRF outputs. We prove semi-honest security in the OPRF-hybrid model.
>
> For n = 2^{24} and m = 2^{10} [ill.], our protocol sends 1.3× [ill.] fewer bytes
> than the best OPRF-based baseline at the same statistical security σ = 40, with
> the same round count. Source code is provided.\footnote{anonymous link}
