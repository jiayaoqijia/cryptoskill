---
name: signaling-and-handshake
domain: software-engineering/signaling-and-handshake
trigger: "Designing the application-owned exchange that connects peers."
anti_trigger: "Not for the media path, and not for TURN provisioning."
scope: "Offer, answer, and the application-owned exchange."
status: seedling
---

# Signaling and handshake

## Standard

The realtime standards deliberately leave signalling to the application: the offer, the answer, and the candidate exchange travel over whatever channel the application builds — a WebSocket, a polling endpoint, a human copying a string. The offer carries the caller's session description, the candidate list, and the requested media; the answer carries the callee's. Neither the peers nor the transport standards know how these blobs move between endpoints, and so the application's signalling channel is the most under-specified and therefore most divergent part of a realtime system.

The sequencing is standard even where the channel is not. Gather the candidates, create the offer, send it, receive the answer, apply it, and run the connectivity checks. The one ordering rule that breaks systems: the offer must describe the media the caller intends to send, and once two peers have applied descriptions, renegotiating mid-call is possible but a different problem, with different states and a different failure surface. The application states what its channel carries and guarantees — ordered, reliable, at-least-once — because a noisily-ordered candidate stream produces half-connected calls.

Primary sources: <https://webrtc.org/getting-started/overview> and <https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection>.

## Decision rules

- Signalling is application code: choose the channel, document its guarantees, and record them in the design.
- Candidates may arrive after the offer or with it; the channel's ordering guarantees decide whether the code must tolerate interleaving.
- Descriptions are immutable once exchanged; renegotiation is a deliberate second exchange with its own state, not an edit.
- The signalling channel shares authentication with the application; a call request is an authenticated act.
- A ringing state is a signalling-channel decision as well: the callee's answer arrives when their device says yes, not when the network does.
- Version and route the signalling messages; peer versions drift during development, and an incomprehensible answer from a stale client is a made support ticket.

## Procedure

1. Choose the signalling channel and write down its guarantees: ordered, reliable, authenticated.
2. Define the message types: offer, answer, candidates, and the closing or cancelling messages.
3. Version the messages and plan for old clients during the rollout window.
4. Implement the handshake sequence on both sides with the interleave tolerances the channel needs.
5. Test a call between the two application versions the deployment plan says will coexist.
6. Record the channel, versions, and message schema in the realtime record.

## Anti-patterns

- Candidates arriving through one channel and offers through another, racing each other.
- Renegotiation attempted by sending a second offer mid-established call, with the states that implies.
- An unauthenticated signalling channel letting anyone ring anyone.
- Ringing implemented on transport connectivity, so on a slow network nobody receives calls at all.
- No message versions, and a debugging session where the two ends speak different dialects.

## Done checklist

- [ ] Channel chosen, guarantees stated.
- [ ] Message types and versions defined.
- [ ] Authentication shared with the application.
- [ ] Interleave tolerance implemented and tested.
- [ ] Cross-version call tested during the rollout window.
- [ ] Channel and versions in the record.

## Sources

- WebRTC getting started: <https://webrtc.org/getting-started/overview>
- RTCPeerConnection handshake: <https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection>
- The protocols involved: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols>
