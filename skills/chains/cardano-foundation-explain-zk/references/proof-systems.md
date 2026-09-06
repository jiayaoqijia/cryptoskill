# Proof systems and on-chain SNARK verification

The SNARK half of `explain-zk`: what a proof guarantees, which proof system to pick, the working
Groth16 verifier shape, the circuit-to-Aiken pipeline, and the costs. The signature / VRF / KDF /
BBS+ half lives in `bls-primitives.md`.

## What a proof actually claims

A zk-SNARK encodes a statement as an **arithmetic circuit** — equations over a finite field. The
prover holds a private **witness** (the secret), the circuit takes some **public inputs** (values
both sides see), and the proof asserts: *I know a witness that satisfies this circuit for these
public inputs.*

Three guarantees: **completeness** (an honest prover with a valid witness always convinces the
verifier), **soundness** (a prover without one cannot, beyond negligible probability), and
**zero-knowledge** (the verifier learns nothing beyond the truth of the statement).

The consequence that matters most in review: **the proof only proves what the circuit constrains.**
A circuit that checks `a * b * c == n` proves you know three factors of `n`, not three *prime*
factors. Every property an application claims must appear as a constraint.

## Choosing a proof system

| System | Proof size | Trusted setup | How it reaches Cardano |
|---|---|---|---|
| **Groth16** | Smallest (~200 bytes: two G1, one G2) | Per circuit | Circom or gnark circuits; Groth16 verifier in Aiken |
| **PLONK** | ~0.5 KB | Universal, reusable across circuits | Circom via a snarkjs adaptation; Plutus/Aiken verifiers |
| **Halo2 (KZG)** | Circuit-dependent | Universal | Verifier generated from a Rust circuit; also the Midnight proof system |
| **Bulletproofs** | Grows with the statement (logarithmic when compressed) | None (transparent) | Aiken range-proof verifier on the BLS12-381 builtins |
| **Sigma protocol** (e.g. Schnorr) | A few group elements | None | Implemented directly on the BLS12-381 builtins |

Three contrasts to internalise. Groth16 gives the smallest proof and cheapest verification but needs
a fresh setup per circuit; PLONK and Halo2 pay a little more per proof for a setup you run once.
**Bulletproofs** remove the setup entirely — no ceremony, no toxic waste — and natively prove range
statements ("this committed value lies in [0, 2^n)"), paying for it with proofs that grow with the
statement and heavier verification. And not everything needs a circuit: a **sigma protocol** proves
knowledge of a discrete logarithm ("I know the secret behind this public point") with no circuit and
no ceremony. If that is all the application needs, it is the lighter tool.

## What a Groth16 verifier does

A Groth16 verification key and proof are just compressed curve points: the key holds one G1 point and
three G2 points plus a list of G1 points (one per public input, with a constant term), and the proof
is three points — two in G1, one in G2.

Verification decompresses those points, folds the public inputs into a single commitment against the
key's point list, and checks one pairing equation — a Miller loop per pair, multiplied together, with
a single final verification. Circuit size does not affect this cost: the proof is the same three
points whether the circuit has five constraints or five million. What grows the cost is the **number
of public inputs**, so keep them few and commit bulky data with a single hash.

Read a real implementation rather than reconstructing one. One is bundled:
`docs/sources/aiken-zkp-verifiers/` carries Groth16, PLONK, and Bulletproofs verifiers in Aiken with
protocol walkthroughs under `zkp/docs/`; its README says the PLONK verifier is still being optimised to
fit resource limits and marks Bulletproofs early-stage. Others are listed in the ZK/BLS section of the
ecosystem map.

## The circuit-to-Aiken pipeline

The validator is the last step of a longer path. The canonical first circuit proves you know a
password whose hash equals a public commitment: the hash is a public input, the password is a private
one, and the single constraint is that hashing the private input reproduces the public commitment.
That one constraint *is* the entire statement being proven — a good illustration of why the circuit,
not the surrounding prose, defines what a proof guarantees.

The end-to-end steps:

1. Write the circuit in Circom (compile with `--prime bls12381`; the default targets a different
   curve) or in gnark.
2. Run the trusted setup to produce the proving key and the verification key.
3. Generate the proof off-chain from the witness and public inputs, in the browser or on a backend.
4. Compress the verification key and proof to Cardano's compressed-point format.
5. The Aiken validator verifies the proof as its spending condition.

The `ZK-from-zero-on-Cardano` eBook walks the whole path — circuit to Aiken verifier, with the password
example. It is not bundled and its README marks it in progress; the ecosystem map has the link. Generic
verifier implementations are in the ZK/BLS ecosystem map.

## The builtins and the CIPs

- The BLS12-381 builtins require **Plutus V3** (CIP-0381): group operations, the pairing
  (`miller_loop`, `mul_miller_loop_result`, `final_verify`), compression, and hash-to-group, backed by
  the audited `blst` library. These are what make pairing-based SNARK verification possible on Cardano.
- Later builtins made it cheaper: CIP-0133 added multi-scalar-multiplication (the operation that
  dominates PLONK and Halo2 verification), and CIP-0109 added `expModInteger` for modular field
  arithmetic.

## Cost

The shape of the cost matters more than any number, because the numbers move with the protocol
parameters, the proof system, and the implementation. What holds: a Groth16 verification consumes a
significant fraction of a single script's CPU budget, PLONK more; **circuit size does not affect it**,
while each **public input does**, which is why public inputs are kept few and bulky data is committed
with a hash.

Do not plan a design around a cost figure quoted here or in an article. Benchmark the verifier you
actually depend on, at the protocol version you are deploying to — the projects in the ecosystem map
publish their own benchmarks.

## Sharp edges in depth

- **Trusted setup is a real ceremony.** Groth16 and PLONK setups produce toxic waste: whoever holds
  the setup randomness can forge proofs. A multi-party ceremony fixes this — the result is secure if
  *any one* participant was honest. Phase 1 ("powers of tau") is circuit-independent and reusable;
  Groth16's phase 2 must be redone per circuit. A single-party setup is fine for a demo and unsafe
  for a real deployment. Transparent systems (Bulletproofs, STARKs) remove the ceremony entirely —
  the trade is proof size and verification cost, not trust.
- **Use circuit-friendly hashes, on the right curve.** SHA-256 or Blake2b inside a circuit costs tens
  of thousands of constraints; **Poseidon** and **MiMC** are built for circuits. Standard Poseidon
  parameters are generated for other curves — if you hash over BLS12-381 in-circuit, generate matching
  parameters or the in-circuit hash will never equal the one your off-chain code computed.
- **A proof on-chain is public and replayable.** Bind every proof to its context by committing a
  nonce, the spending transaction, or a session key into the public inputs.
- **Whoever runs the prover sees the witness.** Browser proving keeps the secret on the user's device;
  outsourcing to a server is a trust assumption — name it if you make it.

## Where to go deeper

- Bundled: `docs/sources/developer-portal/developers/curriculum/smart-contracts/advanced/zero-knowledge.md`
  — the full catalog of verifiers, toolkits, and shipped applications.
- Bundled: `docs/sources/aiken-zkp-verifiers/` — Groth16, PLONK, and Bulletproofs verifiers in Aiken,
  with the protocol math worked step by step in `zkp/docs/step-by-step.md`.
- Toolchains and libraries: see the ZK/BLS section of `suggest-tooling/references/ecosystem-map.md`.
- The CIPs: CIP-0381 (pairing builtins), CIP-0133 (multi-scalar multiplication), CIP-0109 (modular
  exponentiation) under `docs/sources/cips/`.
