---
name: addressing-model
domain: software-engineering/addressing-model
trigger: "Designing or reading a store where the name is derived from the content."
anti_trigger: "Not for choosing a storage product, and not for signing what is stored."
scope: "Hash as name, immutability of the address, collisions, and what addressing does not guarantee."
status: seedling
---

# Addressing model

## Standard

In a content-addressed store, the name is computed from the content: the address is the digest of the bytes, typically hex-encoded and stored with the blob. The consequence is that the address is a claim about the content rather than a location for it. Two stores that hold the same bytes hold the same address, and a reader who obtains the bytes can verify the claim by recomputing the digest.

What follows is immutability of a special kind. The content at an address cannot change — any edit produces a different address, and the old content simply remains — but the association between a human-facing name and an address usually is mutable. Most systems that feel immutable underneath are mutable somewhere above, and locating where the mutability lives is the first step in reading one.

Primary sources: <https://docs.docker.com/registry/spec/api/> and <https://www.rfc-editor.org/rfc/rfc6920>.

## Decision rules

- Record whether addresses are digests of the whole object, of blocks within it, or of a manifest that references other addressed objects.
- Record the address format: algorithm, length, encoding, and any prefix carrying the algorithm name.
- Record what mutability exists above the addressing layer and where it lives.
- Record whether reads verify the digest or merely use it to look up storage.
- Record the trust model: who may write an address, and who may supply content for one.
- Record what happens to the old object when content is logically updated.

## Procedure

1. Identify the layer at which addressing applies: object, block, or manifest.
2. Write out the address format precisely.
3. Find the mutable layer and name it in one sentence.
4. Determine whether verification happens at read, at write, or is skipped.
5. State who can introduce content and how the store authenticates them.
6. Write the addressing summary with the immutability boundary stated.

## Anti-patterns

- Treating a digest naming scheme as a guarantee that content is trustworthy.
- Assuming reads verify what they fetch; many only look it up.
- Forgetting that a name-to-address mapping reintroduces mutability.
- Using addresses as authorization; an address is not a capability unless the store defines it as one.
- Assuming that because content is immutable, it cannot be removed.

## Done checklist

- [ ] Addressing layer identified.
- [ ] Address format written precisely.
- [ ] Mutable layer named.
- [ ] Verification point stated.
- [ ] Trust model stated.
- [ ] Immutability boundary written.

## Sources

- Registry HTTP API specification: <https://docs.docker.com/registry/spec/api/>
- Naming things with hashes: <https://www.rfc-editor.org/rfc/rfc6920>
- LLVM discussion of content-addressed storage behaviour: <https://llvm.org/docs/>
