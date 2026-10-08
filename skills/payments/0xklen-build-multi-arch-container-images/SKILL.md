---
name: build-multi-arch-container-images
description: Use when one image tag must run on both amd64 servers and arm64 laptops or Graviton nodes. Builds a multi-platform manifest list with buildx so the registry serves the right architecture per pull.
---

# Build Multi-Arch Container Images

A single-arch image pushed under a tag makes arm64 nodes run it under emulation or fail with `exec format error`. A manifest list maps one tag to per-platform images, and the runtime picks the matching one at pull time.

## Procedure

1. Use buildx with a builder that can emit multiple platforms:
   `docker buildx create --name multi --use --bootstrap`.
2. For an explainable build, cross-compile where the toolchain allows it (Go, Rust, CGO-disabled) and use `--platform=$BUILDPLATFORM` for the build stage with `TARGETOS`/`TARGETARCH`:
   ```dockerfile
   FROM --platform=$BUILDPLATFORM golang:1.22 AS build
   ARG TARGETARCH
   RUN GOOS=linux GOARCH=$TARGETARCH go build -o /app .
   FROM gcr.io/distroless/static-debian12
   COPY --from=build /app /app
   ENTRYPOINT ["/app"]
   ```
3. For runtimes that cannot cross-compile, register QEMU binfmt once on the builder:
   `docker run --privileged --rm tonistiigi/binfmt --install arm64,amd64`.
4. Build and push the list in one step (a load-only multi-arch build cannot be kept locally):
   `docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/acme/app:1.4 --push .`.
5. Confirm the result is a list, not a single image:
   `docker buildx imagetools inspect ghcr.io/acme/app:1.4` shows one entry per platform with its digest.
6. In CI cache per-platform (`--cache-to type=gha,mode=max`) so the arm64 leg does not rebuild the amd64 layers.
7. For `FROM` bases, pull manifests that themselves are multi-arch; a single-arch base forces emulation for the other platform.

## Pitfalls

- `docker build --platform linux/arm64` alone produces a single-arch image that overwrites the amd64 tag if pushed; always `--platform a,b --push` together.
- QEMU emulation of a compiled language is 5–20× slower and lets architecture-specific bugs through because it is not the real CPU; cross-compile instead.
- `FROM golang:1.22` (no `--platform`) inside a cross-build defaults to the target platform and either emulates or fails; use `--platform=$BUILDPLATFORM` for the toolchain stage.
- Native addons (`node-gyp`) compile against the host arch unless you run the install in the target platform stage; a buildx build with QEMU hides this until runtime `SIGILL`.
- `--load` with multiple platforms errors (`cannot load multi-platform image`); use `--push` or `--output type=image`.
- A pinned base digest from a single arch breaks the other arch; pin the multi-arch index digest, not a platform digest.
- Tagging `latest` from a single-arch local build overwrites the multi-arch `latest`; push from CI only.

## Verification

    docker buildx imagetools inspect ghcr.io/acme/app:1.4 | grep -E 'linux/(amd64|arm64)'
    docker run --rm --platform linux/arm64 ghcr.io/acme/app:1.4 uname -m
    # aarch64

The manifest lists both platforms and each runs natively (`uname -m` matches). Report the platform entries and the native run result.
