---
name: sdp-and-media-negotiation
domain: software-engineering/sdp-and-media-negotiation
trigger: "Reading what the session description actually negotiates."
anti_trigger: "Not for the signalling channel itself, and not for NAT traversal."
scope: "The session description, its codecs, and what the handshake carries."
status: seedling
---

# SDP and media negotiation

## Standard

The session description is the blob the offer and answer carry, and it reads like a config file from a previous era: line-oriented, order-sensitive in places, and dense with parameters that matter. The important lines say which media the sender intends, which codecs it can send or receive, the network details for the connectivity machinery, and the security fingerprints. The answer selects from what the offer proposes: media the answer will not use are declined, codecs the answer cannot decode are rejected, and the intersection is what the call carries.

Reading it is a working skill, because the call's behaviour lives in these lines. A one-way call is an answer that declined the sending direction; a black video in an audible call is a codec mismatch; a doubled echo is the intersection of two configurations. The debugging method is to dump both descriptions and diff them — the field that disagrees is usually the finding — and the discipline is to prefer the stack's own interpretation over hand-assembly, since the deprecated ordering of every parameter is a bug habitat no one needs to live in.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols> and <https://webrtc.org/getting-started/overview>.

## Decision rules

- Dump both peers' descriptions and read them on every setup bug; the intersection is where the defect usually lives.
- Set the direction a media stream intends — send, receive, or both — explicitly; the default is inheritance from browser history.
- Codec preferences are ordered by the offer; if a preferred codec matters, say so rather than taking the stack's default ordering.
- Prefer the stack's session-description APIs to hand-built strings; the format's ordering rules punish assembly by hand.
- Renegotiation produces a new description pair; read the diff between old and new rather than rebuilding the whole model.
- The security fingerprints are part of the description; changing certificate state without a new handshake is a defect class all of its own.

## Procedure

1. In the failing case, export the offer and the answer verbatim.
2. Read the media lines: which streams, which directions, which ports and transports.
3. Read the codec lists and find the intersection the answer chose.
4. Diff the two descriptions field by field, marking every field present in one and absent in the other.
5. Compare the defect symptom to the diff; confirm by changing exactly one field and observing the result.
6. Record the case — the diff and the fix — in the realtime record.

## Anti-patterns

- Debugging a call by reading the application's CSS and HTML, with the two descriptions never printed.
- Hand-constructed SDP that works in testing and fails against a different stack version.
- Directions left implicit, so a "one-way audio" bug reproduces exactly the default configuration.
- Assuming the codec list is unordered and shipping the stack's lowest-preference codec as the call's usual sound.
- Renegotiation by writing directly to the session state rather than exchanging a new pair.

## Done checklist

- [ ] Both descriptions exported on every setup bug.
- [ ] Media directions stated explicitly.
- [ ] Codec preferences stated.
- [ ] Stack APIs used instead of hand assembly.
- [ ] Renegotiations handled as new pairs.
- [ ] Diff-and-fix cases recorded.

## Sources

- Protocols of the API including SDP: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols>
- WebRTC getting started: <https://webrtc.org/getting-started/overview>
- RTP, what the media rides: <https://en.wikipedia.org/wiki/Real-time_Transport_Protocol>
