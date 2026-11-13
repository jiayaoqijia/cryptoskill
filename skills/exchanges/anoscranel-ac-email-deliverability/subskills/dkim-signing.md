---
name: dkim-signing
domain: software-engineering/dkim-signing
trigger: "Setting up or diagnosing DKIM signing and key rotation."
anti_trigger: "Not for SPF evaluation, and not for general DNS security."
scope: "Domain-signatures, key rotation, and the body-hash that breaks."
status: seedling
---

# DKIM signing

## Standard

DKIM puts a cryptographic signature in the mail headers that the receiving side can verify against a public key published in DNS. The signature covers selected headers and — critically — the body hash of the message content. It proves two things SPF cannot: the message was not modified in transit, and the signing domain takes responsibility for it. That responsibility claim is what DMARC's alignment rules read; a signature from the exact visible domain is the strongest position a sender can hold.

The operational reality is that the body hash breaks more often than the key. Any forwarder that appends a footer, re-wraps lines, or converts encoding changes the body, and the signature no longer verifies. This is not an attack; it is the mechanism working as designed — the receiver learns the content changed. Senders who sign must also rotate keys: a selector is the DNS location of the key, and rotation means publishing the new selector, signing with it, and removing the old key only after mail signed with it has drained.

Primary sources: <https://datatracker.ietf.org/doc/html/rfc6376> and <https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail>.

## Decision rules

- Sign with the visible From domain, or a domain that aligns under the DMARC policy, before any subordinate selector.
- Record which headers are signed; the From header must be among them.
- Keep the key size and algorithm within current guidance, and rotate on a stated schedule.
- Rotation is additive: publish the new selector and sign with it while the old key stays in DNS until old mail drains.
- Diagnose a verification failure by separating the signature check from the body hash; a broken body-hash means the content changed.
- Recognise that some corporate forwarders will always break the body hash; plan the DMARC policy with that fact known.

## Procedure

1. Generate a key pair and publish the public key under a dated selector.
2. Configure the sending platform to sign the body-hash plus the required headers with that selector.
3. Send tests through each sending path and verify the signature from the receiving side.
4. Confirm the From header is signed and the signing domain aligns.
5. On rotation: publish the new selector, switch signing, verify, then remove the old key after the drain period.
6. Record the selector inventory and rotation dates in the deliverability record.

## Anti-patterns

- A single eternal key with no selector inventory, so rotation becomes a crisis.
- Removing the old key while a week of signed mail is still in flight.
- Diagnosing a forwarding break as an attack before checking the body hash.
- Signing with a domain that does not align and wondering why the DMARC report quarantines it.
- Assuming the platform signs the From header without checking the signed-headers list.

## Done checklist

- [ ] Key published under a dated, recorded selector.
- [ ] Signing verified end-to-end from the receiving side.
- [ ] From header signed and domain alignment confirmed.
- [ ] Body-hash failures diagnosed as content-change by default.
- [ ] Rotation schedule stated; drain period respected.
- [ ] Selector inventory in the record with dates.

## Sources

- RFC 6376, the DKIM specification: <https://datatracker.ietf.org/doc/html/rfc6376>
- DMARC alignment context: <https://datatracker.ietf.org/doc/html/rfc7489>
- Overview of the mechanism: <https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail>
