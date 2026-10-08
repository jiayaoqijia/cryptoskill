---
name: detect-tool-result-tampering
description: Use when tool output, downloaded data, or an API response must be proven unmodified before use. Verify a digest or signature against a trusted source, not against the same channel that delivered it.
---

# Detect tool result tampering

If an attacker can edit the bytes between a service and your agent, they can rewrite a "safe" result into a destructive command or a redirect. This skill binds each result to a value you obtained out of band, so tampering is detectable.

## Procedure

1. Identify what the result should be bound to: a GPG or sigstore signature, a published checksum, a TLS pin, or a content hash you fetched from a second channel.

2. Verify against an independent source. A checksum served by the same host proves only that the host is self-consistent:

       curl -sO https://mirror-a.example/pack.tar.gz
       shasum -a 256 pack.tar.gz   # compare to the value in release notes on a different origin

3. For signed artefacts, verify the signature before unpacking: `gpg --verify pack.tar.gz.sig pack.tar.gz` or `cosign verify-blob --signature s.sig --certificate c.pem blob`.

4. For API JSON, check integrity markers if offered (HMAC header, ETag, content hash) and re-derive them locally:

       printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$KEY"   # compare with X-Signature header

5. Pin TLS where the channel matters: record the leaf certificate SPKI at first contact and alert on change.

       openssl s_client -connect host:443 -showcerts </dev/null | openssl x509 -pubkey -noout | shasum -a 256

6. Compare the payload against schema and expected range; a signature-less numeric field that suddenly doubles is a tamper smell even without a broken hash.

7. On mismatch, discard the result entirely and re-fetch through a channel you trust; never "use the good parts".

## Pitfalls

- A hash fetched over the same TLS session as the file is not independent verification.
- Mutable tags (`latest`) plus no digest let a compromised upstream swap content silently.
- Checking only size or mtime catches nothing; attackers preserve both.
- Trusting a verification step that pulls its public key from the attacker's server fails.

## Verification

    shasum -a 256 -c expected.sha256   # must print OK; any FAIL is tampering until proven otherwise

Report: "result <path> bound to <source>; signature/hash verified yes|no; TLS SPKI unchanged; verdict accepted|rejected."
