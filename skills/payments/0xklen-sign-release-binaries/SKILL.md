---
name: sign-release-binaries
description: Use when publishing binaries whose origin a user must be able to prove. Produces detached signatures with a keyless or managed key and documents how to verify them.
---

# Sign Release Binaries

Unsigned releases are indistinguishable from a malicious mirror's copy. A signature with a published identity and a documented verification command turns trust into a check.

## Procedure

1. Decide the mode. Keyless (Sigstore/OIDC) ties the signature to a CI workflow identity and needs no stored secret; a managed key (KMS, `gpg`) suits air-gapped or non-CI releases.
2. Keyless in GitHub Actions — give the job `id-token: write` and sign the built artifacts:
   `cosign sign-blob --bundle dist/app.sigstore dist/app`
3. Detached GPG for key-managed releases. Use a dedicated release key, not a personal one:
   `gpg --armor --detach-sign --local-user releases@example.org dist/app`
   Export the public key once per major version: `gpg --armor --export releases@example.org > release-key.asc`.
4. Sign containers by digest, not tag: `cosign sign registry/app@sha256:<digest>`.
5. Sign the checksum file too, so a user can verify many artifacts from one trusted root:
   `sha256sum dist/* > SHA256SUMS && cosign sign-blob --bundle SHA256SUMS.sigstore SHA256SUMS`.
6. Publish signatures next to the artifacts, plus a short `VERIFY.md` with the exact command and the expected certificate identity or key fingerprint.
7. Store any long-lived signing key encrypted (age/GPG) and available only to the release job; never commit it.

## Pitfalls

- Signing before the artifact is final (still gets a timestamp or repack) invalidates the signature; sign the exact bytes you ship.
- Re-signing an artifact with a new key after a compromise does not un-publish the old signature — revoke the key and tell users.
- A signature proves integrity and identity, not safety; pair it with provenance and an SBOM.
- Keyless signatures embed a short certificate lifetime; verification depends on the Rekor transparency log, so do not delete the bundle.
- Committing a passphrase-free private key to CI secrets is a leak waiting to happen; scope the token to the release environment.

## Verification

    cosign verify-blob --bundle dist/app.sigstore \
      --certificate-identity-regexp '^https://github.com/org/repo/' \
      --certificate-oidc-issuer https://token.actions.githubusercontent.com dist/app

For GPG: `gpg --verify dist/app.asc dist/app` prints `Good signature from releases@example.org`. Both must pass with the documented identity.

Report: "Signed <artifacts> keyless from <workflow>; verification command in VERIFY.md returns Verified OK for identity <regexp>."
