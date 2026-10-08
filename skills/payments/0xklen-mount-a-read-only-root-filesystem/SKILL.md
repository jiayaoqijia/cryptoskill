---
name: mount-a-read-only-root-filesystem
description: Use when a compromised container should not be able to modify its own filesystem. Runs with a read-only root and explicit writable tmpfs or volumes so a foothold cannot persist or drop tooling.
---

# Mount a Read-Only Root Filesystem

A writable container filesystem lets an attacker who reaches RCE drop a binary, rewrite the entrypoint, and persist until the next restart. A read-only root with named writable paths keeps normal operation while removing that persistence.

## Procedure

1. Run with the root read-only and give back only what the app needs:
   `docker run --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m --tmpfs /run app:x`.
2. In Kubernetes:
   ```yaml
   securityContext:
     readOnlyRootFilesystem: true
   volumeMounts:
     - { name: tmp,  mountPath: /tmp }
     - { name: cache, mountPath: /var/cache/app }
   volumes:
     - { name: tmp,  emptyDir: {} }
     - { name: cache, emptyDir: {} }
   ```
3. Find what the app writes: run it read-only once and collect the `EROFS` errors:
   `docker run --read-only app:x 2>&1 | grep -i 'read-only file system'`.
4. For each path named, mount an `emptyDir` (or `persistentVolumeClaim` for durable data). List grows only by observed need.
5. Use `noexec,nosuid` on tmpfs mounts so anything dropped in `/tmp` cannot be executed.
6. Pin the app's temp and cache dirs via env so it does not guess: `TMPDIR=/tmp`, `XDG_CACHE_HOME=/var/cache/app`.
7. Some runtimes write next to the binary (e.g. a `.pid` file in `/app`); either change the path or mount `/app/run` writable.

## Pitfalls

- Mounting a single writable dir over a path the image expected to contain files hides the baked content; `emptyDir` starts empty, so `/app/templates` mounted writable loses the templates.
- `readOnlyRootFilesystem: true` breaks images that write a lock file at `/app/.lock` (Go, some Node tooling) at startup, causing a crash loop that looks unrelated.
- Tmpfs counts against the container memory limit; a `/tmp` mounted without `size=` can consume the whole limit and OOM the app.
- `noexec` on the path a launcher needs (e.g. extracted native libs) prevents JIT/extract-to-tmp from running; carve out a separate `exec` mount only if genuinely required.
- A read-only root does not make mounted secrets read-only — a writable secret volume can still be tampered with; mount secrets with `defaultMode: 0400` and `readOnly: true`.
- Entry points that `apt-get install` at runtime fail immediately; install at build time.
- Setting the flag cluster-wide without the `emptyDir`s turns a working deploy into a CrashLoopBackOff across all replicas at once.

## Verification

    docker run --rm --read-only app:x sh -c 'touch /probe && echo writable || echo readonly'
    # readonly

The probe write to the root fails while the app still serves traffic. Report the read-only root status and the writable mounts that were added.
