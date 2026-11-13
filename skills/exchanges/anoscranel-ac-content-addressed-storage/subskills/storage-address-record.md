---
name: storage-address-record
domain: software-engineering/storage-address-record
trigger: "Writing the record for a content-addressed store decision."
anti_trigger: "Not for recommending a store, and not for the store's own documentation."
scope: "The written record of algorithms, root values, retention, and verification evidence."
status: seedling
---

# Storage address record

## Standard

The storage-address record captures the decisions that make a content store auditable: which algorithms produce the addresses, where roots are published, what counts as live, and what verification actually happened at each boundary. Its purpose is the same as any record in this pack — a later reader should be able to reconstruct why a digest was trusted, not merely that it was.

Two entries carry most of the weight. The root publication entry names who checks the root and how often; an unchecked root is a decorative hash. And the verification entry distinguishes what was verified from what was assumed: a fetch that never recomputed a digest verified nothing, however immutable the underlying design claims to be.

Primary sources: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects> and <https://osf.io/prereg/>.

## Decision rules

- The record states the hash algorithms in use and the truncation decisions behind them.
- The root publication points and their checkers are named, with checking frequency.
- The liveness policy is written: roots, grace periods, and deletion logging.
- The dedup boundary and its isolation assessment are recorded.
- Verification events are recorded as performed, not as designed.
- Review triggers are dated: algorithm news, scale milestones, retention changes.

## Procedure

1. Record the algorithms, widths, and any truncation analysis.
2. Record the root publications and their checkers.
3. Record the liveness policy and deletion logging.
4. Record the dedup boundary and isolation findings.
5. Record verification events with dates and boundaries.
6. Set review triggers and amend at each.

## Anti-patterns

- Recording the design without recording the checks actually performed.
- Naming no checker for a published root.
- Stating an immutability property without the verification event that evidenced it.
- Leaving the dedup boundary unstated in a multi-tenant store.
- No triggers, so a weakened algorithm is never revisited.

## Done checklist

- [ ] Algorithms and truncation recorded.
- [ ] Root publications and checkers named.
- [ ] Liveness policy recorded.
- [ ] Dedup boundary recorded.
- [ ] Verification events dated.
- [ ] Review triggers dated.

The record should also state the store's failure posture in one line: what a reader does when a digest lookup misses, and whether a miss is treated as absence, corruption, or eviction. That single sentence converts the store's absence semantics from an implementation detail into a documented contract that callers can program against.

## Sources

- Reachability model reference: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>
- Stated conditions practice: <https://osf.io/prereg/>
- Registry API digest semantics: <https://docs.docker.com/registry/spec/api/>
