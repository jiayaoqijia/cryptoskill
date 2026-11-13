---
name: stun-and-turn
domain: software-engineering/stun-and-turn
trigger: "Choosing and operating the servers that make traversal possible."
anti_trigger: "Not for the ICE process itself, and not for the media path after connection."
scope: "The mapped address and the relay a symmetric NAT forces."
status: seedling
---

# STUN and TURN

## Standard

A STUN server answers one question: what public address did my packet arrive from? The reply teaches a peer its mapped address — the address the outside world can reach. Free public STUN servers exist because the answer is cheap to give, but the answer is also situational: a symmetric NAT assigns a different mapping per destination, so the address learned from one STUN server may not be the address a different peer sees. The design treats the reflexive candidate as a hypothesis the ICE checks test, never as a fact gathering proved.

A TURN server is a relay: the peer sends its media to the TURN server, which forwards packets both ways. It is the fallback when no peer-to-peer pair works — symmetric NAT on both sides, a firewall that only allows outbound, a corporate network with no hospitality — and it is a fundamentally different cost structure, because every relayed call pays for bandwidth twice at the server. The design positions TURN as a configured service with a budget, not as a free fallback: TURN is the difference between the call succeeding and failing for the hard cases, and it is also the difference between a marginal cost and a real one.

Primary sources: <https://www.rfc-editor.org/rfc/rfc5389> and <https://www.rfc-editor.org/rfc/rfc8656>.

## Decision rules

- Operate or select STUN servers deliberately; relying on a public list turns connectivity into an externality of someone else's uptime.
- Treat reflexive addresses as candidates to check, never as verified reachability.
- Configure TURN before launch, with authentication and a stated allocation policy; adding it in production later is an outage-shaped project.
- TURN bandwidth is budgeted: relayed megabits are a provisioning problem, and the fraction of relayed calls is a metric to watch.
- Record which server answered each call's gathering; the servers are part of the call's provenance.
- Fail loudly when both peer pairs and TURN fail; a silent failure is indistinguishable from success in the logs and from a bug in the wild.

## Procedure

1. Select or deploy the STUN servers, and record them in the client configuration.
2. Deploy TURN with authentication and allocation lifetime limits, and record the credentials path — never inline keys.
3. Measure the relayed-call fraction on a realistic network mix during a pilot.
4. Set the TURN bandwidth budget from the measured fraction and a stated headroom.
5. Wire the failure path: when no pair including TURN connects, the caller sees a reason, not silence.
6. Record per-call which server family each candidate came from in the realtime record.

## Anti-patterns

- Hardcoded public STUN servers from a blog post, dead by launch.
- TURN skipping authentication because it was a prototype, and shipping the prototype.
- A TURN budget discovered by an invoice, after a launch to a market full of symmetric NATs.
- The relayed-fraction metric invented during the outage instead of measured during the pilot.
- Relay failures logged at debug while a support channel discovers them at production scale.

## Done checklist

- [ ] STUN servers deliberately chosen and configured.
- [ ] TURN deployed with authentication and allocation limits.
- [ ] Relayed fraction measured in a realistic pilot.
- [ ] TURN bandwidth budgeted with headroom.
- [ ] Failure path visible to the caller.
- [ ] Per-call server provenance recorded.

## Sources

- RFC 5389, the STUN specification: <https://www.rfc-editor.org/rfc/rfc5389>
- RFC 8656, the TURN specification: <https://www.rfc-editor.org/rfc/rfc8656>
- WebRTC for the curious, the practical walkthrough: <https://webrtcforthecurious.com/>
