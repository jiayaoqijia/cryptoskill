---
name: hash-partitioning
domain: software-engineering/hash-partitioning
trigger: "Reading hash-based placement and its rehash cost."
anti_trigger: "Not for cryptographic hash choice, and not for consistent hashing specifically."
scope: "Modulo and hash placement: even spread, no order, and the rehash cost."
status: seedling
---

# Hash partitioning

## Standard

Hash partitioning computes the placement as a function of the key: hash the key, take modulo the node count, and place the record there. The hash scatters values evenly across the space, so keys with no relation to each other land on unrelated nodes, and the cluster's load approximates the key distribution rather than the key order.

Two properties define the scheme's character. First, the placement destroys order: records adjacent in key space are unrelated in placement, so range queries touch every shard. Second, the placement depends on the node count — change the count from ten to eleven and approximately ten of eleven of the keys rehash to new nodes, which is the cost that motivated consistent hashing. Naive modulo placement is simple, spreads well, and rewrites the world on resize.

Primary sources: <https://en.wikipedia.org/wiki/Hash_table> and <https://dataintensive.net/>.

## Decision rules

- Record the hash function and whether it is stable across client versions.
- Record the placement formula, including any seed and the node count's role.
- Record the fraction of keys that move on a node-count change.
- Record how range queries fare under the placement.
- Record whether node identity or a logical slot count appears in the formula.
- Record whether assignment is computed at write, at read, or maintained in a table.

## Procedure

1. Note the hash function and its stability guarantees.
2. Write the placement formula precisely.
3. Compute movement on adding and removing one node.
4. Test a range query's shard fan-out under the placement.
5. Determine whether the formula uses logical slots rather than physical nodes.
6. Write the placement description with the resize cost stated.

## Anti-patterns

- Using physical node identity in the formula and rehashing on every topology change.
- Assuming hash evenness guarantees request evenness; hot keys hash somewhere too.
- Changing the hash function without a migration plan.
- Defending scatter-gather range queries as acceptable because the hash spreads.
- Ignoring seed agreement across client versions, splitting one keyspace.

## Done checklist

- [ ] Hash function and stability recorded.
- [ ] Placement formula written.
- [ ] Resize movement computed.
- [ ] Range query fan-out tested.
- [ ] Slot-versus-node distinction recorded.
- [ ] Assignment maintenance point identified.

Slot-based modulo — a large fixed number of logical slots mapped to physical nodes — is the standard fix for the rehash cost and deserves its own line in the record: slot count, the slot-to-node mapping's maintenance, and the reminder that the slots themselves must be numerous enough that rebalancing moves fractions rather than clumps.

## Sources

- Hash table mechanics: <https://en.wikipedia.org/wiki/Hash_table>
- Partitioning with hashes, chapter reference: <https://dataintensive.net/>
- Sharding technique overview: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
