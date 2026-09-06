---
name: explain-zk
description: >-
  Zero-knowledge and the BLS12-381 primitive family on Cardano: verify SNARK
  proofs on-chain, aggregate BLS signatures, run VRFs, derive keys, and check
  BBS+ credentials in Aiken. Triggers: "explain zero-knowledge", "ZK on Cardano",
  "verify a SNARK on-chain", "Groth16 in Aiken", "zk-SNARK verifier", "BLS
  signatures in Aiken", "aggregate signatures", "VRF on Cardano", "verifiable
  randomness", "BBS+ / selective disclosure", "anonymous credentials",
  "range proof", "Bulletproofs", "prove knowledge without revealing it".
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Explain ZK — zero-knowledge and BLS12-381 on Cardano

Help a developer understand and build with Cardano's on-chain cryptography: verifying
zero-knowledge proofs, and the wider family of protocols the same curve unlocks —
aggregated signatures, verifiable randomness, on-chain key derivation, and anonymous
credentials. Teach the model, then hand them a minimal working verifier they can adapt.

"Zero-knowledge" is the umbrella most people search under, but the engine underneath is
the **BLS12-381** elliptic curve, and proof verification is only one of the things it does.

## When to use

- A developer asks how zero-knowledge proofs work on Cardano, or how to verify a SNARK on-chain
- Someone wants to add a Groth16 / PLONK / Halo2 verifier to a validator
- Questions about BLS signature aggregation, multisig at scale, or committee/consensus signatures
- Building with verifiable randomness (VRF), on-chain key derivation (KDF), or BBS+ credentials
- "Prove I know X without revealing X", private voting, proof of reserves, selective disclosure
- Choosing a proof system, or understanding what a proof actually guarantees

## When NOT to use

- Writing a general (non-ZK) validator or minting policy — use `write-validator`
- Auditing a contract for vulnerabilities — use `review-contract`
- Walking through the text of a specific CIP — use `explain-cip` (CIP-0381 / 0133 / 0109)
- Choosing an SDK or the broader toolchain — use `suggest-tooling`
- Lowering script CPU / memory / size — use `optimize-validator`
- The goal only needs revealing a secret on spend — an HTLC, atomic swap, or hash-lock where the
  reveal is the point. A plain preimage check (`sha2_256(preimage) == commitment`) is simpler than a
  ZK proof and needs no circuit or trusted setup; use `write-validator`. Reach for a proof only when
  the secret must *stay* secret after it is used.

## Key principles

1. **One curve, many protocols.** BLS12-381 is *pairing-friendly*. That single property is
   what lets a validator aggregate thousands of signatures, verify a SNARK, produce verifiable
   randomness, or check an anonymous credential — all from the same handful of builtins. Treat
   the primitives as a construction kit, not a single feature.
2. **Prove off-chain, verify on-chain.** Generating a proof is heavy (seconds to minutes) and
   happens off-chain; verifying is cheap and deterministic and happens inside one validator.
   That asymmetry is exactly what makes the eUTxO model a good fit.
3. **A proof only proves what the circuit constrains.** Read the circuit, not the pitch. Every
   property an application claims must appear as a constraint, or the proof does not guarantee it.
4. **Bind every proof to its context.** A proof or signature sitting in a redeemer is public and
   replayable. Commit a nonce, the spent `OutputReference`, or a session key into the public
   inputs so a copied proof is useless anywhere else.
5. **Everything on-chain is public forever.** Datums and redeemers are permanent and world-readable.
   Whatever secrecy a scheme gives you comes from what you *never publish* (the witness, the
   password, the hidden attributes), not from the ledger.
6. **The builtins are audited; the libraries on top are not.** The BLS12-381 builtins sit on the
   audited `blst` library. The developer portal notes that the higher-level Aiken libraries built on
   them are unaudited and their APIs still change. Prototype on testnets, read the code you depend on,
   and treat published costs as measured snapshots.

## The BLS12-381 primitive family

Each row is a specialization of the same on-chain shape (below).

| Primitive | What it does | Reach for it when |
|---|---|---|
| **ZK-SNARK proof** | Prove knowledge of a witness, or that a computation ran correctly, revealing nothing else | Private eligibility, proof of reserves, "I solved it" bounties, rollup-style succinctness |
| **BLS signatures + aggregation** | Collapse many signatures or public keys into one small value, one pairing to verify | Large multisig, committees, consensus, vote tallies |
| **VRF** | Deterministic, unpredictable, publicly verifiable randomness from a key | Lotteries, leader selection, unlinkable record addresses |
| **KDF** | Turn seeds or shared secrets into valid curve keys, on-chain | Deriving session / child keys from already-public or committed material |
| **BBS+ credentials** | Prove a subset of signed attributes while hiding the rest | Selective disclosure, KYC, membership, compliance |

See `references/proof-systems.md` for the SNARK half and `references/bls-primitives.md` for the
signature / VRF / KDF / credential half.

## The one on-chain shape

Almost every verifier is the same pattern:

- The **trust anchor** — a verification key, an issuer key, or a commitment — lives in the **datum**
  (or a reference input, or is compiled into the validator).
- The **proof or signature** travels in the **redeemer**.
- The **public inputs** come from the datum, the redeemer, or the transaction context.
- The validator **decompresses** the points, runs the protocol's **pairing equation** via the
  BLS12-381 builtins, and returns a `Bool`.

Points cross the datum/redeemer boundary **compressed** (G1 is 48 bytes, G2 is 96 bytes). For BLS
signatures the minimal-public-key-size convention puts keys in G1 (long-lived, small) and signatures
in G2 (transient, larger). The VRF example and BBS+ put the public key in G2 instead, so take the
placement from the scheme, not from this sentence.

## Workflow

### Step 1: Identify the primitive from the goal

Map what the developer wants to the family table. "Prove you know a password" or "private
eligibility" is a **SNARK**; "one signature for a hundred signers" is **aggregation**; "a fair
random winner anyone can check" is a **VRF**; "show you are over 18 without your birthdate" is
**BBS+**. Many goals only need a **sigma protocol** (a discrete-log proof, no circuit) — the
lightest tool; see `references/proof-systems.md`.

### Step 2: Search the bundled documentation

- `${CLAUDE_SKILL_DIR}/../../docs/sources/developer-portal/developers/curriculum/smart-contracts/advanced/zero-knowledge.md`
  — the landscape, what shipped when, and the catalog of real verifiers and apps
- `${CLAUDE_SKILL_DIR}/../../docs/sources/developer-portal/developers/curriculum/smart-contracts/advanced/bls-primitives.md`
  — the signature / VRF / KDF / BBS+ walkthrough with code, the companion to `references/bls-primitives.md`
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-stdlib/aiken/crypto/bls12_381/`
  — the actual `g1`, `g2`, `scalar`, and `pairing` module APIs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/bls12-381-examples-and-standards/`
  — tutorials, worked Aiken examples, and `standards/` with the IETF BLS signature draft and the
  HKDF / PBKDF2 / VRF RFCs. Prefer these specs over any summary for security-relevant claims.
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-bls-signatures/lib/bls/`
  — a working Aiken implementation of the three BLS signing modes
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-zkp-verifiers/`
  — Groth16, PLONK, and Bulletproofs (range proof) verifiers in Aiken, with the protocol math
  worked step by step under `zkp/docs/`; its README says the PLONK verifier is still being optimised
  to fit resource limits and marks Bulletproofs early-stage
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cips/CIP-0381/`, `CIP-0133/`, `CIP-0109/`
  — the builtins these all rest on

### Step 3: Describe the on-chain verifier, then read the real one

The canonical first example is a password lock: funds unlock only for someone who can prove they know
a secret whose hash matches an on-chain commitment. Its shape is the one above — the commitment and
the verification key in the datum, the proof in the redeemer, and a single call into a Groth16
verifier that returns a `Bool`.

That verifier is not something to write from memory. It is a standard component, the same for every
circuit and around a hundred lines of pairing arithmetic, so you take it as a project dependency
rather than reproduce it. Its public inputs are field scalars, so an integer commitment held in a
datum is converted with the stdlib's scalar constructor before it is passed in.

**Do not hand-write cryptographic validator code from this skill's description.** Read the current
API and a working implementation first:

- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-stdlib/aiken/crypto/bls12_381/` for the exact
  `g1`, `g2`, `scalar`, and `pairing` functions and their present signatures
- the verifier and library implementations listed in the ZK/BLS section of `suggest-tooling`
- the bundled ZK page for which projects are doing this today

Two API notes that catch people, both worth checking against the stdlib version you pin: the scalar
constructor **reduces modulo the field prime rather than rejecting** out-of-range input, so it is not
a validation step; and rejecting a zero secret is not the same as rejecting every multiple of the
group order, which also yields the identity point.

For aggregation, VRF, KDF, and BBS+, see `references/bls-primitives.md`.

### Step 4: Outline the off-chain pipeline

The validator is only the last step. For a SNARK the full path runs off-chain first: write the
circuit (Circom or gnark, targeting BLS12-381), run a trusted setup, generate the proof (in the
browser or on a backend), then compress the verification key and proof to Cardano's format. Only
then does the Aiken validator verify it as the spending condition. `references/proof-systems.md`
covers this pipeline and points to a complete written walkthrough.

### Step 5: Flag the sharp edges

Before they ship, walk the relevant items from the list below.

## Sharp edges

- **The circuit is the spec.** A property that is not constrained is not proven.
- **Trusted setup is a real ceremony.** Groth16 and PLONK setups produce toxic waste; whoever holds
  the setup randomness can forge proofs. A single-party setup is fine for a demo and unsafe for a
  real deployment — use a multi-party ceremony (secure if any one participant was honest).
- **Replay.** Bind every proof to its context (nonce / `OutputReference` / session key), or a proof
  read out of one transaction can be reused in another.
- **Public inputs cost.** Each public input adds real verification cost; keep them few and commit
  bulky data with a single hash instead.
- **Circuit-friendly hashes, on the right curve.** SHA-256 inside a circuit is enormous; use Poseidon
  or MiMC, and generate parameters for BLS12-381 or the in-circuit hash will not match your off-chain one.
- **Whoever runs the prover sees the witness.** Browser proving keeps the secret on the user's device;
  a proving server is a trust assumption — name it if you make it.
- **On-chain KDFs are not password hashing.** A password in a redeemer is public forever. See the KDF
  section for the narrow, legitimate uses.
- **Aggregation has a rogue-key trap.** Pick the BLS signing mode (basic / augmented / proof-of-possession)
  by your key-trust model — see `references/bls-primitives.md`.

## Confidence and iteration

The BLS12-381 builtins are stable and audited; the higher-level libraries and toolchains on top of
them are unaudited and still moving.

**This skill deliberately carries no cryptographic code.** A subtly wrong snippet in a skill becomes a
vulnerability in someone's contract, and these APIs change faster than a skill does: the scalar
constructor alone has changed name, signature, and failure behaviour across recent stdlib versions.
So the skill teaches the concepts, the decision criteria, and the failure modes, and sends you to the
bundled docs and the real implementations for anything you will actually deploy.

Treat everything here as orientation to be checked against the version you pin, and prefer a proof
system, library, or figure that you have verified yourself over one described from memory.

## References

- `references/proof-systems.md` — SNARK verification: proof systems, the Groth16 shape, the pipeline, costs
- `references/bls-primitives.md` — signatures + aggregation, VRF, KDF, and BBS+ credentials
- Bundled: `docs/sources/developer-portal/developers/curriculum/smart-contracts/advanced/zero-knowledge.md`
  (landscape + app catalog), `docs/sources/developer-portal/developers/curriculum/smart-contracts/advanced/bls-primitives.md`
  (signatures / VRF / KDF / BBS+ with code),
  `docs/sources/aiken-stdlib/aiken/crypto/bls12_381/` (the API), `docs/sources/cips/` (CIP-0381 / 0133 / 0109)
- Named verifier and BLS libraries: the ZK/BLS section of `suggest-tooling` (ecosystem map)
- Shared principles: `../shared/PRINCIPLES.md`
