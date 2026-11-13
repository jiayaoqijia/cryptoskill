---
name: security-mandatory
domain: software-engineering/security-mandatory
trigger: "Verifying the encryption and authentication provisions of a realtime stack."
anti_trigger: "Not for general application security, and not for asset hardening."
scope: "DTLS keys and encrypted media as defaults, not options."
status: seedling
---

# Security mandatory

## Standard

A realtime connection in the modern stack is encrypted by default: the peers run a DTLS handshake over the candidate path, exchange certificates and derive keys, and the media rides as SRTP with those keys. The DTLS fingerprints inside the session description are the binding between the encryption and the identity — the description says what certificate fingerprint to expect, the handshake presents the certificate, and a mismatch is a connection that must be refused rather than accepted. The design intent is that media cannot be sent in the clear even by accident, because there is no clear mode to fall into.

The mandatory provisions deserve verifying, not assuming. Non-browser implementations and legacy stacks have shipped with permissive verification; embedded devices have shipped debug modes that accept any key; integrations have relayed signalling without authentication. The checklist is short: DTLS handshake present, fingerprints compared against the description, the media protocol negotiated as encrypted, and the signalling channel authenticated as application traffic. Any gap in those four is the hole in the design, and none of them should be optional from the application's point of view.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols> and <https://webrtcforthecurious.com/>.

## Decision rules

- Verify the DTLS handshake is present in the connected path, not only configured.
- The fingerprint in the description must match the presented certificate, and a mismatch is a hard refusal, not a warning.
- Confirm the media layer negotiated encryption, not merely that DTLS succeeded once.
- Signalling carries offers, candidates, and identity: it must share the application's authentication, and an unauthenticated call button is a vulnerability in the product.
- TURN servers carry the media of the hardest cases, and they authenticate with credentials via the signalling path; inline secrets in client code are a defect (they belong behind the server's credential exchange).
- Legacy stacks get checked against the four-provision list rather than being believed, and debug modes that accept any key are disabled in release builds.

## Procedure

1. Inspect the connected path: is the DTLS state established for each call?
2. Confirm the description fingerprints compare against the actual certificates presented.
3. Confirm the media layer under negotiation is the encrypted profile.
4. Review the signalling channel's authentication: is an offer an authenticated request?
5. Review TURN credential distribution: no static inline secrets in the client bundle.
6. Record the four provisions verified once per release, and on every new non-browser client.

## Anti-patterns

- The stack's default checked as a feature, then a permissive debug configuration shipped to production.
- Fingerprint mismatch treated as a network hiccup and retried until the connection accepted something.
- Signalling with no authentication because the product wanted quick integration.
- TURN credentials embedded in the client bundle, published to every user.
- Non-browser clients trusted to implement the standard because their vendor marketing said so.

## Done checklist

- [ ] DTLS verified on the connected path.
- [ ] Fingerprint comparison verified and enforced.
- [ ] Encrypted media profile confirmed under negotiation.
- [ ] Signalling authentication shared with the application.
- [ ] TURN credentials behind the signalling path.
- [ ] Four provisions verified per release and per client.

## Sources

- The protocols and their security: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols>
- A practical, readable stack walkthrough: <https://webrtcforthecurious.com/>
- DTLS identity in RTCPeerConnection: <https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection>
