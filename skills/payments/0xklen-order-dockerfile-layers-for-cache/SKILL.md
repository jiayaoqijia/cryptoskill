---
name: order-dockerfile-layers-for-cache
description: Use when image builds are slow because every code change re-installs dependencies. Orders Dockerfile instructions so rarely-changing layers sit early and cheap layers late.
---

# Order Dockerfile Layers for Cache

Docker caches each instruction keyed on its inputs; the first changed instruction invalidates every layer after it. Put dependency manifests before source code so a one-line edit rebuilds one layer, not the whole dependency graph.

## Procedure

1. Copy only manifests first, install, then copy source:
   ```dockerfile
   COPY package.json package-lock.json ./
   RUN npm ci --omit=dev
   COPY . .
   RUN npm run build
   ```
   The `COPY . .` invalidates the build layer on every edit; the `npm ci` layer stays cached.
2. For Python, keep a lock with hashes and install before copying sources:
   `COPY requirements.txt ./` then `RUN pip install --require-hashes -r requirements.txt` then `COPY . .`.
3. Add a `.dockerignore` so an unrelated file in the context does not bust the copy layer: exclude `.git`, `node_modules`, `*.log`, `dist`, `.env`.
4. Order by change frequency, ascending: base image → system packages → language toolchain → app deps → app code → config that changes per release.
5. Keep expensive-but-stable OS package installs in one `RUN` with a cleanup in the same layer:
   `RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*`.
6. Use cache mounts for package managers to avoid download on a cache miss:
   `RUN --mount=type=cache,target=/root/.npm npm ci`.
7. In CI use `docker buildx build --cache-from type=registry,ref=ghcr.io/acme/app:cache --cache-to type=registry,...` so the runner reuses layers across jobs.

## Pitfalls

- `COPY . .` before the install step is the classic cache-buster; fixing only that often turns a 4-minute build into 20 seconds.
- `apt-get update` in a layer separate from `apt-get install` caches a stale index and later installs 404 on packages.
- Adding `ARG VERSION` above the dependency install invalidates it on every version change even though deps did not move; put the ARG below.
- `RUN` with `--no-cache` (buildkit flag) discards the mount cache too during debugging, making you think the Dockerfile is slow.
- Mounting the source with `-v $(pwd):/app` at `docker run` hides whatever `COPY` put there, so a cached build looks stale — that is runtime, not the cache.
- A `.dockerignore` that excludes a file the install needs (e.g. `patches/`) makes the cached layer silently produce a wrong artifact; the build layer above it still hits cache and never rebuilds.

## Verification

    docker build -t app:x . && touch src/app.js && docker build -t app:x .
    # second build prints: CACHED ... RUN npm ci ... <all deps>

Cold build once, edit one source file, rebuild: the dependency install line reports `CACHED` and total time drops by the dependency-install duration. Report the before/after layer status, not a claim that build "seems faster".
