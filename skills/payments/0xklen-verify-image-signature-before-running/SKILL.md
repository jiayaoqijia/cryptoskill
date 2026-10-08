---
name: verify-image-signature-before-running
description: Use when an image from a registry must be proven to come from your pipeline before it runs. Verifies a cosign/Notation signature against a keyless identity or a public key and refuses unsigned images.
---

# Verify Image Signature Before Running

A digest proves the bytes did not change; it does not prove who produced them. Signature verification binds an image to a signing identity (a KMS key or a CI OIDC workflow), so a digest pulled from a compromised or typosquatted registry is rejected before it starts.

## Procedure

1. Sign in the pipeline after push, keyless against the workflow identity:
   `cosign sign --yes ghcr.io/acme/app@sha256:9f2c...c41`.
2. Verify against that identity before deploy to a dev cluster:
   ```bash
   cosign verify ghcr.io/acme/app@sha256:9f2c...c41 \
     --certificate-identity-regexp '^https://github.com/acme/app/.github/workflows/release.yml@refs/tags/.*$' \
     --certificate-oidc-issuer https://token.actions.githubusercontent.com
   ```
3. For a key-based setup, verify with the public key and reject if it is absent:
   `cosign verify --key cosign.pub ghcr.io/acme/app@sha256:9f2c...c41`.
4. Enforce at admission so an unsigned image cannot schedule. With Kyverno:
   ```yaml
   verifyImages:
     - imageReferences: ["ghcr.io/acme/*"]
       attestors: [{ entries: [{ keyless: { subject: "https://github.com/acme/app/...", issuer: "https://token.actions.githubusercontent.com" } }] }]
   ```
5. Also verify the SBOM/attestation if you produce one:
   `cosign verify-attestation --type spdxjson --key cosign.pub ghcr.io/acme/app@sha256:...`.
6. Pin the exact `--certificate-identity-regexp`; a regexp of `.*` accepts anyone's OIDC identity, which defeats the check.
7. For Notation/ORAS workflows, `notation verify ghcr.io/acme/app@sha256:...` with a trust policy in `~/.config/notation/trustpolicy.json`.

## Pitfalls

- Verifying the tag rather than the digest lets the signature attach to one image while you deploy another resolved later; always verify the `@sha256` you will run.
- In keyless mode, `--certificate-identity-regexp` broad enough to include a fork or any repo under the org is a real bypass; anchor the path and the tag/ref pattern.
- A signature covers the manifest, not the config or layers transitively in all schemes — verify the whole index and pull by digest so the covered object is what runs.
- `cosign verify` prints JSON and exits 0/1; a pipeline that pipes to `jq` and swallows the exit code runs unsigned images. Check `$?`.
- Signing with a long-lived key stored next to the build script is not a trust boundary; use OIDC keyless or a KMS/HSM key.
- Registry mirrors and re-tagging do not carry signatures; an image promoted by copying layers into another registry is unsigned unless re-signed.
- Rekor transparency log absence is not itself a failure, but record the entry index so a later dispute can be checked.

## Verification

    cosign verify --certificate-identity-regexp '<anchored>' \
      --certificate-oidc-issuer https://token.actions.githubusercontent.com \
      ghcr.io/acme/app@sha256:9f2c...c41 >/dev/null && echo SIGNED
    # SIGNED ; an unsigned or wrong-identity image exits non-zero

The verify command exits 0 only for the expected signer, and admission blocks a re-pushed unsigned tag. Report the verified identity and the policy that enforced it.
