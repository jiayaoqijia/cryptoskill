---
name: attach-provenance-to-a-release-artifact
description: Use when publishing a build artifact and a consumer needs to know how it was built. Emits a signed, machine-readable record binding the artifact digest to its source and builder.
---

# Attach Provenance to a Release Artifact

A checksum says the bytes did not change in transit; provenance says where they came from. Bind the artifact digest to the commit, builder identity, and build recipe so consumers can verify the whole story.

## Procedure

1. Hash the exact artifact you intend to publish, before any re-signing:
   `sha256sum dist/app-linux-amd64 > app-linux-amd64.sha256`
2. Generate SLSA provenance. With a supported builder this is automatic; otherwise craft an in-toto statement:
   `slsa-github-generator` on GitHub Actions, or `cosign attest --predicate provenance.json --type slsaprovenance dist/app`.
3. Fill the predicate with: `buildType`, `builder.id` (the workflow URL), `invocation.configSource.uri` (repo), `.digest.sha1` (commit), `materials[]` (inputs by digest), and `metadata.buildStartedOn/FinishedOn`.
4. Sign the provenance as a Sigstore bundle so it is tamper-evident:
   `cosign attest-blob --predicate provenance.json --type slsaprovenance --bundle provenance.sigstore dist/app`
5. Publish the artifact next to `provenance.sigstore` and the `.sha256` file in the same release.
6. Confirm the digest inside the provenance equals the file you uploaded — a mismatch means you attested a different build.
7. Record the builder's OIDC identity, not a long-lived key, so verification does not depend on a static secret.

## Pitfalls

- Attesting after a sign/re-sign step changes the digest; the provenance then points at bytes nobody published. Attest last, or sign in a distinct stage.
- Provenance that names a branch instead of a commit SHA cannot be reproduced — a branch moves.
- Copying a template predicate and leaving `builder.id` pointing at an example repo makes the attestation useless and misleading.
- Storing provenance in a mutable location (a wiki, an S3 object without versioning) defeats the point; ship it alongside the immutable artifact.
- A provenance file without a signature is just JSON an attacker can edit.

## Verification

    cosign verify-blob-attestation \
      --bundle provenance.sigstore \
      --certificate-identity-regexp '^https://github.com/org/repo/' \
      --certificate-oidc-issuer https://token.actions.githubusercontent.com \
      --type slsaprovenance dist/app

A `Verified OK` with the expected identity, plus a subject digest matching `sha256sum dist/app`, is a pass.

Report: "Provenance for <artifact> verified against builder <workflow URL>; subject digest <sha256> matches the published binary."
