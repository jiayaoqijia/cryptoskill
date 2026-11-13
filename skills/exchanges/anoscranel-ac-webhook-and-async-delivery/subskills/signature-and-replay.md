---
name: signature-and-replay
domain: software-engineering/signature-and-replay
trigger: "Proving a webhook came from the sender and is not a replay."
anti_trigger: "Not for TLS configuration, and not for API key management."
scope: "Signing over the raw body, timestamp windows, and rejecting replays."
status: seedling
---

# Signature and replay

## Standard

A receiver that exposes a webhook endpoint is exposing it to anyone who learns the URL. A signature is what distinguishes a request from the sender from one from anyone else: the sender computes a keyed hash over the request body and a timestamp, and the receiver recomputes it and compares.

Two details decide whether the scheme works. The signature must be computed over the raw body as received, because any parsing and reserialisation changes the bytes and produces a different hash. And the timestamp must be included in the signed material and checked against a window, because a valid signature on an old request can otherwise be replayed indefinitely by an attacker who captured it.

Primary sources: <https://csrc.nist.gov/> and <https://www.rfc-editor.org/rfc/rfc2104>.

## Decision rules

- Record the signed material: body, timestamp, and any other headers included.
- Record the algorithm and the key length, and confirm it is a keyed hash rather than a plain digest.
- Record the timestamp window and the behaviour outside it.
- Record the comparison method, which must be constant-time.
- Record key rotation: how many keys are valid at once and how a receiver learns a new one.
- Record the receiver's obligation to reject before parsing, since parsing untrusted input first defeats the ordering.

## Procedure

1. Record the signed material and its encoding.
2. Record the algorithm and key length.
3. Record the timestamp window and rejection behaviour.
4. Record constant-time comparison.
5. Record rotation with overlapping validity.
6. Write the scheme as the receiver implements it.

## Anti-patterns

- Signing parsed fields rather than the raw body.
- A plain hash rather than a keyed one, which anyone can compute.
- No timestamp, permitting indefinite replay.
- Signature checked after the payload is processed.
- A single key with no rotation path, so a leak requires coordinated downtime.

## Done checklist

- [ ] Signed material recorded.
- [ ] Algorithm and key recorded.
- [ ] Timestamp window recorded.
- [ ] Comparison method recorded.
- [ ] Rotation recorded.
- [ ] Rejection ordering recorded.

The key's storage matters as much as the algorithm: a signing secret kept in the same configuration store as the endpoint URL is exposed by any configuration leak, and the record should state where the key lives and who can read it, not only that it exists.


## Sources

- Keyed-hash message authentication: <https://www.rfc-editor.org/rfc/rfc2104>
- Security control guidance: <https://csrc.nist.gov/>
- Application security practice: <https://owasp.org/>
