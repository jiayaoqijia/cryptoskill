---
name: hash-algorithm-choice
domain: software-engineering/hash-algorithm-choice
trigger: "Choosing a hash for addressing content that must be found again later."
anti_trigger: "Not for password hashing, and not for choosing a cryptographic signature."
scope: "Cryptographic versus non-cryptographic, truncation, algorithm agility, and the multi-hash pattern."
status: seedling
---

# Hash algorithm choice

## Standard

The hash algorithm decides what the address means. A cryptographic hash makes the address expensive to forge deliberately; a fast non-cryptographic hash makes lookups cheap but lets a motivated writer produce collisions. For build artifacts and mature data, the choice is usually a cryptographic family, because the cost of hashing is rarely the bottleneck and the address lives far longer than the decision.

Two working rules follow. First, the algorithm's name belongs in the address, or the multi-hash form of an algorithm prefix carries it, so two digest schemes can coexist in one store. Second, truncation trades collision width for address length and should be an explicit, recorded decision rather than a convenience — the surviving bits must still exceed the collision probability the store's lifetime requires.

Primary sources: <https://www.rfc-editor.org/rfc/rfc6920> and <https://csrc.nist.gov/publications/detail/sp/800-107/rev-1/final>.

## Decision rules

- Record the algorithm and its output width, and whether the address includes the algorithm identity.
- Record the expected lifetime of addresses and the collision probability that lifetime implies.
- Record any truncation and the analysis behind its width.
- Record whether the store supports adding a second algorithm without breaking the first.
- Record the attack model: is deliberate collision resistance required, or only accidental?
- Record the migration path when an algorithm weakens.

## Procedure

1. List the algorithms the store may use now and later.
2. Decide the address format so the algorithm is visible in it.
3. Compute the collision probability over the store's expected scale and lifetime.
4. Decide truncation, if any, and record the surviving width.
5. Require the multi-hash or prefix form so future algorithms can coexist.
6. Write the policy with the migration path stated.

## Anti-patterns

- Choosing a hash because a tool defaulted to it rather than for the store's lifetime.
- Truncating addresses to save space without recording the collision math.
- Burying the algorithm identity, making a future migration a format break.
- Using a checksum designed for error detection where collision resistance is needed.
- Treating one algorithm as permanent when history says otherwise.

## Done checklist

- [ ] Algorithms listed, current and future.
- [ ] Address format carries algorithm identity.
- [ ] Collision probability computed for scale and lifetime.
- [ ] Truncation decision recorded with width analysis.
- [ ] Coexistence path stated.
- [ ] Migration path written.

## Sources

- Guidelines for hash function selection: <https://csrc.nist.gov/publications/detail/sp/800-107/rev-1/final>
- Hash-based naming: <https://www.rfc-editor.org/rfc/rfc6920>
- Reference on practical hash use: <https://en.wikipedia.org/wiki/Cryptographic_hash_function>
