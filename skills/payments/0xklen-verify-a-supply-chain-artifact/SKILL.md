---
name: verify-a-supply-chain-artifact
description: Use when consuming a downloaded binary, package or image from a third party. Checks signature, checksum and provenance chain before the artifact runs.
---

# Verify a Supply Chain Artifact

Downloading and running an artifact without verification is executing someone else's code on trust. Verify the digest, then the signature, then the identity that made it.

## Procedure

1. Establish the expected digest from an independent channel — the project's signed release page or a trusted index, never the same host you downloaded from. Compare: `sha256sum artifact.tar.gz` against the published value, or `sha256sum -c artifact.sha256`.
2. Verify the checksum file's own signature before trusting it:
   `gpg --verify artifact.tar.gz.sig artifact.tar.gz` (import the maintainer key from a keyserver and confirm the fingerprint against the project's docs).
3. For Sigstore-signed blobs, verify the certificate identity and issuer rather than trusting any valid signature:
   `cosign verify-blob --certificate-identity-regexp '^https://github.com/org/repo/' --certificate-oidc-issuer https://token.actions.githubusercontent.com --bundle artifact.sigstore artifact.tar.gz`
4. For containers: `cosign verify --certificate-identity-regexp <regexp> --certificate-oidc-issuer <issuer> registry/img:tag`, then read the digest and always deploy by digest: `img@sha256:...`, never by mutable tag.
5. Check provenance: `slsa-verifier verify-artifact artifact.tar.gz --provenance-path provenance.intoto.jsonl --source-uri github.com/org/repo --source-tag v1.2.3`.
6. Confirm the provenance's source commit or tag is what you intended and its builder is the project's real CI, not a fork.
7. Only after all checks pass, install or run the artifact.

## Pitfalls

- Verifying a signature without pinning the identity accepts any signer, including an attacker who generated a valid key.
- A `latest` tag can point at a different digest a second later; pin by digest.
- GPG keys expire and get rotated — a "bad signature" is often a stale local keyring, so refresh with `gpg --refresh-keys` before concluding forgery.
- A checksum published on the same compromised host as the binary is not independent verification.
- `curl | sh` installers run before any of this is possible; prefer a downloadable, signed artifact.

## Verification

    cosign verify-blob --bundle artifact.sigstore \
      --certificate-identity-regexp '^https://github.com/org/' \
      --certificate-oidc-issuer https://token.actions.githubusercontent.com artifact.tar.gz \
      && sha256sum -c artifact.sha256

Both commands exit 0, the signer identity matches the project, and the digest equals the independently published value.

Report: "Verified <artifact> from <project>: sha256 matches <hash>, signature identity <email/issuer>, provenance source commit <sha>."
