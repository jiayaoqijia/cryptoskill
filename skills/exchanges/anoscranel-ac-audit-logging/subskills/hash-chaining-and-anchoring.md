---
name: hash-chaining-and-anchoring
domain: software-engineering/hash-chaining-and-anchoring
trigger: "Making a log whose local edits are detectable and whose wholesale rewrite is visible."
anti_trigger: "Not for blockchain design, and not for cryptographic key management."
scope: "Chain each entry to its predecessor and anchor the head off-host."
status: seedling
---

# Hash chaining and anchoring

## Standard

A hash chain links each entry to its predecessor: the entry contains the hash of the one before it, so altering any past entry invalidates every hash that follows it. An attacker who can rewrite the whole log can recompute the chain, which is why the second mechanism exists — the chain's head, its latest hash, is anchored somewhere the log's writer cannot reach: published, written to WORM media, or sent to a different system with different credentials.

Together the two make the log tamper-evident in the honest sense, not tamper-proof. Local edits break the chain immediately; a full rewrite with recomputation survives the chain check but not the anchor, because the anchored head will not match the rewritten history. The term used in the record should be tamper-evident, and anyone claiming tamper-proof is claiming the attacker cannot stop the logger — a different and usually false claim.

Primary sources: <https://www.rfc-editor.org/rfc/rfc6962.html> and <https://csrc.nist.gov/pubs/sp/800/92/final>.

## Decision rules

- Record the chain's hash function and the exact bytes covered by each entry's link.
- Anchor the chain head off-host, on a schedule, with the anchor's location recorded.
- Verify the chain on read during investigations and periodically as a health check.
- Detect gaps as well as alterations — a missing entry breaks the chain as clearly as an edited one.
- State the trust model in the record: which attacker the chain detects, and which it does not.
- Never describe the mechanism as tamper-proof; record it as tamper-evident.

## Procedure

1. Define the entry format and the exact byte range each hash covers.
2. Implement the chain link and verify it round-trips.
3. Send the head to an off-host anchor on a schedule.
4. Implement verification that walks the chain and checks the anchor.
5. Test the detection paths: edit one entry, delete one entry, rewrite the whole log.
6. Record hash function, anchor location, schedule, and trust model.

## Anti-patterns

- Chaining without anchoring, so a full rewrite goes undetected.
- Anchoring to a location writable by the same credentials as the log.
- Verification implemented but never exercised against a real simulated tamper.
- Claiming tamper-proof because the word sounds stronger in a review.
- Hashing a subset of the entry, leaving fields outside the chain.

## Done checklist

- [ ] Chain bytes defined and hashed.
- [ ] Anchored off-host on a schedule.
- [ ] Verification walks and checks.
- [ ] Edit, delete, and rewrite all detected in tests.
- [ ] Trust model recorded.
- [ ] Claim kept honest: tamper-evident.

## Sources

- Certified-log design and Merkle audit proofs: <https://www.rfc-editor.org/rfc/rfc6962.html>
- Log protection guidance: <https://csrc.nist.gov/pubs/sp/800/92/final>
- Event-content baseline: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
