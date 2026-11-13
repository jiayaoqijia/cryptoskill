---
name: client-quorums
domain: software-engineering/client-quorums
trigger: "Reading how a client trusts a reply from a Byzantine system."
anti_trigger: "Not for client session guarantees, and not for API authentication."
scope: "How a client trusts a reply without trusting any single node."
status: seedling
---

# Client quorums

## Standard

A Byzantine client cannot trust a reply from one replica, because that replica may be the faulty one. The protocol therefore has the client wait for f+1 replies carrying the same result — enough that at least one honest replica vouches for it — and treats disagreement among replies as a signal in itself, since the disagreement itself must be resolved by naming a replica and starting a view change.

The design question is what the f+1 matching replies prove. They prove the value was committed, not merely processed, and the client's read path must respect the same discipline as its writes: forwarded tags, sequence numbers, or digests that let the client verify that the f+1 replies describe the same request. A client that skips the verification because f+1 replies agree has moved its trust to the agreement of liars, which f+1 of them can produce.

Primary sources: <https://pmg.csail.mit.edu/papers/osdi99.pdf> and <https://en.wikipedia.org/wiki/PBFT>.

## Decision rules

- Record the reply threshold the client waits for: f+1 with identical results.
- Record what the replies carry that binds them to the request.
- Record the client's behaviour when replies disagree.
- Record whether reads use the same threshold as writes.
- Record the time a client waits before suspecting the primary.
- Record what a client-side cache is allowed to state and for how long.

## Procedure

1. Trace one write request to its f+1 matching replies.
2. Trace one read path and compare its threshold.
3. Trace a split reply and the client's escalation.
4. Verify that replies carry the request identity verifying their binding.
5. Test the client timeout against a stalled primary.
6. Write the client's trust rule with both paths covered.

## Anti-patterns

- Accepting the first reply rather than f+1.
- Verifying agreement without verifying binding to the request.
- A read path that trusts one replica.
- No escalation when replies disagree.
- Caching without a stated expiry and proof basis.

## Done checklist

- [ ] Write threshold traced.
- [ ] Read threshold traced.
- [ ] Split-reply path traced.
- [ ] Request binding verified.
- [ ] Client timeout tested.
- [ ] Trust rule written for both paths.

A further note: the client's retry path is part of the trust rule, since a request that times out must be retried at a new view rather than re-submitted blind, and the record should say which identifier makes the retry safe from double application.

## Sources

- Client interaction in PBFT: <https://pmg.csail.mit.edu/papers/osdi99.pdf>
- Client behaviour reference: <https://en.wikipedia.org/wiki/PBFT>
- Patterns reference: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
