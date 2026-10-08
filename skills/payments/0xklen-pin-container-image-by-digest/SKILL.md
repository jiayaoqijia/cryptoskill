---
name: pin-container-image-by-digest
description: Use when a deployed container must be byte-identical to what was tested. Pins images by sha256 digest instead of a tag so a re-tagged upstream image cannot silently change the running bits.
---

# Pin Container Images by Digest

A tag is a movable pointer; whoever controls the registry can repoint `app:1.4` at different bytes at any time, and your next `docker pull` gets the new layer without a config change. A digest is the hash of the manifest, so it names exactly one image.

## Procedure

1. Resolve the tag to a digest immediately after your build or your upstream pull:
   `docker buildx imagetools inspect ghcr.io/acme/app:1.4 --format '{{.Manifest.Digest}}'`
   or `docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/acme/app:1.4`.
2. Reference that exact reference everywhere it is deployed:
   `image: ghcr.io/acme/app@sha256:9f2c...c41` (Dockerfile `FROM`, compose `image:`, k8s `image:`).
3. Keep the human tag as a comment or an annotation, never as the pull source, so reviewers know which release it is:
   `# app:1.4 (2026-09-30)`
4. In Kubernetes set `imagePullPolicy: IfNotPresent`. With a digest, `Always` re-resolves nothing new and just adds registry load.
5. Enforce at admission. With Kyverno require a digest: `spec.rules[].validate.pattern.spec.containers[].image: "*@sha256:*"`. With Conftest/OPA gate the manifest:
   `conftest test deploy.yaml -p policy/require_digest.rego`.
6. For a two-stage build, pin the builder base by digest too — an unpinned `golang:1.22` builder is where a supply-chain swap hides because only the final image gets scanned.
7. Record the digest pair (builder + runtime) in the release notes so an auditor can re-pull the exact inputs.

## Pitfalls

- Multi-arch images have a per-platform manifest digest distinct from the top-level index digest. Pinning the index digest (`imagetools inspect --raw` top manifest) is correct for a multi-arch deploy; pinning a platform digest breaks arm64.
- `docker inspect ... .RepoDigests` is empty for a locally built image never pushed. Run `docker buildx imagetools inspect` against the pushed tag instead.
- Digest pinning without a bump process freezes security patches silently — pair it with a scheduled job that opens a PR when `imagetools inspect` shows a new digest for the tracked tag.
- Copying a digest from a web UI truncates the middle. Always resolve programmatically; a wrong-by-one-character digest fails the pull with `manifest unknown`, which reads like a network error.
- `@sha256:` on a tag that was deleted upstream still pulls if the digest is retained; do not treat "the tag is gone" as "the image is gone".

## Verification

    docker buildx imagetools inspect ghcr.io/acme/app@sha256:9f2c...c41 \
      --format '{{.Manifest.Digest}}'
    # prints: sha256:9f2c...c41  (matches the pinned reference)

The printed digest equals the pinned string and `docker run --rm <digest> true` exits 0. Report the running digest, e.g. "deployed digest sha256:9f2c…c41, resolved from tag app:1.4".
