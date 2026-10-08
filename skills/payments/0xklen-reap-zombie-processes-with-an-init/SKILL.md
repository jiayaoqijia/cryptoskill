---
name: reap-zombie-processes-with-an-init
description: Use when a container running a supervisor or forking app accumulates defunct processes. Adds a real init (tini, dumb-init or --init) so PID 1 reaps orphans instead of leaking zombie PIDs.
---

# Reap Zombie Processes with an Init

PID 1 in a container has an extra job the kernel expects: reaping orphaned children. An app that forks workers but does not `wait()` on them leaves `<defunct>` processes, and the process table grows until `fork: Resource temporarily unavailable`. A tiny init fixes it.

## Procedure

1. If the app is not itself init-aware, run a minimal init as PID 1:
   - Docker: `docker run --init app:x` injects `tini` automatically.
   - Dockerfile: `ENTRYPOINT ["/sbin/tini", "--", "/app/start.sh"]`.
   - Kubernetes: there is no `--init` flag; add `tini`/`dumb-init` to the image and prefix the entrypoint.
2. If the app is a supervisor (systemd without a user session, s6, supervisord) it may already reap; verify rather than assume.
3. Make the init forward signals and exit with the child's code so graceful shutdown still works — tini and dumb-init both do this by default.
4. Confirm the app is PID 1 only when it handles signals, or PID 1 is the init and the app is its child.
5. Reduce forks: a shell script that backgrounds and never waits is the common spawner of zombies.
6. Watch for zombies: `docker exec x ps -o pid,ppid,stat,comm` and look for `Z`/`<defunct>`.
7. In Kubernetes, `shareProcessNamespace: true` makes all containers share a PID namespace so one init reaps for sidecars too — use with care, it also exposes sidecar processes.

## Pitfalls

- `CMD sh -c "node app.js"` is the classic: the shell is PID 1, does not reap, and zombies accumulate.
- `docker run --init` has no Kubernetes equivalent; a cluster deploy of an image that relies on the flag leaks zombies with no symptom until the PID limit.
- tini/dumb-init built into the image add a few hundred KB; in a distroless image the static binary must be copied in (`COPY --from=krallin/ubuntu-tini /usr/bin/tini /sbin/tini`).
- An init that does not forward SIGTERM reintroduces the shutdown bug it was added to fix; test signals through it.
- `supervisord` as PID 1 reaps but also swallows children's exit codes; a crashed child may be restarted silently.
- `shareProcessNamespace` lets a sidecar send signals to the app container, which can be an unintended attack path.
- Zombies that are already the parent's children stay until the parent exits; an init only reaps orphans, so fix the forking code too.

## Verification

    docker run -d --init --name x app:x
    docker exec x sh -c 'ps -o stat,comm | grep -c Z'   # 0

After running under load, no process is in state `Z` and the process count is stable. Report the zombie count with the init in place.
