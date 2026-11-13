---
name: nat-traversal-and-ice
domain: software-engineering/nat-traversal-and-ice
trigger: "Understanding how two peers behind NAT find a working path."
anti_trigger: "Not for the media itself, and not for the signalling channel."
scope: "Candidates, checks, and the checkpoint through NAT."
status: seedling
---

# NAT traversal and ICE

## Standard

A home router's network address translation lets internal devices share one public address by rewriting outgoing connections and remembering them. That memory is exactly what blocks inbound calls: an unsolicited packet arriving at the public address has no remembered translation to map it to, so it is dropped. The ICE answer is to make the path a two-way negotiation: each side gathers every address it might be reachable on, exchanges them through the signalling channel, and both sides send connectivity checks — small STUN messages — to every candidate pair. A pair that answers from the same address it was contacted on is a working path; the framework pairs and prunes in priority order until one connects.

The candidates come in three kinds. Host candidates are local interface addresses, useless across NAT but valid on a LAN. Server-reflexive candidates are the public mapped address a STUN server reports for the peer. Relay candidates are addresses on a TURN server that forward packets to the peer. The checks exist because gathering proves nothing: a symmetric NAT rewrites differently per destination, so the mapped address learned from the STUN server may not work for a different peer, and only the pairwise checks reveal which candidate pair survives this network's behaviour.

Primary sources: <https://www.rfc-editor.org/rfc/rfc8445> and <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API>.

## Decision rules

- Gather all three candidate kinds and let the checks decide; discarding a kind in advance discards the networks it serves.
- Exchange candidates through the signalling channel both ways; ICE is pairwise, and one side's list is half the data.
- The checks must go from both sides — a half-open path works for neither.
- Preserve candidate priority order in the implementation; random ordering wastes the pruning that follows.
- Expect the selected pair to differ call to call on the same network; candidate selection is situational, not persistent.
- Record which pair connected and why the others failed — the pruned pairs are the diagnosis of the next bug.

## Procedure

1. Configure the STUN and TURN servers the gathering will query, and record them.
2. Gather host, reflexive, and relay candidates for each side.
3. Exchange all candidates through the application's signalling channel.
4. Run the connectivity checks against every candidate pair in priority order.
5. On a working pair, nominate it and stop; on none, report the failed pairs with reasons.
6. Record the selected pair, the pruned counts, and the servers used.

## Anti-patterns

- Testing on an office LAN where host candidates always win, then shipping to home networks where they never do.
- Sharing only one side's candidates, then debugging a half-connected call.
- No TURN server configured, so symmetric-NAT users fail forever and quietly.
- Assuming yesterday's selected candidate today; ICE state is per-call.
- Discarding the pruned pairs' failures, losing the only diagnostic record of why the network behaved as it did.

## Done checklist

- [ ] All candidate kinds gathered.
- [ ] Candidates exchanged both ways through signalling.
- [ ] Checks run pairwise in priority order.
- [ ] Selected pair recorded per call.
- [ ] Failed pairs recorded with reasons.
- [ ] STUN and TURN servers recorded.

## Sources

- RFC 8445, the ICE specification: <https://www.rfc-editor.org/rfc/rfc8445>
- WebRTC API overview: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API>
- Interactive Connectivity Establishment: <https://en.wikipedia.org/wiki/Interactive_Connectivity_Establishment>
