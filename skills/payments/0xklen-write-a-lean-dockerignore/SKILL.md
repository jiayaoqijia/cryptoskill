---
name: write-a-lean-dockerignore
description: Use when `docker build` sends a multi-GB context or a secret file lands in the image. Writes a .dockerignore that trims the build context and keeps .git, env files and build output out of layers.
---

# Write a Lean .dockerignore

The build context is everything in the directory tree sent to the daemon, minus what `.dockerignore` excludes. Without one, `node_modules`, `.git` and `.env` are uploaded on every build, `COPY . .` bakes them into a layer, and a secret ends up in a pushed image.

## Procedure

1. Create `.dockerignore` next to the Dockerfile (context root, not the Dockerfile's directory if they differ):
   ```
   .git
   .gitignore
   node_modules
   dist
   build
   coverage
   *.log
   .env
   .env.*
   .DS_Store
   docker-compose*.yml
   Dockerfile*
   README.md
   ```
2. Keep anything the build actually needs; excluding `package-lock.json` or `patches/` breaks a cached install silently.
3. Match by regex on the whole path, not glob-by-name: `**/tmp` excludes nested dirs, `tmp` only the root one. Use `!` to re-include: `!src/config.example.json`.
4. Rebuild and watch the context size line the builder prints:
   `docker build . 2>&1 | head -3` shows `transferring context: 4.2MB`.
5. For BuildKit, `.dockerignore` still governs `COPY`; a file excluded from the context cannot be copied even if named explicitly.
6. Add the same ignores to `.gitignore` where they overlap, but do not assume `.gitignore` is respected — Docker ignores it unless a `.dockerignore` mirrors it.
7. Verify no secret is in the context: `docker build --no-cache -t x . && docker save x | tar -tf - | grep -i env`.

## Pitfalls

- No trailing-slash vs leading-slash confusion: `/app` anchors to the context root; `app` matches any path segment named `app`. Losing the leading slash can exclude your source.
- `.dockerignore` is read from the context root, not the Dockerfile directory; with `-f docker/Dockerfile .` the file must be at `.`, not `docker/`.
- Excluding `node_modules` then running `COPY . .` without an `npm ci` step ships an image that cannot run.
- A stale `.dockerignore` that excludes a directory you later started importing causes `COPY failed: no source files` with a confusing message.
- Copying the daemon's `docker build - < .` from a shell does not honour `.dockerignore` patterns the same way; build with a context dir.
- Excluding `package.json` accidentally breaks caching and the install; review before committing.
- `.dockerignore` does not shrink the final image if those paths are also `COPY`ed — it only controls the context; the layer is separate.

## Verification

    docker build . 2>&1 | grep -m1 'transferring context'
    docker run --rm --entrypoint sh x -c 'ls -la / | grep -c "\.git"'   # 0

The "transferring context" figure drops to a few MB and no `.git`/`.env` exists inside the image. Report the context size before and after.
