---
name: use-distroless-or-slim-base-images
description: Use when an image ships a full OS with a shell, package manager and hundreds of packages the app never uses. Moves to a distroless or slim runtime base to cut CVE surface and size.
---

# Use Distroless or Slim Base Images

A `ubuntu:latest` runtime carries apt, a shell, coreutils and a package set that inflates the image to hundreds of MB and the CVE count into the hundreds — all attack surface the app does not need. A distroless or `-slim` runtime keeps only the app and its libraries.

## Procedure

1. Build in a full image, run in a minimal one:
   ```dockerfile
   FROM golang:1.22 AS build
   RUN CGO_ENABLED=0 go build -o /app ./cmd/app
   FROM gcr.io/distroless/static-debian12:nonroot
   COPY --from=build /app /app
   ENTRYPOINT ["/app"]
   ```
2. Match the base to the needs: `static-debian12` for a static binary; `base-debian12` if you need glibc/ca-certificates; `python3-debian12`/`nodejs20-debian12` runtime variants for interpreted apps.
3. For a slim (not distroless) base, still remove the tooling you do not run in production:
   `FROM debian:12-slim` then avoid installing `curl`, `vim`, `git` in the runtime stage.
4. Copy TLS roots and timezone data explicitly if the app needs them — distroless static images include them; a scratch base does not:
   `COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/`.
5. Use the `:nonroot` tag or `USER 65532:65532` (distroless default) so no root exists to escalate to.
6. Compile static where possible (`CGO_ENABLED=0`, Go or Rust) so no shared libraries are needed and `scratch` becomes viable.
7. Re-scan after the switch; the count should drop sharply because fewer packages means fewer advisories.

## Pitfalls

- Distroless has no shell, so `docker exec sh` and shell-form `RUN` healthcheck/`ENTRYPOINT` fail; use exec-form entrypoints and an HTTP probe or a separate debug image (`:debug` tags include busybox).
- `scratch` is not distroless: no `/etc/passwd`, no CA certs, no `/tmp`; a binary that resolves a hostname over TLS fails with `x509: certificate signed by unknown authority`.
- A dynamic-linked binary crashes with `no such file or directory` on a static base because the loader is missing; build static or choose the base with glibc.
- A slim base still has apt at build time only if you installed it; do not `apt-get update && ...` in the runtime stage — provision earlier.
- Distroless images do not run as a login shell, so an entrypoint script with a shebang still works (the kernel handles it) but `sh -c` wrappers do not.
- Fewer OS packages is not zero risk: a statically linked Go binary's modules still need scanning; scan the app's dependencies too.
- `nonroot` UID 65532 may conflict with a mounted volume's ownership; set `fsGroup` or `--user` matching.

## Verification

    docker images app:x --format '{{.Size}}'
    docker run --rm app:x sh -c true; echo "shell exit=$?"   # non-zero (no shell)
    trivy image --severity HIGH,CRITICAL app:x | tail -1

The size drops to tens of MB and the CVE count falls by an order of magnitude while the app still starts. Report before/after image size and finding counts.
