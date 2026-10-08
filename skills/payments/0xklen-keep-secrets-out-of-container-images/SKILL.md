---
name: keep-secrets-out-of-container-images
description: Use when a Dockerfile might bake credentials into an image layer. Injects secrets at build and run time via mounts and stores so the value never lands in a pushed layer or image history.
---

# Keep Secrets Out of Container Images

Every layer of an image is downloadable by anyone who can pull it, and `docker history` plus `docker save` expose values even if a later layer deleted the file. A secret in a layer is a leaked secret the moment the image is pushed.

## Procedure

1. Never `COPY .env` or `ENV DB_PASSWORD=...` in a Dockerfile. Environment variables are visible in `docker inspect` and to any process in the container.
2. For build-time secrets, use BuildKit secret mounts, which are not persisted into any layer:
   ```dockerfile
   RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
       npm ci --omit=dev
   ```
   Pass it: `docker build --secret id=npmrc,src=$HOME/.npmrc .`.
3. For runtime secrets, mount from a secret store rather than copying into the image:
   - Kubernetes: `secretKeyRef` or a CSI secrets store volume mounted at `/run/secrets/...` (tmpfs, mode `0400`).
   - Docker: `--mount type=bind,src=/run/secrets/db,target=/run/secrets/db,ro`.
4. Prefer file-mounted secrets over env vars: env leaks through `/proc/self/environ`, crash dumps, and child processes. Read the file at startup, then unlink it if the app re-reads config.
5. Set restrictive modes and non-root ownership so only the app user can read:
   `chmod 0400 /run/secrets/db; chown 10001:10001 /run/secrets/db`.
6. Add `ENV` with non-secret config only, and audit for accidental secrets:
   `docker history --no-trunc app:x | grep -iE 'passw|secret|token|key'`.
7. Scan the built image for embedded credentials before pushing: `trivy image --scanners secret app:x`.
8. Rotate any secret that a prior image needs, since its layers are already public to anyone with pull access.

## Pitfalls

- `ARG SECRET` then `RUN ... $SECRET` leaves the value in the build history; BuildKit `--mount=type=secret` exists precisely to avoid this.
- Multi-stage builds do not scrub the builder stage from the final image, but a secret used in an earlier `RUN` of a copied stage is still in the intermediate image if it was pushed to a registry cache.
- Kubernetes `Secret` values are base64, not encrypted; anyone with `get secret` in the namespace reads them. Use an external KMS or sealed-secrets for at-rest encryption.
- Mounting a secret as a directory means updating it replaces the file atomically, but a running process that read it once never sees the rotation — reload on `SIGHUP` or watch the file.
- A secret written into a writable tmpfs can be read by any process in the same pod if it runs as the same UID; isolate with a shared process namespace disabled.
- `.dockerignore` missing `.env` puts the file in the build context, and a later `COPY . .` bakes it in.

## Verification

    docker run --rm --entrypoint sh app:x -c 'env | grep -i pass || echo clean'
    trivy image --scanners secret --exit-code 1 app:x

`env` shows no secret values and the secret scanner reports no findings (exit 0). Report the scanner command and its hit count, not an assurance that "secrets are handled".
