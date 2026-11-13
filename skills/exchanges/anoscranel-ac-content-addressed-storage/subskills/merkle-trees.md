---
name: merkle-trees
domain: software-engineering/merkle-trees
trigger: "Reading or designing a verification tree over content-addressed data."
anti_trigger: "Not for choosing a consensus protocol, and not for single-file checksums."
scope: "Batched verification, partial sync, roots as checkpoints, and the cost of changing one leaf."
status: seedling
---

# Merkle trees

## Standard

A Merkle tree hashes content into leaves, then hashes groups of leaves into parents, until a single root represents the entire structure. The root is a checkpoint of everything beneath it, and a leaf can be verified from the root plus a short path of sibling hashes, without re-reading the rest of the tree. The tree turns point verification into a logarithmic operation instead of a full scan.

The two consequences that matter in practice are partial sync and the cost of change. Two parties who hold the same root hold the same data and need exchange nothing; two parties with different roots can descend the tree and transfer only the diverging subtrees. And a change to one leaf invalidates that leaf's path to the root — which is cheap for a leaf near the top and expensive near the bottom, an asymmetry that ordering decisions should exploit.

Primary sources: <https://en.wikipedia.org/wiki/Merkle_tree> and <https://www.rfc-editor.org/rfc/rfc6962>.

## Decision rules

- Record the leaf content: file bytes, block digests, or record fields.
- Record the fan-out factor and the depth it implies for the store's scale.
- Record where the root is published and who is expected to check it.
- Record whether inclusion proofs are exposed to readers or used only internally.
- Record the ordering of leaves, and whether it makes the hot paths short.
- Record what changing one leaf costs in re-hashing and root updates.

## Procedure

1. Define the leaf unit precisely.
2. Choose the fan-out and compute the depth at the expected scale.
3. Decide the root's publication point and its checkers.
4. Decide whether inclusion proofs are needed by readers.
5. Order leaves so frequently verified or updated items sit close to the root.
6. Write the tree design with the change-cost analysis stated.

## Anti-patterns

- Re-hashing the entire tree on every write when depth permits incremental updates.
- Publishing a root nobody is required to check.
- Choosing fan-out by aesthetics rather than depth versus proof-size trade-off.
- Assuming the tree detects malicious substitution; it detects any substitution that changes the root path, which must itself be trusted.
- Ignoring leaf ordering, then paying full-depth updates for the hot data.

## Done checklist

- [ ] Leaf unit defined.
- [ ] Fan-out and depth computed.
- [ ] Root publication and checkers named.
- [ ] Inclusion proof policy decided.
- [ ] Leaf ordering justified.
- [ ] Change-cost analysis written.

## Sources

- Merkle tree reference: <https://en.wikipedia.org/wiki/Merkle_tree>
- Hash tree specification discussion: <https://www.rfc-editor.org/rfc/rfc6962>
- Git object model as a Merkle store: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>
