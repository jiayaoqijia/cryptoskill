# BLS12-381 primitives: signatures, VRFs, KDFs, and credentials

The signature / VRF / KDF / credential half of `explain-zk`. Proof verification lives in
`proof-systems.md`. Everything here composes from the same operations — scalar multiplication, point
addition, hash-to-curve, and the pairing check — exposed through the `g1`, `g2`, `scalar`, and `pairing`
modules under `aiken/crypto/bls12_381/`, with the raw builtins under `aiken/builtin`.

This reference describes what each primitive does and how to choose between them. It deliberately
carries no cryptographic code: these APIs change between library versions, and a subtly wrong snippet
here becomes a vulnerability in a real contract. For the current API read
`docs/sources/aiken-stdlib/aiken/crypto/bls12_381/`; for implementations see the ZK/BLS section of
the ecosystem map via `suggest-tooling`.

## The shared primitives

Keys and signatures are curve points. Deriving a public key is one scalar multiplication of the
generator. Signing is a hash-to-curve followed by another scalar multiplication: hash the message
directly to a curve point, then multiply that point by the secret.

Two conventions matter. **Points cross the datum/redeemer boundary compressed** — 48 bytes in G1, 96
in G2 — so anything stored on-chain is compressed first. And for BLS signatures, by the
minimal-public-key-size convention, **public keys live in G1** (small, long-lived, held in datums)
while **signatures live in G2** (larger, transient). The VRF example below and BBS+ both put the
public key in G2; the placement belongs to the scheme.

Every hash-to-curve takes a **domain separation tag**: a public string mixed into the hash so that a
hash computed for a signature can never collide with one computed for a VRF or any other protocol,
even on an identical message. Using the wrong tag is a silent interoperability failure — off-chain
and on-chain must agree on it exactly.

Verifying a signature is the **pairing check**, the operation the whole curve exists for: it confirms
that the signature point and the public key are related by the same secret, without revealing it.
Concretely it is a Miller loop per point pair followed by a single final verification, and because
intermediate Miller-loop results can be multiplied together, *many* relationships can still end in
*one* final check. That property is what makes aggregation affordable on-chain, and everything below
is a wrapper over it.

## BLS signatures and aggregation

Because signatures are points, they **add together**. Many signatures aggregate into one 96-byte
value, and verification stays cheap. That is what makes large committees, vote tallies, and k-of-n
schemes with big n practical inside one script budget. (For a small fixed signer set, native-script
multisig is simpler and needs no Plutus at all.)

Two patterns, with different costs:

- **Signature aggregation, distinct messages.** Each party signs its own message and the signatures
  sum into one. The verifier does roughly one pairing per `(public key, message)` pair, so cost still
  grows with the signer count — but the witness is a single signature instead of n.
- **Public-key aggregation, one common message.** When everyone signs the *same* message, the public
  keys can be summed too, and verification becomes a **constant two pairings regardless of signer
  count**. This is the committee case, and it is the reason BLS is used for consensus-scale signing.

### The rogue-key attack, and the three signing modes

Aggregation introduces an attack that plain signatures do not have. Seeing honest keys `pk_1` and
`pk_2`, an attacker can claim a key computed as `pk_att - (pk_1 + pk_2)`. They never knew the honest
secrets, but the aggregate of all three collapses to a key they control, so a signature they produce
alone verifies as though everyone signed. Defending against this is exactly what the signing modes in
the IETF BLS signature draft are for.

| Mode | How it signs | Defence against rogue keys |
|---|---|---|
| **Basic** | The raw message | Aggregate verification **rejects duplicate messages**, so the cancellation cannot pay off |
| **Message-augmentation** | The signer's public key prepended to the message | Each hash input is unique per signer, so a forged aggregate never matches |
| **Proof-of-possession** | The raw message, under a distinct domain tag | Each key is **registered once** with a signature over itself, proving the owner holds the secret; a rogue key cannot be registered |

The consequence people get wrong: **the common-message, aggregated-key case belongs to
proof-of-possession.** The draft defines that optimisation (`FastAggregateVerify`) only for the
proof-of-possession scheme, precisely because registration is what makes summing keys safe. Basic
mode cannot serve that case at all — its aggregate verification is specified to reject two identical
messages, which is its whole defence. Message-augmentation binds every signature to its own signer's
key, so an aggregated key no longer satisfies the equation.

Two cautions. First, a library's helper may not follow the draft exactly, and a helper that deviates
will disagree with this description — **verify the mode semantics against the library you actually
depend on**, not against a summary. Second, proof-of-possession is only as good as its registration
step: if unvetted keys can enter the set without a verified proof of possession, the rogue-key attack
is back.

## Verifiable random functions

A VRF is a keyed hash with a public verification story: only the secret-key holder can compute the
output for a given input, the output is deterministic and looks random to everyone else, and it comes
with a proof anyone can check against the public key. Three properties do the work: **verifiability**,
**uniqueness** (exactly one valid output per key and input, so there is nothing to grind), and
**non-interactivity** (one published tuple, no challenge rounds).

An ECVRF over BLS12-381 runs in pure Aiken, so the proof can be checked inside a validator rather than
trusted from an oracle. It follows the RFC 9381 construction, but the RFC's ciphersuites cover P-256 and
Edwards25519 only, so this is a non-standard suite, not one that interoperates with a standard VRF. The
usual API is four operations: derive a key pair from a secret, prove an input, verify a proof, and
extract the output hash from a proof.

What it buys you on-chain:

- **A randomness beacon a validator can enforce.** The input is public and fixed, so the operator gets
  exactly one possible output per round and cannot grind for a favourable one. Liveness still depends
  on the operator publishing.
- **Enumeration-resistant data structures.** Key a public tree by the owner's VRF output rather than
  by a plain hash of the record name, and outsiders see only unlinkable pseudorandom addresses while
  the owner can still prove membership later.
- **Leader selection and proofs of prior knowledge** — the same tool Ouroboros uses, in application space.

## Key derivation functions

Real inputs are messier than a curve-ready secret. A KDF turns a seed, a shared secret, or a password
into a valid private key, reducing the result into the curve's scalar field. Two are practical
on-chain: **HKDF** for input that is already high-entropy (cheap, and its `info` parameter gives
domain separation so one master secret can yield many unlinkable keys), and **PBKDF2** for
low-entropy input, deliberately slowed by iteration — but on-chain the iteration count must stay
small, far below the counts used off-chain, which puts its brute-force resistance well below normal
expectations.

**The caveat that matters most.** A password or salt passed through a datum or redeemer is published
on-chain permanently; anyone can extract it and rerun the KDF off-chain at leisure. On-chain KDFs are
therefore **not** a password-hashing mechanism. Their legitimate inputs are values that are already
public or already committed, and their legitimate uses are narrow: deriving session or child keys
from strong secrets, and testing. Hash human passwords off-chain and put only the resulting key or
hash on-chain.

**Memory-hard KDFs (Argon2, Balloon) are structurally incompatible with on-chain execution** — their
memory requirements exceed the per-transaction budget by orders of magnitude, and the primitives they
need are not exposed. If you need memory-hard hashing it happens off-chain and the chain verifies the
result.

## BBS+ anonymous credentials

BBS+ turns a signed list of attributes into a privacy-preserving credential. An issuer signs n
attributes into one constant-size signature. Later the holder proves they hold a valid signature over
all n attributes **while revealing only a chosen subset** — "over 18 and an EU citizen", without the
birthdate, the name, or a trackable identifier. Each showing randomises the signature and wraps it in
a zero-knowledge proof, so two showings cannot be linked to each other or to issuance.

On-chain it takes the shape described in the main skill: the issuer's public key and the credential's
attribute schema sit in the datum as the trust anchor, the proof travels in the redeemer with its
disclosed indices and values, and the challenge nonce is derived from the UTxO being spent so a proof
lifted from one transaction is useless in another. The signature is constant-size; the proof grows by
one scalar per undisclosed attribute. The pairing count stays constant, while the point arithmetic
grows with the attribute count.

BBS+ has the fewest Aiken implementations of the family — treat it as the least settled of these
primitives and confirm the current landscape before depending on it.

## Where to go deeper

Everything below is bundled, so check the source rather than relying on any summary, including this one.

- **The normative spec**: `docs/sources/bls12-381-examples-and-standards/standards/draft-irtf-cfrg-bls-signature-06.txt`
  — the definitive statement of the three modes, of aggregate verification, and of `FastAggregateVerify`.
  Read this before relying on any claim about which mode fits which aggregation pattern.
  Alongside it: RFC 5869 (HKDF), RFC 8018 (PBKDF2), RFC 9381 (the VRF construction; no BLS12-381
  ciphersuite).
- **A real implementation**: `docs/sources/aiken-bls-signatures/lib/bls/` — `g1/basic.ak`, `g1/aug.ak`,
  and `g1/pop.ak` are the three modes in Aiken.
- **Worked examples**: `docs/sources/bls12-381-examples-and-standards/aiken/` — Groth16, KDF, VRF, a Nova
  folding verifier, and both aggregation cases. Alongside them, `tutorials/zkp-from-first-principles.md`
  builds a proof system up from scratch, and `tutorials/proving-cardano-address-ownership-via-zkp.md`
  works one end to end. (`tutorials/bls12-381-basics.md` is upstream a stub pointing at a blog post —
  the primitives it covered are the subject of this reference.)
- **The stdlib API**: `docs/sources/aiken-stdlib/aiken/crypto/bls12_381/` for the current `g1` / `g2` /
  `scalar` / `pairing` functions.
- **The walkthrough this reference condenses**:
  `docs/sources/developer-portal/developers/curriculum/smart-contracts/advanced/bls-primitives.md`,
  signatures, VRF, KDF, and BBS+ with code.
- Named verifier and BLS libraries: the ZK/BLS section of `suggest-tooling/references/ecosystem-map.md`.
